import os

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

GRAPH_HEIGHT = 750

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([

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
        dcc.Input(id="diameter", value='1000', type='number', debounce=True, min=1, step=1),
        html.Label('Length (m)'),
        dcc.Input(id="length", value='20.0', type='number', debounce=False, min=1.0, step=0.5),
        html.Label('Level (m)'),
        dcc.Input(id="level", value='-2.5', type='number', debounce=False, step=0.5),
        html.Label('Force (kN)'),
        dcc.Input(id="force", value='500', type='number', debounce=False, min=10.0, step=10.0),
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

])


@app.callback(
    Output('div_size', 'children'),
    [Input('length', 'value'), Input('div_num', 'value')])
def update_div_size(length, div_num):
    div_size = float(length)*1e3 / int(div_num)
    return div_size


@app.callback(
    Output('stiff', 'children'),
    [Input('diameter', 'value'), Input('material', 'value')])
def update_stiff(diameter, material):
    return float(material) * np.pi * float(diameter) ** 4 / 64


@app.callback(
    Output('kh0s', 'children'),
    [Input('diameter', 'value'), Input('div_num', 'value'), Input('n_num', 'value'), Input('alpha', 'value'), Input('reduction', 'value')])
def update_kh0s(diameter, div_num, n_num, alpha, reduction):
    # debug ----------------------------------------------------------------
    kh0 = float(n_num) * float(alpha) * float(reduction) * 700 * (float(diameter) / 10) ** (-3 / 4) / 1e6
    kh0s = np.ones(div_num + 1) * kh0
    # ----------------------------------------------------------------------
    return kh0s


@app.callback(
    Output('khs', 'children'),
    [Input('y', 'children'), Input('kh0s', 'children'), Input('mode', 'value'), Input('dec_mode', 'value')])
def update_khs(y, kh0s, mode, dec_mode):
    if mode == 'liner':
        khs = kh0s
    else:
        khs = reduced_khs(y, kh0s, dec_mode)
    return khs


@app.callback(
    Output('x', 'children'),
    [Input('length', 'value'), Input('div_num', 'value')])
def update_x(length, div_num):
    return np.linspace(0, float(length) * 1e3, int(div_num))


@app.callback(
    Output('y', 'children'),
    [Input('mode', 'value'), Input('dec_mode', 'value'), Input('diameter', 'value'), Input('level', 'value'), Input('force', 'value'), Input('condition', 'value'), Input('div_num', 'value'), Input('div_size', 'children'), Input('stiff', 'children'), Input('kh0s', 'children')])
def update_deformations(mode, dec_mode, diameter, _, force, condition, div_num, div_size, stiff, kh0s):
    kh0s = np.array(kh0s)
    if mode == 'liner':
        y = deformation(diameter, div_size, div_num, force, stiff, kh0s, condition)
    else:
        y = deformation_by_non_liner(diameter, div_size, div_num, force, stiff, kh0s, condition, dec_mode)
    return y


@app.callback(
    Output('t', 'children'),
    [Input('y', 'children'), Input('div_size', 'children')])
def update_theta(y, div_size):
    return theta(y, div_size)


@app.callback(
    Output('m', 'children'),
    [Input('t', 'children'), Input('div_size', 'children'), Input('stiff', 'children')])
def update_moments(t, div_size, stiff):
    return moment(t, div_size, stiff)


@app.callback(
    Output('q', 'children'),
    [Input('force', 'value'), Input('m', 'children'), Input('div_size', 'children')])
def update_shears(q0, m, div_size):
    return shear(m, div_size, q0)


@app.callback(
    Output('subplot', 'figure'),
    [Input('x', 'children'), Input('kh0s', 'children'), Input('khs', 'children'), Input('y', 'children'), Input('t', 'children'), Input('m', 'children'), Input('q', 'children')])
