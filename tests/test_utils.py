import pytest
import json
from unittest.mock import Mock, patch, mock_open
from scr.utils import loading_operation, transaction_amount_in_rub, transactions_in_rub


expected_result = [
    {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    },
    {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": "8221.37",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560"
    }
]


def test_loading_operation_success():
    mock_data = json.dumps(expected_result)
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = loading_operation("data_file.json")
        assert result == expected_result

def test_loading_operation_json_decode_error():
    mock_data = 'invalid json'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = loading_operation("data_file.json")
        assert result == []

def test_loading_operation_type_error():
    mock_data = '{"id": 1, "amount": 100}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = loading_operation("data_file.json")
        assert result == []

def test_loading_operation_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = loading_operation("data_file.json")
        assert result == []

def test_loading_operation_empty_file():
    mock_data = ''
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = loading_operation("data_file.json")
        assert result == []

# Test transaction_amount_in_rub function
def test_transaction_amount_in_rub_already_rub():
    operation = {
        "operationAmount": {
            "amount": "1000.00",
            "currency": {
                "code": "RUB"
            }
        }
    }
    result = transaction_amount_in_rub(operation)
    assert result == "1000.00"

def test_transaction_amount_in_rub_conversion_success():
    operation = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }
    mock_conversion_result = '{"result": 7500.00}'

    with patch("scr.external_api.converter_to_ruble", return_value=mock_conversion_result):
        result = transaction_amount_in_rub(operation)
        assert result == 7500.00

def test_transaction_amount_in_rub_conversion_key_error():
    operation = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }
    mock_conversion_result = '{"error": "Invalid data"}'  # Simulated invalid conversion result

    with patch("scr.external_api.converter_to_ruble", return_value=mock_conversion_result):
        result = transaction_amount_in_rub(operation)
        assert result == "Произошла ошибка: 'result'."

def test_transaction_amount_in_rub_conversion_type_error():
    operation = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }
    mock_conversion_result = "invalid json"  # Simulated invalid JSON

    with patch("scr.external_api.converter_to_ruble", return_value=mock_conversion_result):
        result = transaction_amount_in_rub(operation)
        assert "Произошла ошибка:" in result

# Test transactions_in_rub function
def test_transactions_in_rub_success(capsys):
    mock_operations = [
        {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        },
        {
            "operationAmount": {
                "amount": "500.00",
                "currency": {
                    "code": "RUB"
                }
            }
        }
    ]

    with patch("scr.utils.loading_operation", return_value=mock_operations):
        with patch("scr.utils.transaction_amount_in_rub", side_effect=["7500.00", "500.00"]):
            transactions_in_rub()
            captured = capsys.readouterr()
            assert captured.out == "7500.00\n500.00\n"

def test_transactions_in_rub_empty_list(capsys):
    with patch("scr.utils.loading_operation", return_value=[]):
        transactions_in_rub()
        captured = capsys.readouterr()
        assert captured.out == ""

def test_transactions_in_rub_conversion_error(capsys):
    mock_operations = [
        {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }
    ]
    with patch("scr.utils.loading_operation", return_value=mock_operations):
        with patch("scr.utils.transaction_amount_in_rub", return_value=None):
            transactions_in_rub()
            captured = capsys.readouterr()
            assert captured.out == ""