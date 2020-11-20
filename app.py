import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

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
    color="primary",
    dark=True,
)

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.layout = html.Div([
    navbar,
    html.Label("Dash Graph"),
    html.Div([
        dbc.Input(placeholder="A small input...", bs_size="sm", value="USDE5", type="text", id="Stock-input", ),
    ]),

    html.Div([
        html.Div(
            dcc.Graph(id="graph_close"),
            className="col"
        ),
    ], className="row")
], className="container-fluid")


# callbacks

@app.callback(Output("graph_close", "figure"), [Input("Stock-input", "value")])
def update_fig(input_value):
    df = pd.read_csv("rptCoffee.csv")
    df2 = df[df['Symbol'].str.contains(input_value)]
    print(df2)
    data = []
    trace_close = go.Scatter(x=list(df2.index),
                             y=list(df2.Close),
                             name="close",
                             line=dict(color="#f44242")
                             )

    data.append(trace_close)
    layout = dict(title="Stock chart")
    fig = dict(data=data, layout=layout)
    return {
        'data': data,
        'layout': layout
    }


if __name__ == '__main__':
    app.run_server(debug=True)
"""# initializing the app
app = dash.Dash()

app.layout = html.Div(html.H1(children="hello world"))

if __name__ == '__main__':
    app.run_server(debug=True)"""
