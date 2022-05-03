from connect_to_db import db
from bson.objectid import ObjectId
from dateutil import parser
from datetime import datetime, timedelta


record = db.losses.find_one({'_id': ObjectId('62717462eb866a19c00ee335')})
date = record['date']
last_date = parser.parse(date)
now_date = datetime.now()
period = now_date - last_date

find_list = []

for _d in range(1, period.days + 1):
    next_date = last_date + timedelta(days=_d)
    find_list.append(datetime.strftime(next_date, '%d.%m.%Y'))

print(find_list)
