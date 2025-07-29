from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, default='')

    favorites = db.relationship('Favorite', backref='user', cascade="all, delete")

    @classmethod
    def register(cls, username, password):
        hashed = bcrypt.generate_password_hash(password).decode('utf8')
        return cls(username=username, password=hashed)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    meal_id = db.Column(db.String, nullable=False)  # MealDB meal ID
    meal_name = db.Column(db.String, nullable=False)
    meal_image = db.Column(db.String)

    notes = db.Column(db.Text)
    video_url = db.Column(db.Text)


def connect_db(app):
    db.app = app
    db.init_app(app)