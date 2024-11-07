import os
import requests
import json
from dotenv import load_dotenv
import sqlite3
from datetime import datetime

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

querys = ['floresta incêndio']

parametros = {
    'q': querys,
    'limit': 30,
    # 'cursor':'100',
    'lang': 'pt'
}

##adquirindo os dados
resposta_pesquisa = requests.get(url_search, headers=headers, params=parametros);

base_dir = os.path.abspath("src/data")
os.makedirs(base_dir, exist_ok=True)


 
if resposta_pesquisa.status_code == 200:
    resposta_pesquisa_data = resposta_pesquisa.json()
    with open(f'src/data/floresta_{datetime.now().strftime("%Y-%m-%d")}.json', 'w', encoding='utf-8') as json_file:
         json.dump(resposta_pesquisa_data, json_file, ensure_ascii=False, indent=4)
else:
    print(f'ERROR: {resposta_pesquisa.status_code}')
    print(resposta_pesquisa.text)
    

#Add o banco de dados  

##LENDO O JSON
with open(f'src/data/floresta_{datetime.now().strftime("%Y-%m-%d")}.json', 'r', encoding='utf-8') as file:
    data = json.load(file);
    
con = sqlite3.connect("src/bd/bluesky_db")

cur = con.cursor()


## EM BREVE
for item in data['posts']:
    cur.execute("INSERT INTO")
    cur.execute("INSERT INTO")
    
con.commit()
con.close()