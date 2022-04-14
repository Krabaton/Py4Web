from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    storage_size = db.Column(db.Integer, default=0)
    storage_limit = db.Column(db.Integer, default=1e+7)
    token_cookie = db.Column(db.String(254), nullable=True, default=None)
    pictures = relationship("Picture", back_populates='user')

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email})"


class Picture(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(350), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", cascade="all, delete", back_populates='pictures')

    def __repr__(self):
        return f"Picture({self.id}, {self.path}, {self.size})"