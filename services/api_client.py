# services/api_client.py
import requests
from config import API_AWESOME_BASE_URL 

def get_dollar_quote():

    url = f"{API_AWESOME_BASE_URL}last/USD-BRL"
    print(f"DEBUG: URL sendo acessada: {url}") 

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() 

        data = response.json() 
        
        print(f"DEBUG: Tipo de 'data' recebido: {type(data)}") 
        print(f"DEBUG: Conteúdo de 'data' recebido: {data}")   

        
        dollar_info = data.get('USDBRL') 

        if dollar_info:
            return float(dollar_info['bid'])
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição da API: {e}")
        return None
    except Exception as e: 
        print(f"Erro inesperado no processamento da resposta da API: {e}")
        return None

def get_real_quote():

    url = f"{API_AWESOME_BASE_URL}last/BRL-USD"
    print(f"DEBUG: URL sendo acessada: {url}")

    
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    data = response.json()

    print(f"DEBUG: Tipo de 'data' recebido: {type(data)}")
    print(f"DEBUG: Conteúdo de 'data' recebido: {data}")

    real_info = data.get('BRLUSD')

    print(real_info)