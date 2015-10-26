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
    
import datetime
import urllib2
import zipfile

GLEIF_DATE = os.environ.get("GLEIF_DATE", datetime.date.today().strftime("%Y%m%d"))
GLEIF_FILE = GLEIF_DATE + '-GLEIF-concatenated-file.zip'
GLEIF_URL = 'https://www.gleif.org/lei-files/' + GLEIF_DATE + '/GLEIF/' + GLEIF_FILE
GLEIF_DOWNLOAD_DIR  = os.environ.get("GLEIF_DOWNLOAD_DIR", "gleif_downloads/")
GLEIF_DOWNLOAD = GLEIF_DOWNLOAD_DIR + GLEIF_FILE

@manager.command
def download():
    """Downloads file with today's date embedded in it"""
    print 'LEI Smart GLEIF Download'
    print 'starting at ' + str(datetime.datetime.now())

    # download and unzip today's file
    print 'downloading ' + GLEIF_URL
    t = urllib2.urlopen(GLEIF_URL)
    output = open(GLEIF_DOWNLOAD,'wb')
    output.write(t.read())
    output.close()
    print 'unzipping'
    with zipfile.ZipFile(GLEIF_DOWNLOAD, 'r') as gleif_zip:
		gleif_zip.extractall(GLEIF_DOWNLOAD_DIR) 

    # to-dos: 
    # (1) just keep one week of zip files around; 
    # (2) consolidated file is from today - maybe the best is to rm or mv
    # (3) better file listing
    print os.listdir(GLEIF_DOWNLOAD_DIR)        
    print 'completed at ' +  str(datetime.datetime.now())
  
    
if __name__ == "__main__":
    manager.run()