import base64
import io
import os
import gunicorn

import numpy as np
import pandas as pd
from scipy import interpolate
import xlrd

import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from flask_caching import Cache

# from page import *
from page_jpn import *

# GRAPH_WIDTH = 700
# GRAPH_HEIGHT = 540

CACHE_CONFIG = {
    "DEBUG": True,           # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = dash.Dash(__name__)
app.title = '杭の解析'
server = app.server

cache = Cache(server, config=CACHE_CONFIG)

app.layout = create_layout(app)


@app.callback(
    Output('kh0s', 'children'),
    [Input('upload-data', 'contents'), Input('x', 'children'), Input('diameter', 'value')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')])
def update_kh0s(contents, x, diameter, *args):
    if contents is not None:
        try:
            df = decode_upload_file(contents)
        except Exception as e:
            df = pd.read_excel('sample.xlsx')
            print(e)
    else:
        df = pd.read_excel('sample.xlsx')
    kh0s = kh0s_by_df(df, x, diameter)
    return kh0s


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
    Output('decrease', 'children'),
    [Input('y', 'children'), Input('mode', 'value'), Input('dec_mode', 'value')])
def update_decrease(y, mode, dec_mode):
    return reduced(y, mode, dec_mode)


@app.callback(
    Output('khs', 'children'),
    [Input('kh0s', 'children'), Input('decrease', 'children')])
def update_khs(kh0s, dec):
    return np.array(kh0s) * np.array(dec)


@app.callback(
    Output('x', 'children'),
    [Input('length', 'value'), Input('div_num', 'value'), Input('level', 'value')])
def update_x(length, div_num, level):
    return np.linspace(-float(level) * 1e3, float(length) * 1e3 - float(level) * 1e3, int(div_num + 1))


@app.callback(
    Output('y', 'children'),
    [Input('mode', 'value'), Input('dec_mode', 'value'), Input('diameter', 'value'), Input('force', 'value'), Input('condition', 'value'), Input('div_num', 'value'), Input('div_size', 'children'), Input('stiff', 'children'), Input('kh0s', 'children')])
def update_deformations(mode, dec_mode, diameter, force, condition, div_num, div_size, stiff, kh0s):
    kh0s = np.array(kh0s)
    if mode == 'liner':
        y = deformation(diameter, div_size, div_num, force, stiff, kh0s, condition)
    else:
        y = deformation_by_non_liner(diameter, div_size, div_num, force, stiff, kh0s, condition, mode, dec_mode)
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
    Output('max_kh', 'children'),
    [Input('khs', 'children')])
def update_max_kh(khs):
    return "{:.0f}".format(max(khs) * 1e6)


@app.callback(
    Output('min_kh', 'children'),
    [Input('khs', 'children')])
def update_min_kh(khs):
    return "{:.0f}".format(min(khs) * 1e6)


@app.callback(
    Output('max_y', 'children'),
    [Input('y', 'children')])
def update_max_deformation(y):
    return "{:.2f}".format(max(y))


@app.callback(
    Output('min_y', 'children'),
    [Input('y', 'children')])
def update_min_deformation(y):
    return "{:.2f}".format(min(y))


@app.callback(
    Output('max_t', 'children'),
    [Input('t', 'children')])
def update_max_theta(t):
    return "{:.3E}".format(max(t))


@app.callback(
    Output('min_t', 'children'),
    [Input('t', 'children')])
def update_min_theta(t):
    return "{:.3E}".format(min(t))


@app.callback(
    Output('max_m', 'children'),
    [Input('m', 'children')])
def update_max_moment(m):
    return "{:.1f}".format(max(m) / 1e6)


@app.callback(
    Output('min_m', 'children'),
    [Input('m', 'children')])
def update_min_moment(m):
    return "{:.1f}".format(min(m) / 1e6)


@app.callback(
    Output('max_q', 'children'),
    [Input('q', 'children')])
def update_max_shear(q):
    return "{:.1f}".format(max(q) / 1e3)


@app.callback(
    Output('min_q', 'children'),
    [Input('q', 'children')])
def update_max_shear(q):
    return "{:.1f}".format(min(q) / 1e3)


@app.callback(
    Output('subplot', 'figure'),
    [
        Input('x', 'children'),
        Input('decrease', 'children'),
        Input('kh0s', 'children'),
        Input('y', 'children'),
        Input('t', 'children'),
        Input('m', 'children'),
        Input('q', 'children')
    ])
def update_subplot(x, dec, kh0s, y, t, m, q):
    x = np.array(x) * 1e-3
    dec = np.array(dec)
    kh0s = np.array(kh0s) * 1e6
    y = np.array(y)[2:-3]
    t = np.array(t)[2:-3] * 1e3
    m = np.array(m)[2:-3] * 1e-6
    q = np.array(q)[2:-3] * 1e-3
    fig = make_subplots(
        rows=1, cols=6,
        subplot_titles=("Decrease", "kh0", "Deformation", "Degree", "Moment", "Shear"),
        shared_yaxes=True)
    fig.add_trace(go.Scatter(x=dec, y=x, fill='tozerox', line=dict(color="#795548")),row=1, col=1)
    fig.add_trace(go.Scatter(x=kh0s, y=x, fill='tozerox', line=dict(color="#9C27B0")), row=1, col=2)
    fig.add_trace(go.Scatter(x=y, y=x, fill='tozerox', line=dict(color="#2196F3")), row=1, col=3)
    fig.add_trace(go.Scatter(x=t, y=x, fill='tozerox', line=dict(color="#FFC107")), row=1, col=4)
    fig.add_trace(go.Scatter(x=m, y=x, fill='tozerox', line=dict(color="#E91E63")), row=1, col=5)
    fig.add_trace(go.Scatter(x=q, y=x, fill='tozerox', line=dict(color="#4CAF50")), row=1, col=6)

    fig['layout'].update(
        autosize=True,
        # height=GRAPH_HEIGHT,
        margin=dict(l=10, r=10, b=50, t=50),
        showlegend=False,
        yaxis=dict(autorange='reversed')
    )
    for i in fig['layout']['annotations']:
        i['font'] = dict(
            family="'Open Sans', 'HelveticaNeue', 'Helvetica Neue', Helvetica, Arial, sans-serif",
            size=13
        )
    return fig


@cache.memoize()
def decode_upload_file(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))
    return df


