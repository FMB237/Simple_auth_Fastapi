from database import Base
from sqlalchemy import Column,String,Integer

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,unique=True,index=True)
    username = Column(String,unique=True)
    email = Column(String,index=True,unique=True)
    password = Column(String,index=True)
