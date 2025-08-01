"""
File: fetch_btc_headlines.py
Description: contains function fetch_btc_headlines to generate a csv
aggregating headlines related to BTC
Created by: Renesh Ravi
"""

import os
import requests
import pandas as pd
from datetime import datetime


def fetch_btc_headlines(api_key):
    """
    fetch_btc_headlines makes a request to CryptoPanic to get the news
    headlines related to BTC
    :param api_key: CryptoPanic API key
    :return: csv containing BTC headlines
    """
    url = "https://cryptopanic.com/api/v1/posts/"

    params = {
        "auth_token": api_key,
        "currencies": "BTC",
        "kind": "news",
        "public": "true"
    }


    response = requests.get(url, params=params)
    response.raise_for_status()

    posts = response.json()['results']

    headlines = []

    for post in posts:
        source_title = post['source']['title'] if 'source' in post and post[
            'source'] else "Unknown"

        headlines.append({
            "timestamp": datetime.fromisoformat(post['published_at']),
            "headline": post.get('title', 'No Title'),
            "source": source_title,
            "url": post.get('url', 'Unknown')
        })

    df = pd.DataFrame(headlines)

    data_dir = os.path.join(os.path.dirname(__file__), "../data")
    os.makedirs(data_dir, exist_ok=True)

    output_path = os.path.join(data_dir, "btc_headlines.csv")
    df.to_csv(output_path, index=False)

    return df