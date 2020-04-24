import dash_core_components as dcc
import dash_html_components as html


def create_layout(app):
    return html.Div([

        html.H1("Non-linear analysis of piles in single-layered ground"),

        html.H2("Settings"),
        html.Div([
            html.Label('Analysis mode'),
            dcc.RadioItems(
                id='mode',
                options=[
                    {'label': 'Non liner', 'value': 'non_liner'},
                    {'label': 'Liner', 'value': 'liner'},
                ],
                value='non_liner'
            ),
            html.Label('Reduction mode'),
            dcc.RadioItems(
                id='dec_mode',
                options=[
                    {'label': 'Multi', 'value': 'multi'},
                    {'label': 'Single', 'value': 'single'},
                ],
                value='multi'
            ),
            html.Label('Pile top condition'),
            dcc.RadioItems(
                id='condition',
                options=[
                    {'label': 'FIX', 'value': 'fix'},
                    {'label': 'PIN', 'value': 'pin'},
                ],
                value='fix'
            ),
            html.Label('Material'),
            dcc.RadioItems(
                id='material',
                options=[
                    {'label': 'Concrete', 'value': 2.05e4},
                    {'label': 'Steel', 'value': 2.05e5},
                ],
                value=2.05e4
            ),
        ], style={'columnCount': 4}),

        html.Br([]),

        html.Label('Division number'),
        dcc.Slider(
            id='div_num',
            min=100,
            max=500,
            marks={i * 100: str(i * 100) for i in range(1, 6)},
            value=300,
        ),

        html.H2("Pile Parameters"),
        html.Div([
            html.Label('Diameter (mm)'),
            dcc.Input(id="diameter", value='1000', type='number',
                debounce=True, min=1, step=1),
            html.Label('Length (m)'),
            dcc.Input(id="length", value='20.0', type='number', debounce=False,
                min=1.0, step=0.5),
            html.Label('Level (m)'),
            dcc.Input(id="level", value='-2.5', type='number', debounce=False,
                step=0.5),
            html.Label('Force (kN)'),
            dcc.Input(id="force", value='500', type='number', debounce=False,
                min=10.0, step=10.0),
        ], style={'columnCount': 4}),

        html.H2("Ground Parameters"),
        html.Div([
            html.Label('N'),
            dcc.Input(id="n_num", value='10', type='text'),
            html.Label('Alpha'),
            dcc.Input(id="alpha", value='60', type='text'),
            html.Label('Liquefaction reduction'),
            dcc.Input(id="reduction", value='0.350', type='text'),
        ], style={'columnCount': 4}),

        dcc.Graph(id='subplot'),

        html.Div(id='div_size', style={'display': 'none'}),
        html.Div(id='stiff', style={'display': 'none'}),
        html.Div(id='kh0s', style={'display': 'none'}),
        html.Div(id='khs', style={'display': 'none'}),
        html.Div(id='x', style={'display': 'none'}),
        html.Div(id='y', style={'display': 'none'}),
        html.Div(id='t', style={'display': 'none'}),
        html.Div(id='m', style={'display': 'none'}),
        html.Div(id='q', style={'display': 'none'})

    ], className="page")
