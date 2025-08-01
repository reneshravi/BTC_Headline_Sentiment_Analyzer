"""
File: merge_sentiment.py
Description: Merges the aggregated sentiment and news volume signals with
hourly price returns
Created by: Renesh Ravi
"""

import pandas
import os

def merge_sentiment(price_file, sentiment_file, output_file):
