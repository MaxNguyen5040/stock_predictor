# src/plotter.py
import plotly.graph_objects as go
import pandas as pd

def plot_stock_data(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines', name='50-Day SMA'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines', name='200-Day SMA'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_12'], mode='lines', name='12-Day EMA'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_26'], mode='lines', name='26-Day EMA'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], mode='lines', name='MACD'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI', yaxis='y2'))

    fig.update_layout(
        title='Stock Data with Technical Indicators',
        xaxis_title='Date',
        yaxis_title='Price',
        yaxis2=dict(
            title='RSI',
            overlaying='y',
            side='right'
        )
    )
    return fig

if __name__ == "__main__":
    df = pd.read_csv('data/AAPL.csv')
    fig = plot_stock_data(df)
    fig.show()
