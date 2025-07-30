#!/usr/bin/env python3
"""
Script de teste para o bot Manu WhatsApp
Simula mensagens recebidas para testar as respostas da IA
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from whatsapp_bot import get_ai_response
import json

def test_responses():
    """Testar diferentes tipos de mensagens"""
    
    test_phone = "5528999771140"  # Número de teste
    
    test_messages = [
        "Oi, quanto custa a consulta?",
        "Olá, gostaria de saber sobre os valores",
        "Preciso emagrecer, você pode me ajudar?",
        "Já fiz várias dietas e nada funciona",
        "Qual o preço do acompanhamento?",
        "Tenho dificuldade para perder peso",
        "Conheci vocês pelo Instagram",
        "Quero agendar uma consulta"
    ]
    
    print("🤖 TESTE DO BOT MANU WHATSAPP")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📱 TESTE {i}")
        print(f"Usuário: {message}")
        print("-" * 30)
        
        try:
            response = get_ai_response(message, test_phone)
            print(f"Manu: {response}")
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
        
        print("-" * 50)

def test_conversation_flow():
    """Testar fluxo de conversa completo"""
    
    test_phone = "test_conversation"
    
    conversation = [
        "Oi, quanto custa a consulta?",
        "Não, nunca fiz acompanhamento nutricional",
        "Quero emagrecer 15kg",
        "Já tentei várias dietas mas sempre volto a engordar",
        "Me sinto muito frustrada",
        "Quanto custa então?"
    ]
    
    print("\n\n🗣️ TESTE DE CONVERSA COMPLETA")
    print("=" * 50)
    
    for i, message in enumerate(conversation, 1):
        print(f"\n💬 MENSAGEM {i}")
        print(f"Usuário: {message}")
        print("-" * 30)
        
        try:
            response = get_ai_response(message, test_phone)
            print(f"Manu: {response}")
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    # Verificar se as variáveis de ambiente estão configuradas
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY não configurada")
        print("Configure a variável de ambiente antes de executar o teste")
        sys.exit(1)
    
    print("Iniciando testes do bot...")
    
    # Executar testes
    test_responses()
    test_conversation_flow()
    
    print("\n✅ Testes concluídos!")
    print("\nPara testar com WhatsApp real:")
    print("1. Configure as variáveis WHATSAPP_TOKEN e WHATSAPP_PHONE_NUMBER_ID")
    print("2. Execute: python3 whatsapp_bot.py")
    print("3. Configure o webhook no Facebook Developer Console")

