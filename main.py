import numpy as np
from flask import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import calculations

app = Flask(__name__)


# initial values

init_form_values = {
    'mode': 'non_liner',
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


# interface

@app.route("/", methods=["GET"])
def init_page():
    return render_template("main.html", fig="", **init_form_values, **init_result_values)


@app.route("/", methods=["POST"])
def main_page():

    inputs = request.form
    results = calculations.get_results(**inputs)  # TODO: API
    summary = update_summary(results)
    fig = update_figure(results)

    return render_template("main.html", fig=fig, **inputs, **summary)


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


def update_figure(results):

    x = results['x']
    dec = results['dec']
    kh0s = results['kh0s']
    y = results['y']
    t = results['t']
    m = results['m']
    q = results['q']

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

    return fig.to_html()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
