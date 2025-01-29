import pytest

from scr.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "type_card_number, expected_result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(type_card_number: str, expected_result: str) -> None:
    assert mask_account_card(type_card_number) == expected_result


def test_mask_account_card_invalid() -> None:
    with pytest.raises(ValueError):
        mask_account_card("Error")


@pytest.mark.parametrize(
    "string_date, expected_result",
    [("2024-03-11T02:26:18.671407", "11.03.2024"), ("2023-12-31T23:59:59.999999", "31.12.2023")],
)
def test_get_date(string_date: str, expected_result: str) -> None:
    assert get_date(string_date) == expected_result


def test_get_date_invalid() -> None:
    with pytest.raises(ValueError):
        get_date("Error")
