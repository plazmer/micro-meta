from lxml import html
from urllib.parse import quote
import sys
import traceback

name='UBU'
base_url = 'https://www.ubu.ru'
search_url = '/ru?str={query}&show=1'

def request(query, params, engine):
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
                    'photo': ''.join(result.xpath('./td[2]//img[@itemprop="image"][1]/@src')),
                    'price':''.join(result.xpath('.//meta[@itemprop="price"]/@content'))+' РУБ.',
                    'from':name }
            if res['photo'][0:2]=='//':
                res['photo'] = 'https:' + res['photo']
            else:
                res['photo'] = base_url + res['photo']
        except Exception as e:
            traceback.print_exc()
            continue
        results.append(res)
    return results
