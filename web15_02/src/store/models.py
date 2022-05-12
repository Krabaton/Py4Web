from gino.ext.starlette import Gino
from src.config import config

db = Gino(
    user=config['postgres']['db_user'],
    password=config['postgres']['db_password'],
    host=config['postgres']['db_host'],
    port=config['postgres']['db_port'],
    database=config['postgres']['db_database'],
)


class DbNotes(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String)
    content = db.Column(db.String)


class DbUser(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
