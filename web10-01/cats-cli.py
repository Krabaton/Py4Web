from pymongo import MongoClient
from bson.objectid import ObjectId
import argparse

client = MongoClient('mongodb://localhost:27017')
db = client.test

parser = argparse.ArgumentParser(description='Cats catalogue')

parser.add_argument('--action', '-a', help='Дія над котом: create, update, find, remove')
parser.add_argument('--id')
parser.add_argument('--name')
parser.add_argument('--age')
parser.add_argument('--features', nargs='+')

arguments = parser.parse_args()
my_vars = vars(arguments)

action = my_vars.get('action')
_id = my_vars.get('id')
name = my_vars.get('name')
age = my_vars.get('age')
features = my_vars.get('features')


def create(name, age, features):
    result = db.cats.insert_one(
        {
            "name": name,
            "age": age,
            "features": features,
        }
    )
    findById(result.inserted_id)


def findAll():
    result = db.cats.find({})
    # print(result.next())
    for el in result:
        print(el)


def findById(_id):
    result = db.cats.find_one({"_id": ObjectId(_id)})
    print(result)


def remove(_id):
    result = db.cats.delete_one({"_id": ObjectId(_id)})
    print('Delete success!')


def update(_id, name, age, features):
    db.cats.update_one(
        {"_id": ObjectId(_id)},
        {
            "$set": {
                "name": name,
                "age": age,
                "features": features
            }
        }
    )
    findById(_id)


def validate(*args) -> bool:
    for el in args:
        if el is None:
            return False
    return True


if __name__ == '__main__':
    if action == 'create':
        if validate(name, age, features):
            create(name, age, features)
        else:
            print('Вхідні дані не валідні')
    elif action == 'find':
        if validate(_id):
            findById(_id)
        else:
            print('Вхідні дані не валідні')
    elif action == 'findAll':
        findAll()
    elif action == 'remove':
        if validate(_id):
            remove(_id)
        else:
            print('Вхідні дані не валідні')
    elif action == 'update':
        if validate(_id, name, age, features):
            update(_id, name, age, features)
        else:
            print('Вхідні дані не валідні')
    else:
        print('Такої команди не існує')
