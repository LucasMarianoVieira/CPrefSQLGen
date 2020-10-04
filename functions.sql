CREATE OR REPLACE FUNCTION best_bnl( prefs text) 
RETURNS TABLE (like r) AS 
$$
    from algorithms.nested_loops import get_best
    
    rv = plpy.execute('SELECT * FROM r;')
    
    BEST_LIST = get_best(prefs, rv)
    
    return BEST_LIST
$$ LANGUAGE plpython3u;

CREATE OR REPLACE FUNCTION topk_bnl( prefs text, topk integer) 
RETURNS TABLE (like r) AS 
$$
    from algorithms.nested_loops import get_topk
    
    rv = plpy.execute('SELECT * FROM r;')
    
    TOPK_LIST = get_topk(prefs, rv, topk)
    
    return TOPK_LIST
$$ LANGUAGE plpython3u;

CREATE OR REPLACE FUNCTION best_partition( prefs text ) 
RETURNS TABLE (like r) AS 
$$
    from algorithms.partition import get_best_partition
    
    rv = plpy.execute('SELECT * FROM r;')
    BEST_LIST = get_best_partition(prefs, rv)
    
    return BEST_LIST
$$ LANGUAGE plpython3u;

CREATE OR REPLACE FUNCTION topk_partition( prefs text, topk integer) 
RETURNS TABLE (like r) AS 
$$
    from algorithms.partition import get_topk_partition
    
    rv = plpy.execute('SELECT * FROM r;')
    
    TOPK_LIST = get_topk_partition(prefs, rv, topk)
    
    return TOPK_LIST
$$ LANGUAGE plpython3u;



CREATE OR REPLACE FUNCTION best_maxpref( prefs text) 
RETURNS TABLE (like r) AS 
$$
    from algorithms.maxpref import get_mbest_partition
    
    rv = plpy.execute('SELECT * FROM r;')
    
    BEST_LIST = get_mbest_partition(prefs, rv)
    
    return BEST_LIST
$$ LANGUAGE plpython3u;

CREATE OR REPLACE FUNCTION topk_maxpref( prefs text, topk integer) 
RETURNS TABLE (like r) AS 
$$
    from algorithms.maxpref import get_mtopk_partition
    
    rv = plpy.execute('SELECT * FROM r;')
    
    TOPK_LIST = get_mtopk_partition(prefs, rv, topk)
    
    return TOPK_LIST
$$ LANGUAGE plpython3u;
