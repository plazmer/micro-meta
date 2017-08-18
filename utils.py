import os
import sys
import requests
import re
 
def http( params ):
    if not params.get('headers'):
        params['headers'] = {}
    params['headers']['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    if params.get('method')=='GET':
        r = requests.get(params['url'],headers=params['headers'])
    else:
        r = requests.post(params['url'],data=params.get('post'),headers=params['headers'])

    encoding='utf-8'
    tmp = r.headers.get('Content-Type').split('=')
    if len(tmp)>1:
        encoding=tmp[-1]

    page = r.content.decode(encoding)
    return page
    

def threadHttp(params, results={}, index=0):
    params['page'] = http(params)
    results[index] = params


def normalizePrice(price):
    p = re.compile('[^0-9\.,]')
    price = p.sub('',price).replace(',','.')
    if price=='':
        price = 0
    elif price[-1]=='.':
        price = price[:-1]
    return price

