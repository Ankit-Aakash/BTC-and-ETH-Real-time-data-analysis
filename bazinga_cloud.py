import requests
import json
import pandas as pd
import time
from google.cloud import storage


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


def upload_to_gcs(bucket_name, file_name, data):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(data.to_csv(index=False), content_type='text/csv')


def main(look_back_days, bucket_name, file_name):
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

    appended_df = pd.concat(dataframes)
    appended_df = appended_df.reset_index(drop=True)

    upload_to_gcs(bucket_name, file_name, appended_df)

    print("Data uploaded to Google Cloud Storage successfully.")


if __name__ == '__main__':
    try:
        main(60, 'your-bucket-name', 'data.csv')

    except Exception as e:
        print(f"An error occurred: {e}")
