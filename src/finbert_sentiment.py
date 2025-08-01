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

def finbert_sentiment_scorer(input, output):
    """
    Applies FinBERT sentiment classification to headlines and saves the results.
    :param input: Path to the input CSV file containing columns ['timestamp', 'headline'].
    :param output: Path where the output CSV with sentiment labels will be saved.
    :return: A DataFrame containing the original data with an additional column:
            - 'finbert_sentiment': The predicted sentiment label for each headline.
    """
    df = pd.read_csv(input, parse_dates=['timestamp'])

    model_name = "yiyanghkust/finbert-tone"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    sentiments = []
    for headline in tqdm(df['headline'], desc="Scoring Sentiment with "
                                              "FinBERT"):
        result = nlp(headline)[0]
        sentiments.append(result['label'])

    df['finbert_sentiment'] = sentiments

    os.makedirs(os.path.dirname(output), exist_ok=True)
    df.to_csv(output, index=False)
    return df

if __name__ == "__main__":
    input = os.path.join(os.path.dirname(__file__),
                         "../data/btc_headlines.csv")
    output = os.path.join(os.path.dirname(__file__),
                         "../data/btc_headlines_sentiment_finbert.csv")

    finbert_sentiment_scorer(input, output)