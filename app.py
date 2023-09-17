from flask import Flask

app = Flask(__name__)


@app.route('/')
def interface():
    return "<p>Hello, World!</p>"


@app.errorhandler(404)
def page_not_found(error):
    return "<p>Sorry, this page was not found.</p>", 404


if __name__ == '__main__':
    app.run()
