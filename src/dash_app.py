import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from data_fetcher import fetch_stock_data
from plotter import plot_stock_data
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='ticker-input', type='text', value='AAPL'),
    dcc.DatePickerRange(
        id='date-picker',
        start_date='2022-01-01',
        end_date='2023-01-01'
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    dcc.Graph(id='stock-graph'),
    dcc.Graph(id='volume-graph')
])

@app.callback(
    [Output('stock-graph', 'figure'), Output('volume-graph', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [Input('ticker-input', 'value')],
    [Input('date-picker', 'start_date'), Input('date-picker', 'end_date')]
)
def update_graph(n_clicks, ticker, start_date, end_date):
    df = fetch_stock_data(ticker, start_date, end_date)
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

    return fig, fig_volume

if __name__ == '__main__':
    app.run_server(debug=True)