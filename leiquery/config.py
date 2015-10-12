import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI="postgresql://ubuntu:thinkful@localhost:5432/lei"
    DEBUG=True
    SECRET_KEY=os.environ.get("LEIQUERY_SECRET_KEY", "")
    