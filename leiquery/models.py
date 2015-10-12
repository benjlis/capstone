import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base, engine

from flask.ext.login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=True, nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(128), nullable=False)
    firstname = Column(String(32)) 
    lastname = Column(String(32))
    company = Column(String(32))
    created = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

Base.metadata.create_all(engine)    