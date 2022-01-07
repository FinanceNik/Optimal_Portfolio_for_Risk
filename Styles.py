# Wrapper class for html elements provided by Dash.
from dash import html
# Class for the table element that is used on the result page as well as in the Input Form under Final Check.
from dash import dash_table

# The following colors are or have been used during the creation of this tool.
greys = ['#2b2b2b', '#3b3b3b', '#cfcfcf']
lightgrey = '#f0f0f0'
color_1 = '#5C4A72'
color_2 = '#F3B05A'
color_3 = '#F46A4E'

lightRed = '#FF9F9F'
strongGreen = '#37D151'
lightGreen = '#99E7A6'
mainColor = '#2F4050'
subColor1 = '#F2F2F2'
yellow = '#FFC000'
accgreen = '#00D2AA'
accblue = '#137EB3'
strongRed = '#FF5B5B'
darkgrey = '#404040'
blues1 = '#002060'
blues2 = '#305496'
blues3 = '#6CA6DA'
blues4 = '#9BC2E6'
blues5 = '#DDEBF7'

# The padding between a graph and elements next to it.
graph_padding = '5px'

# This variable adjusts the size and positioning of the drop-shadow behind table, graph and box elements for
# visual appeal.
boxshadow = '5px 4px 5px 5px lightgrey'

# Specifies the style of the tab elements under the GUI's Input Form section.
TAB_STYLE = {'box-shadow': boxshadow,
             'border-style': '',
             'border-color': greys[2],
             'font-size': '20px',
             'color': greys[2],
             "background-color": greys[0],
             'borderRadius': '15px'}

# Specifies the dark-blue sidebar to the left of the GUI.
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12em",
    "padding": "2rem 1rem",
    "background-color": greys[0],
    'color': greys[2],
    'font-size': '23px',
    'box-shadow': '5px 5px 5px 5px lightgrey'}

# The overall style of the elements and their margins. Necessary for the layout of the GUI.
CONTENT_STYLE = {"margin-left": "18rem", "margin-right": "2rem", "padding": "2rem 1rem"}


# Created this function to make styling of Divs easier and faster.
def STYLE(width):
    return{'width': f'{width}%', 'display': 'inline-block', 'align': 'center', 'padding': '10px',
           'box-shadow': boxshadow,
           'borderRadius': '10px',
           'overflow': 'hidden'}


# The KPI Boxes are the elements used on the result page to display for instance the results of the Monte Carlo
# Analysis. This function is coded so that there are always four boxed next to each other with some space in between.
def kpiboxes(id, formula, color):
    return html.Div([
        dash_table.DataTable(
            id='kpi_table_TV',
            columns=[{'name': id, 'id': id}],
            style_cell_conditional=[],
            style_as_list_view=False,
            style_cell={'padding': '10px', 'textAlign': 'left'},
            style_header={'font-size': '22px',
                          'font-family': 'Calibri',
                          'border': '1px solid white',
                          'backgroundColor': color,
                          'fontWeight': 'bold',
                          'color': 'white'},
            style_data={'font-family': 'Calibri',
                        'border': '1px solid white',
                        'backgroundColor': color,
                        'color': 'white',
                        'font-size': '22px'},
            style_table={'border': '1px solid lightgrey',
                         'borderRadius': '10px',
                         'overflow': 'hidden',
                         'box-shadow': '5px 4px 5px 5px lightgrey'},
            data=[{id: formula}]
        )], style={'width': '25%', 'display': 'inline-block', 'align': 'left', 'padding': "20px"})


# The conditional box is just like the kpiboxes function above, however when using this function, the fields that have
# a value of above 0, are colorized.
def conditional_box(id, formula):
    return html.Div([
        dash_table.DataTable(
            id='kpi_table_TV',
            columns=[{'name': id, 'id': id}],
            style_cell_conditional=[],
            style_as_list_view=False,
            style_cell={'padding': '10px', 'textAlign': 'left'},
            data=[{id: formula}],
            editable=False,
            style_header={'font-size': '18px',
                          'font-family': 'Calibri',
                          'border': '1px solid white',
                          'backgroundColor': blues1,
                          'fontWeight': 'bold',
                          'color': 'white'},
            style_data={'font-family': 'Calibri',
                        'border': '1px solid white',
                        'backgroundColor': blues1,
                        'color': 'white',
                        'font-size': '22px'},
            style_table={'border': '1px solid lightgrey',
                         'borderRadius': '10px',
                         'overflow': 'hidden',
                         'box-shadow': '5px 4px 5px 5px lightgrey'},
            style_data_conditional=[{'if': {'filter_query': f'{{{id}}} <= 0',
                                            'column_id': f'{id}'},
                                     'backgroundColor': strongRed, 'color': 'black'},
                                    {'if': {'filter_query': f'{{{id}}} > 0',
                                            'column_id': f'{id}'},
                                     'backgroundColor': strongGreen, 'color': 'black'},
                                    ]

        )], style={'width': '25%', 'display': 'inline-block', 'align': 'left', 'padding': "20px"})

