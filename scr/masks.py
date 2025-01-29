import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler("../logs/masks.log", maxBytes=723, backupCount=1)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер карты"""
    if len(card_number) != 16:
        logger.error("Номер карты должен содержать 16 цифр")
        raise ValueError("Номер карты должен содержать 16 цифр")

    else:
        logger.info("Номер карты скрыт")
        card_digits = list(card_number)

        for i in range(6, len(card_digits) - 4):
            card_digits[i] = "*"

        masked_card = "".join(card_digits)
        formatted_card = " ".join([masked_card[:4], masked_card[4:8], masked_card[8:12], masked_card[12:]])
        return formatted_card


def get_mask_account(account_number: str) -> str:
    """Функция, которая маскирует номер счета"""
    if len(account_number) != 20:
        logger.error("Номер счета должен содержать 20 цифр")
        raise ValueError("Номер счета должен содержать 20 цифр")
    else:
        logger.info("Номер счета скрыт")
        return f"**{account_number[-4:]}"


if __name__ == "__main__":
    try:
        get_mask_card_number("1234567890123456")
        get_mask_account("12345678901234567890")
    except Exception as e:
        logger.exception(e)
