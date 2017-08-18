from bottle import *
import plugin
import utils
import sqlite3

plugin.LoadPlugins()

@get('/')
def search_handler():
    vars = {}
    vars['results']=[]

    #import pdb; pdb.set_trace()    
    vars['q'] = request.query.getunicode('q')
    if vars['q']:
        print('query ', vars['q'])

        cnt = len(plugin.Plugins)
        results_thread = [None] * cnt
        threads = [None] * cnt
        for i in range(cnt):
            params = plugin.Plugins[i].request(vars['q'],plugin.default_params(),plugin.Plugins[i])
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

    return template('index.html', vars)

@get('/list')
def list_query():
    connection=sqlite3.connect('.queries.db')
    connection.row_factory = sqlite3.Row
    
    return template('index.html', vars)


if __name__ == "__main__":    
    run(host='localhost', port=8080, debug=True)  
else:
    #app=application=default_app()
    app = application = default_app()
