from fastapi import FastAPI, HTTPException
from schemas import User, Message
import db.models as models
import db.database as database
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime


app = FastAPI()

# Initialization of database
models.Base.metadata.create_all(bind=database.engine)

def connect_to_db():
    conn = database.SessionLocal()
    try:
        yield conn
    finally:
        conn.close()

@app.get("/")
def home():
    return "Welcome to messaging app"

@app.get("/users")
async def getUsers(conn : Session = Depends(connect_to_db)):
    users = conn.query(models.User).all()
    return users

@app.get("/users/{user_id}")
async def getUser(user_id: int, conn : Session = Depends(connect_to_db)):
    user = conn.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return user
    else:
        raise_not_found_exception(user_id)

@app.post("/users")
async def addUser(user: User, conn : Session = Depends(connect_to_db)):
    myuser = models.User(username=user.name, email=user.email, mobile=user.mobile, birthdate=datetime.strptime(user.birthdate, '%d/%m/%Y').date(), password=user.password)
    conn.add(myuser)
    conn.commit()
    conn.refresh(myuser)
    return myuser

@app.put("/users/{id}")
async def updateUser(id: int, user: User, conn : Session = Depends(connect_to_db)):
    myuser = conn.query(models.User).filter(models.User.id == id).first()
    if myuser:
        result = conn.query(models.User).filter(models.User.id == id).update({
            "username": user.name,
            "email": user.email,
            "mobile": user.mobile,
            "birthdate": datetime.strptime(user.birthdate, "%d/%m/%Y").date(),
            "password": user.password

        })
        conn.commit()
        conn.refresh(myuser)
        return result
    
    else:
        raise_not_found_exception(id)

@app.delete("/users/{user_id}")
async def deleteUser(user_id: int, conn: Session = Depends(connect_to_db)):
    myuser = conn.query(models.User).filter(models.User.id == user_id).first()
    if myuser:
        conn.query(models.User).filter(models.User.id == user_id).delete()
        conn.commit()
        return "User deleted successfully"
    else:
        raise_not_found_exception(user_id)
    
@app.get("/messages")
async def get_all_messages(conn : Session = Depends(connect_to_db)):
    messages = conn.query(models.Message).all()
    return messages

@app.post("/messages")
async def add_message(message: Message, conn : Session = Depends(connect_to_db)):
    sender = conn.query(models.User).filter(models.User.id == message.sender).first()
    receiver = conn.query(models.User).filter(models.User.id == message.receiver).first()
    if sender and receiver:
        my_message = models.Message(message= message.message, date= datetime.strptime(message.date, '%d/%m/%Y').date(), sender=message.sender, receiver=message.receiver)
        conn.add(my_message)
        conn.commit()
        conn.refresh(my_message)
        return my_message
    else:
        return 

# @app.get("/messages/{user_id}")
# async def get_user_messages(user_id: int, skip: int = 0, limit: int = 10):
#     return messages[user_id][skip: skip+limit]

# @app.post("/messages/{user_id}")
# async def add_user_message(user_id: int, message: Message):
#     if user_id in messages:
#         try:
#             messages[user_id].append(message)
#             return user_id
#         except:
#             HTTPException(status_code=500, detail="Something went wrong!!!")
#     else:
#         return HTTPException(status_code=404, detail="User not found")

# raise item not found exception
def raise_not_found_exception(user_id: int):
    error_str: str = "User with id = " + str(user_id) + " not found"
    raise HTTPException(status_code=404, detail=error_str)

    