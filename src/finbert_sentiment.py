"""
File: finbert_sentiment.py
Description: Utilizes FinBERT to score headlines for sentiment analysis
Created by: Renesh Ravi
"""

import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm

def finbert_sentiment_scorer(master_input, scored_output):
    df = pd.read_csv(master_input, parse_dates=['timestamp'])

    if os.path.exists(scored_output):
        scored = pd.read_csv(scored_output, parse_dates=['timestamp'])
        df = pd.merge(
            df, scored[['timestamp','headline','finbert_sentiment']],
            on=['timestamp','headline'], how='left'
        )
    else:
        df['finbert_sentiment'] = pd.NA

    model_name = "yiyanghkust/finbert-tone"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    mask = df['finbert_sentiment'].isna()
    if mask.sum() == 0:
        print("No new headlines to score.")
    else:
        sentiments = []
        for text in tqdm(df.loc[mask, 'headline'], desc="FinBERT scoring"):
            result = nlp(text)[0]
            sentiments.append(result['label'])
        df.loc[mask, 'finbert_sentiment'] = sentiments

    os.makedirs(os.path.dirname(scored_output), exist_ok=True)
    df.to_csv(scored_output, index=False)
    print(f"✅ Saved FinBERT-scored headlines to {scored_output}")
    return df

if __name__ == "__main__":
    base = os.path.dirname(__file__)
    master_input = os.path.join(base, "../data/btc_headlines_master.csv")
    scored_output = os.path.join(base, "../data/btc_headlines_scored.csv")
    finbert_sentiment_scorer(master_input, scored_output)