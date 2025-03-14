import os
import requests
import json
from dotenv import load_dotenv
import sqlite3
import mysql.connector
from datetime import datetime
import pandas as pd
import re

load_dotenv()


email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

url_auth = 'https://bsky.social/xrpc/com.atproto.server.createSession'

auth = {
    'identifier': email,
    'password': password
}

autenticado = requests.post(url= url_auth, json= auth)

if autenticado.status_code == 200:
    print('Autenticado com sucesso')
    token_data = autenticado.json()
    token = token_data.get('accessJwt')
else:
    print(f'ERROR: {autenticado.status_code}')
    print(autenticado.text)
   
    
url_search = 'https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts'

headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}',
}

def sanitize_filename(filename):
    if isinstance(filename, list):
        filename = " ".join(filename)
        
    return re.sub(r'[<>:"/\\|?*[\]\']', '', filename)

def criandoJson(resposta, query):
    
    querys_limpo = sanitize_filename(query)
    
    base_dir = os.path.abspath("src/data")
    os.makedirs(base_dir, exist_ok=True)
    
    if resposta.status_code == 200:
        resposta_pesquisa_data = resposta.json()
        with open(f'src/data/{querys_limpo}_{datetime.now().strftime("%Y-%m-%d")}.json', 'w', encoding='utf-8') as json_file:
            json.dump(resposta_pesquisa_data, json_file, ensure_ascii=False, indent=4)
    else:
        print(f'ERROR: {resposta.status_code}')
        print(resposta.text)


agora = datetime.now()
data_anterior = datetime(2024,11,11)

data_anterior_formatada = data_anterior.strftime("%Y-%m-%dT%H:%M:%S")
agora_formatada = agora.strftime("%Y-%m-%dT%H:%M:%S")

dataFrame = pd.read_csv('Search_terms.twitter_terms.csv')

filtros = dataFrame['term']

for index in filtros:
    querys = index.replace('+', ' ')

    parametros = {
        'q': querys,
        'limit': 100,
        'lang': 'pt',
    }

    ##adquirindo os dados
    resposta_pesquisa = requests.get(url_search, headers=headers, params=parametros)
    
    criandoJson(resposta_pesquisa, querys)

    #Add o banco de dados  

    querys_limpo =  re.sub(r'[<>:"/\\|?*]', '', querys)
    nome_arquivo = f'src/data/{querys_limpo}_{datetime.now().strftime("%Y-%m-%d")}.json'
    print(querys_limpo)

    if os.path.exists(nome_arquivo):
        ##LENDO O JSON
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            data = json.load(file);
        
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="bluesky_db",
        charset="utf8mb4"
        )

        cursores = mydb.cursor()

        for item in data['posts']:
            
            #VARIAVEIS DE AUTOR
            did = item['author']['did']
            nomeAutor = item['author'].get('displayName', 'Nome desconhecido')
            handleAutor = item['author'].get('handle', 'Handle desconhecido')
            
            # Variavel cid de postagem
            cid = item['cid']
            
            cursores.execute("SELECT id_postagens FROM postagens WHERE cid = %s", (cid,))
                
            cid_postagens = cursores.fetchone() 
            
            if cid_postagens:
                continue
            
            cursores.execute("SELECT id_autores FROM autores WHERE did = %s", (did,))
            
            autor_existente = cursores.fetchone()
            
            if autor_existente is None:
                cursores.execute('''
                INSERT INTO autores
                (did,
                nome,
                handle)
                VALUES
                (%s,%s,%s);
                ''', (did, nomeAutor, handleAutor))
                
                cursores.execute("SELECT id_autores FROM autores WHERE did = %s", (did,))
            
                autor_existente = cursores.fetchone()
                
            
            #VARIAVEIS DE POSTAGEM

            create_date_post = item['record']['createdAt']
            create_date_post_formatado = datetime.fromisoformat(create_date_post.replace("Z", "")).strftime('%Y-%m-%d %H:%M:%S')
            
            text = item['record'].get('text', '')
            
            thumb = (item.get('embed', {}).get('images', [{}])[0].get('thumb', 'Thumb não disponível'))
            
            like_count = item.get('likeCount', 0)
            repost_count = item.get('repostCount', 0)
            reply_count = item.get('replyCount', 0)
            quote_count = item.get('quoteCount', 0)
            
            quote_to = None
            reply_to = None
            
            
            autor_existente_formatado = autor_existente[0] 
            
            cursores.execute('''
                    INSERT INTO postagens
                    (
                        cid,
                        dataDeCriacao,
                        texto,
                        media,
                        qtd_likes,
                        qtd_repost,
                        qtd_reply,
                        qtd_quote,
                        id_autores,
                        quote_to,
                        reply_to
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (cid, create_date_post_formatado, text, thumb, like_count, repost_count, reply_count, quote_count, autor_existente_formatado, quote_to, reply_to))
            cursores.reset()

        mydb.commit()
        mydb.close()
        print("Dados inseridos")