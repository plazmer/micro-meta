from lxml import html
from urllib.parse import quote
import sys


name='doski'
base_url = 'http://www.doski.ru'
search_url = '/?cat=0&plc=1&src={query}&fl2=on'

def request(query, params, engine):
    print(type(query),query)
    params['url'] = base_url + search_url.format(query=quote(query.encode('windows-1251')))
    params['method'] = 'GET'
    params['page'] = 1
    params['engine'] = engine
    return params

def parse(resp):
    dom = html.fromstring(resp)
    results = []

    for result in dom.xpath('//table[@class="ml"]/tr'):
        try:
            res = { 'url': 'http:'+''.join(result.xpath('./td[@class="tdc"]/a/@href')),
                    'title': ''.join(result.xpath('.//a[@class="sbj"]/text()')),
                    'content': ''.join(result.xpath('.//td[2]/text()')).strip(),
                    'price': ''.join(result.xpath('.//td[3]//text()')).replace('Цена','').strip(),
                    'photo': 'http:'+''.join(result.xpath('./td[@class="tdc"]/a/img/@src')),
                    'from':name }
        except Exception as e:
            print(sys.exc_info())
            continue
        results.append(res)
    return results
