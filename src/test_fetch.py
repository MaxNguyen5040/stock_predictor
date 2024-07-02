from data_fetcher import fetch_stock_data
from data_fetcher import fetch_multiple_stocks

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL"]
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    data = fetch_multiple_stocks(tickers, start_date, end_date)
    for ticker, df in data.items():
        print(f"{ticker} data:\n", df.head())