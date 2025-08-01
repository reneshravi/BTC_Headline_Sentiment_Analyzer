"""
File: sentiment_analyzer.py
Description: Utilizes VADER to score headlines for sentiment analysis
Created by: Renesh Ravi
"""

import os
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def vader_sentiment_scorer(input, output):
    """
    Applies VADER sentiment classification to headlines and saves the results.
    :param input: Path to the input CSV file containing columns ['timestamp', 'headline'].
    :param output: Path where the output CSV with sentiment labels will be saved.
    :return: DataFrame containing the original data with an additional column:
            - 'compound_score': The VADER compound sentiment score for each headline (float between -1 and 1).
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

    vader_sentiment_scorer(input, output)