from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import Session, declarative_base

engine = create_engine('sqlite:///db.sqlite')
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(100))

class Save_Game(Base):
    __tablename__ = 'save_game'

Base.metadata.create_all(engine)