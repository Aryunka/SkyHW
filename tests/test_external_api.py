import unittest
import os
from dotenv import load_dotenv
from unittest.mock import patch
import requests_mock
from scr.external_api import converter_to_ruble

load_dotenv()

class TestConverterToRuble(unittest.TestCase):

    @patch.dict(os.environ, {'API_KEY': 'test_api_key'})
    def setUp(self):
        pass

    @requests_mock.Mocker()
    def test_successful_conversion(self, m):
        expected_response = {
            "result": 12345,
            "info": "successful conversion",
            "query": {
                "from": "USD",
                "to": "RUB",
                "amount": 100
            }
        }
        m.get('https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100', json=expected_response)
        result = converter_to_ruble(100, 'USD')
        self.assertIn('"result": 12345', result)

    @requests_mock.Mocker()
    def test_unsuccessful_request(self, m):
        m.get('https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100', status_code=400, text='Bad Request')
        result = converter_to_ruble(100, 'USD')
        self.assertEqual(result, None)

if __name__ == '__main__':
    unittest.main()
