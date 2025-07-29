from app import app
from models import db, User, Favorite
import pytest

@pytest.fixture
def sample_user():
    user = User.register("testuser", "password")
    db.session.add(user)
    db.session.commit()
    return User.query.filter_by(username="testuser").first()

def test_user_creation(sample_user):
    assert sample_user.username == "testuser"
    assert sample_user.password.startswith("$2b$")