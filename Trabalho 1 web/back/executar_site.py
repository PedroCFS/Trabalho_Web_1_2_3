import subprocess
import sys
import os

def main():
    print("GamePub - Gerador de Site")
    print("=" * 40)
    
    caminho_dados = None
    modo_watch = False
    
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg in ['--watch', '-w']:
                modo_watch = True
            elif not arg.startswith('-'):
                caminho_dados = arg
    
    # Loop para obter caminho válido
    while True:
        try:
            if not caminho_dados:
                caminho_dados = input("Digite o caminho para o arquivo ou diretório com dados JSON: ").strip()
            
            if not caminho_dados:
                print("Caminho não pode estar vazio. Tente novamente.")
                continue
                
            # Verificar se o caminho existe
            if not os.path.exists(caminho_dados):
                print(f"Caminho não encontrado: {caminho_dados}")
                print("Tente novamente.")
                caminho_dados = None
                continue
                
            break
            
        except KeyboardInterrupt:
            print("\nOperação cancelada.")
            sys.exit(0)
        except Exception as e:
            print(f"Erro: {e}")
            print("Tente novamente.")
            caminho_dados = None
    
    # Executar o script principal
    try:
        print("Processando dados...")
        
        # Construir comando
        cmd = [sys.executable, "back/gerar_site.py", caminho_dados]
        if modo_watch:
            cmd.append("--watch")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            print(result.stdout)
            if not modo_watch:
                print("\nSite gerado com sucesso!")
                print("Abra os arquivos HTML no navegador para visualizar")
                print("\nPara monitorar mudanças automaticamente, execute:")
                print(f"python back/executar_site.py {caminho_dados} --watch")
        else:
            print("Erro ao gerar o site:")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
