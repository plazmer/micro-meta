import model

if __name__ == "__main__":
    #import cProfile, pstats, io
    #pr = cProfile.Profile()
    #pr.enable()

    model.checkDB()    
    q = model.getNextQuery()
    if not q:
        model.loadQuery()
        q = model.getNextQuery() 
    print('query: %s'%q)
    model.search(q)

    #pr.disable()
    #s = io.StringIO()
    #sortby = 'cumulative'
    #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)B
    #ps.print_stats()
    #print(s.getvalue())