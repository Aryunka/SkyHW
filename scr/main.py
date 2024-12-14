from scr.masks import get_mask_account, get_mask_card_number
from scr.processing import filter_by_state, sort_by_date
from scr.widget import get_date, mask_account_card

card_number = input("Номер карты ")
account_number = input("Номер счета ")
print(get_mask_card_number(card_number))
print(get_mask_account(account_number))
type_card_number = input("Тип и номер ")
string_date = input("Дата ")
print(mask_account_card(type_card_number))
print(get_date(string_date))
print(filter_by_state)
print(sort_by_date)
