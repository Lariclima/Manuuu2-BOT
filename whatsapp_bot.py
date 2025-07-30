from flask import Flask, request, jsonify, session
from flask_cors import CORS
import openai
import os
import logging
import requests
import json
from datetime import datetime
import traceback
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configurações do WhatsApp Business API
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'manu_verify_token_2024')

# Configurar OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')

# Configurações do negócio
BUSINESS_PHONE = os.getenv('BUSINESS_PHONE_NUMBER', '+5528999771140')
BUSINESS_NAME = os.getenv('BUSINESS_NAME', 'Dra. Larissa Carleth - Nutricionista')
SECRETARY_NAME = os.getenv('SECRETARY_NAME', 'Manu')

# Armazenar conversas em memória (em produção, usar banco de dados)
conversations = {}

# Prompt da Manu para WhatsApp
PROMPT_MANU_WHATSAPP = """
Você é Manu, a secretária virtual da Dra. Larissa Carleth, nutricionista especializada em emagrecimento e mudança de estilo de vida.

SOBRE A DRA. LARISSA:
A Dra. Larissa desenvolveu um método único baseado em sua própria trajetória pessoal. Ela já foi paciente, enfrentou o processo de emagrecimento e sabe exatamente como é se sentir perdida, sem direcionamento, com dietas copiadas e atendimentos rápidos que não olhavam para a individualidade. Foi a partir dessas dificuldades que nasceu o desejo de fazer diferente. Com muito estudo, prática e empatia, ela criou um formato de atendimento único, que une ciência, escuta e estratégia, acolhendo cada paciente como ela gostaria de ter sido acolhida.

VALORES DAS CONSULTAS:
- Primeira consulta: R$ 400,00 (a prazo) ou R$ 380,00 (à vista com 5% de desconto)
- Demais consultas: R$ 300,00 (a prazo) ou R$ 285,00 (à vista com 5% de desconto)

PACOTES DISPONÍVEIS:
- Pacote 4 consultas: Parcelamento em 4x (sinal via Pix, restante em 3x sem juros)
- Pacote 7 consultas: Parcelamento em 7x (sinal via Pix, restante em 6x sem juros)  
- Pacote 13 consultas: Parcelamento em 13x (sinal via Pix, restante em 12x sem juros)
- Pagamento à vista para pacotes: 10% de desconto

DIRETRIZES DE ATENDIMENTO NO WHATSAPP:
1. Sempre se apresente como Manu, secretária da Dra. Larissa
2. Quando perguntarem sobre preços diretamente, primeiro pergunte se já conhecem a Dra. Larissa e se já fizeram acompanhamento nutricional antes
3. Faça descoberta de necessidades antes de discutir valores
4. Use perguntas que incentivem a pessoa a articular suas dores (emocionais, físicas, comportamentais, sociais)
5. Enfatize como a Dra. Larissa ajuda a superar dores e resolver problemas de emagrecimento
6. Mencione que apenas 5 novas pacientes são aceitas por mês (escassez)
7. NUNCA ofereça promoções ou descontos além dos já estabelecidos
8. Se não souber responder algo, informe que precisa verificar com a Dra. Larissa
9. Mantenha mensagens concisas e adequadas para WhatsApp (máximo 2-3 parágrafos)
10. Use emojis moderadamente para tornar a conversa mais calorosa

CARACTERÍSTICAS DA SUA PERSONALIDADE:
- Cordial, educada e prestativa
- Linguagem acolhedora e empática no WhatsApp
- Demonstra compreensão das dificuldades de emagrecimento
- Proativa em identificar dores e necessidades
- Tom profissional mas humano e próximo

EXEMPLO DE RESPOSTA INICIAL:
"Oi! 😊 Sou a Manu, secretária da Dra. Larissa Carleth. 

Você já conhece o trabalho da Dra. Larissa? Ela é nutricionista especializada em emagrecimento e já ajudou centenas de mulheres a transformarem suas vidas.

Me conta, você já fez acompanhamento nutricional antes? O que te trouxe até aqui hoje?"

Responda sempre em português brasileiro, mantendo o foco no atendimento especializado em nutrição e emagrecimento, adequado para conversas no WhatsApp.
"""

