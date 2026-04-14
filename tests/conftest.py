import pytest
from app import create_app
from app.extensions import db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app('testing')
    
    with app.app_context():
        from app.models.admin import Admin
        from app.models.announcement import Announcement
        from app.models.roadmap import Roadmap
        
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
