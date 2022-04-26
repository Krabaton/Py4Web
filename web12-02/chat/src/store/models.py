from datetime import datetime
from gino import Gino

db = Gino()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    login = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())

    async def check_user(self, **kw):
        return await self.query.where()

    def __init__(self, **kw):
        super().__init__(**kw)
        self._messages = set()

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def add_message(self, message):
        self._messages.add(message)


class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    def __repr__(self) -> str:
        return self.message
