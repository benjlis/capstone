import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base, engine

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
    created = Column
    
class LegalEntity(Base):
    __tablename__ = "legal_entities"
    
    lei = Column(String(20), primary_key=True)
    legal_name = Column(String(500), nullable=False)
    legal_address_line1 = Column(String(500)) # nullable=False, generates error as of 20151109
    legal_address_line2 = Column(String(500))
    legal_address_line3 = Column(String(500))
    legal_address_line4 = Column(String(500))
    legal_address_city = Column(String(500), nullable=False)
    legal_address_region = Column(String(6))
    legal_address_country = Column(String(2), nullable=False)
    legal_address_postal_code = Column(String(500))
    hq_address_line1 = Column(String(500)) # nullable=False error, see above
    hq_address_line2 = Column(String(500))
    hq_address_line3 = Column(String(500))
    hq_address_line4 = Column(String(500))
    hq_address_city = Column(String(500), nullable=False)
    hq_address_region = Column(String(6))
    hq_address_country = Column(String(2), nullable=False)
    hq_address_postal_code = Column(String(500))
    business_registry = Column(String(500))
    business_registry_id = Column(String(500))
    legal_jurisdiction = Column(String(6))
    legal_form = Column(String(500))
    entity_status = Column(String(8), nullable=False)
    entity_expiration_date = Column(DateTime)
    entity_expiration_reason = Column(String(20))
    successor_lei = Column(String(20))
    initial_registration_date = Column(DateTime, nullable=False)
    last_update_date = Column(DateTime, nullable=False)
    registration_status = Column(String(20), nullable=False)
    next_renewal_date = Column(DateTime, nullable=False)
    managing_lou = Column(String(20), nullable=False)
    validation_status = Column(String(24))

Base.metadata.create_all(engine)    