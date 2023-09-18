from flask import Flask
from flask_assets import Environment, Bundle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mejnoon'
assets = Environment(app)

scss_bundle = Bundle('styles/main.scss', filters='pyscss', output='styles/styles.css', depends='styles/*.scss')
assets.register('scss_all', scss_bundle)

from app import routes