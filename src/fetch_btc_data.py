"""
File: fetch_btc_data.py
Description:
Created by: Renesh Ravi
"""
import os

import requests
import pandas as pd

def fetch_btc_data(api_key, limit=2000):
    """
    fetch_btc_data generates a csv containing the last 2000 hours of
    bitcoin data, namely the OHLCV data.
    :param api_key: CryptoCompare API key
    :param limit: 2000 hours per request
    """

    # Creates 'data' directory if it does not exist
    data_directory = os.path.join(os.path.dirname(__file__), "../data")
    os.makedirs(data_directory, exist_ok=True)

    url = "https://min-api.cryptocompare.com/data/v2/histohour"
    params = {
        "fsym": "BTC",
        "tsym": "USD",
        "limit": limit,
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()['Data']['Data']
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)

    output_path = os.path.join(data_directory, "btc_data.csv")
    df.to_csv(output_path)