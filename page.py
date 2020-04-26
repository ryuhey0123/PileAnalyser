import dash_core_components as dcc
import dash_html_components as html


def create_layout(app):
    return html.Div([

        html.Section([

            html.H2("Analysis of piles"),

            html.H5("Settings"),

            html.Table([
                html.Tr([
                    html.Th('Analysis mode'),
                    html.Th('Reduction mode'),
                    html.Th('Pile top condition'),
                    html.Th('Material')
                ]),
                html.Tr([
                    html.Td(
                        dcc.RadioItems(
                            id='mode',
                            options=[
                                {'label': 'Non liner', 'value': 'non_liner'},
                                {'label': 'Liner', 'value': 'liner'},
                            ],
                            value='non_liner'
                        )
                    ),
                    html.Td(
                        dcc.RadioItems(
                            id='dec_mode',
                            options=[
                                {'label': 'Multi', 'value': 'multi'},
                                {'label': 'Single', 'value': 'single'},
                            ],
                            value='multi'
                        )
                    ),
                    html.Td(
                        dcc.RadioItems(
                            id='condition',
                            options=[
                                {'label': 'FIX', 'value': 'fix'},
                                {'label': 'PIN', 'value': 'pin'},
                            ],
                            value='fix'
                        )
                    ),
                    html.Td(
                        dcc.RadioItems(
                            id='material',
                            options=[
                                {'label': 'Concrete', 'value': 2.05e4},
                                {'label': 'Steel', 'value': 2.05e5},
                            ],
                            value=2.05e4
                        )
                    )
                ])
            ], style={'width': '100%'}),

            html.H5("Pile Parameters"),

            html.Table([
                html.Tr([
                    html.Th('Diameter (mm)'),
                    html.Th('Length (m)'),
                    html.Th('Level (m)'),
                    html.Th('Force (kN)')
                ]),
                html.Tr([
                    html.Td(
                        dcc.Input(id="diameter", value='1000', type='number',
                            debounce=True, min=1, step=1),
                    ),
                    html.Td(
                        dcc.Input(id="length", value='20.0', type='number',
                            debounce=False,
                            min=1.0, step=0.5),
                    ),
                    html.Td(
                        dcc.Input(id="level", value='-2.5', type='number',
                            debounce=False,
                            step=0.5),
                    ),
                    html.Td(
                        dcc.Input(id="force", value='500', type='number',
                            debounce=False,
                            min=10.0, step=10.0),
                    )
                ])
            ], style={'width': '100%'}),

            html.H5("Ground Parameters"),

            html.Table([
                html.Tr([
                    html.Th('N'),
                    html.Th('Alpha'),
                    html.Th('Liquefaction reduction'),
                ]),
                html.Tr([
                    html.Td(
                        dcc.Input(id="n_num", value='10', type='text'),
                    ),
                    html.Td(
                        dcc.Input(id="alpha", value='60', type='text'),
                    ),
                    html.Td(
                        dcc.Input(id="reduction", value='0.350', type='text'),
                    )
                ])
            ], style={'width': '75%'}),

            dcc.Graph(id='subplot'),

            html.Label('Division number'),
            dcc.Slider(
                id='div_num',
                min=100,
                max=500,
                marks={i * 100: str(i * 100) for i in range(1, 6)},
                value=300,
            ),

            html.Div(id='div_size', style={'display': 'none'}),
            html.Div(id='stiff', style={'display': 'none'}),
            html.Div(id='kh0s', style={'display': 'none'}),
            html.Div(id='khs', style={'display': 'none'}),
            html.Div(id='x', style={'display': 'none'}),
            html.Div(id='y', style={'display': 'none'}),
            html.Div(id='t', style={'display': 'none'}),
            html.Div(id='m', style={'display': 'none'}),
            html.Div(id='q', style={'display': 'none'})

        ], className="sheet padding-10mm")

    ], className="page")
