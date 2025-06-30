from services.api_client import get_dollar_quote, get_euro_quote, get_bitcoin_quote, get_dollar_history, get_euro_history, get_bitcoin_history, get_selic_rate_history
import datetime
from utils.logger import logger

def main():

    logger.info("Iniciando a coleta de dados de moedas...")

    moedas_atuais_para_coletar = {
        "Dólar": get_dollar_quote,
        "Euro": get_euro_quote,
        "Bitcoin": get_bitcoin_quote
    }
    
    collected_current_quotes = {}

    for nome_moeda, get_quote_func in moedas_atuais_para_coletar.items():

        logger.info(f"Coletando cotação atual para {nome_moeda}...")
        quote_data = get_quote_func()

        if quote_data:
            bid = float(quote_data.get('bid', 0.0))
            high = float(quote_data.get('high', 0.0))
            low = float(quote_data.get('low', 0.0))
            logger.info(f"{nome_moeda} (BRL) - Compra: R${bid:.2f}, Máxima: R${high:.2f}, Mínima: R${low:.2f}")
            collected_current_quotes[nome_moeda] = {
                "bid": bid, "high": high, "low": low,
                "code": quote_data.get('code'),
                "codein": quote_data.get('codein'),
                "name": quote_data.get('name')
            }
        else:
            logger.error(f"Não foi possível obter a cotação do {nome_moeda}.")

    logger.info("\n--- Coletando Dados Históricos (Últimos 30 dias) ---")
    moedas_historico_para_coletar = {
        "Dólar": get_dollar_history,
        "Euro": get_euro_history,
        "Bitcoin": get_bitcoin_history
    }
    collected_history_data = {}

    for nome_moeda, get_history_func in moedas_historico_para_coletar.items():

        logger.info(f"Coletando histórico para {nome_moeda}...")
        history_data = get_history_func(30)

        if history_data:

            logger.info(f"Histórico do {nome_moeda} (últimos {len(history_data)} dias):")
            collected_history_data[nome_moeda] = []
            
            for i, day_data in enumerate(history_data):
                date_str = 'N/A' 
                if 'create_date' in day_data and day_data['create_date']:
                    date_str = day_data['create_date']
                elif 'timestamp' in day_data and day_data['timestamp']:
                    try:
                        timestamp_int = int(day_data['timestamp'])
                        date_obj = datetime.datetime.fromtimestamp(timestamp_int)
                        date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                    except (ValueError, TypeError):
                        date_str = 'Erro na conversão de data'
                
                bid = float(day_data.get('bid', 0.0))
                logger.debug(f"  Data: {date_str}, Compra: R${bid:.2f}")
                collected_history_data[nome_moeda].append({
                    "date": date_str, "bid": bid, "high": float(day_data.get('high', 0.0)),
                    "low": float(day_data.get('low', 0.0))
                })
            logger.info(f"Histórico de {nome_moeda} coletado com sucesso.")
        else:
            logger.error(f"Não foi possível obter o histórico do {nome_moeda}.")

    logger.info("\n--- Coletando Dados da Taxa SELIC (Últimos 6 meses) ---")
    selic_data = get_selic_rate_history(months=6) 
    collected_selic_data = [] 
    if selic_data:
        hoje = datetime.date.today()
        seis_meses_atras = hoje - datetime.timedelta(days=30 * 6)
        
        for entry in selic_data:
            try:
                entry_date = datetime.datetime.strptime(entry['data'], '%d/%m/%Y').date()
                if entry_date >= seis_meses_atras:
                    collected_selic_data.append({
                        "data": entry.get("data"),
                        "valor": float(entry.get("valor", 0.0))
                    })
            except (ValueError, KeyError) as e:
                logger.error(f"Não foi possível processar entrada de data da SELIC: {entry}. Detalhe: {e}")
                continue
        
        if collected_selic_data:
            logger.info(f"Taxa SELIC (últimos {len(collected_selic_data)} registros nos 6 meses) coletada.")
            for entry in collected_selic_data[-5:]:
                logger.info(f"  Data: {entry['data']}, Valor: {entry['valor']:.2f}%")
        else:
            logger.warning("Nenhum dado SELIC encontrado nos últimos 6 meses ou falha no filtro.")
    else:
        logger.error("Não foi possível obter os dados da Taxa SELIC.")

    logger.info("\nColeta de todos os dados concluída. Pronto para gerar o Excel.")
        
if __name__ == "__main__":
    main()