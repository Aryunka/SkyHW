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
        content = response.text
        return content
    else:
        return response.reason


#
# result = converter_to_ruble(3000, "USD")
# if result:
#     print(result)
