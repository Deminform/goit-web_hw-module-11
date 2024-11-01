import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("USER")
password = os.getenv("PASSWORD")
dbname = os.getenv("DBNAME")
host = os.getenv("HOST")
port = os.getenv("PORT")

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
