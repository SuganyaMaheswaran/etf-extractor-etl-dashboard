import unittest

from src import DataScraperService as ds
from unittest.mock import patch 

class TestGetFundList(unittest.TestCase):
    def test_get_fund_list_return_list(self):
        """Tests that the scraper returns a non-empty list of ETFs"""
        etfs = ds.get_fund_list(); 
        #Check that etfs is a Python List
        self.assertIsInstance(etfs, list)
        self.assertEqual(len(etfs),12)
        if etfs:
            #Check if etf[0] is a tuple
            self.assertIsInstance(etfs[0], tuple)
            self.assertEqual(len(etfs[0]), 3)
    @patch('src.DataScraperService.requests.get')
    def test_get_fund_list_mocked(self, mock_get):
        html = """
        <div class="fund-list-nav">
            <ul>
                <li>
                    <a href="/urnm-sprott-uranium-miners-etf" title="Sprott Uranium Miners ETF">URNM</a>
                </li>
            </ul>
        </div>
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.text = html
        
        etfs = ds.get_fund_list()
        self.assertIsInstance(etfs, list)
        self.assertEqual(len(etfs), 1)
        if etfs:
            self.assertEqual(len(etfs[0]), 3)



if __name__ == "__main__":
    unittest.main()