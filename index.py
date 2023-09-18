import os
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    message = "Awaiting Command..."
    if request.method == "POST" and "brew" in request.values:
        message = "<a href=\"https://www.rfc-editor.org/rfc/rfc2324#section-2.3.2\">Error 418</a> I'm a teapot"

    table = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', message=message, table=table)
        file = request.files['file']
        rawData = pd.read_csv(file)
        table = rawData.to_html(index=False)

    #todo, maintain dataframe in backend somehow use global variables?

    return render_template('index.html', message=message, table=table)

if __name__ == '__main__':
    app.run(debug=True)