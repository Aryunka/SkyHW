import pytest

from scr.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected_result",
    [("7000792289606361", "7000 79** **** 6361"), ("1234567890123456", "1234 56** **** 3456")],
)
def test_get_mask_card_number(card_number: str, expected_result: str) -> None:
    assert get_mask_card_number(card_number) == expected_result


def test_get_card_number_invalid() -> None:
    with pytest.raises(ValueError):
        get_mask_card_number("1234")


@pytest.mark.parametrize(
    "account_number, expected_result",
    [("73654108430135874305", "**4305"), ("12345678901234567890", "**7890")],
)
def test_get_mask_account(account_number: str, expected_result: str) -> None:
    assert get_mask_account(account_number) == expected_result


def test_get_mask_account_invalid() -> None:
    with pytest.raises(ValueError):
        get_mask_account(" ")
