from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

db = client.test

result_many = db.cats.insert_many(
    [
        {
            "name": "Lama",
            "age": 2,
            "features": ["ходит в лоток", "не дает себя гладить", "серый"],
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["ходит в лоток", "дает себя гладить", "белый"],
        },
    ]
)