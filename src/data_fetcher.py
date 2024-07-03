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

def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    stock_data['EMA_12'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
    stock_data['EMA_26'] = stock_data['Close'].ewm(span=26, adjust=False).mean()
    stock_data['MACD'] = stock_data['EMA_12'] - stock_data['EMA_26']
    stock_data['RSI'] = compute_rsi(stock_data['Close'])
    return stock_data

def compute_rsi(series, period=14):
    delta = series.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
