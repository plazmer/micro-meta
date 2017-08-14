from lxml import html
from urllib.parse import quote
import sys


name='Avito'
base_url = 'https://avito.ru'
search_url = '/rossiya?user=1&bt=1&q={query}&s=2'

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

    for result in dom.xpath('//div[contains(@class,"js-catalog_before-ads")]/div[contains(@class,"item_table")]'):
        try:
            res = {'url': base_url+result.xpath('.//a[@class="item-description-title-link"]/@href')[0],
                   'title': ''.join(result.xpath('.//a[@class="item-description-title-link"]/text()')).strip(),
                   'content': ' '.join(result.xpath('.//div[@class="data"]/p/text()')).strip(),
                   'photo':'https:'+result.xpath('.//div[@class="b-photo"]/a/img/@src')[0],
                   'price': ''.join(result.xpath('.//div[@class="about"]/text()')).strip(),
                   'from':name
                    }
        except Exception as e:
            print(sys.exc_info())
            continue
        results.append(res)
    return results
