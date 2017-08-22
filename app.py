from bottle import *
import plugin
import utils
import sqlite3
import model
from pprint import pprint

@get('/')
def search_handler():
    vars = {}

    vars['results']=[]
    query = request.query.getunicode('q')
    if query:
        print('query ', query)
        vars['q'] = query

        cnt = len(plugin.Plugins)
        results_thread = [None] * cnt
        threads = [None] * cnt
        for i in range(cnt):
            params = plugin.Plugins[i].request(query,plugin.default_params(),plugin.Plugins[i])
            threads[i] = threading.Thread(target=utils.threadHttp, args=(params, results_thread, i))
            threads[i].start()

        for i in range(cnt):
            threads[i].join()

        for results in results_thread:
            parsed = results['engine'].parse(results['page'])
            searched = results['url']
            for result in parsed:
                result['searched'] = searched
                vars['results'].append(result)        
    return template('results.html', vars)

@get('/list')
def list_query():
    vars = {}

    headers = model.getQuerys()
    vars['headers'] = headers

    vars['results'] = []
    for h in headers:
        vars['results'].append( {'id':h['id'], 'items': model.getResults(h['q']) } )
    return template('tabs.html', vars)


if __name__ == "__main__":    
    run(host='localhost', port=8080, debug=True, reloader=True)  
else:
    #app=application=default_app()
    app = application = default_app()
