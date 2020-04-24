import os

import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from page import create_layout
from utils import *

GRAPH_HEIGHT = 750

app = dash.Dash(__name__)
server = app.server

app.layout = create_layout(app)


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


if __name__ == '__main__':
    app.run_server(debug=True)
