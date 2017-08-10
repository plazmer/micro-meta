from bottle import *
import plugin

#@route('<filepath:path>')
#def server_static(filepath):
#    return static_file(filepath, root='static')


def search_multi(q):
    results = []
    for result in plugin.search(vars['q']):
        results.append(result)



@get('/')
def search_handler():
    vars = {}
    vars['results']=[]
    print(plugin.Plugins)
    #import pdb; pdb.set_trace()    
    vars['q'] = request.query.getunicode('q')
    if vars['q']:
        print(vars['q'])
        plugin.Query = vars['q']

        
        

            
        for result in plugin.search(vars['q']):
            vars['results'].append(result)

    return template('index.html', vars)

#run(host='0.0.0.0', port=8888, debug=True)

if __name__ == "__main__":
    plugin.LoadPlugins()
    query = 'холодильник'
    requests = []
    for p in plugin.Plugins:
        requests.append(p.request(query,plugin.default_params,p))

    results = []
    pages = map(plugin.http,requests)
    for p in pages:
        results.append(p['engine'].parse(p['page']))
    print(results)
    #import pdb;pdb.set_trace()
    #pool = multiprocessing.Pool(len(plugin.Plugins))
    #print(pool)
    #threads_arr = list(range(len(plugin.Plugins)))
    #results = pool.map(plugin.search,threads_arr)
    #print(results)
    


