from services.api_client import get_dollar_quote, get_euro_quote, get_bitcoin_quote, get_dollar_history, get_euro_history, get_bitcoin_history, get_selic_rate_history
import datetime

def main():

    dollar_data = get_dollar_quote()
    euro_data = get_euro_quote()
    bitcoin_data = get_bitcoin_quote()
    
    #print(f"DEBUG(main): Tipo de dollar_data: {type(dollar_data)}")
    #print(f"DEBUG(main): Conteúdo de dollar_data: {dollar_data}")

    if dollar_data:

        dollar_bid = float(dollar_data.get('bid', 0.0))
        dollar_high = float(dollar_data.get('high', 0.0))
        dollar_low = float(dollar_data.get('low', 0.0))

        print(f"Dólar (USD-BRL) - Compra: R${dollar_bid:.2f}, Máxima: R${dollar_high:.2f}, Mínima: R${dollar_low:.2f}")
    else:
        print("Não foi possível obter a cotação do Dólar.")

    

    if euro_data:

        euro_bid = float(euro_data.get('bid', 0.0))
        euro_high = float(euro_data.get('high', 0.0))
        euro_low = float(euro_data.get('low', 0.0))

        print(f"Euro (EUR-BRL) - Compra: R${euro_bid:.2f}, Máxima: R${euro_high:.2f}, Mínima: R${euro_low:.2f}")
    else:
        print("Não foi possível obter a cotação do Euro.")

    if bitcoin_data:

        bitcoin_bid = float(bitcoin_data.get('bid', 0.0))
        bitcoin_high = float(bitcoin_data.get('high', 0.0))
        bitcoin_low = float(bitcoin_data.get('low', 0.0))

        print(f"Bitcoin (BTC-BRL) - Compra: R${bitcoin_bid:.2f}, Máxima: R${bitcoin_high:.2f}, Mínima: R${bitcoin_low:.2f}")
    else:
        print("Não foi possível obter a cotação do Bitcoin.")



    dollar_history_data = get_dollar_history(30)
    euro_history_data = get_euro_history(30)
    bitcoin_history_data = get_bitcoin_history(30)

    if dollar_history_data:
        print(f"Histórico do Dólar(últimos {len(dollar_history_data)} dias):")

        for i, day_data in enumerate(dollar_history_data):
            if i >= 5:
                break

            date_str = "N/A"

            if "timestamp" in day_data and day_data["timestamp"]:

                date_str = day_data

                try:
                    timestamp_int = int(day_data["timestamp"])
                    date_obj = datetime.datetime.fromtimestamp(timestamp_int)
                    date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, TypeError):
                    date_str = 'Erro na conversão de data'    
            bid = float(day_data.get('bid', 0.0))
            print(f"  Data: {date_str}, Compra: R${bid:.2f}")
    else:
        print("Não foi possível obter o histórico do Dólar.")

    if euro_history_data:

        print(f"Histórico do Euro(últimos {len(euro_history_data)})")

        for i, day_data in enumerate(euro_history_data):
            if i >= 5:
                break

            date_str = "N/A"

            if "timestamp" in day_data and day_data["timestamp"]:

                date_str = day_data

                try:
                    timestamp_int = int(day_data["timestamp"])
                    date_obj = datetime.datetime.fromtimestamp(timestamp_int)
                    date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                except(ValueError, TypeError):
                    date_str = "Erro na conversão de data"
            bid = float(day_data.get("bid", 0.0))
            print(f" Data: {date_str}, Compra: R${bid:.2f}")
    else:
        print("Não foi possível obter o histórico do Euro")  

    if bitcoin_history_data:

        print(f"Histórico do Bitcoin(últimos {len(bitcoin_history_data)})")

        for i, day_data in enumerate(bitcoin_history_data):
            if i >= 5:
                break

            date_str = "N/A"

            if "timestamp" in day_data and day_data["timestamp"]:

                date_str = day_data

                try:
                    timestamp_int = int(day_data["timestamp"])
                    date_obj = datetime.datetime.fromtimestamp(timestamp_int)
                    date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                except(ValueError, TypeError):
                    date_str = "Erro na conversão de data"
            bid = float(day_data.get("bid", 0.0))
            print(f"Data: {date_str}, Compra: R${bid:.2f}")
    else:
        print("Não foi possível obter o histórico do Bitcoin")



    selic_data = get_selic_rate_history(months=6)

    if selic_data:
        print(f"Taxa SELIC (últimos {len(selic_data)} registros nos 6 meses):")

        for entry in selic_data[-10:]:
            data_formatada = entry.get("data", "N/A")
            valor = float(entry.get("valor", 0.0))
            print(f" Data: {data_formatada}, Valor {valor:.2f}%")
    else:
        print("Não foi possível obter os dados da taxa selic.")
                
        
     
        
if __name__ == "__main__":
    main()