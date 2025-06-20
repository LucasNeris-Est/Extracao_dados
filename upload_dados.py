#!/usr/bin/env python3
"""
Script para upload dos dados processados para Google Drive ou outros serviços.
Este script facilita o compartilhamento dos dados finais via links.
"""

import os
import shutil
import zipfile
from datetime import datetime
import argparse

def criar_zip_dados():
    """
    Cria um arquivo ZIP com os dados processados para facilitar o upload.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"dados_processados_{timestamp}.zip"
    
    # Verificar se os dados existem
    dados_path = "dados"
    if not os.path.exists(dados_path):
        print("❌ Diretório 'dados' não encontrado. Execute primeiro a extração.")
        return None
    
    # Lista de arquivos para incluir no ZIP
    arquivos_dados = [
        "dados/anp_precos_transformado.parquet",
        "dados/dolar.parquet",
        "dados/anp_precos.csv"  # Dados brutos como backup
    ]
    
    # Criar ZIP
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for arquivo in arquivos_dados:
            if os.path.exists(arquivo):
                zipf.write(arquivo)
                print(f"✅ Adicionado: {arquivo}")
            else:
                print(f"⚠️  Arquivo não encontrado: {arquivo}")
    
    print(f"\n📦 ZIP criado: {zip_name}")
    return zip_name

def listar_arquivos_dados():
    """
    Lista os arquivos de dados disponíveis com informações de tamanho.
    """
    dados_path = "dados"
    if not os.path.exists(dados_path):
        print("❌ Diretório 'dados' não encontrado.")
        return
    
    print("📊 Arquivos de dados disponíveis:")
    print("-" * 50)
    
    for arquivo in os.listdir(dados_path):
        caminho_completo = os.path.join(dados_path, arquivo)
        if os.path.isfile(caminho_completo):
            tamanho = os.path.getsize(caminho_completo)
            tamanho_mb = tamanho / (1024 * 1024)
            print(f"📁 {arquivo}")
            print(f"   Tamanho: {tamanho_mb:.2f} MB")
            print(f"   Caminho: {caminho_completo}")
            print()

def instrucoes_upload():
    """
    Exibe instruções para upload manual dos dados.
    """
    print("📤 INSTRUÇÕES PARA UPLOAD DOS DADOS")
    print("=" * 50)
    print()
    print("1. Google Drive:")
    print("   - Acesse drive.google.com")
    print("   - Faça upload dos arquivos da pasta 'dados/'")
    print("   - Clique com botão direito → 'Compartilhar'")
    print("   - Configure como 'Qualquer pessoa com o link pode visualizar'")
    print("   - Copie o link e atualize o README.md")
    print()
    print("2. GitHub Releases:")
    print("   - Vá para seu repositório no GitHub")
    print("   - Clique em 'Releases' → 'Create a new release'")
    print("   - Faça upload dos arquivos como assets")
    print("   - Use os links gerados no README.md")
    print()
    print("3. Outros serviços:")
    print("   - Dropbox, OneDrive, AWS S3, etc.")
    print("   - Configure links públicos e atualize o README.md")
    print()

def main():
    parser = argparse.ArgumentParser(description="Gerenciador de upload de dados")
    parser.add_argument("--listar", action="store_true", help="Listar arquivos de dados")
    parser.add_argument("--zip", action="store_true", help="Criar ZIP com dados processados")
    parser.add_argument("--instrucoes", action="store_true", help="Mostrar instruções de upload")
    
    args = parser.parse_args()
    
    if args.listar:
        listar_arquivos_dados()
    elif args.zip:
        criar_zip_dados()
    elif args.instrucoes:
        instrucoes_upload()
    else:
        print("🔧 Gerenciador de Upload de Dados")
        print("=" * 30)
        print()
        print("Comandos disponíveis:")
        print("  python upload_dados.py --listar     # Listar arquivos de dados")
        print("  python upload_dados.py --zip        # Criar ZIP para upload")
        print("  python upload_dados.py --instrucoes # Instruções de upload")
        print()
        print("Após fazer upload, atualize os links no README.md!")

if __name__ == "__main__":
    main() 