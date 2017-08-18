import os
import sys
 
Plugins = []

debug = True

def default_params():
    return {'method':'GET','page':1}

def LoadPlugins(destdir='plugins'):
    ss = [ f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f)) and f!='__init__.py' ]
    sys.path.insert( 0, destdir) 
 
    for s in ss:
        print('Found plugin', s)
        p = __import__(s.split('.')[0])
        Plugins.append(p)      

    print(Plugins)
 
