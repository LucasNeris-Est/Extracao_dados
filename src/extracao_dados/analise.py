import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Carregar os dados
anp = pd.read_parquet('../../dados/anp_precos_transformado.parquet')
dolar = pd.read_parquet('../../dados/dolar.parquet')

# Exibir as primeiras linhas para entender os dados
def explorar_df(df, nome):
    print(f'\n--- {nome} ---')
    print(df.head())
    print(df.columns)
    print(df.dtypes)

explorar_df(anp, 'ANP')
explorar_df(dolar, 'Dólar')

# Para cada data_inicial, data_final em anp fazer uma média do valor do dolar nesse periodo, e depois fazer um left join pelo par data_inicial, data_final

### Valores unicos do par data_inicial, data_final
unicos_dt_anp = anp[['data_inicial', 'data_final']].drop_duplicates()

# Para cada data_inicial, data_final em unicos_dt_anp, fazer um left join pelo par data_inicial, data_final com dolar e calcular a média do valor do dolar nesse periodo
lista_anp_dolar = []
for index, row in unicos_dt_anp.iterrows():
    data_inicial = row['data_inicial']
    data_final = row['data_final']
    dolar_periodo = dolar[(dolar['data'] >= data_inicial) & (dolar['data'] <= data_final)]
    media_dolar = dolar_periodo['valor'].mean()
    lista_anp_dolar.append({'data_inicial': data_inicial, 'data_final': data_final, 'media_dolar': media_dolar})

df_anp_dolar = pd.DataFrame(lista_anp_dolar)

# Fazer um left join pelo par data_inicial, data_final com anp e dolar
df_anp_dolar = df_anp_dolar.merge(anp, on=['data_inicial', 'data_final'], how='left')

# Exibir as primeiras linhas para entender os dados
explorar_df(df_anp_dolar, 'ANP com Dólar')

# Criar um diretório para os gráficos
if not os.path.exists('../../graficos'):
    os.makedirs('../../graficos')

# Analisendo correlação preco_medio_revenda com media_dolar por tipo de combustivel
# Gráfico de dispesao com regressão linear com intervalo de confiança de 95% com cor vermelho

for tipo in df_anp_dolar['produto'].unique():
    df_tipo = df_anp_dolar[df_anp_dolar['produto'] == tipo]
    correlacao = df_tipo['media_dolar'].corr(df_tipo['preco_medio_revenda'], method='pearson')
    sns.regplot(x='media_dolar', y='preco_medio_revenda', data=df_tipo, color='blue', line_kws={'color': 'red'}, ci=95)
    plt.xlabel('Média do Dólar')
    plt.ylabel('Preço Médio de Revenda')
    plt.title(f'Correlação entre Preço Médio de Revenda e Média do Dólar para {tipo}')
    plt.text(0.05, 0.95, f'Correlação Pearson: {correlacao:.2f}', transform=plt.gca().transAxes, verticalalignment='top', fontsize=12, 
             color='red', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
    plt.savefig(f'../../graficos/correlação_{tipo}.png')
    plt.show()

# Analisando relação temporal (eixo X = Data, eixo Y = Preço/Cotação) para cada tipo de combustivel
# Utilizando a média do preco_medio_revenda por data_inicial

for tipo in df_anp_dolar['produto'].unique():
    df_tipo = df_anp_dolar[df_anp_dolar['produto'] == tipo]

    # Agrupando os dados por data para garantir um ponto por data
    df_tipo_anp = df_tipo.groupby('data_inicial')['preco_medio_revenda'].mean().reset_index()
    df_tipo_dolar = df_tipo.groupby('data_inicial')['media_dolar'].mean().reset_index()
    df_tipo_anp_dolar = pd.merge(df_tipo_anp, df_tipo_dolar, on='data_inicial', how='inner')

    # --- Início das Modificações para o Eixo Duplo ---

    # 1. Criar a figura e o primeiro eixo (ax1)
    # Isso nos dá mais controle sobre os elementos do gráfico.
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 2. Plotar o Preço Médio no primeiro eixo (ax1)
    cor_preco = 'tab:blue'
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Preço Médio de Revenda (R$)', color=cor_preco)
    ax1.plot(df_tipo_anp_dolar['data_inicial'], df_tipo_anp_dolar['preco_medio_revenda'], color=cor_preco, label='Preço Médio Revenda')
    ax1.tick_params(axis='y', labelcolor=cor_preco)
    ax1.tick_params(axis='x', rotation=45)


    # 3. Criar o segundo eixo (ax2) que compartilha o eixo x (twinx)
    ax2 = ax1.twinx()

    # 4. Plotar a Média do Dólar no segundo eixo (ax2)
    cor_dolar = 'tab:red'
    ax2.set_ylabel('Média do Dólar (R$)', color=cor_dolar)
    ax2.plot(df_tipo_anp_dolar['data_inicial'], df_tipo_anp_dolar['media_dolar'], color=cor_dolar, linestyle='--', label='Média Dólar')
    ax2.tick_params(axis='y', labelcolor=cor_dolar)

    # --- Fim das Modificações ---

    # Título e legenda unificada
    plt.title(f'Preço Médio de Revenda vs. Média do Dólar para {tipo}')
    fig.tight_layout() # Ajusta o layout para evitar que os rótulos se sobreponham
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9)) # Adiciona uma legenda única

    # Salvar a figura em um arquivo
    # Modifiquei o nome do arquivo para refletir o novo tipo de gráfico
    plt.savefig(f'../../graficos/relacao_temporal_eixo_duplo_{tipo.replace(" ", "_")}.png')




