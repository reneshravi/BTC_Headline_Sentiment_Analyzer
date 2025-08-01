"""
File: finbert_sentiment.py
Description: Utilizes FinBERT to score headlines for sentiment analysis
Created by: Renesh Ravi
"""

import os
import pandas  as pd
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          pipeline)
from tqdm import tqdm
