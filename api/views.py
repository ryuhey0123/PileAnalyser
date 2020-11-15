import time

from flask import session, request, render_template, json, jsonify

from api import app
from api import calculations as calc
from models import Sess, User, Content, Project, Soildata


# Page Routing


@app.route("/", methods=["GET"])
def main_page():
    return render_template("main.html")


# API Routing


@app.route('/login', methods=["POST"])
def login():
    inputs = request.json
    session['user'] = inputs['name']
    return '500'


@app.route("/solve", methods=["POST"])
def solve():
    start = time.time()

    inputs = request.json
    inputs['soil_data'] = session['soil_data']

    results = calc.get_results(**inputs)

    # for key, value in results.items():
    #     results[key] = value.tolist()

    solution_time = "time : {:.3f} sec".format(time.time() - start)

    return json.dumps({"results": results, "time": solution_time})


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get('file')

    if file is None:
        soil_data = calc.decode_upload_file('./assets/sample/sample1.xlsx')
    else:
        soil_data = calc.decode_upload_file(file)

    session['soil_data'] = soil_data

    return jsonify(soil_data)


# @app.route("/upload", methods=["GET"])
# def upload():
#     soil_data = calc.decode_upload_file('./assets/sample/sample1.xlsx')
#     return jsonify(soil_data)

# Database Routing


@app.route("/database/save", methods=["POST"])
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

    return '500'


@app.route("/database/load", methods=["POST"])
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


@app.route("/database/projects", methods=["GET"])
def get_projects():
    user: User = Sess.query(User).\
        filter(User.name == session['user']).first()

    projects = Sess.query(Project).\
        filter(Project.user_id == user.id)

    return {'titles': [project.title for project in projects]}


@app.route("/database/contents/<project_title>", methods=["GET"])
def get_contents_name_by_project(project_title):
    user: User = Sess.query(User).\
        filter(User.name == session['user']).first()

    project: Project = Sess.query(Project).\
        filter(Project.user_id == user.id, Project.title == project_title).first()

    contents = Sess.query(Content).\
        filter(Content.project_id == project.id)

    return {'titles': [content.title for content in contents]}
