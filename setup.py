#!/usr/bin/env python3
"""
Script de configuração rápida para o bot Manu WhatsApp
"""

import os
import sys

def create_env_file():
    """Criar arquivo .env interativamente"""
    print("🤖 CONFIGURAÇÃO DO BOT MANU WHATSAPP")
    print("=" * 50)
    
    # Verificar se .env já existe
    if os.path.exists('.env'):
        response = input("Arquivo .env já existe. Sobrescrever? (s/N): ")
        if response.lower() != 's':
            print("Configuração cancelada.")
            return
    
    print("\nVamos configurar as variáveis de ambiente:")
    print("(Pressione Enter para usar valores padrão)")
    
    # Coletar informações
    config = {}
    
    print("\n📱 CONFIGURAÇÕES DO WHATSAPP:")
    config['WHATSAPP_TOKEN'] = input("WhatsApp Token: ").strip()
    config['WHATSAPP_PHONE_NUMBER_ID'] = input("Phone Number ID: ").strip()
    config['VERIFY_TOKEN'] = input("Verify Token [manu_verify_token_2024]: ").strip() or "manu_verify_token_2024"
    
    print("\n🤖 CONFIGURAÇÕES DA OPENAI:")
    config['OPENAI_API_KEY'] = input("OpenAI API Key: ").strip()
    config['OPENAI_API_BASE'] = input("OpenAI API Base [https://api.openai.com/v1]: ").strip() or "https://api.openai.com/v1"
    
    print("\n⚙️ CONFIGURAÇÕES GERAIS:")
    config['BUSINESS_PHONE_NUMBER'] = input("Número do Business [+5528999771140]: ").strip() or "+5528999771140"
    config['PORT'] = input("Porta [8000]: ").strip() or "8000"
    config['DEBUG'] = input("Debug mode [True]: ").strip() or "True"
    
    # Criar arquivo .env
    with open('.env', 'w') as f:
        f.write("# Configurações do Manu WhatsApp Bot\n")
        f.write("# Gerado automaticamente pelo setup.py\n\n")
        
        f.write("# WhatsApp Business API\n")
        f.write(f"WHATSAPP_TOKEN={config['WHATSAPP_TOKEN']}\n")
        f.write(f"WHATSAPP_PHONE_NUMBER_ID={config['WHATSAPP_PHONE_NUMBER_ID']}\n")
        f.write(f"VERIFY_TOKEN={config['VERIFY_TOKEN']}\n\n")
        
        f.write("# OpenAI\n")
        f.write(f"OPENAI_API_KEY={config['OPENAI_API_KEY']}\n")
        f.write(f"OPENAI_API_BASE={config['OPENAI_API_BASE']}\n\n")
        
        f.write("# Configurações Gerais\n")
        f.write(f"BUSINESS_PHONE_NUMBER={config['BUSINESS_PHONE_NUMBER']}\n")
        f.write(f"PORT={config['PORT']}\n")
        f.write(f"DEBUG={config['DEBUG']}\n")
    
    print("\n✅ Arquivo .env criado com sucesso!")
    
    # Verificar configurações obrigatórias
    missing = []
    if not config['WHATSAPP_TOKEN']:
        missing.append('WHATSAPP_TOKEN')
    if not config['WHATSAPP_PHONE_NUMBER_ID']:
        missing.append('WHATSAPP_PHONE_NUMBER_ID')
    if not config['OPENAI_API_KEY']:
        missing.append('OPENAI_API_KEY')
    
    if missing:
        print(f"\n⚠️ ATENÇÃO: Variáveis obrigatórias não configuradas:")
        for var in missing:
            print(f"   - {var}")
        print("\nEdite o arquivo .env antes de executar o bot.")
    else:
        print("\n🎉 Configuração completa! Você pode executar:")
        print("   python whatsapp_bot.py")

def install_dependencies():
    """Instalar dependências"""
    print("\n📦 Instalando dependências...")
    os.system("pip install -r requirements.txt")
    print("✅ Dependências instaladas!")

def run_tests():
    """Executar testes"""
    print("\n🧪 Executando testes...")
    os.system("python test_bot.py")

def main():
    """Menu principal"""
    while True:
        print("\n🤖 SETUP MANU WHATSAPP BOT")
        print("=" * 30)
        print("1. Configurar variáveis de ambiente")
        print("2. Instalar dependências")
        print("3. Executar testes")
        print("4. Iniciar bot")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '1':
            create_env_file()
        elif choice == '2':
            install_dependencies()
        elif choice == '3':
            run_tests()
        elif choice == '4':
            print("\n🚀 Iniciando bot...")
            os.system("python whatsapp_bot.py")
        elif choice == '5':
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()