@cache.memoize()
def kh0s_by_df(df, x, diameter):
    data = df[['採掘深度', 'αβE0\n(採用値)']].values.astype(np.float64).T
    data = np.array([data[0] * 1e3, data[1]])
    fitted1 = interpolate.interp1d(data[0], data[1])
    kh0s = fitted1(np.array(x)) * (float(diameter) / 10) ** (-3 / 4) / 1e6
    return kh0s


@cache.memoize()
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


@cache.memoize()
def deformation_by_non_liner(diameter, div_size, div_num, force, stiff, kh0s, condition, mode, dec_mode):
    err = np.ones(int(div_num) + 5) * 10
    y = deformation(diameter, div_size, div_num, force, stiff, kh0s, condition)
    while np.any(err > 0.1):
        y0 = y
        dec = reduced(y, mode, dec_mode)
        khs_dec = kh0s * dec
        y = deformation(diameter, div_size, div_num, force, stiff, khs_dec, condition)
        err = abs(y - y0)
    return y


@cache.memoize()
def reduced(y, mode, dec_mode):
    y = np.array(y)
    if mode == 'liner':
        dec = np.ones_like(y)[2:-2]
    else:
        if dec_mode == 'multi':
            dec = np.where(abs(y) > 10, (abs(y) / 10)**(-1/2), 1.0)[2:-2]
        else:
            dec = np.ones_like(y)[2:-2]
            dec = dec * (abs(y[2]) / 10)**(-1/2) if abs(y[2]) > 10 else 1.0
    return dec


@cache.memoize()
def theta(y, h):
    return np.gradient(np.array(y), float(h))


@cache.memoize()
def moment(t, h, stiff):
    return - np.gradient(np.array(t), float(h)) * float(stiff)


@cache.memoize()
def shear(m, h, q0):
    q = np.gradient(np.array(m), float(h))
    q[2] = -float(q0) * 1e3
    return q


if __name__ == '__main__':
    app.run_server(debug=True)
