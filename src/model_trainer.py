import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from data_fetcher import fetch_stock_data

def train_model(ticker, start_date, end_date):
    df = fetch_stock_data(ticker, start_date, end_date)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date_ordinal'] = df['Date'].apply(lambda date: date.toordinal())

    X = df[['Date_ordinal']]
    y = df['Close']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test

if __name__ == "__main__":
    model, X_test, y_test = train_model('AAPL', '2022-01-01', '2023-01-01')
    print("Model trained successfully")