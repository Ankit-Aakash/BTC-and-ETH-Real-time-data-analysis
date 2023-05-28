import requests
import json
import pandas as pd
import time


def fetch_historical_data(crypto_id, time_start, time_end, symbol):
    url = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={crypto_id}&convertId=2781&timeStart={time_start}&timeEnd={time_end}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP status codes
        data = json.loads(response.text)
        quotes = data["data"]["quotes"]

        result = []
        for quote in quotes:
            values = quote["quote"].values()
            result.append(list(values))

        df = pd.DataFrame(result, columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Market_Cap', 'Time'])
        df.insert(0, 'Symbol', symbol)
        return df

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error occurred during the HTTP request: {e}")

    except (KeyError, json.JSONDecodeError):
        raise RuntimeError("Error occurred while parsing the JSON response.")


def concat_df(dataframes):
    appended_df = pd.concat(dataframes)

    # Reset index
    appended_df = appended_df.reset_index(drop=True)

    appended_df.to_csv('data.csv', index=False)


def main(look_back_days):
    crypto_data = {
        1: 'BTC',
        1027: 'ETH'
    }

    seconds_per_day = 60 * 60 * 24
    time_start = int(time.time()) - (look_back_days * seconds_per_day)
    time_end = int(time.time())

    dataframes = []
    for crypto_id, symbol in crypto_data.items():
        historical_data = fetch_historical_data(crypto_id, time_start, time_end, symbol)
        dataframes.append(historical_data)

    concat_df(dataframes)

    print("CSV file created successfully.")


if __name__ == '__main__':
    try:
        main(60)

    except Exception as e:
        print(f"An error occurred: {e}")
