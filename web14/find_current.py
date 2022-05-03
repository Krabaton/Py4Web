import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

html_doc = requests.get('https://index.minfin.com.ua/ua/russian-invading/casualties/')
soup = BeautifulSoup(html_doc.content, 'html.parser')
info = soup.select('ul[class=see-also] li[class=gold]')

date = info[0].find('span', attrs={'class': 'black'}, text='02.05.2022').text
print(date)
losses = info[0].find('span', attrs={'class': 'black'}, text='02.05.2022').parent.find('div', attrs={'class': 'casualties'})
print(losses)