"""
Project Zenith
PostgreSQL Configuration v1.0.0
"""

import os

from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(

    "DATABASE_URL",

    "postgresql://postgres:password@localhost:5432/project_zenith"

)

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True,

    pool_size=10,

    max_overflow=20,

    echo=False

)

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)

Base = declarative_base()


# -----------------------------------------
# Database Session
# -----------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# -----------------------------------------
# Initialize Database
# -----------------------------------------

def init_database():

    Base.metadata.create_all(bind=engine)

    print("PostgreSQL Connected Successfully.")


# -----------------------------------------
# Database Health
# -----------------------------------------

def database_health():

    try:

        connection = engine.connect()

        connection.close()

        return {

            "database": "PostgreSQL",

            "status": "Connected"

        }

    except Exception as e:

        return {

            "database": "PostgreSQL",

            "status": "Disconnected",

            "error": str(e)

        }


# -----------------------------------------
# Test
# -----------------------------------------

if __name__ == "__main__":

    print(database_health())
