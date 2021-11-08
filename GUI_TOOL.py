import warnings
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import Styles
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
            html.Div([
                html.H2('Assessment of the Client\'s Risk Adversity'),
                html.Hr(),
                html.H5('1. Knowledge about financial markets:'),
                html.Div(['How often do you inform yourself about the happenings in the financial markets?']),
                dcc.Dropdown(id='Q_1',
                             options=[{'label': i, 'value': i} for i in ['never',
                                                                         'seldom',
                                                                         'sometimes',
                                                                         'often',
                                                                         'very often']]),
                html.Hr(),
                html.H5('2. Knowledge about financial instruments:'),
                html.Div(['For how many years are you investing in financial instruments of any kind?']),
                dcc.Dropdown(id='Q_2',
                             options=[{'label': i, 'value': i} for i in ['< 1',
                                                                         '1 - 3',
                                                                         '3 - 5',
                                                                         '4 - 8',
                                                                         '> 8']]),
                html.Hr(),
                html.H5('3. Risk & return preference:'),
                html.Div(['Which of the following portfolio returns seem most interesting to you?   [-2 to +2%  |  '
                          '-5 to +5%  |  -10 to +10%  |  -15 to +15%  |  -20 to +20%]']),
                dcc.Dropdown(id='Q_3',
                             options=[{'label': i, 'value': i} for i in ['-2 to +2%',
                                                                         '-5 to +5%',
                                                                         '-10 to +10%',
                                                                         '-15 to +15%',
                                                                         '-20 to +20%']]),
                html.Hr(),
                html.H5('4. Dealing with falling prices:'),
                html.Div(['What would you do if your portfolio suddenly lost 15% in value?']),
                dcc.Dropdown(id='Q_4',
                             options=[{'label': i, 'value': i} for i in ['Liquidate all positions.',
                                                                         'Liquidate all negative positions.',
                                                                         'Change my investing strategy.',
                                                                         'Do nothing. Markets can be volatile.',
                                                                         'I would by the dip.']]),
                html.Hr(),
                html.H5('5. Preference towards risk and return distribution:'),
                html.Div(['What statement is most closely resembling you investment philosophy?']),
                dcc.Dropdown(id='Q_5',
                             options=[{'label': i, 'value': i} for i in ['First and foremost, I want safety and stability.',
                                                                         'I would take slight risk to increase my return.',
                                                                         'I take considerable risk to get higher return.',
                                                                         'I want high return, therefore I accept great risk.',
                                                                         'All I care about is return, no matter the risk.']]),
                html.Hr(),
                html.H2('Assessment of the Client\'s Risk Capacity'),
                html.Hr(),
                html.H5('1. Liquidity:'),
                html.Div(['How large is the portion of your cash equivalent assets to your total net worth?']),
                dcc.Dropdown(id='Q_6',
                             options=[{'label': i, 'value': i} for i in ['< 20%',
                                                                         '20 - 40%',
                                                                         '40 - 60%',
                                                                         '60 - 80%',
                                                                         '> 80%']]),
                html.Hr(),
                html.H5('2. Investment horizon:'),
                html.Div(['When would you probably like to access the invested capital?']),
                dcc.Dropdown(id='Q_7',
                             options=[{'label': i, 'value': i} for i in ['In less than 2 years.',
                                                                         'In about 4 years.',
                                                                         'In about 6 years.',
                                                                         'Not within 10 years.',
                                                                         'No time horizon less than 10 years.']]),
                html.Hr(),
                html.H5('3. Savings rate:'),
                html.Div(['What statement best reflects your cost & income situation?']),
                dcc.Dropdown(id='Q_8',
                             options=[{'label': i, 'value': i} for i in ['I have higher costs than income.',
                                                                         'My costs and income are equal.',
                                                                         'My costs are slightly lower than income.',
                                                                         'My costs are less than half of my income.',
                                                                         'My income is significantly higher than my costs.']]),
                html.Hr(),
                html.H5('4. Liquidity reserves:'),
                html.Div(['For how many years would the cash portion of your total net worth '
                          'cover your living expenses if you had no other income?']),
                dcc.Dropdown(id='Q_9',
                             options=[{'label': i, 'value': i} for i in ['Less than 2 years.',
                                                                         '2 to 6 years.',
                                                                         '6 to 10 years.',
                                                                         '10 to 15 years.',
                                                                         'More than 15 years.']]),
                html.Hr(),
            ])
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Div([
                html.H2('Please select the portfolio constraints.'),
                html.Hr(),
                html.Div([
                    html.H5('Tick the assets that should be included in the client\'s portfolio.'),
                ], style={'margin-left': '25%'}),
                html.Div([
                    dcc.Checklist(
                        options=[
                            {'label': '  Cash', 'value': 'CA'},
                            {'label': '  Bonds', 'value': 'BO'},
                            {'label': '  Bonds FC (hedged)', 'value': 'BOFC'},
                            {'label': '  Swiss Equity', 'value': 'SE'},
                            {'label': '  Global Equity', 'value': 'GE'},
                            {'label': '  Global Equity Small Cap', 'value': 'GES'},
                            {'label': '  Emerging Markets Equity', 'value': 'EME'},
                            {'label': '  Real Estate', 'value': 'RE'},
                        ], value=['CA', 'BO', 'BOFC', 'SE', 'GE', 'GES', 'EME', 'RE'],
                        labelStyle={'display': 'block'}
                    )
                ], style={'width': f'{25}%', 'display': 'inline-block', 'align': 'center', 'padding': '10px',
                          'margin-left': '35%',
                          'font-size': '24px',
                          'box-shadow': '5px 4px 5px 5px lightgrey',
                          'borderRadius': '10px',
                          'overflow': 'hidden'})
            ])
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H1('ZZ')
        ])


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)