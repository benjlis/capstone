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
from urllib2 import Request, urlopen, URLError, HTTPError
import zipfile
import leiquery.parse

GLEIF_DATE = os.environ.get("GLEIF_DATE", datetime.date.today().strftime("%Y%m%d"))
GLEIF_ZIP = GLEIF_DATE + '-GLEIF-concatenated-file.zip'
GLEIF_XML = GLEIF_DATE + '-GLEIF-concatenated.xml'
GLEIF_CSV = GLEIF_DATE + '-GLEIF-concatenated.csv'
GLEIF_URL = 'https://www.gleif.org/lei-files/' + GLEIF_DATE + '/GLEIF/' + GLEIF_ZIP
GLEIF_DOWNLOAD_DIR  = os.environ.get("GLEIF_DOWNLOAD_DIR", "gleif_downloads/")
GLEIF_DOWNLOAD_ZIP = GLEIF_DOWNLOAD_DIR + GLEIF_ZIP
GLEIF_DOWNLOAD_XML = GLEIF_DOWNLOAD_DIR + GLEIF_XML
GLEIF_DOWNLOAD_CSV = GLEIF_DOWNLOAD_DIR + GLEIF_CSV

@manager.command
def download_gleif():
    """Download GLEIF file with today's date embedded in it"""
    print 'LEI Smart GLEIF Download'
    print 'starting at ' + str(datetime.datetime.now())

    # download and unzip today's file
    print 'downloading ' + GLEIF_URL
    try:
        t = urlopen(GLEIF_URL)
        output = open(GLEIF_DOWNLOAD_ZIP,'wb')
        output.write(t.read())
        output.close()
    except HTTPError as e:
        print 'The GLEIF server couldn\'t fulfill the request.'
        print 'HTTP Error code: ', e.code
        return 1
    except URLError as e:
        print 'Failed to reach the GLEIF server.'
        print 'Reason: ', e.reason
        return 1
        
    print 'unzipping'
    with zipfile.ZipFile(GLEIF_DOWNLOAD_ZIP, 'r') as gleif_zip:
		gleif_zip.extractall(GLEIF_DOWNLOAD_DIR) 

    # to-dos: 
    # (1) just keep one week of zip files around; 
    # (2) consolidated file is from today - maybe the best is to rm or mv
    # (3) better file listing
    print os.listdir(GLEIF_DOWNLOAD_DIR)        
    print 'completed at ' +  str(datetime.datetime.now())

@manager.command
def xml2csv_gleif(xmlfile=GLEIF_DOWNLOAD_XML, csvfile=GLEIF_DOWNLOAD_CSV):
    """Converts the GLEIF XML download into a CSV"""
    print 'LEI Smart GLEIF XML to CSV conversion'
    print 'starting at ' + str(datetime.datetime.now())
    # 
    leiquery.parse.process_gleif(xmlfile, csvfile)
    #
    print os.listdir(GLEIF_DOWNLOAD_DIR)
    print 'completed at ' + str(datetime.datetime.now())

@manager.command
def process_gleif(file=GLEIF_DOWNLOAD_XML):
    """Parses and loads GLEIF data"""
    print "will process this file: " + file
    
if __name__ == "__main__":
    manager.run()