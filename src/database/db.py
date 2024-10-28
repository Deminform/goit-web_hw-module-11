from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("USER")
password = os.getenv("PASSWORD")
dbname = os.getenv("DBNAME")
host = os.getenv("HOST")
port = os.getenv("PORT")

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'


