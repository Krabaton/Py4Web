from pymongo import MongoClient

client = MongoClient('mongodb+srv://goitlearn:567234@cluster0.smeju.mongodb.net/?retryWrites=true&w=majority')

db = client['infowar']

if __name__ == '__main__':
    result = db.losses.find(sort=[('date', -1)])
    for el in result:
        print(el)
