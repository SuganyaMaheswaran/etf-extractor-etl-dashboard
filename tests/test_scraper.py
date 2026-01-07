import unittest
import requests
from bs4 import BeautifulSoup
from src import DataScraperService as ds
from src import constant as c
from unittest.mock import patch 

class TestGetFundList(unittest.TestCase):
    @patch('src.DataScraperService.requests.get')
    def test_fetch_html_returns_string(self, mock_get):
        """Test that fetch_html returns a string when request succeeds"""
        dummy_html = "<html><body><h1>Test Page</h1></body></html>"
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = dummy_html
        html = ds.fetch_html("https://dummy-url.com")
        self.assertIsInstance(html, str)
        self.assertEqual(html, dummy_html)

    @patch('src.DataScraperService.requests.get')
    def test_fetch_html_handles_request_exception(self, mock_get):
        """Test that fetch_html returns empty string on request failure"""
        # Simulate a network error
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        html = ds.fetch_html("https://fake.url.com")
        self.assertEqual(html, "")

    def test_parse_fund_div_returns_soup_object(self):
        html = '<html><body><h1 class="headerDiv">Test Page</h1></body></html>'
        soup_object = ds.parse_fund_div(html, 'h1', 'headerDiv' )
        self.assertIsNotNone(soup_object)
        self.assertEqual(soup_object.name, 'h1')
        self.assertEqual(soup_object.text.strip(), "Test Page")
        self.assertIn('headerDiv', soup_object.get('class', []))

    def test_parse_fund_div_returns_none_for_invalid_html_parm(self):
        html = ''
        soup_object = ds.parse_fund_div(html, 'h1', 'headerDiv' )
        self.assertIsNone(soup_object)

    def test_parse_fund_div_returns_none_for_invalid_element_parm(self):
        html ='<html><body><h1 class="headerDiv">Test Page</h1></body></html>'
        element = None
        soup_object = ds.parse_fund_div(html, element, 'headerDiv' )
        self.assertIsNone(soup_object)
    def test_parse_fund_div_returns_none_for_invalid_class_parm(self):
        html ='<html><body><h1 class="headerDiv">Test Page</h1></body></html>'
        element = 'h1'
        class_name = ''
        soup_object = ds.parse_fund_div(html, element, class_name )
        self.assertIsNone(soup_object)
if __name__ == "__main__":
    unittest.main()