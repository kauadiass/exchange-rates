# services/api_client.py
import requests
from config import API_AWESOME_BASE_URL, CURRENCY_PAIR

def get_currency_quote(currency_pair: str):

    url = f"{API_AWESOME_BASE_URL}last/{currency_pair}"

   # print(f"Buscando cotação em: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        key_without_hyphen = currency_pair.replace('-', '')

        currency_info = data.get(key_without_hyphen)

        if currency_info:
            #print(f"DEBUG(api_client): Retornando currency_info (dicionário): {currency_info}")
            return currency_info
        else:
            #print(f"Chave {key_without_hyphen} não encontrada na resposta da API para {currency_pair}. Resposta: {data}")
            return None
        
    except requests.exceptions.Timeout:
        print(f"Erro: Tempo limite excedido ao buscar {currency_pair}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Erro: Falha na conexão ao buscar {currency_pair}. A API pode estar inacessível.")
    except requests.exceptions.RequestException as e:
        print(f"Erro: Erro na requisição para {currency_pair} de {url}: {e}")
        return None
    except ValueError as e:
        print(f"Erro: Resposta da API para {currency_pair} não é JSON válido : {e}")
        return None
    except Exception as e:
        print(f"Erro: Um erro inesperado ocorreu ao buscar {currency_pair}: {e}")
        return None
    
def get_dollar_quote():
    return get_currency_quote(CURRENCY_PAIR["DOLAR_BRL"])

def get_euro_quote():
    return get_currency_quote(CURRENCY_PAIR["EURO_BRL"])

def get_bitcoin_quote():
    return get_currency_quote(CURRENCY_PAIR["BITCOIN_BRL"])