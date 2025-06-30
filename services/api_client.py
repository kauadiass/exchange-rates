from config import API_AWESOME_BASE_URL, CURRENCY_PAIR, API_BCB_SELIC_URL
import requests
import datetime
from utils.logger import logger

#CURRENCY QUOTE
def get_currency_quote(currency_pair: str):

    url = f"{API_AWESOME_BASE_URL}last/{currency_pair}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        key_without_hyphen = currency_pair.replace('-', '')

        currency_info = data.get(key_without_hyphen)

        if currency_info:
            return currency_info
        else:
            return None
        
    except requests.exceptions.Timeout as e:
        logger.error(f"Tempo limite excedido ao buscar {currency_pair}: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Falha na conexão ao buscar {currency_pair}. A API pode estar inacessível: {e}")
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else "N/A"
        error_text = e.response.text if e.response else "N/A"
        logger.error(f"HTTP Error ao buscar {currency_pair}: Status {status_code}. Detalhe: {e}. Resposta da API: {error_text[:200]}...")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição para {currency_pair} de {url}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Resposta da API para {currency_pair} não é JSON válido: {e}")
        return None
    except Exception as e:
        logger.critical(f"Um erro inesperado ocorreu ao buscar {currency_pair}: {e}")
        return None
    
def get_dollar_quote():
    return get_currency_quote(CURRENCY_PAIR["DOLAR_BRL"])

def get_euro_quote():
    return get_currency_quote(CURRENCY_PAIR["EURO_BRL"])

def get_bitcoin_quote():
    return get_currency_quote(CURRENCY_PAIR["BITCOIN_BRL"])

#CURRENCY HISTORY
def get_currency_history(currency_pair: str, days: int = 30):

    url = f"{API_AWESOME_BASE_URL}daily/{currency_pair}/{days}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data
        else:
            logger.warning(f"Resposta inesperada para histórico de {currency_pair}. Não é uma lista. Resposta: {data}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição de histórico para {currency_pair}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Resposta de histórico para {currency_pair} não é JSON válido: {e}")
        return None
    except Exception as e:
        logger.critical(f"Um erro inesperado ocorreu ao buscar histórico para {currency_pair}: {e}")
        return None
    
def get_dollar_history(days: int = 30):
    return get_currency_history(CURRENCY_PAIR["DOLAR_BRL"], days)

def get_euro_history(days: int = 30):
    return get_currency_history(CURRENCY_PAIR["EURO_BRL"], days)

def get_bitcoin_history(days: int = 30):
    return get_currency_history(CURRENCY_PAIR["BITCOIN_BRL"], days)

#SELIC RATE 

def get_selic_rate_history(months: int = 6):

    hoje = datetime.date.today()
    data_final = hoje.strftime("%d/%m/%Y")

    data_inicial_obj = hoje - datetime.timedelta(days=30 * months)
    data_inicial = data_inicial_obj.strftime("%d/%m/%Y")

    url = f"{API_BCB_SELIC_URL}&dataInicial={data_inicial}&dataFinal={data_final}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, list) and data:
            return data
        else:
            return None
    except requests.exceptions.Timeout:
        logger.error(f"Tempo limite excedido ao buscar taxa selic.")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Erro de conexão ao buscar taxa selic. API pode estar inacessível")
        return None
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else "N/A"
        error_text = e.response.text if e.response else "N/A"
        logger.error(f"Erro ao buscar taxa SELIC: Status {status_code}. Detalhe: {e}. Resposta da API: {error_text[:200]}...")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição geral da SELIC: {e}")
        return None
    except ValueError as e:
        logger.error(f"Resposta da API para SELIC não é JSON válido: {e}")
        return None
    except Exception as e:
        logger.critical(f"Um erro inesperado ocorreu ao buscar taxa SELIC: {e}")
        return None