import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

url_auth = 'https://bsky.social/xrpc/com.atproto.server.createSession'

auth = {
    'identifier': email,
    'password': password
}

autenticado = requests.post(url= url_auth, json= auth);

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

querys = ['floresta' , 'incêndio']

parametros = {
    'q': querys,
    'sort': 'top',
    'lang': 'pt',
    'limit': 100
}

resposta_pesquisa = requests.get(url_search, headers=headers, params=parametros);

if resposta_pesquisa.status_code == 200:
    resposta_pesquisa_data = resposta_pesquisa.json()
    with open('search_data.json', 'w', encoding='utf-8') as json_file:
         json.dump(resposta_pesquisa_data, json_file, ensure_ascii=False, indent=4)
else:
    print(f'ERROR: {resposta_pesquisa.status_code}')
    print(resposta_pesquisa.text)
    
