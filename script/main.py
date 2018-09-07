# Web Scraping do TWiki.
# Criador: Adriano Santos.
# Web Scraping para obtenção dos dados do antigo ambiente Twiki.

# P.S: Caso você utilize este código, lembre-se de me referenciar.

# Bibliotecas utilizadas.
import requests
from lxml import html
from bs4 import BeautifulSoup
import re
import unicodedata
import numpy as np
import sys


# Página inicial. Escolha a página utilizada para a autenticação.
url_inicial = "http://URL_DO_SEU_PROJETO.XXXXX/XXXXXXX/pmwiki.php?n=XXXXXX.XXXXXXXX"
# Diretório em que serão armazenados as páginas.
diretorio_onde_serao_salvos_arquivos = 'c:/temp/paginas/'
# Lista que guardará as urls utilizadas no processo de recuperação da página.
lista_urls = []

# Senha do TWiki.
# Este é um esquema utilizado pelo objeto session para submissão de dados post. Aconselho que você veja a documentação.
senha = {
	"authpw": "COLOQUE_AQUI_A_SUA_SENHA"
}

# Expressão regular para obter padrão aceito de URL.
# Utilizei essa regra porque o Twike tem um padrão que diferenciam as páginas próprias e os links externos. 
regra = re.compile(r'n\=\w+\.\w+$')

# Função utilizada para abertura de sessão.
def abre_sessao(url_inicial):
    sessao = requests.session() # Instancia o objeto de sessão.
    sessao.post(url_inicial, data = senha, headers = dict(referer=url_inicial)) # Submete dados para autenticação.
    return sessao

# Função para obtenção de uma página de acordo com a url.
def obtem_pagina(url, sessao):
    pagina = sessao.get(url, verify=False) # Obtem uma página. O parâmetro verify evita o erro relacionado à quantidade de requisições.
    return pagina

# Função utilizada para salvar conteúdo em arquivo.
def salva_pagina_html(pagina):
    soup = BeautifulSoup(pagina.content, 'html.parser') # Cria instancia de objeto do Web Scraping.
    titulo = soup.select('title')[0].get_text() # Obtem o título da página para ser utilizado como título do arquivo.
    titulo = removerAcentosECaracteresEspeciais(titulo) # Prepara string do título.
    # Escreve arquivo.
    with open(diretorio_onde_serao_salvos_arquivos + titulo + '.htm' , "w", encoding='UTF-8') as file:
        file.write(str(soup)) # Utilizado para manter a formatação. Optei por utilizar o próprio soup object à página. Fiz isso para obter os dados já formatados.
    soup = ""

# Função para obtenção dos links existentes em uma página.
def obtem_lista_de_links (pagina):
    soup = BeautifulSoup(pagina.content, 'html.parser') # Cria instancia de objeto do Web Scraping.
    links = soup.find_all('a', href=True) # Obtem todos os links existentes na página.
    for i in links:
        link = i['href'] # Obtem o link. Adicionei o MAIS_UMA_REGRA para remover um conjunto específicos de páginas desnecessárias.
        if (link not in lista_urls and regra.search(link) and not regra.search('MAIS_UMA_REGRA')) : # Se o link já estiver presente na lista e não seguir a regra definida, não é inserido.
            lista_urls.append(link) # Adiciona o link à lista.
    soup = ""

# Função para remoção de caracteres especiais para formação do título da página.
# Não desenvolvi essa função. Ela está disponível aqui: https://gist.github.com/boniattirodrigo/67429ada53b7337d2e79
# Muito obrigado.
def removerAcentosECaracteresEspeciais(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço.
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

# *******************************************
# Início do Programa
# *******************************************
if __name__ == '__main__':
    # Adiciona a primeira página.
    lista_urls.append(url_inicial)
    # Abre sessão no servidor web.
    sessao = abre_sessao(url_inicial)
    # Variáveis de apoio.
    status = True # Utilizada como condição de parada.
    contador = 0 # Utilizado para acompanhar o processamento das páginas e ser condição de parada.
    try:
        while status: # Início da captura recursiva dos dados.
            print ("Tamanho da lista: %s; Contador: %s" % (len(lista_urls), contador)) # Para acompanhar a adição dos links na lista e quantas páginas já foram capturadas.   
            pagina = obtem_pagina(lista_urls[contador], sessao) # Obtem nova página da lista.
            obtem_lista_de_links(pagina) # Atualiza lista com novos links.
            salva_pagina_html(pagina) # Salva a página corrente.
            # Condição de parada da pseudo-recursividade.
            # Como os links são adicionados a cada leitura de página, o script será executado até que a última página seja capturada e não tenha mais links sem ser visitados.
            if(contador >= len(lista_urls)):
                status = False
            contador = contador + 1 # Incrementa o contato.
    except: # Você pode melhorar isso aqui. :)
        print ("Erro inesperado:", sys.exc_info()[0])