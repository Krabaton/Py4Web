from datetime import datetime
from gino import Gino

db = Gino()


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.String(150), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._tags = set()

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def add_tag(self, tag):
        self._tags.add(tag)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    notes_id = db.Column(db.Integer, db.ForeignKey('notes.id', ondelete='cascade'))

    def __repr__(self) -> str:
        return self.name


