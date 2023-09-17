from flask import Flask
from flask_assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)

scss_bundle = Bundle('static/main.scss', filters='pyscss', output='static/styles.css', depends='static/*.scss')
assets.register('scss_all', scss_bundle)

from data_clean import routes