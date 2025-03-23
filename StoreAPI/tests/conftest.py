import os
import sys
import pytest
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from resources.database import db, init_app


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    test_db_uri = f'sqlite:///{db_path}'
    
    # Configure the app for testing
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': test_db_uri,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    
    # Initialize the database
    with flask_app.app_context():
        init_app(flask_app)
        db.create_all()
        
        # Add test data
        from tests.test_data import populate_test_data
        populate_test_data(db)
    
    # Return the app for testing
    yield flask_app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner() 