import os
import sys
import requests
from io import BytesIO
 
# Экземпляры загруженных плагинов
Plugins = []
 
def http( params ):    
    headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    if params.get('method')=='GET':
        r = requests.get(params['url'])
    else:
        r = requests.post(params['url'],data=params.get('post'))
    encoding = r.headers.get('Content-Type').split('=')[-1]    
    return r.content.decode(encoding)

def search(query):
    for p in Plugins:
        params = {'method':'GET','page':1}
        #import pdb; pdb.set_trace()
        r = http(p.request(query,params))
        for item in p.response(r):
            yield item

def LoadPlugins(destdir='plugins'):
    ss = [ f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f)) ]
    sys.path.insert( 0, destdir) # Добавляем папку плагинов в $PATH, чтобы __import__ мог их загрузить
 
    for s in ss:
        print('Found plugin', s)
        p = __import__(s.split('.')[0])
        Plugins.append(p)      

    print(Plugins)
    return
 
if __name__ == "__main__":
    query = 'холодильник'
    LoadPlugins()
    print(Plugins)
    p = Plugins[0]
    params = {'method':'GET','page':1}
    req = p.request(query,params)
    print(req)
    r = http(req)
    print(p.response(r))
