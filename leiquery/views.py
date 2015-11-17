from flask import render_template
from flask import flash
from flask import request, redirect, url_for
from flask.ext.login import login_required
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash


from leiquery import app
from .database import session
from sqlalchemy import or_
from .models import User, LegalEntity


@app.route("/", methods=["GET"])
@app.route("/gui", methods=["GET"])
def landing_get():
    return render_template("index.html")

@app.route("/", methods=["POST"])
@app.route("/gui", methods=["POST"])
def landing_post():
    lei = request.form["lei"]
    name = request.form["name"]
    if lei:
        query_string = '?lei=' + lei
        if name:
            query_string += '&name=' + name
    elif name:
        query_string = '?name=' + name
    else:
        query_string = ""
    return redirect(url_for("search_post") + query_string)
    #lei, name, results = query_lei()
    #return(render_template("search.html", lei_arg=lei, name_arg=name,
    #                        results_arg=results))

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
    #lei = request.args.get("lei")
    #if lei is None:
    #    lei = ""
    #name = request.args.get("name")
    #if name is None:
    #    name = ""
    results=[]
    lei = request.args.get("lei")
    name = request.args.get("name")
    # check for None and set to null for later display in template
    if lei == None: 
        lei = ""
    if name == None:
        name = ""
    if lei: 
        results = session.query(LegalEntity).filter(LegalEntity.lei == lei)
        name = ""
    elif name:
        results = session.query(LegalEntity).filter( 
                                LegalEntity.legal_name.ilike('%'+name+'%'))
        lei=""                        
    return render_template("search.html", lei_arg=lei, name_arg=name,
                                results_arg=results)
    
@app.route("/gui/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return render_template("logout.html")
    
def query_lei():
    # check form or args for values
    lei = request.form["lei"]
    name = request.form["name"]
    results = []
    if lei: 
        results = session.query(LegalEntity).filter(LegalEntity.lei == lei)
        name = ""
    elif name:
        results = session.query(LegalEntity).filter( 
                                LegalEntity.legal_name.ilike('%'+name+'%'))
        lei = ""
    return lei, name, results
            
    
@app.route("/gui/search", methods=["POST"])
@login_required
def search_post():
    # check for arguments
    #lei = request.form["lei"]
    #name = request.form["name"]
    #if lei: 
    #    results = session.query(LegalEntity).filter(LegalEntity.lei == lei)
    #    name = ""
    #elif name:
    #    results = session.query(LegalEntity).filter( 
    #                           LegalEntity.legal_name.ilike('%'+name+'%'))
    lei, name, results = query_lei()
    return(render_template("search.html", lei_arg=lei, name_arg=name,
                            results_arg=results))
