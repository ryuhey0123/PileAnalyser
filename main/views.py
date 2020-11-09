import time

from flask import session, request, render_template, json

from main import app
from main import calculations
from models import Sess, User, Content, Project, Soildata


@app.route("/", methods=["GET"])
def main_page():

    soil_data = calculations.decode_upload_file('./sample/sample1.xlsx')
    session['soil_data'] = soil_data

    return render_template("main.html")


@app.route("/solve", methods=["POST"])
def solve():

    start = time.time()

    inputs = request.json
    soil_data = session['soil_data']
    inputs['soil_data'] = soil_data
    inputs['div_num'] = 100

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
    soil_data = calculations.decode_upload_file(files['file'])
    session['soil_data'] = soil_data
    soil_table = update_soil_data_table(soil_data)

    return soil_table


@app.route("/save", methods=["POST"])
def save_data():
    from models.database import Base, ENGINE

    inputs = request.json

    Base.metadata.drop_all(bind=ENGINE)
    Base.metadata.create_all(bind=ENGINE)

    Sess.add(User(name='MacLOve', password='fuckyou'))

    project = Project(title='Test Project1')
    Sess.add(project)

    test_soildata1 = Soildata(data=json.dumps(session['soil_data']))
    Sess.add(test_soildata1)

    test_user: User = Sess.query(User).filter(User.name == 'MacLOve').first()

    Sess.add(Content(
        title=inputs["contents"]["title"],
        input=inputs["inputs"],
        user_id=test_user.id,
        project_id=project.id,
        soildata_id=test_soildata1.id,
    ))

    Sess.commit()

    return 'Hello'


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
