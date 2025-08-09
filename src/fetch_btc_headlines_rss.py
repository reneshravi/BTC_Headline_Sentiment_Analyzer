"""
File: fetch_btc_headlines_rss.py
Description: Poll multiple RSS feeds for BTC-related headlines, dedupe, append to master CSV.
Created by: Renesh Ravi
"""

import os, re, time, html
import pandas as pd
import feedparser
from dateutil import parser as dtparse
from datetime import timezone

# --- CHANGE THIS TO YOUR REAL PATH ---
PROJECT_DIR = r"C:\Users\Renesh\Documents\BTC_Headline_Sentiment_Analyzer"
OUTPUT_DIR = os.path.join(PROJECT_DIR, "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "btc_headlines_master.csv")

FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.theblock.co/rss.xml",
    "https://bitcoinmagazine.com/.rss/full/",
    "https://blog.coinbase.com/feed",
    "https://www.binance.com/en/blog/rss",
]

BTC_PATTERN = re.compile(r"\b(bitcoin|btc)\b", re.IGNORECASE)

def _parse_ts(entry):
    ts = getattr(entry, "published", None) or getattr(entry, "updated", None)
    if not ts:
        return None
    try:
        dt = dtparse.parse(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt.isoformat()
    except Exception:
        return None

def fetch_rss_batch() -> pd.DataFrame:
    rows = []
    for feed_url in FEEDS:
        d = feedparser.parse(feed_url)
        src = d.feed.get("title", "Unknown")
        for e in d.entries:
            title = html.unescape(getattr(e, "title", "")).strip()
            if not title or not BTC_PATTERN.search(title):
                continue
            ts = _parse_ts(e)
            if ts is None:
                continue
            url = getattr(e, "link", None)
            rows.append({
                "timestamp": ts,
                "headline": title,
                "source": src,
                "url": url if url else "Unknown",
            })
        time.sleep(0.2)
    if not rows:
        return pd.DataFrame(columns=["timestamp","headline","source","url"])
    df = pd.DataFrame(rows).drop_duplicates(subset=["url","headline"])
    return df

def append_to_master(new_df: pd.DataFrame):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if os.path.exists(OUTPUT_FILE):
        master = pd.read_csv(OUTPUT_FILE, parse_dates=["timestamp"])
    else:
        master = pd.DataFrame(columns=["timestamp","headline","source","url"])

    if new_df.empty:
        print("No new RSS headlines.")
        return master

    new_df["timestamp"] = pd.to_datetime(new_df["timestamp"], utc=True)
    combined = pd.concat([master, new_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=["url","headline"], keep="first")
    combined = combined.sort_values("timestamp", ascending=False)
    combined.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ RSS updated. Total headlines: {len(combined)}")
    return combined

if __name__ == "__main__":
    df_new = fetch_rss_batch()
    append_to_master(df_new)
