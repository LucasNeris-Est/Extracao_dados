import requests
import pandas as pd
import os

def extract_bc(data_inicial, data_final):
    '''
    Extrai os dados do Banco Central do Brasil de preço do dolar.
    Parâmetros:
        data_inicial: string, data inicial no formato dd/mm/yyyy
        data_final: string, data final no formato dd/mm/yyyy
    '''
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}'

    # Fazendo a requisição
    response = requests.get(url)
    dolar_data = response.json()

    # Convertendo para DataFrame
    df_dolar = pd.DataFrame(dolar_data)
    df_dolar['data'] = pd.to_datetime(df_dolar['data'], dayfirst=True)
    df_dolar['valor'] = df_dolar['valor'].astype(float)

    if not os.path.exists('../../dados'):
        os.makedirs('../../dados')
    # Salvando em parquet
    df_dolar.to_parquet('../../dados/dolar.parquet')

