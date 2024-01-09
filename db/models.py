from sqlalchemy import Column, Integer, String, Date
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=False)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    birthdate = Column(Date, nullable=True)
    password = Column(String)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=False)
    date = Column(Date)
    sender = Column(String, index=True)
    receiver = Column(String, index=True)
