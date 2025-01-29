def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер карты"""
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    else:
        card_digits = list(card_number)

        for i in range(6, len(card_digits) - 4):
            card_digits[i] = "*"

        masked_card = "".join(card_digits)
        formatted_card = " ".join([masked_card[:4], masked_card[4:8], masked_card[8:12], masked_card[12:]])

        return formatted_card


def get_mask_account(account_number: str) -> str:
    """Функция, которая маскирует номер счета"""
    if len(account_number) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")
    else:
        return f"**{account_number[-4:]}"
