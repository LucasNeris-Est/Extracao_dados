# Extração de Dados

Este projeto é responsável por extrair, processar e analisar dados de diferentes fontes, gerando visualizações e insights através de gráficos.

## Requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd Extracao_dados
```

2. Crie e ative um ambiente virtual (recomendado):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências do projeto:
```bash
pip install -e .
```

## Estrutura do Projeto

```
Extracao_dados/
├── src/               # Código fonte do projeto
├── dados/            # Diretório para armazenamento de dados
├── graficos/         # Diretório para armazenamento de gráficos gerados
├── pyproject.toml    # Configuração do projeto e dependências
└── README.md         # Este arquivo
```

## Dependências Principais

- requests: Para fazer requisições HTTP
- beautifulsoup4: Para web scraping
- pandas: Para manipulação e análise de dados
- openpyxl: Para trabalhar com arquivos Excel
- pyarrow: Para processamento eficiente de dados
- tqdm: Para barras de progresso
- matplotlib e seaborn: Para criação de gráficos
- statsmodels: Para análise estatística

## Uso

1. Certifique-se de que o ambiente virtual está ativado
2. Para realizar a extração ou atualização dos dados, execute o arquivo principal:
```bash
python src/main.py
```
3. Os dados processados serão salvos na pasta `dados/`
4. Os gráficos gerados serão salvos na pasta `graficos/`

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

