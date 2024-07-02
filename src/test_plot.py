from data_fetcher import fetch_stock_data
from plotter import plot_stock_data

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL"]
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    data = fetch_multiple_stocks(tickers, start_date, end_date)
    plot_multiple_stocks(data)