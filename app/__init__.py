from flask import Flask
from flask_assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)

scss_bundle = Bundle('styles/main.scss', filters='pyscss', output='styles/styles.css', depends='styles/*.scss')
assets.register('scss_all', scss_bundle)

from data_clean import routes