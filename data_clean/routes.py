from data_clean import app


@app.route('/')
def interface():
    return "<p>Hello, World!</p>"


@app.errorhandler(404)
def page_not_found(error):
    return "<p>Sorry, this page was not found.</p>", 404