def send_whatsapp_message(phone_number, message):
    """Enviar mensagem via WhatsApp Business API"""
    try:
        url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
        
        headers = {
            'Authorization': f'Bearer {WHATSAPP_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            logger.info(f"Mensagem enviada com sucesso para {phone_number}")
            return True
        else:
            logger.error(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem WhatsApp: {str(e)}")
        return False

def get_ai_response(user_message, phone_number):
    """Obter resposta da IA usando OpenAI"""
    try:
        # Recuperar histórico da conversa
        if phone_number not in conversations:
            conversations[phone_number] = []
        
        # Adicionar mensagem do usuário ao histórico
        conversations[phone_number].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Preparar mensagens para a API (últimas 10 mensagens)
        messages = [{'role': 'system', 'content': PROMPT_MANU_WHATSAPP}]
        
        for msg in conversations[phone_number][-10:]:
            messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        # Chamar API da OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,  # Mensagens mais curtas para WhatsApp
                temperature=0.7
            )
            
            # Verificar se a resposta é um objeto ou dicionário
            if hasattr(response, 'choices'):
                ai_message = response.choices[0].message.content
            else:
                ai_message = response['choices'][0]['message']['content']
                
        except Exception as api_error:
            logger.error(f"Erro específico da API OpenAI: {str(api_error)}")
            # Resposta de fallback baseada no prompt
            if "preço" in user_message.lower() or "valor" in user_message.lower() or "custa" in user_message.lower():
                ai_message = """Oi! 😊 Sou a Manu, secretária da Dra. Larissa Carleth.

Você já conhece o trabalho da Dra. Larissa? Ela é nutricionista especializada em emagrecimento e já ajudou centenas de mulheres a transformarem suas vidas.

Me conta, você já fez acompanhamento nutricional antes? O que te trouxe até aqui hoje?"""
            else:
                ai_message = """Oi! 😊 Sou a Manu, secretária da Dra. Larissa Carleth.

Como posso ajudá-la hoje? Estou aqui para tirar suas dúvidas sobre nossos atendimentos de nutrição! ✨"""
        
        # Adicionar resposta da IA ao histórico
        conversations[phone_number].append({
            'role': 'assistant',
            'content': ai_message,
            'timestamp': datetime.now().isoformat()
        })
        
        return ai_message
        
    except Exception as e:
        logger.error(f"Erro ao obter resposta da IA: {str(e)}")
        logger.error(traceback.format_exc())
        return "Desculpe, estou com dificuldades técnicas no momento. A Dra. Larissa entrará em contato em breve! 😊"

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verificar webhook do WhatsApp"""
    try:
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("Webhook verificado com sucesso")
            return challenge
        else:
            logger.warning("Falha na verificação do webhook")
            return 'Forbidden', 403
            
    except Exception as e:
        logger.error(f"Erro na verificação do webhook: {str(e)}")
        return 'Error', 500

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Processar mensagens recebidas do WhatsApp"""
    try:
        data = request.get_json()
        logger.info(f"Webhook recebido: {json.dumps(data, indent=2)}")
        
        # Verificar se há mensagens na requisição
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if 'value' in change and 'messages' in change['value']:
                            for message in change['value']['messages']:
                                # Extrair informações da mensagem
                                phone_number = message['from']
                                message_type = message['type']
                                
                                # Processar apenas mensagens de texto
                                if message_type == 'text':
                                    user_message = message['text']['body']
                                    logger.info(f"Mensagem recebida de {phone_number}: {user_message}")
                                    
                                    # Obter resposta da IA
                                    ai_response = get_ai_response(user_message, phone_number)
                                    
                                    # Enviar resposta
                                    send_whatsapp_message(phone_number, ai_response)
                                
                                elif message_type in ['image', 'audio', 'video', 'document']:
                                    # Responder para tipos de mídia não suportados
                                    response_msg = "Oi! 😊 Sou a Manu, secretária da Dra. Larissa. No momento consigo responder apenas mensagens de texto. Como posso ajudá-la hoje?"
                                    send_whatsapp_message(phone_number, response_msg)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Verificar saúde da aplicação"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'service': 'Manu WhatsApp Bot'
    })

@app.route('/conversations')
def get_conversations():
    """Endpoint para visualizar conversas (apenas para debug)"""
    return jsonify({
        'total_conversations': len(conversations),
        'conversations': {phone: len(msgs) for phone, msgs in conversations.items()}
    })

@app.route('/clear_conversation/<phone_number>', methods=['POST'])
def clear_conversation(phone_number):
    """Limpar conversa específica"""
    if phone_number in conversations:
        del conversations[phone_number]
        return jsonify({'status': 'success', 'message': f'Conversa de {phone_number} limpa'})
    else:
        return jsonify({'status': 'error', 'message': 'Conversa não encontrada'}), 404

if __name__ == '__main__':
    # Verificar variáveis de ambiente
    required_vars = ['WHATSAPP_TOKEN', 'WHATSAPP_PHONE_NUMBER_ID', 'OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Variáveis de ambiente faltando: {missing_vars}")
        print(f"⚠️  ATENÇÃO: Configure as seguintes variáveis de ambiente:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nVeja o arquivo README.md para instruções de configuração.")
    
    logger.info("Iniciando Manu WhatsApp Bot...")
    app.run(host='0.0.0.0', port=8000, debug=True)

