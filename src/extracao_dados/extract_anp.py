import pandas as pd
from bs4 import BeautifulSoup
import requests
import io
import time
import os

def extract_anp(max_downloads=None):
    '''
    Extrai os dados da ANP de preços de combustíveis.
    Parâmetros:
        max_downloads: int, número máximo de downloads. Se não for especificado, todos os arquivos serão baixados.
    '''
    url = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/levantamento-de-precos-de-combustiveis-ultimas-semanas-pesquisadas"

    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar todos os elementos <ul>
    uls = soup.find_all('ul')

    # Para cada <ul>, buscar <li> cujo texto contenha 'Preços médios', e extrair o href do link
    hrefs = []
    for ul in uls:
        lis = ul.find_all('li')
        for li in lis:
            if 'Preços médios' in li.get_text():
                a_tag = li.find('a', href=True)
                if a_tag:
                    hrefs.append(a_tag['href'])

    # Carregar hrefs já utilizados
    hrefs_usados_path = '../../hrefs_usados.txt'
    hrefs_usados = set()
    try:
        with open(hrefs_usados_path, 'r', encoding='utf-8') as f:
            for line in f:
                hrefs_usados.add(line.strip())
    except FileNotFoundError:
        pass

    # Para cada href, baixar o arquivo xlsx ignorando as primeiras 9 (Se não encontrar, ignorar as primeiras 10) linhas e salvar em um dataframe
    # Pula hrefs já utilizados
    if not os.path.exists('../../dados'):
        os.makedirs('../../dados')
    csv_path = '../../dados/anp_precos.csv'
    downloads = 0
    for href in hrefs:
        if href in hrefs_usados:
            print(f"Pulando href já utilizado: {href}")
            continue
        if max_downloads is not None and downloads >= max_downloads:
            break
        time.sleep(1)
        try:
            response = requests.get(href, verify=False)
            content = response.content
            df = pd.read_excel(io.BytesIO(content), skiprows=9)
            if df.columns[0] == 'Unnamed: 0':
                df = pd.read_excel(io.BytesIO(content), skiprows=10)

            # Salvar imediatamente no CSV
            if not os.path.exists(csv_path):
                df.to_csv(csv_path, index=False, mode='w', encoding='utf-8')
            else:
                df.to_csv(csv_path, index=False, mode='a', header=False, encoding='utf-8')

            # Salvar href como utilizado
            with open(hrefs_usados_path, 'a', encoding='utf-8') as f:
                f.write(href + '\n')
            downloads += 1
        except Exception as e:
            print(f"Erro ao baixar o arquivo {href}: {e}")
            continue





