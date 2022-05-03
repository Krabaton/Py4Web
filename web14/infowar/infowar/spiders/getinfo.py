import re
from datetime import datetime

import scrapy


class GetinfoSpider(scrapy.Spider):
    name = 'getinfo'
    allowed_domains = ['index.minfin.com.ua']
    start_urls = ['https://index.minfin.com.ua/ua/russian-invading/casualties/',
                  'https://index.minfin.com.ua/ua/russian-invading/casualties/month.php?month=2022-03',
                  'https://index.minfin.com.ua/ua/russian-invading/casualties/month.php?month=2022-02']

    def parse(self, response):
        element_dict = {}
        for element in response.xpath('/html//ul[@class="see-also"]/li[@class="gold"]'):
            date = element.xpath('span/text()').get()
            try:
                date = datetime.strptime(date, '%d.%m.%Y').isoformat()
            except ValueError:
                continue

            element_dict.update({'date': date})
            losses = element.xpath('div[@class="casualties"]/div/ul/li')
            for l in losses:
                f = l.css('*::text').extract()
                field = ' '.join(f)
                name, count = field.split('—')
                name = re.sub('\xa0', '', name)
                name = re.sub('  ', ' ', name)
                name = name.strip()
                count = re.search(r'\d+', count).group()
                element_dict.update(({name: int(count)}))
            yield element_dict
