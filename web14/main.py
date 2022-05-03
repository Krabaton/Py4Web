import requests
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup

start_urls = ['https://index.minfin.com.ua/ua/russian-invading/casualties/',
              'https://index.minfin.com.ua/ua/russian-invading/casualties/month.php?month=2022-03',
              'https://index.minfin.com.ua/ua/russian-invading/casualties/month.php?month=2022-02']

data = []

for url in start_urls:
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    content = soup.select('ul[class=see-also] li[class=gold]')

    for element in content:
        element_dict = {}
        date = element.find('span', attrs={'class': 'black'}).text
        try:
            date = datetime.strptime(date, '%d.%m.%Y').isoformat()
        except ValueError:
            continue

        element_dict.update({'date': date})
        losses = element.find('div', attrs={'class': 'casualties'})
        if losses:
            losses = losses.find('div').find('ul')
            for l in losses:
                name, count = l.text.split('—')
                name = re.sub('\xa0', '', name)
                count = re.search(r'\d+', count).group()
                element_dict.update(({name: count}))
        data.append(element_dict)

for el in data:
    print(el)

with open('bsdata.json', "w", encoding='utf-8') as fh:
    json.dump(data, fh, ensure_ascii=False)