from bottle import *
import plugin
from  time import time
import requests

def http( params ):    
    headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    if params.get('method')=='GET':
        r = requests.get(params['url'])
    else:
        r = requests.post(params['url'],data=params.get('post'))
    tmp = r.headers.get('Content-Type').split('=')
    encoding='utf-8'
    if len(tmp)>1:
        encoding=tmp[-1]
    params['page'] = r.content.decode(encoding)
    return params


def http_thread( params, result, index ):    
    headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    if params.get('method')=='GET':
        r = requests.get(params['url'])
    else:
        r = requests.post(params['url'],data=params.get('post'))
    tmp = r.headers.get('Content-Type').split('=')
    encoding='utf-8'
    if len(tmp)>1:
        encoding=tmp[-1]
    params['page'] = r.content.decode(encoding)
    result[index] = params
    

cnt = 100

if __name__ == "__main__":
    req = []
    for i in range(cnt):
        req.append({'method':'GET','page':1,'url':'http://remzalp.ru'})
    results = []
    start = time()
    pages = map(http, req)
    for p in pages:
        results.append(p['page'])
    end = time()    
    print('map', end - start)


    print("=============================")

    start = time()
    results_thread = [None] * cnt
    threads = [None] * cnt
    for i in range(cnt):
        threads[i] = threading.Thread(target=http_thread, args=(req[i], results_thread, i))
        threads[i].start()

    for i in range(cnt):
        threads[i].join()
    end = time()    
    print('thread',end - start)
    