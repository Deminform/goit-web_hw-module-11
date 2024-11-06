import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("USER")
password = os.getenv("PASSWORD")
dbname = os.getenv("DBNAME")
host = os.getenv("HOST")
port = os.getenv("PORT")

class Config:
    DB_URL = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}'

db_config = Config