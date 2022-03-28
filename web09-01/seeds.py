from random import randint

from sqlalchemy.orm import sessionmaker
from faker import Faker
from connect_db import engine
from tables import Cats, Owners

fake = Faker()

DBSession = sessionmaker(bind=engine)
session = DBSession()


def seed_data():
    for _ in range(7):
        name = fake.first_name()
        age = randint(1, 20)
        new_cat = Cats(name=name, age=age)
        session.add(new_cat)
        # session.commit()
        email = fake.email()
        owner = Owners(cat=new_cat, email=email)
        session.add(owner)
        session.commit()


if __name__ == '__main__':
    seed_data()
