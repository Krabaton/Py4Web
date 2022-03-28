from sqlalchemy.orm import sessionmaker, joinedload
from connect_db import engine
from tables import Cats, Owners

DBSession = sessionmaker(bind=engine)
session = DBSession()


def query_cats():
    cats = session.query(Cats).order_by(Cats.age.desc()).all()
    for cat in cats:
        print(cat.id, cat.name, cat.age)


def get_cat_by_id(_id):
    cat = session.query(Cats).filter_by(id=_id).one()
    print(cat.id, cat.name, cat.age)


def get_owners_with_cat():
    owners = session.query(Owners).options(joinedload(Owners.cat)).order_by(Owners.email.desc()).all()
    for owner in owners:
        print(owner.id, owner.email, owner.cat.id, owner.cat.name, owner.cat.age)


if __name__ == '__main__':
    query_cats()
    get_cat_by_id(6)
    get_owners_with_cat()
