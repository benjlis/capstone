import os

from flask.ext.script import Manager
from leiquery import app
from leiquery.database import session

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
from getpass import getpass
from werkzeug.security import generate_password_hash
from leiquery.models import User

@manager.command
def adduser():
    
    username = ""
    while username == "":
        username = raw_input("Enter username: ")
        if session.query(User).filter_by(username=username).first():
            print "User with that username already exists. Try another."
            username = ""
    
    email = ""
    while email == "":
        email = raw_input("Enter email (required):")
        
    password = ""
    password2 = ""
    while not (password and password2) or password != password2:
        password = getpass("Enter password:")
        password2 = getpass("Re-enter password:")
        
    firstname = raw_input("Enter firstname:") 
    lastname = raw_input("Enter lastname:")
    company = raw_input("Enter company: ")
    
    user = User(username=username, email=email, password=generate_password_hash(password), 
        firstname=firstname, lastname=lastname, company=company)
    session.add(user)
    session.commit()
    
if __name__ == "__main__":
    manager.run()