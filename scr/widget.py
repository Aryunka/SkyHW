from datetime import datetime

from scr.masks import get_mask_account, get_mask_card_number


def mask_account_card(type_card_number: str) -> str:
    """Функция, которая маскирует номер карты или счета с типом"""
    numbers_str = ""
    type_str = ""
    for i in type_card_number:
        if i.isalpha():
            type_str += i
        elif i.isdigit():
            numbers_str += i
    if type_card_number[-18:].isdigit():
        mask_card = type_str + " " + get_mask_account(numbers_str)
        return mask_card
    else:
        mask_account = type_str + " " + get_mask_card_number(numbers_str)
        return mask_account


def get_date(string_date: str) -> str:
    """Функция, которая выводит дату"""
    date_obj = datetime.fromisoformat(string_date)
    result = date_obj.strftime("%d.%m.%Y")
    return result
