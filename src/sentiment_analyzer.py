"""
File: sentiment_analyzer.py
Description: Utilizes VADER to score headlines for sentiment
Created by: Renesh Ravi
"""

import os
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def vader_sentiment_scorer(input, output):
    """
    vader_sentiment_scorer takes in an input of headlines and performs and
    sentiment analysis using VADER on the headlines and returns the results in a csv
    with the headlines and other information
    :param input: input csv file containing headlines
    :param output: output csv file containing headlines and sentiment score
    :return: pandas dataframe containing the headlines and their respective sentiment score
    """
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