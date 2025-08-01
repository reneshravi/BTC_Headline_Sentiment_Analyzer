"""
File: sentiment_analyzer.py
Description: Utilizes VADER to score headlines for sentiment
Created by: Renesh Ravi
"""

import os
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk



def score_sentiment(input, output):
    df = pd.read_csv(input, parse_dates=['timestamp'])

    lexicon_path = os.path.join(os.path.dirname(__file__),
                                "../resources/vader_lexicon.txt")
    sentiment_scorer = SentimentIntensityAnalyzer(lexicon_file=lexicon_path)



    df['compound_score'] = (df['headline']
                            .apply(lambda x: sentiment_scorer
                                   .polarity_scores(x)['compound']))

    os.makedirs(os.path.dirname(output), exist_ok=True)
    df.to_csv(output, index=False)

    return df

if __name__ == "__main__":
    input = os.path.join(os.path.dirname(__file__),
                         "../data/btc_headlines.csv")
    output = os.path.join(os.path.dirname(__file__),
                         "../data/btc_headlines_sentiment.csv")

    score_sentiment(input, output)