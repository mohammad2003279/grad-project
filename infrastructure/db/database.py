from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
engine = create_engine(DATABASE_URL) # type: ignore
DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
engine = create_engine(DATABASE_URL) # type: ignore

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
