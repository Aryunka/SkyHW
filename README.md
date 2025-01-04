# Проект по курсу Python
## Описание
Этот проект - это виджет, который показывает несколько последних успешных банковских операций.
## Установка
1. Клонируйте репозиторий 
`https://github.com/Ashiuna/SkyHW.git`
2. Установите зависимости 
`poerty install`
3. Запустите файл **main.py**
## Описание функций
### get_mask_card_number
Функция `get_mask_card_number` принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован и отображается в формате 
`XXXX XX** **** XXXX`, где `X` — это цифра номера. То есть видны первые 6 цифр и последние 4 цифры, остальные символы отображаются звездочками, номер разбит по блокам по 4 цифры, разделенным пробелами.
```
Пример работы функции:
7000792289606361     # входной аргумент
7000 79** **** 6361  # выход функции
```
### get_mask_account
Функция `get_mask_account` принимает на вход номер счета и возвращает его маску. Номер счета замаскирован и отображается в формате 
`**XXXX` , где `X` — это цифра номера. То есть видны только последние 4 цифры номера, а перед ними — две звездочки. 
```
Пример работы функции:
73654108430135874305  # входной аргумент
**4305  # выход функции
```
### mask_account_card
Функция умеет обрабатывать информацию как о картах, так и о счетах.
Она может:
- Принимать один аргумент — строку, содержащую тип и номер карты или счета.
Аргументом может быть строка типа 
Visa Platinum 7000792289606361, или Maestro 7000792289606361, или Счет 73654108430135874305.
- Возвращать строку с замаскированным номером. Для карт и счетов используйте разные типы маскировки.
### filter_by_state
Функция принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари, у которых ключ `state` соответствует указанному значению.
### sort_by_date
Функция принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание).

## Тестированине
### test_masks
#### @pytest.mark.parametrize
#### test_masks
Данные для get_mask_card_number
````
@pytest.mark.parametrize(
    "card_number, expected_result",
    [("7000792289606361", "7000 79** **** 6361"), ("1234567890123456", "1234 56** **** 3456")],
)
````

Данные для test_get_mask_account
````
@pytest.mark.parametrize(
    "account_number, expected_result",
    [("73654108430135874305", "**4305"), ("12345678901234567890", "**7890")],
)
````
#### test_get_mask_card_number
Тест функции get_mask_card_number
#### test_get_mask_account
Тест функции get_mask_account
#### test_get_mask_account_invalid
Тест функции get_mask_account на ошибки ValueError
### test_processing
Данные для test_filter_by_state, test_sort_by_date, 
````
@pytest.fixture
def fix_list() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
````
#### test_filter_by_state
Тест функции filter_by_state
#### test_sort_by_date
Тест функции sort_by_date
#### test_sort_by_date_invalid
Тест функции sort_by_date на ошибку TypeError
### test_widget
Данные для test_mask_account_card
````
@pytest.mark.parametrize(
    "type_card_number, expected_result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
````
Данные для test_get_date
````
@pytest.mark.parametrize(
    "string_date, expected_result",
    [("2024-03-11T02:26:18.671407", "11.03.2024"), ("2023-12-31T23:59:59.999999", "31.12.2023")],
)
````
#### test_mask_account_card
Тест функции mask_account_card
#### test_mask_account_card_invalid
Тест функции mask_account_card на ошибки ValueError
#### test_get_date
Тест функции get_date
#### test_get_date_invalid
Тест функции get_date на ошибки TypeError