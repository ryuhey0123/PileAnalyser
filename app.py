import time

import numpy as np
import pandas as pd
from flask import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import calculations

app = Flask(__name__)
app.secret_key = "hogehoge"


# initial values

init_form_values = {
    'mode': 'liner',
    'dec_mode': 'multi',
    'condition': 'fix',
    'material': 'concrete',
    'diameter': 1300,
    'length': 17.5,
    'level': -2.5,
    'force': 500,
}

init_result_values = {
    'kh': [0, 0],
    'deformation': [0, 0],
    'degree': [0, 0],
    'moment': [0, 0],
    'shear': [0, 0],
}

init_soil_data = {
    'depth': [1.15, 2.15, 3.15, 4.15, 5.15, 6.15, 7.15, 8.15, 9.15, 10.15, 11.15, 12.15, 13.15, 14.15, 15.15, 16.15, 17.15, 18.15, 19.15, 20.15, 21.15, 22.15, 23.1],
    'nValue': [15.0, 1.9, 3.9, 2.0, 1.9, 3.9, 4.8, 5.0, 3.0, 4.5, 5.8, 2.5, 11.0, 105.9, 225.0, 163.6, 49.0, 90.0, 257.1, 180.0, 450.0, 128.6, 600.0],
    'soil': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    'alpha': [80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80],
    'reductions': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'adopted_reductions': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'E0': [10500.0, 1330.0, 2730.0, 1400.0, 1330.0, 2730.0, 3360.0, 3500.0, 2100.0, 3150.0, 4060.0, 1750.0, 7700.0, 74130.0, 157500.0, 114520.0, 34300.0, 63000.0, 179970.00000000003, 126000.0, 315000.0, 90020.0, 420000.0],
}


# interface

@app.route("/", methods=["GET"])
def init_page():
    session['soil_data'] = init_soil_data
    return render_template("main.html", fig="", **init_form_values, **init_result_values)


@app.route("/", methods=["POST"])
def refresh():

    start = time.time()

    inputs = request.form.to_dict()
    soil_data = session['soil_data']

    inputs['soil_data'] = soil_data
    soil_table = make_soil_data_table(soil_data)

    results = calculations.get_results(**inputs)
    summary = update_summary(results)
    fig = update_figure(**results)

    solution_time = "time : {:.3f} sec".format(time.time() - start)

    return render_template("main.html", fig=fig, **inputs, **summary, soil_table=soil_table, solution_time=solution_time)


# file upload

@app.route("/upload", methods=["POST"])
def upload():

    files = request.files
    soil_data = decode_upload_file(files['uploadFile'])

    session['soil_data'] = soil_data
    soil_table = make_soil_data_table(soil_data)

    return render_template("main.html", fig="", **init_form_values, **init_result_values, soil_table=soil_table)


def make_soil_data_table(soil_data: dict):

    td = {}
    for key, value in soil_data.items():
        data = list(map(lambda i: '<td><input type="text" value="{}"></td>'.format(i), value))
        td[key] = data

    html = ""
    for i in range(len(td['depth'])):
        row = "<tr>" + td['depth'][i] + td['nValue'][i] + td['soil'][i] + td['alpha'][i] + td['reductions'][i] + td['adopted_reductions'][i] + td['E0'][i] + "</tr>"
        html += row

    return html


def decode_upload_file(file):
    df = pd.read_excel(file)
    return dict(
        depth=df['深度'].values.tolist(),
        nValue=df['N値'].values.tolist(),
        soil=df['土質'].values.tolist(),
        reductions=df['低減係数'].values.tolist(),
        adopted_reductions=df['採用低減係数'].values.tolist(),
        alpha=df['alpha'].values.tolist(),
        E0=df['E0'].values.tolist()
    )


# formatters

def update_summary(results):

    def max_and_min_values_by(key: str, field='{:.1f}'):
        return list(map(lambda x: field.format(x), [np.max(results[key]), np.min(results[key])]))

    return dict(
        kh=max_and_min_values_by('kh0s'),
        deformation=max_and_min_values_by('y', field='{:.2f}'),
        degree=max_and_min_values_by('t', field='{:.3f}'),
        moment=max_and_min_values_by('m'),
        shear=max_and_min_values_by('q'),
    )


def update_figure(x, dec, kh0s, y, t, m, q):

    fig = make_subplots(
        rows=1, cols=6,
        subplot_titles=("Decrease", "kh0", "Deformation", "Degree", "Moment", "Shear"),
        shared_yaxes=True)

    fig.add_trace(go.Scatter(x=dec, y=x, fill='tozerox', line=dict(color="#795548")), row=1, col=1)
    fig.add_trace(go.Scatter(x=kh0s, y=x, fill='tozerox', line=dict(color="#9C27B0")), row=1, col=2)
    fig.add_trace(go.Scatter(x=y, y=x, fill='tozerox', line=dict(color="#2196F3")), row=1, col=3)
    fig.add_trace(go.Scatter(x=t, y=x, fill='tozerox', line=dict(color="#FFC107")), row=1, col=4)
    fig.add_trace(go.Scatter(x=m, y=x, fill='tozerox', line=dict(color="#E91E63")), row=1, col=5)
    fig.add_trace(go.Scatter(x=q, y=x, fill='tozerox', line=dict(color="#4CAF50")), row=1, col=6)

    fig.update_xaxes(range=[0, 1.1], row=1, col=1)

    fig['layout'].update(
        autosize=True,
        margin=dict(l=10, r=10, b=50, t=50),
        showlegend=False,
        yaxis=dict(autorange='reversed')
    )

    for i in fig['layout']['annotations']:
        i['font'] = dict(
            family="'Open Sans', 'HelveticaNeue', 'Helvetica Neue', Helvetica, Arial, sans-serif",
            size=13
        )

    return fig.to_html()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
