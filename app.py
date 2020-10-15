import time

import numpy as np
import pandas as pd
from flask import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import calculations

app = Flask(__name__)
app.secret_key = "hogehoge"


@app.route("/", methods=["GET"])
def main_page():

    soil_data = decode_upload_file('./sample/sample1.xlsx')
    session['soil_data'] = soil_data

    return render_template("main.html")


@app.route("/solve", methods=["POST"])
def solve():

    start = time.time()

    inputs = request.json
    soil_data = session['soil_data']
    inputs['soil_data'] = soil_data

    results = calculations.get_results(**inputs)

    summary = update_summary(results)
    fig = update_figure(**results)

    solution_time = "time : {:.3f} sec".format(time.time() - start)

    return json.dumps({
        "summary": summary,
        "fig": fig,
        "time": solution_time
    })


@app.route("/init_upload_ajax", methods=["POST"])
def init_upload_ajax():

    soil_data = session['soil_data']
    soil_table = update_soil_data_table(soil_data)

    return soil_table


@app.route("/upload_ajax", methods=["POST"])
def upload_ajax():

    files = request.files
    soil_data = decode_upload_file(files['file'])
    session['soil_data'] = soil_data
    soil_table = update_soil_data_table(soil_data)

    return soil_table


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


def update_soil_data_table(soil_data: dict):

    td = {}
    for key, value in soil_data.items():
        data = list(map(lambda i: '<td>{}</td>'.format(i), value))
        td[key] = data

    html = ""
    for i in range(len(td['depth'])):
        row = "<tr>" + td['depth'][i] + td['nValue'][i] + td['soil'][i] + td['alpha'][i] + td['reductions'][i] + td['adopted_reductions'][i] + td['E0'][i] + "</tr>"
        html += row

    html = "<tr><th>深度</th><th>N値</th><th>土質</th><th>alpha</th><th>低減係数</th><th>採用</th><th>E0</th></tr>" + html

    return html


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
    # app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
    app.run()
