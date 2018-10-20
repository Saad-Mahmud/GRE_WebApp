from zSaad_Test.Backend.app import APP_MAIN
from flask import render_template



@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")