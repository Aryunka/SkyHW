import pytest
from mypy.types import Any

from scr.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    "currency, expected_ids",
    [("USD", [939719570, 142264268, 895315941]), ("RUB", [873106923, 594226727]), ("EUR", []), (None, [])],
)
def test_filter_by_currency(currency: str, expected_ids: int, transactions: list[dict]) -> None:
    filtered_transactions = list(filter_by_currency(transactions, currency))
    actual_ids = [tr["id"] for tr in filtered_transactions]
    assert actual_ids == expected_ids


def test_filter_by_currency_no_matches(transactions: list[dict]) -> None:
    filtered_transactions = list(filter_by_currency(transactions, "EUR"))
    assert len(filtered_transactions) == 0


def test_filter_by_currency_empty_list() -> None:
    empty_transactions: list[dict[Any, Any]] = []
    filtered_transactions = list(filter_by_currency(empty_transactions, "USD"))
    assert len(filtered_transactions) == 0


@pytest.mark.parametrize(
    "expected_descriptions",
    [
        [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ],
    ],
)
def test_transaction_descriptions(expected_descriptions: str, transactions: list[dict]) -> None:
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == expected_descriptions


def test_transaction_descriptions_empty_list() -> None:
    empty_transactions: list[dict[Any, Any]] = []
    descriptions = list(transaction_descriptions(empty_transactions))
    assert len(descriptions) == 0


@pytest.mark.parametrize(
    "start, stop, expected_numbers",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        )
    ],
)
def test_card_number_generator(start: int, stop: int, expected_numbers: Any) -> None:
    generated_numbers = list(card_number_generator(start, stop))
    assert generated_numbers == expected_numbers


def test_card_number_generator_edge_cases() -> None:
    # Проверка граничных значений
    start = 9999999999999997
    stop = 9999999999999999
    expected_numbers = ["9999 9999 9999 9997", "9999 9999 9999 9998", "9999 9999 9999 9999"]
    generated_numbers = list(card_number_generator(start, stop))
    assert generated_numbers == expected_numbers


def test_card_number_generator_invalid_range() -> None:
    result = list(card_number_generator(10, 5))
    assert not result
