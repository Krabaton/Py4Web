from src import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    storage_size = db.Column(db.Integer, default=0)
    storage_limit = db.Column(db.Integer, default=1e+7)

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email})"

