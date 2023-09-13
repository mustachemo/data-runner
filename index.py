from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    message = "Awaiting Command..."
    if request.method == "POST" and "brew" in request.values:
        message = "<a href=\"https://www.rfc-editor.org/rfc/rfc2324#section-2.3.2\">Error 418</a> I'm a teapot"
    return render_template('index.html', message=message)
