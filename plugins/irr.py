from lxml import html
from urllib.parse import quote
import sys


name='IRR'
base_url = 'http://russia.irr.ru'
search_url = '/searchads/search/keywords={query}/sort/date_sort:desc/'

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

    for result in dom.xpath('//div[@class="listing__itemInner"]'):
        try:
            res = { 'url': ''.join(result.xpath('.//a/@href')),
                    'title': ''.join(result.xpath('.//a/div/text()')),
                    'content': ', '.join(result.xpath('.//div[contains(@class,"listing__itemPrice")]/text()')).strip(),
                    'photo': ''.join(result.xpath('.//img/@data-src')),
                    'name':name }
        except Exception as e:
            print(sys.exc_info())
            continue
        results.append(res)
    return results