def update_subplot(x, kh0s, khs, y, t, m, q):
    x = np.array(x) * 1e-3
    kh0s = np.array(kh0s) * 1e6
    khs = np.array(khs) * 1e6
    y = np.array(y)[2:-3]
    t = np.array(t)[2:-3]
    m = np.array(m)[2:-3] * 1e-6
    q = np.array(q)[2:-3] * 1e-3
    fig = make_subplots(
        rows=1, cols=5,
        subplot_titles=("Kh(kN/m3)", "Deformation(mm)", "Degree(rad)", "Moment(kNm)", "Shear(kN)"),
        shared_yaxes=True)
    # fig.add_trace(go.Scatter(x=kh0s, y=x, fill='tozerox', line=dict(color="#9C27B0")), row=1, col=1)
    fig.add_trace(go.Scatter(x=khs, y=x, fill='tozerox', line=dict(color="#9C27B0")), row=1, col=1)
    fig.add_trace(go.Scatter(x=y, y=x, fill='tozerox', line=dict(color="#2196F3")), row=1, col=2)
    fig.add_trace(go.Scatter(x=t, y=x, fill='tozerox', line=dict(color="#FFC107")), row=1, col=3)
    fig.add_trace(go.Scatter(x=m, y=x, fill='tozerox', line=dict(color="#E91E63")), row=1, col=4)
    fig.add_trace(go.Scatter(x=q, y=x, fill='tozerox', line=dict(color="#4CAF50")), row=1, col=5)
    fig['layout'].update(height=GRAPH_HEIGHT, showlegend=False)
    fig['layout']['yaxis'].update(autorange='reversed')
    return fig


def deformation(diameter, div_size, div_num, force, stiff, khs, condition):
    k0 = np.inf if condition == "fix" else 1.0e-10
    # 式が見やすいように整理
    b, n, h, ei = float(diameter), int(div_num), float(div_size), float(stiff)
    p = float(force) * 1e3
    # 事前計算（stiff = EI）
    c1s = 6 + h ** 4 * np.array(khs) * b / ei
    c2 = ei / k0
    c3 = -2 * p * h ** 3 / ei

    # 左辺のマトリクスを作成
    left = np.zeros((n + 5, n + 5))
    # 境界条件を入力
    left[0, 0:5] = [-1, 2, 0, -2, 1]
    left[1, 0:5] = [0, c2 - h, -2 * c2, c2 + h, 0]
    left[-1, -5:] = [-1, 2, 0, -2, 1]
    left[-2, -5:] = [0, 1, -2, 1, 0]
    # その他の行に一般式を入れ込んでいく
    for i in range(2, n + 3):
        left[i, i - 2:i + 3] = [1, -4, c1s[i - 2], -4, 1]

    # 右辺のマトリクスを作成
    right = np.zeros(n + 5)
    right[0] = c3

    return -np.linalg.solve(left, right)


def deformation_by_non_liner(diameter, div_size, div_num, force, stiff, kh0s, condition, dec_mode):
    err = np.ones(int(div_num) + 5) * 10
    y = deformation(diameter, div_size, div_num, force, stiff, kh0s, condition)
    while np.any(err > 0.1):
        y0 = y
        khs_dec = reduced_khs(y, kh0s, dec_mode)
        y = deformation(diameter, div_size, div_num, force, stiff, khs_dec, condition)
        err = abs(y - y0)
    return y


def reduced_khs(y, kh0s, dec_mode):
    y = np.array(y)
    kh0s = np.array(kh0s)
    if dec_mode == 'multi':
        dec = np.where(abs(y) > 10, (abs(y) / 10)**(-1/2), 1.0)[2:-2]
    else:
        dec = (abs(y[2]) / 10)**(-1/2) if abs(y[2]) > 10 else 1.0
    return kh0s * dec


def theta(y, h):
    return np.gradient(np.array(y), float(h))


def moment(t, h, stiff):
    return - np.gradient(np.array(t), float(h)) * float(stiff)


def shear(m, h, q0):
    q = np.gradient(np.array(m), float(h))
    q[2] = -float(q0) * 1e3
    return q


if __name__ == '__main__':
    app.run_server(debug=True)
