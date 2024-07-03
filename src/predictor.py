import pandas as pd
from data_fetcher import fetch_stock_data
from model_trainer import train_models
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_future_prices(trained_model, start_date, end_date, days_ahead):
    # Generate future dates
    future_dates = pd.date_range(start=start_date, periods=days_ahead+1).tolist()[-days_ahead:]

    future_features = np.arange(len(future_dates)).reshape(-1, 1)

    predicted_prices = trained_model.predict(future_features)

    return future_dates, predicted_prices

def train_models(ticker, start_date, end_date):
    # Your data fetching and preprocessing logic here
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, X_test, y_test


def predict_future_prices(ticker, start_date, end_date, days_ahead):
    trained_models, _, _ = train_models(ticker, start_date, end_date)
    last_date = pd.to_datetime(end_date)
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, days_ahead+1)]
    future_dates_ordinal = [date.toordinal() for date in future_dates]
    future_years = [date.year for date in future_dates]
    future_months = [date.month for date in future_dates]
    future_days = [date.day for date in future_dates]

    future_features = pd.DataFrame({
        'Date_ordinal': future_dates_ordinal,
        'Year': future_years,
        'Month': future_months,
        'Day': future_days
    })

    predictions = {}
    for name, model in trained_models.items():
        predictions[name] = model.predict(future_features)
    
    future_data = pd.DataFrame({'Date': future_dates})
    for name, pred in predictions.items():
        future_data[f'Predicted_Close_{name}'] = pred

    return future_data

if __name__ == "__main__":
    future_data = predict_future_prices('AAPL', '2022-01-01', '2023-01-01', 30)
    print(future_data)