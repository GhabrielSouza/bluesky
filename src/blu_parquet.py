import mysql.connector
import pandas as pd
import mysql

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="bluesky_db",
        charset="utf8mb4"
        )

cursores = mydb.cursor()

sql = 'SELECT postagens.cid, postagens.dataDeCriacao, postagens.texto,postagens.media, postagens.qtd_likes, postagens.qtd_repost, postagens.qtd_reply, postagens.qtd_quote, autores.did, autores.nome, autores.handle FROM postagens JOIN autores ON autores.id_autores=postagens.id_autores order by 1'

df = pd.read_sql(sql, mydb)

# Verificação se tudo veio como DataFrame corretamente. 
print(df)

mydb.close()


# Se tudo vier corretamente, só descomentar as linhas abaixo para salvar em Parquet

df.to_parquet('bluesky.parquet', engine='pyarrow')
print('Dados salvos!!')


# Aqui ta umas linhas para a gente depois ler os arquivos em Parquet, verificar se tudo foi certo

df_parquet = pd.read_parquet('bluesky.parquet', engine='pyarrow')
print(df_parquet)
