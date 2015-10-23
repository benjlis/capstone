from flask import render_template
from flask import flash
from flask import request, redirect, url_for
from flask.ext.login import login_required
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash


from leiquery import app
from .database import session
from .models import User


@app.route("/", methods=["GET"])
@app.route("/gui", methods=["GET"])
def landing_get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
@app.route("/gui", methods=["POST"])
def landing_post():
    lei = request.form["lei"]
    name = request.form["name"]
    return redirect(url_for("search_get"))

@app.route("/gui/signup", methods=["GET"])
def signup_get():
    return render_template("signup.html")

@app.route("/gui/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
@app.route("/gui/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    user = session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    login_user(user)
    return redirect(request.args.get('next') or url_for("landing_get"))

@app.route("/gui/search", methods=["GET"])
@login_required
def search_get():
    return render_template("search.html")
    
@app.route("/gui/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return render_template("logout.html")
    
    
@app.route("/gui/search", methods=["POST"])
def search_post():
    # return  redirect(request.args.get('next') or url_for("search_get"))
    render_template("search.html")
