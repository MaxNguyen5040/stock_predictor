import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from data_fetcher import fetch_stock_data
from plotter import plot_stock_data
from predictor import predict_future_prices
from model_trainer import train_models
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='ticker-input', type='text', value='AAPL'),
    dcc.DatePickerRange(
        id='date-picker',
        start_date='2022-01-01',
        end_date='2023-01-01'
    ),
    dcc.Input(id='days-ahead', type='number', value=30),
    html.Button('Submit', id='submit-button', n_clicks=0),
    dcc.Graph(id='stock-graph'),
    dcc.Graph(id='volume-graph'),
    dcc.Graph(id='prediction-graph'),
    html.Div(id='model-performance')
])

@app.callback(
    [Output('stock-graph', 'figure'), Output('volume-graph', 'figure'), Output('prediction-graph', 'figure'), Output('model-performance', 'children')],
    [Input('submit-button', 'n_clicks')],
    [Input('ticker-input', 'value'), Input('date-picker', 'start_date'), Input('date-picker', 'end_date'), Input('days-ahead', 'value')]
)
def update_graph(n_clicks, ticker, start_date, end_date, days_ahead):
    df = fetch_stock_data(ticker, start_date, end_date)
    future_df = predict_future_prices(ticker, start_date, end_date, days_ahead)
    trained_models, X_test, y_test, performance = train_models(ticker, start_date, end_date)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines', name='50-Day SMA'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines', name='200-Day SMA'))
    fig.update_layout(title=f'{ticker} Stock Price with Moving Averages',
                      xaxis_title='Date',
                      yaxis_title='Price')

    fig_volume = go.Figure()
    fig_volume.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='Volume'))
    fig_volume.update_layout(title=f'{ticker} Trading Volume',
                             xaxis_title='Date',
                             yaxis_title='Volume')

    fig_prediction = go.Figure()
    for column in future_df.columns:
        if 'Predicted_Close' in column:
            fig_prediction.add_trace(go.Scatter(x=future_df['Date'], y=future_df[column], mode='lines', name=column))
    fig_prediction.update_layout(title=f'{ticker} Predicted Prices for Next {days_ahead} Days',
                                 xaxis_title='Date',
                                 yaxis_title='Predicted Close Price')

    performance_text = "Model Performance (Mean Squared Error):\n" + "\n".join([f"{name}: {mse:.2f}" for name, mse in performance.items()])

    return fig, fig_volume, fig_prediction, performance_text

if __name__ == '__main__':
    app.run_server(debug=True)