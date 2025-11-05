import json
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser

def carregar_dados(caminho_dados):
    """Carrega os dados dos arquivos JSON"""
    dados = {}
    
    for arquivo in ['cardapio.json', 'index.json', 'jogos.json']:
        caminho_arquivo = os.path.join(caminho_dados, arquivo)
        if os.path.isfile(caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                nome_base = arquivo.replace('.json', '')
                dados[nome_base] = json.load(f)
    
    return dados

def gerar_cardapio_html(cardapio_data):
    """Gera HTML para o cardapio - SEMPRE recria do zero"""
    if not cardapio_data:
        return "<!-- Cardapio vazio -->"
    
    html = ""
    for item in cardapio_data:
        html += f"""
        <div class="menu-item">
            <div class="item-image">
                <img src="{item.get('imagem', 'assets/default.jpg')}" alt="{item['nome']}">
            </div>
            <div class="item-content">
                <h3>{item['nome']}</h3>
                <p class="item-description">{item['descricao']}</p>"""
        
        if 'preco' in item and item['preco'] is not None:
            html += f'<p class="item-price">Preco: R$ {item["preco"]:.2f}</p>'
        
        html += """
            </div>
        </div>
        """
    return html

def gerar_jogos_html(jogos_data):
    """Gera HTML para os jogos - SEMPRE recria do zero"""
    if not jogos_data:
        return "<!-- Jogos vazios -->"
    
    html = ""
    for jogo in jogos_data:
        html += f"""
        <div class="menu-item">
            <div class="item-image">
                <img src="{jogo.get('imagem', 'assets/default.jpg')}" alt="{jogo['nome']}">
            </div>
            <div class="item-content">
                <h3>{jogo['nome']}</h3>
                <p class="item-description">{jogo['descricao']}</p>
                <p class="item-style">Estilo: {jogo['estilo']}</p>
                <p class="item-players">Jogadores: {jogo['jogadores']}</p>
            </div>
        </div>
        """
    return html

def gerar_areas_html(areas_data):
    """Gera HTML para as areas - SEMPRE recria do zero"""
    if not areas_data:
        return "<!-- Areas vazias -->"
    
    html = ""
    for area in areas_data:
        html += f"""
        <div class="menu-item">
            <div class="item-image">
                <img src="{area.get('imagem', 'assets/default.jpg')}" alt="{area['area']}">
            </div>
            <div class="item-content">
                <h3>{area['area'].title()}</h3>
                <p class="item-description">{area['descricao']}</p>
            </div>
        </div>
        """
    return html

def limpar_e_recriar_pagina(caminho_pagina, novo_conteudo):

    # Template base da pagina - RECRIA DO ZERO
    template_base = """<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">
    <title>GamePub</title>
</head>
<body>
    <div class="header">
        <span class="logo">GamePub</span>
        <div class="btn-box">
            <button class="hd-button" id="home-btn">Home</button>
            <button class="hd-button" id="menu-btn">Cardapio</button>
            <button class="hd-button" id="games-btn">Jogos</button>
        </div>
    </div>
    <div class="container">
{conteudo_dinamico}
    </div>
    <script src="scripts.js"></script>
</body>
</html>"""
    
    # Substitui o placeholder pelo conteudo novo
    pagina_completa = template_base.replace("{conteudo_dinamico}", novo_conteudo)
    
    # Escreve o arquivo COMPLETAMENTE NOVO
    with open(caminho_pagina, 'w', encoding='utf-8') as f:
        f.write(pagina_completa)

def gerar_pagina_completa(dados, tipo_pagina):
    """Gera conteudo completo para cada tipo de pagina - SEMPRE RECRIA DO ZERO"""
    if tipo_pagina == 'index':
        areas_data = dados.get('index', [])
        cardapio_data = dados.get('cardapio', [])
        jogos_data = dados.get('jogos', [])
        
        return f"""
        <div class="title">Aqui sua diversao e nossa prioridade!</div>
        
        <div class="container ct-2">
        {gerar_areas_html(areas_data)}
        </div>
        
        <div class="title">Menu</div>
        <div class="container ct-2">
        {gerar_cardapio_html(cardapio_data)}
        </div>
        
        <div class="title">Jogos</div>
        <div class="container ct-2">
        {gerar_jogos_html(jogos_data)}
        </div>
        """
        
    elif tipo_pagina == 'menu':
        cardapio_data = dados.get('cardapio', [])
        return f"""
        <div class="title">Cardapio</div>
        <div class="container ct-2">
        {gerar_cardapio_html(cardapio_data)}
        </div>
        """
        
    elif tipo_pagina == 'games':
        jogos_data = dados.get('jogos', [])
        return f"""
        <div class="title">Jogos</div>
        <div class="container ct-2">
        {gerar_jogos_html(jogos_data)}
        </div>
        """
    
    return ""

def atualizar_todas_paginas(dados):
    """Atualiza TODAS as paginas HTML - RECRIA COMPLETAMENTE CADA UMA"""
    paginas = [
        ('index.html', 'index'),
        ('menu.html', 'menu'),
        ('games.html', 'games')
    ]
    
    for arquivo, tipo in paginas:
        try:
            # Gera o conteudo NOVO do zero
            conteudo = gerar_pagina_completa(dados, tipo)
            
            # RECRIA a pagina completamente
            limpar_e_recriar_pagina(arquivo, conteudo)
            print(f"Pagina {arquivo} RECRIADA completamente")
            
        except Exception as e:
            print(f"Erro ao recriar {arquivo}: {e}")

class DataChangeHandler(FileSystemEventHandler):
    """Monitora mudancas nos arquivos JSON"""
    
    def __init__(self, caminho_dados):
        self.caminho_dados = caminho_dados
        self.ultima_atualizacao = 0
        
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.json'):
            return
        
        # Evitar multiplas execucoes rapidas
        tempo_atual = time.time()
        if tempo_atual - self.ultima_atualizacao < 1:
            return
        self.ultima_atualizacao = tempo_atual
        
        print(f"Arquivo modificado: {os.path.basename(event.src_path)}")
        print("RECRIANDO todas as paginas do zero...")
        
        try:
            dados = carregar_dados(self.caminho_dados)
            atualizar_todas_paginas(dados)
            print("Todas as paginas foram RECRIADAS com sucesso!")
        except Exception as e:
            print(f"Erro ao recriar paginas: {e}")

class AutoRefreshHTTPHandler(SimpleHTTPRequestHandler):
    """Handler HTTP que VERIFICA e RECRIA paginas a cada acesso"""
    
    def do_GET(self):
        # SEMPRE verificar e recriar antes de servir a pagina
        if self.path.endswith(('.html', '.htm')) or self.path == '/':
            try:
                print(f"Verificando atualizacoes para: {self.path}")
                # Usar o caminho correto para os dados
                caminho_dados = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'back', 'data')
                dados = carregar_dados(caminho_dados)
                atualizar_todas_paginas(dados)
                print("Paginas verificadas e atualizadas")
            except Exception as e:
                print(f"Verificacao de atualizacao falhou: {e}")
        
        # Servir o arquivo (que ja foi recriado)
        super().do_GET()

