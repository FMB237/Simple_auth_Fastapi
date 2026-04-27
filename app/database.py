# Let add our database config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker


DATABASE_URL="sqlite:///user.db"

engine =create_engine(DATABASE_URL,connect_args={
    "check_same_thread":False
})

SessionLocal=sessionmaker(autoflush=False,bind=engine,autocommit=False)

Base = declarative_base()