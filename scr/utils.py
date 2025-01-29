import json
import os

from scr.external_api import converter_to_ruble


def loading_operation():
    """Функция читает JSON, преобразует в список словарей транзакций, возвращает пустой список при ошибке."""
    current_dir = os.path.dirname(__file__)
    project_dir = os.path.dirname(current_dir)
    file_path = os.path.join(project_dir, "data", "operations.json")
    try:
        with open(file_path) as f:
            datas = json.load(f)
            return datas
    except json.JSONDecodeError:
        return []
    except TypeError:
        return []
    except FileNotFoundError:
        return []


def transaction_amount_in_rub(operation):
    """Функция, которая выводит одну транзакцию в рублях"""
    amount = operation["operationAmount"]["amount"]
    code = operation["operationAmount"]["currency"]["code"]
    if code == "RUB":
        return amount
    else:
        result = converter_to_ruble(amount, code)
        try:
            datas = json.loads(result)
            return datas["result"]
        except (KeyError, TypeError) as e:
            return f"Произошла ошибка: {e}."



def transactions_in_rub():
    """Функция выводит результат конвертации транзакций в рубль."""
    operations = loading_operation()
    for operation in operations:
        rub_amount = transaction_amount_in_rub(operation)
        if rub_amount is not None:
            print(rub_amount)


if __name__ == "__main__":
    transactions_in_rub()