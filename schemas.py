from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    name: str
    email: str
    mobile: str
    birthdate: str
    password: str

class Message(BaseModel):
    message: str
    date: str
    sender: int
    receiver: int