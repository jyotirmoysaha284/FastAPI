from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # Establish the POSTGRESQL Database Connection and loop until connection is Established
# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#                                 password='root', cursor_factory=RealDictCursor)         # RealDictCursor to return headers along with data
#         cursor = conn.cursor()
#         print("Databse connection established!!!")
#         break

#     except Exception as error:
#         print("Connection not established") 
#         print("Error ", error)
#         time.sleep(3)                   # Wait 3 secs before next try