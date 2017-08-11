from lxml import html
import sys
from urllib.parse import quote
import re

name='Dorus'

base_url = 'http://www.dorus.ru'
search_url = '/search.html?query={query}&city=34'

def clean_html(text):
    return re.sub('<[^<]+?>', '', text)

def request(query, params,engine):
    params['url'] = base_url + search_url.format(query=quote(query.encode('windows-1251')))
    params['method'] = 'GET'
    params['page'] = 1
    params['engine'] = engine
    return params

def parse(resp):
    dom = html.fromstring(resp)
    results = []

    for result in dom.xpath('//div[@class="onepost"]'):
        try:
            res = {'url': result.xpath('.//a/@href')[0],
                   'title': ''.join(result.xpath('.//a/text()')).strip(),
                   'content': clean_html(''.join(result.xpath('.//text()')).strip()),
                   'photo':'',
                   'name':name
                    }
        except:
            print(sys.exc_info())
            continue
        results.append(res)
    return results
