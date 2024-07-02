from data_fetcher import fetch_stock_data

if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    data = fetch_stock_data(ticker, start_date, end_date)
    print(data.head())