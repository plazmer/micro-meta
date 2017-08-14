from lxml import html
from urllib.parse import quote
import sys

name='UBU'
base_url = 'https://www.ubu.ru'
search_url = '/ru?str={query}&show=1'

def request(query, params, engine):
    print(type(query),query)
    params['url'] = base_url + search_url.format(query=quote(query))
    params['method'] = 'GET'
    params['page'] = 1
    params['engine'] = engine
    return params

def parse(resp):
    dom = html.fromstring(resp)
    results = []

    for result in dom.xpath('//table[@class="ajax_container"]//tr'):
        try:
            res = { 'url': base_url+''.join(result.xpath('./td[3]//a/@href')),
                    'title': ''.join(result.xpath('./td[3]//a/h3/text()')),
                    'content': ''.join(result.xpath('./td[3]//div[@itemprop="description"]/text()')).strip() + ' ' + ' '.join(result.xpath('./td[3]//span[@class="name-town"]/text()')).strip(),
                    'photo': 'https:'+''.join(result.xpath('./td[2]//a/img/@src')),
                    'price':''.join(result.xpath('.//meta[@itemprop="price"]/@content'))+' РУБ.',
                    'from':name }
        except Exception as e:
            print(sys.exc_info())
            continue
        results.append(res)
    return results
