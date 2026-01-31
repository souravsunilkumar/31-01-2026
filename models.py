from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    email = Column(String, nullable = False)
    message = Column(String, nullable = False)