import sqlite3
import plugin
import utils
import timeit
from log import logger

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
        logger.debug('check table %s result %s: '%(table, checkTable(table)))
        if not checkTable(table):
            logger.debug('creating table %s'%table)
            cursor.execute(tables[table])
    connection.commit()

def loadQuery(): #utility for test load
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

def getQuerys():
    result = []
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM query ORDER BY q')
    for res in cursor.fetchall():
        result.append(dict(res))
    return result

def getResults(query, limit=30):
    result = []
    cursor = connection.cursor()
    cursor.execute('SELECT *, datetime(added, "localtime") as added_local FROM results where query=? ORDER BY added desc LIMIT ?',(query,limit, ))
    for res in cursor.fetchall():
        result.append(dict(res))
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

def search(q):
    cnt = 0
    start_time_full = timeit.default_timer()
    for p in plugin.Plugins:
        start_time = timeit.default_timer()
        params = p.request(q,plugin.default_params(),None)
        page = utils.http(params)
        elapsed = timeit.default_timer() - start_time
        logger.debug('%s - download %.2f s'%(p.name,elapsed))
        
        start_time = timeit.default_timer()
        results = p.parse(page)
        elapsed = timeit.default_timer() - start_time
        logger.debug('%s - parse %.2f s'%(p.name,elapsed))

        start_time = timeit.default_timer()
        for r in results:
            r['price'] = utils.normalizePrice(r['price'])
            if saveResult(r['url'], r['title'], r['content'], r['photo'], r['price'], p.name, q):
                cnt+=1
        elapsed = timeit.default_timer() - start_time
        logger.debug('%s - save %.2f s'%(p.name,elapsed))

        start_time = timeit.default_timer()
        connection.commit() #saveResult not commits for speed, do not remove
        elapsed = timeit.default_timer() - start_time
        logger.debug('%s - commit %.2f s'%(p.name,elapsed))

    elapsed = timeit.default_timer() - start_time_full
    logger.debug('query: %s \t\t added: %s \t\tin %.2f s'%(q,cnt,elapsed))


connection=sqlite3.connect('.queries.db')
connection.row_factory = sqlite3.Row
plugin.LoadPlugins()
checkDB()