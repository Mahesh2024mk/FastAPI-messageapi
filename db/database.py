from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5432/messagedb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base: DeclarativeMeta = declarative_base()

