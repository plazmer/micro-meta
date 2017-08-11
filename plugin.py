import os
import sys
import requests
from io import BytesIO
 
Plugins = []

debug = True

def default_params():
    return {'method':'GET','page':1}
 
def http( params, results={}, index=0 ):
    headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    if params.get('method')=='GET':
        r = requests.get(params['url'],headers=headers)
    else:
        r = requests.post(params['url'],data=params.get('post'),headers=headers)

    tmp = r.headers.get('Content-Type').split('=')
    encoding='utf-8'
    if len(tmp)>1:
        encoding=tmp[-1]
    page = r.content.decode(encoding)
    params['page'] = page

    results[index] = params #return to thread
    return params

def LoadPlugins(destdir='plugins'):
    ss = [ f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f)) and f!='__init__.py' ]
    sys.path.insert( 0, destdir) 
 
    for s in ss:
        print('Found plugin', s)
        p = __import__(s.split('.')[0])
        Plugins.append(p)      

    print(Plugins)
 
