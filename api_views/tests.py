import unittest
from unittest.mock import patch, Mock

import requests

from test_func import is_valid_url, fetch_data


class TestUtilities(unittest.TestCase):

    def test_is_valid_url(self):
        # Valid URLs
        self.assertTrue(is_valid_url("https://www.example.com"))
        self.assertTrue(is_valid_url("http://example.com"))

        # Invalid URLs
        self.assertFalse(is_valid_url("not-a-url"))
        self.assertFalse(is_valid_url("http://"))
        self.assertFalse(is_valid_url("ftp://example.com"))  # Assuming only HTTP/HTTPS are valid

        # Too long URL
        long_url = "http://" + "a" * 2049 + ".com"
        self.assertFalse(is_valid_url(long_url))

    @patch('your_module_name.requests.get')  # Mock requests.get
    def test_fetch_data_success(self, mock_get):
        # Mock a successful HTTP response
        mock_get.return_value = Mock(status_code=200, text='Success response')

        result = fetch_data("https://api.example.com/data")
        self.assertEqual(result, {'status': 'success', 'data': 'Success response'})

    @patch('your_module_name.requests.get')
    def test_fetch_data_client_error(self, mock_get):
        # Mock a 404 client error response
        mock_get.return_value = Mock(status_code=404, reason='Not Found')

        result = fetch_data("https://api.example.com/data")
        self.assertEqual(result, {'status': 'error', 'data': 'Client error 404: Not Found'})

    @patch('your_module_name.requests.get')
    def test_fetch_data_server_error(self, mock_get):
        # Mock a 500 server error response
        mock_get.return_value = Mock(status_code=500, reason='Internal Server Error')

        result = fetch_data("https://api.example.com/data")
        self.assertEqual(result, {'status': 'error', 'data': 'Server error 500: Internal Server Error'})

    @patch('your_module_name.requests.get')
    def test_fetch_data_request_exception(self, mock_get):
        # Simulate a RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")

        result = fetch_data("https://api.example.com/data")
        self.assertEqual(result, {'status': 'error', 'data': 'Connection Error'})

    def test_fetch_data_invalid_url(self):
        result = fetch_data("invalid-url")
        self.assertEqual(result, {'status': 'error', 'data': 'API URL is required'})

if __name__ == '__main__':
    unittest.main()