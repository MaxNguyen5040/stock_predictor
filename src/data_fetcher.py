import yfinance as yf
import pandas as pd
import cachetools.func


def clean_stock_data(df):
    df.dropna(inplace=True)
    df = df[df['Volume'] > 0]
    df['Date'] = df.index
    df.reset_index(drop=True, inplace=True)
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    return df

def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    df = clean_stock_data(df)
    df['SMA_50'] = df['Close'].rolling(window=50).mean()  # 50-day Simple Moving Average
    df['SMA_200'] = df['Close'].rolling(window=200).mean()  # 200-day Simple Moving Average
    return df

def fetch_multiple_stocks(tickers, start_date, end_date):
    data = {}
    for ticker in tickers:
        data[ticker] = fetch_stock_data(ticker, start_date, end_date)
    return data

def clean_stock_data(df):
    df.dropna(inplace=True)
    df = df[df['Volume'] > 0]  # Filter out days with no trading volume
    df['Date'] = df.index
    df.reset_index(drop=True, inplace=True)
    return df

@cachetools.func.ttl_cache(maxsize=100, ttl=600)
def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    df = clean_stock_data(df)
    return df