# main.py
from services.api_client import get_real_quote

if __name__ == "__main__":
    print("Iniciando coleta de dados...")
    real = get_real_quote()
    if real:
        print(f"Cotação do Real: R${real:.2f}")
    else:
        print("Não foi possível obter a cotação do dólar.")
    print("Coleta concluída.")