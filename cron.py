import sqlite3
import plugin
import utils
import sys

connection=sqlite3.connect('.queries.db')
connection.row_factory = sqlite3.Row
plugin.LoadPlugins()

def checkDB():
    def checkTable(table):
        cursor=connection.cursor()
        try:
            cursor.execute('SELECT * FROM %s LIMIT 1'%table)
            res=cursor.fetchall()
            result = True
        except:
            result = False
        return result

    tables = {}
    tables['query'] = 'CREATE TABLE query (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, q TEXT, last DATETIME)'
    tables['results'] = 'CREATE TABLE results (url TEXT, added DATETIME, title TEXT, content TEXT, photo TEXT, price REAL, engine TEXT, query TEXT)'

    cursor=connection.cursor()
    cursor.execute('PRAGMA encoding="UTF-8";')
    for table in tables.keys():
        print('check table %s: '%table, checkTable(table))
        if not checkTable(table):
            print('creating table %s'%table)
            cursor.execute(tables[table])
    connection.commit()

def loadQuery():
    cursor = connection.cursor()
    for row in open('.query.txt'):
        row = row.strip()
        cursor.execute('SELECT id FROM query WHERE q=?',(row,))
        res = cursor.fetchone()
        if not res:
            cursor.execute('INSERT INTO query (q, last) VALUES (?, 0)',(row,))
            connection.commit()

def addQuery(text, region='russia'):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO query (q, region, last) VALUES (?,?,?)',(text,region, 0))
    connection.commit()

def getNextQuery():
    result = None
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM query ORDER BY last LIMIT 1')
    res = cursor.fetchone()    
    if res:
        result = res['q']

        cursor.execute('UPDATE query SET last=datetime("now") WHERE id=?',(res['id'],))
        connection.commit()
        
    return result

def saveResult(url, title, content, photo, price, engine, query):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM results WHERE url=? AND query=?',(url,query,))
    res = cursor.fetchone()
    if not res:
        cursor.execute(
            'INSERT INTO results (url, title, content, photo, price, engine, query, added) VALUES (?,?,?,?,?,?,?,datetime("now"))',
            (url, title, content, photo, price, engine, query,))        
        result = True
    else:
        result = False
    return result


if __name__ == "__main__":
    #import cProfile, pstats, io
    #pr = cProfile.Profile()
    #pr.enable()

    checkDB()    
    q = getNextQuery()
    if not q:
        loadQuery()
        q = getNextQuery() 
    print('query: %s'%q)
    cnt = 0
    for p in plugin.Plugins:
        params = p.request(q,plugin.default_params(),None)
        page = utils.http(params)
        results = p.parse(page)
        for r in results:
            r['price'] = utils.normalizePrice(r['price'])
            if saveResult(r['url'], r['title'], r['content'], r['photo'], r['price'], p.name, q):
                cnt+=1
        connection.commit() #saveResult not commits for speed
    print('query: %s \t\t added: %s'%(q,cnt))

    #pr.disable()
    #s = io.StringIO()
    #sortby = 'cumulative'
    #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    #ps.print_stats()
    #print(s.getvalue())