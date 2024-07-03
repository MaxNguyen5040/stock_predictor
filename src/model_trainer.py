import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from data_fetcher import fetch_stock_data

def train_models(ticker, start_date, end_date):
    df = fetch_stock_data(ticker, start_date, end_date)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date_ordinal'] = df['Date'].apply(lambda date: date.toordinal())
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    X = df[['Date_ordinal', 'Year', 'Month', 'Day']]
    y = df['Close']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'LinearRegression': LinearRegression(),
        'XGBRegressor': XGBRegressor(),
        'LGBMRegressor': LGBMRegressor()
    }

    trained_models = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        trained_models[name] = model

    performance = {name: mean_squared_error(y_test, model.predict(X_test)) for name, model in trained_models.items()}

    return trained_models, X_test, y_test, performance

if __name__ == "__main__":
    trained_models, X_test, y_test, performance = train_models('AAPL', '2022-01-01', '2023-01-01')
    for name, mse in performance.items():
        print(f"{name} model MSE: {mse}")