import json
import logging
import os
from logging.handlers import RotatingFileHandler

from scr.external_api import converter_to_ruble

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler("../logs/utils.log", maxBytes=723, backupCount=1)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def loading_operation():
    """Функция читает JSON, преобразует в список словарей транзакций, возвращает пустой список при ошибке."""
    current_dir = os.path.dirname(__file__)
    project_dir = os.path.dirname(current_dir)
    file_path = os.path.join(project_dir, "data", "operations.json")
    try:
        logger.info("Успешно")
        with open(file_path) as f:
            datas = json.load(f)
            return datas
    except json.JSONDecodeError:
        logger.error("SONDecodeError")
        return []
    except TypeError:
        logger.error("TypeError")
        return []
    except FileNotFoundError:
        logger.error("FileNotFoundError")
        return []


def transaction_amount_in_rub(operation):
    """Функция, которая выводит одну транзакцию в рублях"""
    amount = operation["operationAmount"]["amount"]
    code = operation["operationAmount"]["currency"]["code"]
    if code == "RUB":
        logger.info("Успешно")
        return amount
    else:
        result = converter_to_ruble(amount, code)
        try:
            logger.info("Успешно")
            datas = json.loads(result)
            return datas["result"]
        except (KeyError, TypeError) as e:
            logger.error(f"Произошла ошибка: {e}.")
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
