from flask import Flask

app = Flask(__name__)
app.config.from_object('main.config')

import main.views
