from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from connect_db import engine

Base = declarative_base()


class Cats(Base):
    __tablename__ = 'cats'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)


class Owners(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    cat_id = Column(Integer, ForeignKey('cats.id'))
    cat = relationship(Cats)


Base.metadata.bind = engine
Base.metadata.create_all(engine)
