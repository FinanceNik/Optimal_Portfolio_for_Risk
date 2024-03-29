import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import Styles
import DataHandler as dh
import PortfolioCreation as pc
import Risk_Scoring
from MonteCarloSimulation import monte_carlo_simulation as mcs

# The dash.Dash class is the framework for the whole app.
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Defining the sidebar and all the elements within. That includes links (dbc.Nav - elements, which are navigation
# elements), headings for the different sections and the title of the application "Portfolio Optimizer".
sidebar = html.Div(
    [
        html.H1("Portfolio\nOptimizer", style={'font-size': '46px', 'font-weight': 'bold'}),
        html.Hr(style={'borderColor': Styles.lightgrey}),
        html.H2("Go To:", className="lead", style={'font-size': '30px'}),
        html.Hr(style={'borderColor': Styles.lightgrey}),
        # NavLink elements are the buttons that navigate the user to various sections.
        # In total there are three navigatable sections: Welcome, Input Form, and About.
        dbc.Nav(
            [
                dbc.NavLink("Welcome", href="/", active="exact"),
                dbc.NavLink("Input Form", href="/input-form", active="exact"),
                dbc.NavLink("About", href="/about", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    # The style of the sidebar is imported from the STYLES module.
    style=Styles.SIDEBAR_STYLE,
)

# How the content within the web-application is supposed to be styled. Also imported from the STYLES module.
content = html.Div(id="page-content", style=Styles.CONTENT_STYLE)

# The complete layout of the app. Meaning that the application is supposed to contain the sidebar element, the content
# element and the background color is defined.
app.layout = html.Div([
    html.Div([dcc.Location(id="url"), sidebar, content], style={'backgroundColor': 'white'}),
    html.Div([dcc.ConfirmDialog(id='confirm-dialog', message="data submitted!")])
])


# This is the callback element that saves the information of which assets are selected under the asset constraint
# section in the input form and writes that data to the database file.
@app.callback(
    Output("checklist-output", "value"),
    Input("submit-assets", "n_clicks"),
    Input("checklist", "value"))
def update_checklist(n_clicks, value_list):
    # In order to just trigger the function once the button is clicked, it is defined that the database population
    # function is only triggered once the button is clicked at least once.
    if n_clicks > 0:
        dh.SQL_Populator_Constraints_Assets(value_list)


# This callback saves the answers to each questionnaire question to the database. There are nine questions.
@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('submit', 'n_clicks'),
     dash.dependencies.Input('Q_1', 'value'),
     dash.dependencies.Input('Q_2', 'value'),
     dash.dependencies.Input('Q_3', 'value'),
     dash.dependencies.Input('Q_4', 'value'),
     dash.dependencies.Input('Q_5', 'value'),
     dash.dependencies.Input('Q_6', 'value'),
     dash.dependencies.Input('Q_7', 'value'),
     dash.dependencies.Input('Q_8', 'value'),
     dash.dependencies.Input('Q_9', 'value')])
def update_output(n_clicks, value1, value2, value3, value4, value5, value6, value7, value8, value9):
    input_list = [value1, value2, value3, value4, value5, value6, value7, value8, value9]
    # Only trigger the function that writes the data to the database once the button is clicked at least once.
    if n_clicks > 0:
        dh.SQL_Populator_Questionnaire(input_list)


# This is the callback for the main navigation elements: Welcome, Input Form, and About.
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    # the / section is the Welcome page. This is the default landing page for the user that introduces him/her to
    # the tool.
    if pathname == "/":
        return html.Div(children=[
            # Heading of the Page
            html.Div([html.H1('Optimal Portfolio Creation and Automation Tool')], style={'textAlign': 'center'}),
            html.Hr(),
            # Introduction text to let the user know what the tool is for.
            html.Div([
                html.Div(['By using this tool, the customer`s risk capacity as well as risk adversity are defined.']),
                html.Div(['Furthermore, the above-mentioned metrics are separated numerically scored.']),
                html.Div(['Lastly, an algorithm will create the best possible portfolio for the selection.']),
            ], style={"font-size": "20px", "textAlign": "center"}),
            html.Hr(),
            # Here starts the section of the page that lets the user press the button to be navigated to the Input Form.
            html.Div([
                html.I("Start the Customer Process:"),
            ], style={'font-size': '20px', 'textAlign': 'center'}),
            html.Div([
                dbc.Nav(
                    [
                        dbc.NavLink("Start", href="/input-form", active="exact"),
                    ],
                    vertical=True,
                    pills=True)
                # Because this element has unique style properties, the STYLES.STYLE function was not used.
            ], style={'margin-left': '40%',
                      'display': 'flex', 'fontWeight': 'bold', 'align-items': 'center', 'justify-content': 'center',
                      'width': '20%', 'align': 'center', 'padding': '10px',
                      'box-shadow': '5px 4px 5px 5px lightgrey', "font-size": "30px", "textAlign": "center",
                      'borderRadius': '10px',
                      'overflow': 'hidden'}),
            html.Div([
                html.Hr(),
                html.Div(['Minor instructions when using this application:'], style={'fontWeight': 'bold'}),
                html.Br(),
                html.Div(['1. It is not required, but beneficial to run the application in a 16:9 window, as '
                          'otherwise']),
                html.Div(['Some margins may be off.']),
                html.Br(),
                html.Div(['2. When in the Input Form section. Please press every button to the bottom on the '
                          'respective']),
                html.Div(['pages. They trigger the functions that are saving the data to the database.']),
                html.Br(),
                html.Div(['3. After submitting the information when pressing the buttons on the respective pages, you']),
                html.Div(['may click the next tab to the bottom of the Input Form page.']),
            ], style={"font-size": "20px", "textAlign": "center"}),

        ])
    # This function contains the elements for the About page such as pictures and text bodies.
    if pathname == "/about":
        return html.Div(children=[
            html.Div([html.H1('About the Creators...')], style={"textAlign": "center"}),
            html.Hr(),
            html.Div([], style={'width': f'{32}%', 'display': 'inline-block'}),
            # Display a picture for each creator of the tool.
            html.Div([
                html.Div([html.Img(src=app.get_asset_url('image.jpg'))], style={'width': f'{17.3}%', 'display': 'inline-block'}),
                ], style={'width': f'{17.3}%', 'display': 'inline-block', 'align': 'center', 'padding': '10px',
                          'box-shadow': Styles.boxShadow,
                          'borderRadius': '10px',
                          'overflow': 'hidden'}),
            html.Div([], style={'width': f'{1}%', 'display': 'inline-block'}),
            html.Div([
                html.Div([html.Img(src=app.get_asset_url('image_2.jpg'))],
                         style={'width': f'{17.3}%', 'display': 'inline-block'}),
            ], style={'width': f'{17.3}%', 'display': 'inline-block', 'align': 'center', 'padding': '10px',
                      'box-shadow': Styles.boxShadow,
                      'borderRadius': '10px',
                      'overflow': 'hidden'}),
            html.Div([], style={'width': f'{32}%', 'display': 'inline-block'}),
            html.Div([], style={'width': f'{32}%', 'display': 'inline-block'}),
            # Short descriptions of the creators and what they are specialized in.
            html.Div([
                html.Div([html.I("HSLU")], style={'textAlign': 'center'}),
                html.Div([html.I("MSc Banking & Finance")], style={'textAlign': 'center'}),
                html.Div([html.I("3rd Semester")], style={'textAlign': 'center'}),
                html.Div(html.Hr()),
                html.Div([html.I("Specialization:")], style={'textAlign': 'center', 'fontWeight': 'bold'}),
                html.Div([html.I("Data Science")], style={'textAlign': 'center'}),
            ], style={'textAlign': 'center', 'width': '17.3%', 'display': 'inline-block'}),
            html.Div([], style={'width': f'{1}%', 'display': 'inline-block'}),
            html.Div([
                html.Div([html.I("HSLU")], style={'textAlign': 'center'}),
                html.Div([html.I("MSc Banking & Finance")], style={'textAlign': 'center'}),
                html.Div([html.I("3rd Semester")], style={'textAlign': 'center'}),
                html.Div(html.Hr()),
                html.Div([html.I("Specialization:")], style={'textAlign': 'center', 'fontWeight': 'bold'}),
                html.Div([html.I("Asset Management")], style={'textAlign': 'center'}),
            ], style={'textAlign': 'center', 'width': '17.3%', 'display': 'inline-block'}),
            html.Hr(),
            html.Div([html.H1('About the Tool...')], style={"textAlign": "center"}),
            # Text body of what this tool was designed for and some background information.
            html.Div([
                html.P([
                    'This tool has been created as the final project for a masters level university course in Banking and',
                    html.Br(),
                    'Finance at the Lucerne School of Business. The subject is called Module 11 and focuses on a',
                    html.Br(),
                    'research project with practical application. The tool is meant as a way for asset managers,',
                    html.Br(),
                    'banks, and brokers to automate the process of creating a client`s portfolio.',
                    html.Br(),
                    html.Br(),
                    'Firstly, during an interview, the bank teller fills out a questionnaire with the respective client.',
                    html.Br(),
                    'This questionnaire establishes the client`s relationship towards risk tolerance and his or hers',
                    html.Br(),
                    'ability to take on risk and to absorb possible downfalls in the financial markets.',
                    html.Br(),
                    html.Br(),
                    'Secondly, the client can select the asset classes in which it is desired to be invested in',
                    html.Br(),
                    'and furthermore give the respective asset classes a minimum weight in the portfolio',
                    html.Br(),
                    'if so is desired.',
                    html.Br(),
                    html.Br(),
                    'Lastly, the inputs can be checked before submitting the data to the portfolio creation algorithm.',
                    html.Br(),
                    'The algorithm back-tests the performance of the selected assets and constraints when combined',
                    html.Br(),
                    'to a portfolio. The tool is calibrated to use the latest, scientifically established',
                    html.Br(),
                    'portfolio theory, namely Markowitz`s Modern Portfolio Theory and the accommodating',
                    html.Br(),
                    'Efficient Frontier. Moreover, the portfolio is selected based on a risk score',
                    html.Br(),
                    'that is established via the questionnaire`s input selections. The ',
                    html.Br(),
                    'selections splits the back-tested portfolios by volatility',
                    html.Br(),
                    'and chooses the portfolio with the highest Sharpe ratio',
                    html.Br(),
                    'that fits within a volatility bracket.',
                        ]),
                html.Hr()
            ], style={'textAlign': 'center', 'width': '100%', 'display': 'inline-block'}),
        ])

    # This is the Result's page that contains all the Dashboard elements.
    elif pathname == "/results":
        return html.Div(children=[
            html.Div([
                html.H1('Personalized Portfolio Result'),
            ], style={'width': '100%', 'display': 'inline-block', 'align': 'right', 'padding': Styles.graph_padding}),
            # Display the first row of key performance indicators, triggered via the kpiboxes function located in the
            # Styles module.
            html.Div([
                # Show the risk willingness score.
                Styles.kpiboxes('Risk Capacity Score:',
                                Risk_Scoring.risk_willingness_scoring()[0], Styles.accblue),
                # Show the risk adversity score.
                Styles.kpiboxes('Risk Adversity Score:',
                                Risk_Scoring.risk_capacity_scoring()[0], Styles.accblue),
                # Display the historical volatility of the chosen, optimal portfolio.
                Styles.kpiboxes('Expected Volatiliy:',
                                f"{round(pc.optimal_portfolio()[1] * 100, 4)}%", Styles.accblue),
                # Show the forward-looking expected return that is calculated as a sumproduct of the asset allocations
                # and the expected returns of each asset class under the neutral scenario described in the paper.
                Styles.kpiboxes('Expected Return:',
                                f"{round(dh.forward_looking_expected_return('neutral')*100, 4)}%", Styles.accblue),
            ]),
            html.Hr(),
            # This is the second section of the dashboard that displays the graph with the backtesting values.
            html.Div([
                html.H3('Portfolio Backtesting'),
            ], style={'width': '100%', 'display': 'inline-block', 'align': 'right', 'padding': Styles.graph_padding}),
            html.Div([
                # Dash Core Components Graph element.
                dcc.Graph(
                    id='Portfolio Backtesting Graph',
                    # Trigger the function in the Data_Handler module that retrieves both the date values as well as
                    # the backtesting values.
                    figure={'data': [{'x': dh.portfolio_backtesting_values_lists()[0],
                                      'y': dh.portfolio_backtesting_values_lists()[1],
                                      'type': 'line', 'title': "Portfolio Backtesting (01.01.2007 = 100.000)",
                                      'marker': {'color': Styles.accblue},
                                      'mode': 'line',
                                      'line': {'width': 8}}],
                            'layout': {'title': 'Portfolio Backtesting (01.01.2007 = 100.000)',
                                       'xaxis': {'title': 'Time as Date Stamps', 'tickangle': 45},
                                       'yaxis': {'title': 'Portfolio Value'}}}
                ),
            ], style=Styles.STYLE(100)),
            html.Hr(),
            # The third section of the dashboard that displays a table with the names of the assets and the allocation
            # given to them by the Portfolio_Creation module function optimal_portfolio.
            html.Div([
                html.H3('Portfolio Asset Allocation'),
            ], style={'width': '100%', 'display': 'inline-block', 'align': 'right', 'padding': Styles.graph_padding}),
            html.Div([
                dash_table.DataTable(
                    id='stat_table',
                    # Call the function that retrieves the asset names and allocations from the database.
                    columns=[{'name': i, 'id': i} for i in dh.selected_portfolio_weights()[0].columns],
                    style_cell_conditional=[],
                    style_as_list_view=False,
                    style_cell={'padding': '5px', 'border-radius': '50px'},
                    style_header={'backgroundColor': Styles.blues1, 'fontWeight': 'bold', 'color': 'white',
                                  'border': '1px solid grey', 'height': '50px', 'font-size': '16px'},
                    style_table={'border': '1px solid lightgrey',
                                 'borderRadius': '10px',
                                 'overflow': 'hidden',
                                 'box-shadow': '5px 4px 5px 5px lightgrey'},
                    style_data={'border': '1px solid grey', 'font-size': '12px'},
                    style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#DDEBF7'},
                                            {'if': {'row_index': 'even'}, 'backgroundColor': '#F2F2F2'},
                                            {'if': {'filter_query': '{Selected} > 0',
                                                    'column_id': 'Selected'},
                                             'backgroundColor': Styles.lightGreen, 'color': 'black'},
                                            {'if': {'filter_query': '{Selected} = 0',
                                                    'column_id': 'Selected'},
                                             'backgroundColor': Styles.lightRed, 'color': 'black'},
                                            ],
                    data=dh.selected_portfolio_weights()[0].to_dict('records'),

                )
            ], style={"width": "30%", 'align': 'center', 'margin-left': '34.5%'}),
            html.Hr(),
            # The fourth and last section of the dashboard that contains three rows of KPI boxes that display the three
            # scenarios of the Monte Carlo Analysis
            html.Div([
                html.H3('Monte Carlo Simulation'),
            ], style={'width': '100%', 'display': 'inline-block', 'align': 'right', 'padding': Styles.graph_padding}),
            # Bull scenario.
            html.Div([
                html.H5('Bull Scenario'),
            ], style={'width': '100%', 'display': 'inline-block', 'align': 'right', 'padding': Styles.graph_padding}),
            html.Div([
                # Display the mean portfolio value of the scenario.
                Styles.kpiboxes('Mean Portf. Value:', "{:,}".format(mcs('bull')[0]), Styles.lightRed),
                # Display the standard deviation of the portfolio value.
                Styles.kpiboxes('Standard Dev.:', "{:,}".format(mcs('bull')[1]), Styles.accblue),
                # Display the maximum portfolio value of the scenario.
                Styles.kpiboxes('Max Portf. Value:', "{:,}".format(mcs('bull')[2]), Styles.accblue),
                # Show the minimum portfolio value of the scenario.
                Styles.kpiboxes('Min Portf. Value:', "{:,}".format(mcs('bull')[3]), Styles.accblue),
            ]),
            # Bear scenario.
            html.Div([
                html.H5('Bear Scenario'),
            ], style={'width': '100%', 'display': 'inline-block', 'align': 'right', 'padding': Styles.graph_padding}),
            html.Div([
                Styles.kpiboxes('Mean Portf. Value:', "{:,}".format(mcs('bear')[0]), Styles.lightRed),
                Styles.kpiboxes('Standard Dev.:', "{:,}".format(mcs('bear')[1]), Styles.accblue),
                Styles.kpiboxes('Max Portf. Value:', "{:,}".format(mcs('bear')[2]), Styles.accblue),
                Styles.kpiboxes('Min Portf. Value:', "{:,}".format(mcs('bear')[3]), Styles.accblue),
            ]),
            # Neutral scenario.
            html.Div([
                html.H5('Neutral Scenario'),
            ], style={'width': '100%', 'display': 'inline-block', 'align': 'right', 'padding': Styles.graph_padding}),
            html.Div([
                Styles.kpiboxes('Mean Portf. Value:', "{:,}".format(mcs('neutral')[0]), Styles.lightRed),
                Styles.kpiboxes('Standard Dev.:', "{:,}".format(mcs('neutral')[1]), Styles.accblue),
                Styles.kpiboxes('Max Portf. Value:', "{:,}".format(mcs('neutral')[2]), Styles.accblue),
                Styles.kpiboxes('Min Portf. Value:', "{:,}".format(mcs('neutral')[3]), Styles.accblue),
            ]),
            html.Hr(),
        ])

    # This function returns what tab was selected. In total there are three tabs selectable on the
    # input form section.
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


# This callback controls the output of the tab selection and returns the actual content.
@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    # The first tab is the questionnaire.
    if tab == 'tab-1':
        return html.Div([
            html.Div([
                html.H2('Assessment of the Client\'s Risk Adversity'),
                html.Hr(),
                html.H5('1. Knowledge about financial markets:'),
                html.Div(['How often do you inform yourself about the happenings in the financial markets?']),
                html.Div([
                    # dcc.Dropdown is the dropdown element that shows the available answers.
                    dcc.Dropdown(id='Q_1',
                                 options=[{'label': i, 'value': i} for i in ['never',
                                                                             'seldom',
                                                                             'sometimes',
                                                                             'often',
                                                                             'very often']]),
                    html.Div(id='dd-output-container')
                ]),

                html.Hr(),
                html.H5('2. Knowledge about financial instruments:'),
                html.Div(['For how many years are you investing in financial instruments of any kind?']),
                html.Div([
                    dcc.Dropdown(id='Q_2',
                                 options=[{'label': i, 'value': i} for i in ['< 1',
                                                                             '1 - 3',
                                                                             '3 - 5',
                                                                             '4 - 8',
                                                                             '> 8']]),
                    html.Div(id='dd-output-container')
                ]),
                html.Hr(),
                html.H5('3. Risk & return preference:'),
                html.Div(['Which of the following portfolio returns seem most interesting to you?   [-2 to +2%  |  '
                          '-5 to +5%  |  -10 to +10%  |  -15 to +15%  |  -20 to +20%]']),
                html.Div([
                    dcc.Dropdown(id='Q_3',
                                 options=[{'label': i, 'value': i} for i in ['-2 to +2%',
                                                                             '-5 to +5%',
                                                                             '-10 to +10%',
                                                                             '-15 to +15%',
                                                                             '-20 to +20%']]),
                    html.Div(id='dd-output-container')
                ]),

                html.Hr(),
                html.H5('4. Dealing with falling prices:'),
                html.Div(['What would you do if your portfolio suddenly lost 15% in value?']),
                html.Div([
                    dcc.Dropdown(id='Q_4',
                                 options=[{'label': i, 'value': i} for i in ['Liquidate all positions.',
                                                                             'Liquidate all negative positions.',
                                                                             'Change my investing strategy.',
                                                                             'Do nothing. Markets can be volatile.',
                                                                             'I would by the dip.']]),
                    html.Div(id='dd-output-container')
                ]),
                html.Hr(),
                html.H5('5. Preference towards risk and return distribution:'),
                html.Div(['What statement is most closely resembling you investment philosophy?']),
                html.Div([
                    dcc.Dropdown(id='Q_5',
                                 options=[{'label': i, 'value': i} for i in
                                          ['First and foremost, I want safety and stability.',
                                           'I would take slight risk to increase my return.',
                                           'I take considerable risk to get higher return.',
                                           'I want high return, therefore I accept great risk.',
                                           'All I care about is return, no matter the risk.']]),
                    html.Div(id='dd-output-container')
                ]),
                html.Hr(),
                html.H2('Assessment of the Client\'s Risk Capacity'),
                html.Hr(),
                html.H5('1. Liquidity:'),
                html.Div(['How large is the portion of your cash equivalent assets to your total net worth?']),
                html.Div([
                    dcc.Dropdown(id='Q_6',
                                 options=[{'label': i, 'value': i} for i in ['< 20%',
                                                                             '20 - 40%',
                                                                             '40 - 60%',
                                                                             '60 - 80%',
                                                                             '> 80%']]),
                    html.Div(id='dd-output-container')
                ]),
                html.Hr(),
                html.H5('2. Investment horizon:'),
                html.Div(['When would you probably like to access the invested capital?']),
                html.Div([
                    dcc.Dropdown(id='Q_7',
                                 options=[{'label': i, 'value': i} for i in ['In less than 2 years.',
                                                                             'In about 4 years.',
                                                                             'In about 6 years.',
                                                                             'Not within 10 years.',
                                                                             'No time horizon less than 10 years.']]),
                    html.Div(id='dd-output-container')
                ]),
                html.Hr(),
                html.H5('3. Savings rate:'),
                html.Div(['What statement best reflects your cost & income situation?']),
                html.Div([
                    dcc.Dropdown(id='Q_8',
                                 options=[{'label': i, 'value': i} for i in ['I have higher costs than income.',
                                                                             'My costs and income are equal.',
                                                                             'My costs are slightly lower than income.',
                                                                             'My costs are less than half of my income.',
                                                                             'My income is significantly higher than my costs.']]),
                    html.Div(id='dd-output-container')
                ]),
                html.Hr(),
                html.H5('4. Liquidity reserves:'),
                html.Div(['For how many years would the cash portion of your total net worth '
                          'cover your living expenses if you had no other income?']),
                html.Div([
                    dcc.Dropdown(id='Q_9',
                                 options=[{'label': i, 'value': i} for i in ['Less than 2 years.',
                                                                             '2 to 6 years.',
                                                                             '6 to 10 years.',
                                                                             '10 to 15 years.',
                                                                             'More than 15 years.']]),
                    html.Div(id='dd-output-container')
                ]),
                html.Hr(),
                html.Div([
                    html.Button('Click to Submit', className='btn btn-primary', id='submit', n_clicks=0)
                ], style={'width': '11.4%', 'display': 'inline-block', 'align': 'center', 'padding': '10px',
                          'margin-left': '0%',
                          'font-size': '24px',
                          'overflow': 'hidden'}),
                html.Hr()
            ], style={'textAlign': 'center'})
        ])
    elif tab == 'tab-2':
        # the second tab is the asset constraint section.
        return html.Div([
            html.Div([
                html.H2('Please select the portfolio constraints.'),
                html.Hr(),
            ], style={'textAlign': 'center'}),
            # Disclaimer to the asset selection and deselection.
            html.Div([
                html.Div([
                    html.H5('Tick the assets that should be included in the client\'s portfolio.'),
                    html.Div([html.I('Important Note:')], style={'fontWeight': 'bold'}),
                    html.I('You can only remove assets from a portfolio with absolut certainty by un-ticking'),
                    html.Br(),
                    html.I(' the respective box. It is not given, however, that an asset class will be added '),
                    html.Br(),
                    html.I('to one`s portfolio if the tool does not recognize it as a fitting class for'),
                    html.Br(),
                    html.I('the respective risk/return characteristics of the portfolio.'),
                    html.Hr(),
                ], style={'textAlign': 'center'}),
                html.Div([
                    html.Div([
                        # The dcc.Checklist element creates a table with tick-able buttons.
                        dcc.Checklist(
                            id="checklist",
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
                        ),
                        html.Div(id='checklist-output')])
                    ], style={'width': f'{18}%', 'display': 'inline-block', 'align': 'center', 'padding': '10px',
                              'margin-left': '41%',
                              'box-shadow': Styles.boxShadow,
                              'borderRadius': '10px',
                              'font-size': '20px',
                              'overflow': 'hidden'}),
                html.Div([
                    html.Button('Submit Asset Selection', className='btn btn-primary', id='submit-assets', n_clicks=0)
                        ], style={'width': f'{20}%', 'display': 'inline-block',
                                  'margin-left': '41%',
                                  'align': 'center', 'padding': '10px',
                                  'font-size': '24px'}),
            ]),
            html.Hr(),
        ])

    elif tab == 'tab-3':
        # The third tab contains the final check page, on which the user can check whether the information selected was
        # as desired. Afterwards the user can click on a button called "Results" and be navigated to the result
        # dashboard on which the constructed portfolio is depicted as well as a backtesting visualization, asset weights
        # and the result of the Monte Carlo Simulation.
        return html.Div([
            html.H1('Summary of your selection'),
            html.H5('A portfolio will be created according to the following selection:'),
            html.Hr(),
            html.H3("The following answers have been given in the questionnaire:"),
            html.Br(),
            html.Div([
                html.H6("Question 1 - How often do you inform yourself about the happenings in the financial markets?"),
                html.Div(f"{dh.Answer('Question_0')}")
            ]),
            html.Br(),
            html.Div([
                html.H6("Question 2 - For how many years are you investing in financial instruments of any kind?"),
                html.Div(f"{dh.Answer('Question_1')}")
            ]),
            html.Br(),
            html.Div([
                html.H6("Question 3 - Which of the following portfolio returns seem most interesting to you?   "
                        "[-2 to +2%  |  -5 to +5%  |  -10 to +10%  |  -15 to +15%  |  -20 to +20%]"),
                html.Div(f"{dh.Answer('Question_2')}")
            ]),
            html.Br(),
            html.Div([
                html.H6("Question 4 - What would you do if your portfolio suddenly lost 15% in value?"),
                html.Div(f"{dh.Answer('Question_3')}")
            ]),
            html.Br(),
            html.Div([
                html.H6("Question 5 - What statement is most closely resembling you investment philosophy?"),
                html.Div(f"{dh.Answer('Question_4')}")
            ]),
            html.Br(),
            html.Div([
                html.H6("Question 6 - How large is the portion of your cash equivalent assets to your total net worth?"),
                html.Div(f"{dh.Answer('Question_5')}")
            ]),
            html.Br(),
            html.Div([
                html.H6("Question 7 - When would you probably like to access the invested capital?"),
                html.Div(f"{dh.Answer('Question_6')}")
            ]),
            html.Br(),
            html.Div([
                html.H6("Question 8 - What statement best reflects your cost & income situation?"),
                html.Div(f"{dh.Answer('Question_7')}")
            ]),
            html.Br(),
            html.Div([
                html.H6("Question 9 - For how many years would the cash portion of your total net worth "
                        "cover your living expenses if you had no other income?"),
                html.Div(f"{dh.Answer('Question_8')}")
            ]),
            html.Hr(),
            html.H3("The following asset classes have been selected:"),
            html.Br(),
            html.Div([
                dash_table.DataTable(
                    id='stat_table',
                    columns=[{'name': i, 'id': i} for i in dh.selected_assets()[0].columns],
                    style_cell_conditional=[],
                    style_as_list_view=False,
                    style_cell={'padding': '5px', 'border-radius': '50px'},
                    style_header={'backgroundColor': Styles.blues1, 'fontWeight': 'bold', 'color': 'white',
                                  'border': '1px solid grey', 'height': '50px', 'font-size': '16px'},
                    style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#DDEBF7'},
                                            {'if': {'row_index': 'even'}, 'backgroundColor': '#F2F2F2'},
                                            {'if': {'filter_query': '{Selected} contains false',
                                                    'column_id': 'Selected'},
                                             'backgroundColor': Styles.lightRed, 'color': 'black'},
                                            {'if': {'filter_query': '{Selected} contains "true"',
                                                    'column_id': 'Selected'},
                                             'backgroundColor': Styles.lightGreen, 'color': 'black'},
                                            ],
                    style_table={'border': '1px solid lightgrey',
                                 'borderRadius': '10px',
                                 'overflow': 'hidden',
                                 'box-shadow': '5px 4px 5px 5px lightgrey'},
                    style_data={'border': '1px solid grey', 'font-size': '12px'},
                    data=dh.selected_assets()[0].to_dict('records'),

                )
            ], style={"width": "30%", 'margin-left': '34.5%'}),
            html.Hr(),
            html.Br(),
            html.Div([
                # This is the button that navigates the user to the results page once pressed.
                dbc.Nav(
                    [
                        dbc.NavLink("Results", href="/results", active="exact"),
                    ],
                    vertical=True,
                    pills=True)
            ], style={'width': '20%', 'display': 'inline-block', 'align': 'center', 'padding': '10px',
                      'box-shadow': '5px 4px 5px 5px lightgrey', "font-size": "30px", "textAlign": "center",
                      'borderRadius': '10px',
                      'overflow': 'hidden'}),
            html.Hr()


        ], style={'textAlign': 'center'})


if __name__ == "__main__":
    # If pages are not loading or there may seem to be unwanted behaviour of the application, you may change
    # debug=False to debug=True. This enables the developer tool, which allows to see the error messages if there are
    # any.
    app.run_server(port=8888, debug=True)
