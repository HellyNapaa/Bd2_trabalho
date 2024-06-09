from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLAlchemy
DATABASE_URL = "postgresql+psycopg2://postgres:x4rov5um@localhost/northwind"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Psycopg2
import psycopg2

def get_psycopg_connection():
    return psycopg2.connect(
        dbname="northwind",
        user="postgres",
        password="x4rov5um",
        host="localhost"
    )
