from lxml import html
from urllib.parse import quote
import sys
import traceback


name='Avito'
base_url = 'https://avito.ru'
search_url = '/rossiya?user=1&bt=1&q={query}&s=2'

def request(query, params, engine):
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
            res = {}
            res['url'] = base_url+result.xpath('.//a[@class="item-description-title-link"]/@href')[0]
            res['title'] = ''.join(result.xpath('.//a[@class="item-description-title-link"]/text()')).strip()
            res['content'] = ' '.join(result.xpath('.//div[@class="data"]/p/text()')).strip()
            res['photo'] = result.xpath('.//div[@class="b-photo"]/a/img[1]/@src')
            if len(res['photo'])>0:
                res['photo'] = 'https:'+res['photo'][0]
            else:
              res['photo'] = None
            res['price'] = ''.join(result.xpath('.//div[@class="about"]/text()')).strip()
            res['from'] = name
            print(res)
        except Exception as e:
            traceback.print_exc()
            continue
        results.append(res)
    return results
