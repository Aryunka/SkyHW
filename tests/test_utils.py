import unittest
from unittest.mock import patch, mock_open
from scr.utils import loading_operation, transaction_amount_in_rub, transactions_in_rub


class TestLoadingOperation(unittest.TestCase):

    def test_loading_operation(self):
        fake_json_content = """
        [
            {"transaction_id": 1, "amount": 100},
            {"transaction_id": 2, "amount": 200}
        ]
        """

        with patch("builtins.open", mock_open(read_data=fake_json_content)):
            result = loading_operation()

        self.assertEqual(result, [
            {"transaction_id": 1, "amount": 100},
            {"transaction_id": 2, "amount": 200}
        ])

    def test_file_not_found_error(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = loading_operation()

        self.assertEqual(result, [])

    def test_json_decode_error(self):
        invalid_json_content = "{invalid_json}"

        with patch("builtins.open", mock_open(read_data=invalid_json_content)):
            result = loading_operation()

        self.assertEqual(result, [])

    def test_type_error(self):
        with patch("json.load", side_effect=TypeError):
            result = loading_operation()

        self.assertEqual(result, [])


class TestTransactionAmountInRub(unittest.TestCase):
    def setUp(self):
        self.operation = {
            "operationAmount": {
                "amount": 100,
                "currency": {"code": "USD"}
            }
        }

    @patch('scr.utils.converter_to_ruble')
    def test_transaction_amount_in_rub(self, mock_converter_to_ruble):
        mock_converter_to_ruble.return_value = '{"result": 7000}'
        result = transaction_amount_in_rub(self.operation)
        self.assertEqual(result, 7000)
        mock_converter_to_ruble.assert_called_once_with(100, "USD")

    @patch('scr.utils.converter_to_ruble')
    def test_transaction_amount_in_rub_rub(self, mock_converter_to_ruble):
        self.operation['operationAmount']['currency']['code'] = 'RUB'
        result = transaction_amount_in_rub(self.operation)
        self.assertEqual(result, 100)
        mock_converter_to_ruble.assert_not_called()


class TestTransactionsInRub(unittest.TestCase):
    def setUp(self):
        # Создаем фиктивные данные операций
        self.fake_operations = [
            {
                "operationAmount": {
                    "amount": 100,
                    "currency": {"code": "USD"}
                }
            },
            {
                "operationAmount": {
                    "amount": 150,
                    "currency": {"code": "EUR"}
                }
            }
        ]

    @patch('scr.utils.loading_operation')
    @patch('scr.utils.transaction_amount_in_rub')
    def test_transactions_in_rub_success(self, mock_transaction_amount_in_rub, mock_loading_operation):
        mock_loading_operation.return_value = self.fake_operations
        mock_transaction_amount_in_rub.side_effect = [7000, 12000]
        transactions_in_rub()
        mock_loading_operation.assert_called_once()
        mock_transaction_amount_in_rub.assert_has_calls([
            unittest.mock.call(self.fake_operations[0]),
            unittest.mock.call(self.fake_operations[1])
        ])

    @patch('scr.utils.loading_operation')
    @patch('scr.utils.transaction_amount_in_rub')
    def test_transactions_in_rub_failure(self, mock_transaction_amount_in_rub, mock_loading_operation):
        mock_loading_operation.return_value = self.fake_operations
        mock_transaction_amount_in_rub.side_effect = [None, 12000]
        transactions_in_rub()
        mock_loading_operation.assert_called_once()
        mock_transaction_amount_in_rub.assert_has_calls([
            unittest.mock.call(self.fake_operations[0]),
            unittest.mock.call(self.fake_operations[1])
        ])


if __name__ == '__main__':
    unittest.main()