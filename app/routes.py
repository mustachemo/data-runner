from app import app
from flask import render_template, request, redirect, url_for, flash


@app.route('/')
def interface():
    flash('This is a flash message', 'info')
    flash('This is another flash message', 'warning')
    flash('This is a third flash message', 'danger')
    flash('This is a fourth flash message', 'success')
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(error):
    return "<p>Sorry, this page does not exist.</p>", 404

@app.errorhandler(500)
def page_not_found(error):
    return "<p>Sorry, something went wrong.</p>", 500
