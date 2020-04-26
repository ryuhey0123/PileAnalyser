import dash_core_components as dcc
import dash_html_components as html


# @formatter:off


def create_layout(app):
    return html.Div([

        html.Section([

            html.H3("Analysis of piles"),

            html.H6("Settings"),

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

            html.H6("Pile Parameters"),

            html.Table([
                html.Tr([
                    html.Th('Diameter (mm)'),
                    html.Th('Length (m)'),
                    html.Th('Level (m)'),
                    html.Th('Force (kN)')
                ]),
                html.Tr([
                    html.Td(dcc.Input(id="diameter", value='1000', type='number',debounce=True, min=1, step=1)),
                    html.Td(dcc.Input(id="length", value='20.0', type='number', debounce=False, min=1.0, step=0.5)),
                    html.Td(dcc.Input(id="level", value='-2.5', type='number', debounce=False, step=0.5)),
                    html.Td(dcc.Input(id="force", value='500', type='number', debounce=False, min=10.0, step=10.0))
                ])
            ], style={'width': '100%'}),

            html.H6("Ground Parameters"),

            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),

            html.H6("Result"),

            html.Table([
                html.Tr([
                    html.Th('', style={"width": "80px"}),
                    html.Th([html.Div('kh'), html.Div('kN/m3', className='unit')]),
                    html.Th([html.Div('Deformation'), html.Div('mm', className='unit')]),
                    html.Th([html.Div('Degree'), html.Div('rad', className='unit')]),
                    html.Th([html.Div('Moment'), html.Div('kNm', className='unit')]),
                    html.Th([html.Div('Shear'), html.Div('kN', className='unit')]),
                ]),
                html.Tr([
                    html.Th('MAX'),
                    html.Td(id='max_kh'),
                    html.Td(id='max_y'),
                    html.Td(id='max_t'),
                    html.Td(id='max_m'),
                    html.Td(id='max_q', style={"padding": "2px 5px"})
                ]),
                html.Tr([
                    html.Th('MIN'),
                    html.Td(id='min_kh'),
                    html.Td(id='min_y'),
                    html.Td(id='min_t'),
                    html.Td(id='min_m'),
                    html.Td(id='min_q', style={"padding": "2px 5px"})
                ]),
            ], style={'width': '100%'}, className='result'),

            dcc.Graph(id='subplot'),

            html.Label('Division number'),
            dcc.Slider(
                id='div_num',
                min=100,
                max=500,
                marks={i * 100: str(i * 100) for i in range(1, 6)},
                value=100,
            ),

            html.Div(id='div_size', style={'display': 'none'}),
            html.Div(id='stiff', style={'display': 'none'}),
            html.Div(id='decrease', style={'display': 'none'}),
            html.Div(id='kh0s', style={'display': 'none'}),
            html.Div(id='khs', style={'display': 'none'}),
            html.Div(id='x', style={'display': 'none'}),
            html.Div(id='y', style={'display': 'none'}),
            html.Div(id='t', style={'display': 'none'}),
            html.Div(id='m', style={'display': 'none'}),
            html.Div(id='q', style={'display': 'none'})

        ])

    ], className="page")

