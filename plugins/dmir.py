from lxml import html
from urllib.parse import quote
import sys
import traceback

name='Dmir'
base_url = 'http://www.dmir.ru'
search_url = '/search/result.aspx?keywords={query}&pagesize=20&sort=Date&direction=Descending&st=table'

def request(query, params, engine):
    params['url'] = base_url + search_url.format(query=quote(query))
    params['method'] = 'GET'
    params['page'] = 1
    params['engine'] = engine
    return params

def parse(resp):
    dom = html.fromstring(resp)
    results = []

    for result in dom.xpath('//ul[@class="result-list"]/li[not(contains(@class,"noprint"))]'):   
        try:
            res = { 'url': ''.join(result.xpath('./a/@href')),
                    'title': ''.join(result.xpath('.//a[@class="announcementlink"]/text()')).strip(),
                    'content': ' '.join(result.xpath('./div[@class="result-body"]/p/text()')).strip(),
                    'photo': ''.join(result.xpath('./a/img/@src')),
                    'price': ''.join(result.xpath('.//span[@class="price"]/b/text()'))+' РУБ.',
                    'from':name }
            if res['photo'][0:2]=='//':
                res['photo'] = 'http:' + res['photo']
            else:
                res['photo'] = base_url + res['photo']
        except Exception as e:
            traceback.print_exc()
            continue
        results.append(res)
    return results
