import plotly.graph_objects as go

def plot_stock_data(df, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
    fig.update_layout(title=f'{ticker} Stock Price',
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