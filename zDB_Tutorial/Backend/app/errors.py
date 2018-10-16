from flask import render_template
from zDB_Tutorial.Backend.app import APP_MAIN

@APP_MAIN.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@APP_MAIN.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500