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
    plugin.LoadPlugins()

    vars = {}
    vars['results']=[]
    
    print(plugin.Plugins)
    cnt = len(plugin.Plugins)

    #import pdb; pdb.set_trace()    
    vars['q'] = request.query.getunicode('q')
    if vars['q']:
        print('query ', vars['q'])

        results_thread = [None] * cnt
        threads = [None] * cnt
        for i in range(cnt):
            params = plugin.Plugins[i].request(vars['q'],plugin.default_params,plugin.Plugins[i])
            threads[i] = threading.Thread(target=plugin.http, args=(params, results_thread, i))
            threads[i].start()

        for i in range(cnt):
            threads[i].join()

        for results in results_thread:
            for result in results:
                vars['results'].append(result)

    return template('index.html', vars)

if __name__ == "__main__":
    run(host='localhost', port=8888, debug=True)
    