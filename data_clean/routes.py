from data_clean import app
from flask import render_template, request, redirect, url_for


@app.route('/')
def interface():
    return render_template('base.html')


@app.errorhandler(404)
def page_not_found(error):
    return "<p>Sorry, this page does not exist.</p>", 404

@app.errorhandler(500)
def page_not_found(error):
    return "<p>Sorry, something went wrong.</p>", 500
