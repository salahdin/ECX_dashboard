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
    brand="ECX dashboard",
    brand_href="#",
    color="dark",
    dark=True,
)

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.layout = html.Div([
    navbar,
    html.Div([
    html.Label("Dash Graph"),
    html.Div([
        dbc.Input(placeholder="Enter a symbol", bs_size="sm", value="UGDUG", type="text", id="Stock-input", ),
        html.Div([dbc.Button("Go", color="dark", id="submit-button", className="mr-1", n_clicks=0)],
                 className="input-group-append"),
    ], className="col-lg-8 input-group mb-3"),
    html.Div([
        html.Div(
            dcc.Graph(id="graph_close"),
            className="col"
        ),
    ], className="row")
,], className="container-fluid")])


# callbacks

@app.callback(Output("graph_close", "figure"),
              [Input("submit-button", "n_clicks")],
              [State("Stock-input", "value")])
def update_fig(n_clicks, input_value):
    df = pd.read_csv("rptCoffee.csv")
    df['Trade_Date'] = pd.to_datetime(df['Trade_Date'], format='%m/%d/%Y')
    df2 = df[df['Symbol'].str.contains(input_value)]
    df3 = df2[['High','Close','Opening_Price', 'Low']].replace({',': ''}, regex=True)
    df3 = df3.apply(pd.to_numeric)
    data = []
    trace_line = go.Scatter(x=list(df2.Trade_Date),
                            y=list(df2.Close),
                            # visible=False,
                            name="Close",
                            showlegend=False)

    trace_candle = go.Candlestick(x=df2.Trade_Date,
                                  open=df3.Opening_Price,
                                  high=df3.High,
                                  low=df3.Low,
                                  close=df3.Close,
                                  # increasing=dict(line=dict(color="#00ff00")),
                                  # decreasing=dict(line=dict(color="white")),
                                  visible=False,
                                  showlegend=True,
                                  )

    trace_bar = go.Ohlc(x=df2.Trade_Date,
                        open=df2.Opening_Price,
                        low=df2.Low,
                        high=df2.High,
                        close=df2.Close,
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
        title=input_value,
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

    return {
        'data': data,
        'layout': layout
    }


if __name__ == '__main__':
    app.run_server(debug=True)
