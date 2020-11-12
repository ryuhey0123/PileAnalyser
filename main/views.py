import time

from flask import session, request, render_template, json

from main import app
from main import calculations as calc
from models import Sess, User, Content, Project, Soildata


@app.route("/", methods=["GET"])
def main_page():

    soil_data = calc.decode_upload_file('./sample/sample1.xlsx')
    session['soil_data'] = soil_data

    return render_template("main.html")


@app.route("/solve", methods=["POST"])
def solve():

    start = time.time()

    inputs = request.json
    soil_data = session['soil_data']
    inputs['soil_data'] = soil_data
    inputs['div_num'] = 100

    results = calc.get_results(**inputs)

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
    soil_table = calc.update_soil_data_table(soil_data)

    return soil_table


@app.route("/upload_ajax", methods=["POST"])
def upload_ajax():

    files = request.files
    soil_data = calc.decode_upload_file(files['file'])
    session['soil_data'] = soil_data
    soil_table = calc.update_soil_data_table(soil_data)

    return soil_table


@app.route("/save", methods=["POST"])
def save():
    inputs = request.json

    user: User = Sess.query(User).\
        filter(User.name == session['user']).first()

    project: Project = Sess.query(Project).\
        filter(Project.title == inputs['contents']['project']).first()

    soildata = Soildata(data=json.dumps(session['soil_data']), user_id=user.id)
    Sess.add(soildata)
    Sess.flush()

    Sess.add(Content(
        title=inputs["contents"]["title"],
        input=inputs["inputs"],
        user_id=user.id,
        project_id=project.id,
        soildata_id=soildata.id,
    ))

    Sess.commit()

    return 'Hello'


@app.route("/load", methods=["POST"])
def load():
    user: User = Sess.query(User).\
        filter(User.name == session['user']).first()

    project: Project = Sess.query(Project).\
        filter(Project.user_id == user.id).\
        filter(Project.title == request.json['project']).first()

    content: Content = Sess.query(Content).\
        filter(Content.project_id == project.id).\
        filter(Content.title == request.json['content']).first()

    soil_data: Soildata = Sess.query(Soildata).get(content.soildata_id)

    session['soil_data'] = json.loads(soil_data.data)

    soil_table = calc.update_soil_data_table(json.loads(soil_data.data))

    return json.dumps({
        'input': content.input,
        'soil_data': soil_table
    })


@app.route('/login', methods=["POST"])
def login():
    inputs = request.json
    session['user'] = inputs['name']
    return 'OK'


@app.route("/get_projects", methods=["POST"])
def get_projects():
    user: User = Sess.query(User).\
        filter(User.name == session['user']).first()

    projects = Sess.query(Project).\
        filter(Project.user_id == user.id)

    return {'titles': [project.title for project in projects]}


@app.route("/get_contents_name", methods=["POST"])
def get_contents_name():
    project: Project = Sess.query(Project).\
        filter(Project.title == request.json['project']).first()

    contents = Sess.query(Content).\
        filter(Content.project_id == project.id)

    return {'titles': [content.title for content in contents]}
