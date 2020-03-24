# Código teste para acesso de sites, e leitura de seu conteúdo
# Autor: Guilherme Farias
# Data: 23.03.2020

# importação de bibliotecas necessárias para o processamento da descriptografia
from pprint import pprint
from urllib.request import urlopen
from hashlib import sha1
import json
import requests

#variavéis auxiliares globais

texto_final= ''

# funcao para aplicar o método SHA1 (dispersão criptográfica) = função hash criptográfica
def make_sha1(entrada, encoding='uft-8'):
    return sha1(entrada.encode(encoding)).hexdigest()

# Chamada da requisição http derivada do token: b1e88f0af0df595e223aa4b015044dafbfe9d477
url_source = urlopen('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=b1e88f0af0df595e223aa4b015044dafbfe9d477')
response_content = url_source.read()

# Impressão do json derivado da resposta da requisição
json_response = json.loads(response_content)
# data pretty printer: pprinter
#pprint(json_response)

# Criar um arquivo chamado answer.json e escrever o conteúdo de json_response nele.
with open('answer.json', 'w') as json_file:
    json.dump(json_response, json_file, indent=4)

# Abrir esse arquivo json criado e começar e ler o conteúdo dentro dele (aqui a gente tem que tomar muito cuidado para
# respeitar a indexações do json).
with open('answer.json', 'r') as json_salvo:
    data = json.load(json_salvo)
    pprint(data)

# Acessar os dados importantes do json_salvo, para o processamento da decifragem (o nome do dict é data)
cifrado_content = data['cifrado']
pulo = data['numero_casas']
print(cifrado_content)
print(pulo)

# Algoritmo para descriptografar:
# caractere = letra a ser processada da frase criptografada
alfabeto ='abcdefghijklmnopqrstuvwxyz'

# garantir que a palavra cifrada venha em letras minusculas.
cifrado_content = cifrado_content.lower()

for caractere in cifrado_content:
    if caractere in alfabeto:
        # a funcao find, vai retornar a posicao numerica da letra, caso ela seja encontrada dentro do alfabeto
        index = alfabeto.find(caractere) - pulo
        texto_final += alfabeto[index]
    elif caractere == ' ':
        #garantir que os espaços sejam respeitados
        texto_final += ' '
    elif caractere == '.':
        #garantir os pontos finais
        texto_final += '.'

print(texto_final)

# Add o resultado do texto final na aba decifrado do json
data['decifrado'] = texto_final

# Salvar o arquivo com a nova modificação
with open('answer.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

# aplicação de sha1
resumo = make_sha1(texto_final, encoding='utf-8')

# Add o resultado do resumo na aba resumo_criptografico do json
data['resumo_criptografico'] = resumo

# Salvar o arquivo com a nova modificação
with open('answer.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

#url_target = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=b1e88f0af0df595e223aa4b015044dafbfe9d477'

with open('answer.json', 'rb') as f:
    r = requests.post('https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=b1e88f0af0df595e223aa4b015044dafbfe9d477', files={'answer': f})
    print(r.status_code)

    if r.status_code == requests.codes.ok:
         print('ok')
         print(r.request.body)
         print(r.request.headers)
         resultado = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=b1e88f0af0df595e223aa4b015044dafbfe9d477')
         print(r.json())