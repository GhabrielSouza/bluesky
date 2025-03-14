import pandas as pd
import os

# CONVERTENDO TODOS OS ARQUIVOS CSV PARA PARQUET
pasta_csv = "./data_twitterFiltrado"

arquivos_csv = [os.path.join(pasta_csv, f) for f in os.listdir(pasta_csv) if f.endswith('.csv')]

dataframes = []

for arquivo in arquivos_csv:
    df = pd.read_csv(arquivo)
    dataframes.append(df)

df_final = pd.concat(dataframes, ignore_index=True)

print(df_final.shape)

df_final.to_parquet('convertido.parquet', engine='pyarrow', compression='snappy')

print("Arquivos CSV combinados e convertidos para Parquet ")

##CONVERTENDO TODOS OS DADOS DE BANCO PARA PARQUET