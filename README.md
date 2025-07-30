# 🤖 Manu - Secretária Virtual WhatsApp

Secretária virtual inteligente para WhatsApp Business da **Dra. Larissa Carleth**, nutricionista especializada em emagrecimento.

## 📋 Sobre o Projeto

A Manu é uma secretária virtual que responde automaticamente mensagens no WhatsApp Business, seguindo um prompt especializado para:

- ✅ Atendimento inicial e triagem de pacientes
- ✅ Descoberta de necessidades antes de apresentar preços
- ✅ Informações sobre consultas e pacotes
- ✅ Agendamento e direcionamento
- ✅ Abordagem empática e profissional

**Número do WhatsApp Business:** +5528999771140

## 🚀 Funcionalidades

### Respostas Inteligentes
- Detecta perguntas sobre preços e faz descoberta de necessidades primeiro
- Apresenta a Dra. Larissa e sua metodologia única
- Informa valores apenas após qualificação do lead
- Menciona escassez (apenas 5 pacientes/mês)

### Informações Disponíveis
- **Primeira consulta:** R$ 400 (a prazo) ou R$ 380 (à vista)
- **Demais consultas:** R$ 300 (a prazo) ou R$ 285 (à vista)
- **Pacotes:** 4, 7 ou 13 consultas com parcelamento
- **Desconto à vista:** 10% nos pacotes

### Personalidade da Manu
- Cordial, educada e prestativa
- Linguagem acolhedora e empática
- Compreende dificuldades de emagrecimento
- Tom profissional mas humano

## 🛠️ Configuração

### 1. Pré-requisitos

- Python 3.8+
- Conta WhatsApp Business
- Facebook Developer Account
- Chave da API OpenAI

### 2. Instalação

```bash
# Clonar/baixar o projeto
cd manu-whatsapp-bot

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
```

### 3. Configurar Variáveis de Ambiente

Edite o arquivo `.env`:

```env
# WhatsApp Business API
WHATSAPP_TOKEN=seu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id_aqui
VERIFY_TOKEN=manu_verify_token_2024

# OpenAI
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_API_BASE=https://api.openai.com/v1

# Configurações
BUSINESS_PHONE_NUMBER=+5528999771140
PORT=8000
DEBUG=True
```

### 4. Configurar WhatsApp Business API

#### Passo 1: Facebook Developer Console
1. Acesse [developers.facebook.com](https://developers.facebook.com)
2. Crie um app "Business"
3. Adicione o produto "WhatsApp"

#### Passo 2: Configurar Webhook
1. URL do Webhook: `https://seu-dominio.com/webhook`
2. Verify Token: `manu_verify_token_2024`
3. Campos de assinatura: `messages`

#### Passo 3: Obter Tokens
1. **Access Token:** Copie do painel WhatsApp
2. **Phone Number ID:** Encontre em "Phone Numbers"

### 5. Deploy

#### Opção A: Servidor Local (Teste)
```bash
python whatsapp_bot.py
```

#### Opção B: Produção com Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 whatsapp_bot:app
```

#### Opção C: Deploy na Nuvem
- **Heroku:** Adicione `Procfile`
- **Railway:** Configure variáveis de ambiente
- **DigitalOcean:** Use Docker ou servidor VPS

## 🧪 Testes

### Testar Localmente
```bash
python test_bot.py
```

### Testar Webhook
```bash
curl -X GET "http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=manu_verify_token_2024&hub.challenge=test"
```

### Verificar Saúde
```bash
curl http://localhost:8000/health
```

## 📱 Como Funciona

### Fluxo de Conversa

1. **Usuário envia mensagem** → WhatsApp Business API
2. **Webhook recebe** → Processa mensagem
3. **IA analisa** → Gera resposta personalizada
4. **Bot responde** → Envia via WhatsApp API

### Exemplo de Conversa

```
👤 Usuário: "Oi, quanto custa a consulta?"

🤖 Manu: "Oi! 😊 Sou a Manu, secretária da Dra. Larissa Carleth.

Você já conhece o trabalho da Dra. Larissa? Ela é nutricionista especializada em emagrecimento e já ajudou centenas de mulheres a transformarem suas vidas.

Me conta, você já fez acompanhamento nutricional antes? O que te trouxe até aqui hoje?"
```

## 🔧 Estrutura do Projeto

```
manu-whatsapp-bot/
├── whatsapp_bot.py      # Aplicação principal
├── test_bot.py          # Script de testes
├── requirements.txt     # Dependências
├── .env.example        # Exemplo de configuração
├── README.md           # Esta documentação
└── logs/               # Logs da aplicação
```

## 📊 Monitoramento

### Endpoints Disponíveis

- `GET /health` - Status da aplicação
- `GET /conversations` - Estatísticas de conversas
- `POST /clear_conversation/<phone>` - Limpar conversa específica

### Logs

A aplicação gera logs detalhados para:
- Mensagens recebidas e enviadas
- Erros da API
- Respostas da IA
- Status do webhook

## 🔒 Segurança

- ✅ Verificação de token do webhook
- ✅ Validação de mensagens
- ✅ Rate limiting (implementar se necessário)
- ✅ Logs de auditoria
- ✅ Variáveis de ambiente para credenciais

## 🚨 Troubleshooting

### Problemas Comuns

**1. Webhook não recebe mensagens**
- Verifique URL pública acessível
- Confirme verify_token correto
- Teste conectividade

**2. Erro na API OpenAI**
- Verifique OPENAI_API_KEY
- Confirme créditos disponíveis
- Bot usa fallback automático

**3. Mensagens não são enviadas**
- Verifique WHATSAPP_TOKEN
- Confirme PHONE_NUMBER_ID
- Teste permissões da API

### Comandos de Debug

```bash
# Ver logs em tempo real
tail -f logs/app.log

# Testar conexão OpenAI
python -c "import openai; print(openai.Model.list())"

# Verificar variáveis
python -c "import os; print(os.getenv('WHATSAPP_TOKEN'))"
```

## 📈 Próximos Passos

### Melhorias Futuras
- [ ] Integração com Google Calendar para agendamentos
- [ ] Banco de dados para persistir conversas
- [ ] Dashboard de analytics
- [ ] Respostas com imagens/documentos
- [ ] Integração com CRM
- [ ] Notificações para a Dra. Larissa

### Escalabilidade
- [ ] Redis para cache de conversas
- [ ] Queue system para mensagens
- [ ] Load balancer
- [ ] Backup automático

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs da aplicação
2. Consulte esta documentação
3. Teste com o script `test_bot.py`
4. Entre em contato com o desenvolvedor

---

**Desenvolvido para Dra. Larissa Carleth - Nutricionista**  
WhatsApp Business: +5528999771140  
Instagram: @nutrilaricarleth

