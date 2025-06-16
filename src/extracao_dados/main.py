from extract_anp import extract_anp
from extract_bc import extract_bc
import datetime

# Geração e atualização dos dados

try:
    extract_anp()
    extract_bc('01/01/2022', datetime.datetime.now().strftime('%d/%m/%Y'))
    print("Dados atualizados com sucesso!")
except Exception as e:
    print(f"Erro ao atualizar os dados: {e}")