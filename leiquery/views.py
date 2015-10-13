from flask import render_template

from leiquery import app
from .database import session
from .models import User

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")