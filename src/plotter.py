import plotly.graph_objects as go

def plot_stock_data(df, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines', name='50-Day SMA'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines', name='200-Day SMA'))
    fig.update_layout(title=f'{ticker} Stock Price with Moving Averages',
                      xaxis_title='Date',
                      yaxis_title='Price')
    fig.show()

def plot_multiple_stocks(data):
    fig = go.Figure()
    for ticker, df in data.items():
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name=f'{ticker} Close Price'))
    fig.update_layout(title='Stock Price Comparison',
                      xaxis_title='Date',
                      yaxis_title='Price')
    fig.show()