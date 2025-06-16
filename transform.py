import pandas as pd
import numpy as np

def transform():
    '''
    Transforma os dados da ANP em um formato mais adequado para o modelo de machine learning.
    '''
    dados = pd.read_csv('dados/anp_precos.csv')

    # Removendo colunas que contem Unnamed no nome
    dados = dados.drop(columns=[col for col in dados.columns if 'Unnamed' in col])

    # Ajustando o nome das colunas, removendo acentos e deixando em caixa baixa
    dados.columns = dados.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
    dados.columns = dados.columns.str.lower()
    dados.columns = dados.columns.str.replace(' ', '_')

    # Removendo linhas com NA em qualquer coluna
    dados = dados.dropna()

    # Dicionario para os tipos de cada coluna
    colunas_tipos = {
        'data_inicial': 'datetime64[ns]',
        'data_final': 'datetime64[ns]',
        'estado': 'string',
        'municipio': 'string',
        'produto': 'string',
        'numero_de_postos_pesquisados': 'int64',
        'unidade_de_medida': 'string',
        'preco_medio_revenda': 'float64',
        'desvio_padrao_revenda': 'float64',
        'preco_minimo_revenda': 'float64',
        'preco_maximo_revenda': 'float64',
        'coef_de_variacao_revenda': 'float64'
    }

    # Tratando '-' como NA float64
    dados = dados.replace('-', np.nan)

    # Convertendo as colunas para os tipos correspondentes
    dados = dados.astype(colunas_tipos)

    # Salvando em parquet
    dados.to_parquet('dados/anp_precos_transformado.parquet')