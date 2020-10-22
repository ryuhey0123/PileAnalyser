from flask import Flask

app = Flask(__name__)
app.config.from_object('main.config')

import main.views

# app.run(host='127.0.0.1', port=5000, debug=True)
