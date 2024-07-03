import pandas as pd
from data_fetcher import fetch_stock_data
from model_trainer import train_model

def predict_future_prices(ticker, start_date, end_date, days_ahead):
    model, _, _ = train_model(ticker, start_date, end_date)
    last_date = pd.to_datetime(end_date)
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, days_ahead+1)]
    future_dates_ordinal = [date.toordinal() for date in future_dates]

    predictions = model.predict(pd.DataFrame(future_dates_ordinal, columns=['Date_ordinal']))
    future_data = pd.DataFrame({'Date': future_dates, 'Predicted_Close': predictions})

    return future_data

if __name__ == "__main__":
    future_data = predict_future_prices('AAPL', '2022-01-01', '2023-01-01', 30)
    print(future_data)