import time

import pandas as pd
from flask import session, request, render_template, json

from main import app
from main import calculations


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

    for key, value in results.items():
        results[key] = value.tolist()

    solution_time = "time : {:.3f} sec".format(time.time() - start)

    return json.dumps({
        "results": results,
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
    # app.run()
