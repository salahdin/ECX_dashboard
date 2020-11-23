import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="ECX dashboard playground",
    brand_href="#",
    color="primary",
    dark=True,
)
df = pd.read_csv("finance-charts-apple.csv")
# df['Trade_Date'] = pd.to_datetime(df['Trade_Date'], format='%m/%d/%Y')
# df2 = df[df['Symbol'].str.contains(input_value)]
# df3 = pd.read_csv("finance-charts-apple.csv")
# df3 = df3[['Date', 'High']][:100]

trace_line = go.Scatter(x=list(df.index),
                        y=list(df.Close),
                        # visible=False,
                        name="Close",
                        showlegend=False)

trace_candle = go.Candlestick(x=df.index,
                              open=df.Open,
                              high=df.High,
                              low=df.Low,
                              close=df.Close,
                              # increasing=dict(line=dict(color="#00ff00")),
                              # decreasing=dict(line=dict(color="white")),
                              visible=False,
                              showlegend=False)

trace_bar = go.Ohlc(x=df.index,
                    open=df.Open,
                    low=df.Low,
                    high=df.High,
                    close=df.Close,
                    # increasing=dict(line=dict(color="#888888")),
                    # decreasing=dict(line=dict(color="#888888")),
                    visible=False,
                    showlegend=False)

data = [trace_line, trace_candle, trace_bar]

updatemenus = list([
    dict(
        buttons=list([
            dict(
                args=[{'visible': [True, False, False]}],
                label='Line',
                method='update'
            ),
            dict(
                args=[{'visible': [False, True, False]}],
                label='Candle',
                method='update'
            ),
            dict(
                args=[{'visible': [False, False, True]}],
                label='Bar',
                method='update'
            ),
        ]),
        direction='down',
        pad={'r': 10, 't': 10},
        showactive=True,
        x=0,
        xanchor='left',
        y=1.05,
        yanchor='top'
    ),
])

layout = dict(
    title="input_value",
    updatemenus=updatemenus,
    autosize=False,
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                     label='YTD',
                     step='year',
                     stepmode='todate'),
                dict(count=1,
                     label='1y',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type='date'
    )
)
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.layout = html.Div([
    navbar,
    html.Label("Dash Graph"),
    html.Div([
        dbc.Input(placeholder="A small input...", bs_size="sm", value="", type="text", id="Stock-input", ),
        html.Div([dbc.Button("Go!", color="dark", id="submit-button", className="mr-1", n_clicks=0)],
                 className="input-group-append"),
    ], className="col-lg-8 input-group mb-3"),

    html.Div([
        html.Div(
            dcc.Graph(id="graph_close",
                      figure={
                          "data": data,
                          "layout": layout,
                      },
                      ),
            className="col"
        ),
    ], className="row")
], className="container-fluid")

# callbacks


if __name__ == '__main__':
    app.run_server(debug=True)
