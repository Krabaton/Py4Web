import requests
import re
from datetime import datetime, timedelta
from dateutil import parser
import json
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import TypeLosses, Losses

# Create your views here.
from .mongodb.connect import db


def main(request):
    results = Losses.objects.raw('''
    SELECT itl.id, itl.name, il.total, il.updated_at
    FROM infoboard_losses as il
    JOIN infoboard_typelosses as itl ON itl.id = il.lose_name_id
    ''')
    return render(request, 'infoboard/index.html', {'results': results})


def create_type(request):
    message = None
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        tl = TypeLosses(name=name, description=description)
        tl.save()
        message = f'Створено тип втрат {name}. Опис: {description}'
    return render(request, 'infoboard/info.html', {'message': message})


def get_losses_actual(request):
    now_date = datetime.strftime(datetime.now(), '%d.%m.%Y')
    html_doc = requests.get('https://index.minfin.com.ua/ua/russian-invading/casualties/')
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    info = soup.select_one('ul[class=see-also] > li[class=gold]')
    el_dict = {}

    losses = info.find('span', attrs={'class': 'black'}, text=now_date).parent.find('div', attrs={
        'class': 'casualties'}).find('div').find('ul')

    for l in losses:
        name, count = l.text.split('—')
        name = re.sub('\xa0', '', name)
        count = re.search(r'\d+', count).group()
        el_dict.update(({name: count}))

    Losses.objects.all().delete()
    for key, value in el_dict.items():
        name = TypeLosses.objects.get(name=key)
        record = Losses(lose_name=name, total=value)
        record.save()

    return redirect('main')


def losses_list(request):
    results = db.losses.find(sort=[('date', -1)])
    # [('date', [(Tanks, 123), (), ...]), (...)]
    return render(request, 'infoboard/losses-list.html', {'results': transform_data_for_losses_list(results)})


def transform_data_for_losses_list(data):
    result = []
    for el in data:
        date = datetime.strftime(parser.parse(el['date']), '%d.%m.%Y')
        list_tuple = []
        for key, value in el.items():
            if key != '_id' and key != 'date':
                list_tuple.append((key, value))
        result.append((date, list_tuple))
    return result


def get_chart(request, id):
    namelose = str(TypeLosses.objects.filter(pk=id).get())
    print(namelose)
    return render(request, 'infoboard/chart.html', {'namelose': namelose})


def get_chart_info(request, id):
    namelose = str(TypeLosses.objects.filter(pk=id).get())
    date_start = datetime(2022, 2, 24).isoformat()
    date_finish = datetime.now().isoformat()
    # date_finish = datetime(2022, 4, 30).isoformat()
    records = db.losses.find({"$and": [{"date": {"$gte": date_start}}, {"date": {"$lte": date_finish}}]},
                             {'date': 1, namelose: 1, '_id': 0}, sort=[('date', 1)])
    result = json.dumps(list(records))
    return HttpResponse(result, content_type='application/json')


def sync_losses(request):
    record = db.losses.find_one(sort=[('date', -1)])
    date = record['date']
    last_date = parser.parse(date)
    now_date = datetime.now()
    period = now_date - last_date

    find_list = []

    for _d in range(1, period.days + 1):
        next_date = last_date + timedelta(days=_d)
        find_list.append(datetime.strftime(next_date, '%d.%m.%Y'))

    print(find_list)
    html_doc = requests.get('https://index.minfin.com.ua/ua/russian-invading/casualties/')
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    info = soup.select_one('ul[class=see-also] li[class=gold]')

    data_to_insert = []
    for current_date in find_list:
        el_dict = {}
        el_dict.update({'date': datetime.strptime(current_date, '%d.%m.%Y').isoformat()})
        losses = info.find('span', attrs={'class': 'black'}, text=current_date).parent.find('div', attrs={
            'class': 'casualties'}).find('div').find('ul')
        for l in losses:
            name, count = l.text.split('—')
            name = re.sub('\xa0', '', name)
            count = re.search(r'\d+', count).group()
            el_dict.update(({name: int(count)}))
        print(el_dict)
        data_to_insert.append(el_dict)
    print(data_to_insert)
    if len(data_to_insert) != 0:
        r = db.losses.insert_many(data_to_insert)
        print(r.inserted_ids)
    return redirect('losseslist')