def iniciar_servidor_web(port=8000):
    """Inicia um servidor web local com verificacao de atualizacao"""
    os.chdir('..')  # Volta para a raiz do projeto para acessar os arquivos HTML
    
    handler = AutoRefreshHTTPHandler
    httpd = HTTPServer(('localhost', port), handler)
    
    print(f"Servidor web iniciado em http://localhost:{port}")
    print("Acesse pelo navegador - as paginas serao VERIFICADAS e RECRIADAS a cada acesso")
    
    # Abrir navegador automaticamente
    webbrowser.open(f'http://localhost:{port}')
    
    httpd.serve_forever()

def main():
    # Caminho absoluto para a pasta data
    caminho_dados = os.path.join(os.path.dirname(__file__), 'data')
    
    if not os.path.exists(caminho_dados):
        print(f"Pasta {caminho_dados} nao encontrada!")
        print("Verifique se o caminho esta correto")
        return
    
    print("Iniciando sistema de atualizacao do GamePub...")
    print("Arquivos monitorados: cardapio.json, index.json, jogos.json")
    
    # Recriar paginas inicialmente
    try:
        dados = carregar_dados(caminho_dados)
        atualizar_todas_paginas(dados)
        print("Paginas RECRIADAS inicialmente com sucesso!")
    except Exception as e:
        print(f"Erro ao recriar paginas iniciais: {e}")
        return
    
    # Iniciar monitoramento de arquivos em thread separada
    def iniciar_monitoramento():
        event_handler = DataChangeHandler(caminho_dados)
        observer = Observer()
        observer.schedule(event_handler, caminho_dados, recursive=False)
        observer.start()
        print("Monitoramento de arquivos ativo - QUALQUER mudanca RECRIA as paginas")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Parando monitoramento...")
            observer.stop()
        observer.join()
    
    # Thread para monitoramento de arquivos
    monitor_thread = threading.Thread(target=iniciar_monitoramento, daemon=True)
    monitor_thread.start()
    
    # Iniciar servidor web com verificacao
    print("Sistema de RECRIACAO COMPLETA ativado:")
    print("  1. Monitoramento em tempo real - RECRIA ao detectar mudancas")
    print("  2. Verificacao a cada acesso - RECRIA antes de servir paginas")
    print("  3. Pressione Ctrl+C para parar completamente")
    
    try:
        iniciar_servidor_web()
    except KeyboardInterrupt:
        print("Servidor web finalizado")
    except Exception as e:
        print(f"Erro no servidor web: {e}")

if __name__ == "__main__":
    main()