from flask import Flask

app = Flask(__name__)
app.config.from_object('api.config')

from . import views
