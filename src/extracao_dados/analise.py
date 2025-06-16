import pandas as pd
import seaborn as sns

# Carregar os dados
anp = pd.read_parquet('dados/anp_precos_transformado.parquet')
dolar = pd.read_parquet('dados/dolar.parquet')

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

# Analisendo correlação preco_medio_revenda com media_dolar por tipo de combustivel
# Gráfico de dispesao com regressão linear

for tipo in df_anp_dolar['produto'].unique():
    df_tipo = df_anp_dolar[df_anp_dolar['produto'] == tipo]
    sns.regplot(x='media_dolar', y='preco_medio_revenda', data=df_tipo)
    plt.xlabel('Média do Dólar')
    plt.ylabel('Preço Médio de Revenda')
    plt.title(f'Correlação entre Preço Médio de Revenda e Média do Dólar para {tipo}')
    plt.savefig(f'graficos/correlação_{tipo}.png')
    plt.show()




