import os
import sys
import requests
from io import BytesIO
 
# Экземпляры загруженных плагинов
Plugins = []
Query = ''

default_params = {'method':'GET','page':1}

 
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

def search(num):
    print(num, Plugins)
    p = Plugins[num]
    print('started',p)
    """
    params = {'method':'GET','page':1}
    #import pdb; pdb.set_trace()
    r = http(p.request(Query,params))
    return p.response(r)"""

def LoadPlugins(destdir='plugins'):
    ss = [ f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f)) ]
    sys.path.insert( 0, destdir) # Добавляем папку плагинов в $PATH, чтобы __import__ мог их загрузить
 
    for s in ss:
        print('Found plugin', s)
        p = __import__(s.split('.')[0])
        Plugins.append(p)      

    print(Plugins)
    return
 