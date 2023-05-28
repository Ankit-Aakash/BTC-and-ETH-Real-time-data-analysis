import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from bazinga import fetch_historical_data, concat_df
import pandas as pd

class TestFetchHistoricalData(unittest.TestCase):

    @patch('bazinga.requests.get')
    def test_fetch_historical_data_success(self, mock_get):
        # Mocking the requests module
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.text = '''
            {
                "data": {
                    "quotes": [
                        {
                            "quote": {
                                "open": 3560.89,
                                "high": 3580.43,
                                "low": 3510.21,
                                "close": 3550.76,
                                "volume": 2134800000,
                                "market_cap": 63774619254,
                                "time": 1654195200
                            }
                        },
                        {
                            "quote": {
                                "open": 2475.62,
                                "high": 2495.89,
                                "low": 2450.31,
                                "close": 2480.53,
                                "volume": 1831200000,
                                "market_cap": 293982278978,
                                "time": 1654195200
                            }
                        }
                    ]
                }
            }
        '''

        mock_get.return_value = response_mock

        crypto_id = 1
        time_start = int(datetime(2022, 2, 1).timestamp())
        time_end = int(datetime(2022, 2, 2).timestamp())
        symbol = "BTC"

        expected_df = pd.DataFrame(
            {
                "Symbol": ["BTC", "BTC"],
                "Open": [3560.89, 2475.62],
                "High": [3580.43, 2495.89],
                "Low": [3510.21, 2450.31],
                "Close": [3550.76, 2480.53],
                "Volume": [2134800000, 1831200000],
                "Market_Cap": [63774619254, 293982278978],
                "Time": [1654195200, 1654195200],
            }
        )

        # Call the function under test
        actual_df = fetch_historical_data(crypto_id, time_start, time_end, symbol)
        
        # Assert the results
        pd.testing.assert_frame_equal(actual_df, expected_df)
        
        mock_get.assert_called_with(
            f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={crypto_id}&convertId=2781&timeStart={time_start}&timeEnd={time_end}"
        )

    @patch('bazinga.pd.concat')
    def test_concat_df(self, mock_concat):
        # Creating sample dataframes
        df1 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        df2 = pd.DataFrame({"A": [7, 8, 9], "B": [10, 11, 12]})
        expected_df = pd.DataFrame({"A": [1, 2, 3, 7, 8, 9], "B": [4, 5, 6, 10, 11, 12]})

        mock_concat.return_value = expected_df

        # Call the function under test

if __name__ == "__main__":
    unittest.main()