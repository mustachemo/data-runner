import os
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    message = "Awaiting Command..."
    if request.method == "POST" and "brew" in request.values:
        message = "<a href=\"https://www.rfc-editor.org/rfc/rfc2324#section-2.3.2\">Error 418</a> I'm a teapot"
        return render_template('index.html', message=message)

    if request.method == 'POST' and "upload" in request.values:
        # todo implement file upload
        pass

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)