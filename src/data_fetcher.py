import yfinance as yf
import pandas as pd

def clean_stock_data(df):
    df.dropna(inplace=True)
    df['Date'] = df.index
    df.reset_index(drop=True, inplace=True)
    return df

# Update the fetch_stock_data function to include cleaning
def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    df = clean_stock_data(df)
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