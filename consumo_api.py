import requests
import sys

url = "https://api.github.com/users/hashicorp/repos"

try:
    # Timeout de 5 segundos é lei em DevOps
    response = requests.get(url, timeout=5)
    
    # raise_for_status() é um atalho do requests. 
    # Se o status code for 4XX ou 5XX, ele gera um erro automaticamente e vai pro 'except'
    response.raise_for_status() 
    
    data = response.json()
    
    for item in data:
        # Usando o método .get() por segurança, caso a chave 'name' não venha na API
        name = item.get('name', '')
        if 'terraform' in name:
            print(f"Nome: {item['name']}")
            print(f"URL: {item['html_url']}") 

# Captura qualquer erro de rede (Timeout, DNS falho, Erro 500, etc)
except requests.exceptions.RequestException as e:
    print(f"[CRÍTICO] Falha ao comunicar com a API do GitHub: {e}")
    sys.exit(1) # Força o script a falhar para que o pipeline de CI/CD pare