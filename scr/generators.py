from collections.abc import Iterator
from typing import Generator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator:
    """Функция, которая принимает список словарей, представляющих транзакции. И возвращает итератор по валюте."""

    def filter_currency(transaction: dict) -> bool:
        name = transaction["operationAmount"]["currency"]["code"]
        if name == currency:
            return True
        else:
            return False

    return iter(filter(filter_currency, transactions))


def transaction_descriptions(transactions: list[dict]) -> Generator:
    """Генератор, который принимает список словарей с транзакциями и возвращает описание каждой операции."""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Generator:
    """Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты."""
    for num in range(start, stop + 1):
        formatted_num = f"{num:016}"
        yield f"{formatted_num[:4]} {formatted_num[4:8]} {formatted_num[8:12]} {formatted_num[12:16]}"


transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


for tr in filter_by_currency(transactions, "USD"):
    print(tr)

descriptions = transaction_descriptions(transactions)
for _ in range(len(transactions)):
    print(next(descriptions))

for card_number in card_number_generator(1, 5):
    print(card_number)
