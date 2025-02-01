import os

import requests
from dotenv import load_dotenv

load_dotenv()


def converter_to_ruble(amount, code):
    """Функция преобразует транзакции в рубли, учитывая курсы валют."""
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={code}&amount={amount}"
    api_key = os.getenv("API_KEY")
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["result"]
    else:
        return response.reason


amount = 30001
code = "USD"
result = converter_to_ruble(amount, code)
if result:
    print(result)
