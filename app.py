from flask import Flask

app = Flask()
# app.debug = True
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')
app.config['DEBUG'] = True


@app.route('/')
def interface():
    return "<p>Hello, World!</p>"


@app.errorhandler(404)
def page_not_found(error):
    return "<p>Sorry, this page was not found.</p>", 404


if __name__ == '__main__':
    app.run()
