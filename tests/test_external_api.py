import os
from unittest.mock import patch

import pytest
import requests_mock
from dotenv import load_dotenv

from scr.external_api import converter_to_ruble

load_dotenv()


@pytest.fixture(autouse=True)
def setup_env():
    os.environ["API_KEY"] = "test_api_key"


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0].endswith("convert?to=RUB&from=USD&amount=100"):
        return MockResponse({"result": 12345}, 200)
    elif args[0].endswith("convert?to=RUB&from=EUR&amount=50"):
        return MockResponse({"result": 4567}, 200)
    else:
        return MockResponse(None, 400)


@patch("scr.external_api.requests.get", side_effect=mocked_requests_get)
def test_successful_conversion(mock_get):
    result = converter_to_ruble(100, "USD")
    assert result == 12345


@patch("scr.external_api.requests.get", side_effect=mocked_requests_get)
def test_another_successful_conversion(mock_get):
    result = converter_to_ruble(50, "EUR")
    assert result == 4567


def test_unsuccessful_request():
    with requests_mock.Mocker() as m:
        m.get(
            "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100",
            status_code=400,
            text="Bad Request",
        )

        result = converter_to_ruble(100, "USD")
        assert result is None
