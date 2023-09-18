from flask import Flask
from flask_assets import Environment, Bundle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mejnoon'
assets = Environment(app)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['xml', 'pdf', 'csv', 'xls', 'xlsx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


scss_bundle = Bundle('styles/main.scss', filters='pyscss', output='styles/styles.css', depends='styles/*.scss') # this is to bundle all scss files into one css file
assets.register('scss_all', scss_bundle) # this is to register the bundle with the app

from app import routes