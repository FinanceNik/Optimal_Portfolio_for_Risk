import warnings
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import Styles
from time import sleep
import threading
import os.path
warnings.simplefilter("ignore", UserWarning)

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


sidebar = html.Div(
    [
        html.H1("Portfolio\nOptimizer", style={'font-size': '46px', 'font-weight': 'bold'}),
        html.Hr(style={'borderColor': Styles.lightgrey}),
        html.H2("Go To:", className="lead", style={'font-size': '30px'}),
        html.Hr(style={'borderColor': Styles.lightgrey}),
        dbc.Nav(
            [
                dbc.NavLink("Welcome", href="/", active="exact"),
                dbc.NavLink("Input Form", href="/input-form", active="exact"),
                dbc.NavLink("Result", href="/result", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=Styles.SIDEBAR_STYLE,
)


content = html.Div(id="page-content", style=Styles.CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content],
                      style={'backgroundColor': 'white'})


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(children=[
            html.H1('XX'),
        ])

    elif pathname == "/result":
        return html.Div(children=[
            html.H1('XX')
        ])

    elif pathname == "/input-form":
        return html.Div(children=[
            dcc.Tabs(id='tabs-example', value='tab-1', children=[
                dcc.Tab(label='Questionnaire', value='tab-1'),
                dcc.Tab(label='Constraints', value='tab-2'),
                dcc.Tab(label='Final Check', value='tab-3'),
            ], style=Styles.TAB_STYLE),
            html.Hr(),
            html.Div(id='tabs-example-content')
        ])


@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H1('XX')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H1('YY')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H1('ZZ')
        ])


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)