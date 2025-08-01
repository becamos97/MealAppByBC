import pytest
from app import app, flask_app, db
from models import User

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mealapp_test'
    flask_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for form testing
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_user(app):
    with app.app_context():
        user = User.register("testuser", "password")
        db.session.add(user)
        db.session.commit()
        return User.query.filter_by(username="testuser").first()