from bottle import *
import plugin
plugin.LoadPlugins()

#@route('<filepath:path>')
#def server_static(filepath):
#    return static_file(filepath, root='static')

@get('/')
def search():       
    vars = {}
    vars['results']=[]
    print(plugin.Plugins)
    #import pdb; pdb.set_trace()    
    vars['q'] = request.query.getunicode('q')
    if vars['q']:
        print(vars['q'])
            
        for result in plugin.search(vars['q']):
            vars['results'].append(result)

    return template('index.html', vars)

run(host='localhost', port=8888, debug=True)

