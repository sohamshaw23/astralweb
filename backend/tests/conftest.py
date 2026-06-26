import os
import sys

# Force DATABASE_URL to use SQLite in-memory database before any other module imports it
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from unittest.mock import MagicMock
import sqlalchemy

# Wrap create_engine to dynamically strip pool arguments for SQLite
original_create_engine = sqlalchemy.create_engine

def mock_create_engine(url, *args, **kwargs):
    if url.startswith("sqlite"):
        kwargs.pop("pool_size", None)
        kwargs.pop("max_overflow", None)
    return original_create_engine(url, *args, **kwargs)

sqlalchemy.create_engine = mock_create_engine

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import DB and models to ensure schema creation works
from database.postgres import Base, engine, SessionLocal
from database.models import User, Satellite, DisasterEvent, Hotspot

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all tables in the SQLite test database once per test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Provide a transactional database session for unit tests, rolling back changes after each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def app():
    """Create and configure a Flask application instance for testing."""
    # Prevent scheduler from starting during Flask app tests
    os.environ["WERKZEUG_RUN_MAIN"] = "true"  # This flags Flask not to start background scheduler in create_app
    
    from app import create_app
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
    })
    return flask_app

@pytest.fixture
def client(app):
    """A Flask test client."""
    return app.test_client()
