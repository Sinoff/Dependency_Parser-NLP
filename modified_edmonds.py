
# --------------------------------------------------------------------------------- #


def _reverse(graph):
    r = {}
    for src in graph:
        for (dst,c) in graph[src].items():
            if dst in r:
                r[dst][src] = c
            else:
                r[dst] = { src : c }
    return r


def _getCycle(n,g,visited,cycle):
    if n not in g:
        return cycle    
    visited.add(n)
    cycle += [n]
    for e in g[n]:
        if e not in visited:
            cycle = _getCycle(e,g,visited,cycle)
    return cycle


def _mergeCycles(cycle,G,RG,g,rg):
    allInEdges = []
    maxInternal = None
    maxInternalWeight = -float("inf")

    # find minimal internal edge weight
    for n in cycle:
        for e in RG[n]:
            if e in cycle:
                if maxInternal is None or RG[n][e] > maxInternalWeight:
                    maxInternal = (n,e)
                    maxInternalWeight = RG[n][e]
                    continue
            else:
                allInEdges.append((n,e))        

    # find the incoming edge with minimum modified cost
    maxExternal = None
    maxModifiedWeight = -float("inf")
    for s,t in allInEdges:
        u,v = rg[s].popitem()
        rg[s][u] = v
        w = RG[s][t] - (v - maxInternalWeight)
        if maxExternal is None or maxModifiedWeight < w:
            maxExternal = (s,t)
            maxModifiedWeight = w

    u,w = rg[maxExternal[0]].popitem()
    rem = (maxExternal[0],u)
    rg[maxExternal[0]].clear()
    if maxExternal[1] in rg:
        rg[maxExternal[1]][maxExternal[0]] = w
    else:
        rg[maxExternal[1]] = { maxExternal[0] : w }
    if rem[1] in g:
        if rem[0] in g[rem[1]]:
            del g[rem[1]][rem[0]]
    if maxExternal[1] in g:
        g[maxExternal[1]][maxExternal[0]] = w
    else:
        g[maxExternal[1]] = { maxExternal[0] : w }

# --------------------------------------------------------------------------------- #

def mst(root,G):
    """ The Chu-Lui/Edmond's algorithm

    arguments:

    root - the root of the MST
    G - the graph in which the MST lies

    returns: a graph representation of the MST

    Graph representation is the same as the one found at:
    http://code.activestate.com/recipes/119466/

    Explanation is copied verbatim here:

    The input graph G is assumed to have the following
    representation: A vertex can be any object that can
    be used as an index into a dictionary.  G is a
    dictionary, indexed by vertices.  For any vertex v,
    G[v] is itself a dictionary, indexed by the neighbors
    of v.  For any edge v->w, G[v][w] is the length of
    the edge.  This is related to the representation in
    <http://www.python.org/doc/essays/graphs.html>
    where Guido van Rossum suggests representing graphs
    as dictionaries mapping vertices to lists of neighbors,
    however dictionaries of edges have many advantages
    over lists: they can store extra information (here,
    the lengths), they support fast existence tests,
    and they allow easy modification of the graph by edge
    insertion and removal.  Such modifications are not
    needed here but are important in other graph algorithms.
    Since dictionaries obey iterator protocol, a graph
    represented as described here could be handed without
    modification to an algorithm using Guido's representation.

    Of course, G and G[v] need not be Python dict objects;
    they can be any other object that obeys dict protocol,
    for instance a wrapper in which vertices are URLs
    and a call to G[v] loads the web page and finds its links.
    """
    
    RG = _reverse(G)
    if root in RG:
        RG[root] = {}
    g = {}
    for n in RG:
        if len(RG[n]) == 0:
            continue
        maximum = -float("inf")
        s,d = None,None
        for e in RG[n]:
            if RG[n][e] > maximum:
                maximum = RG[n][e]
                s,d = n,e
        if d in g:
            g[d][s] = RG[s][d]
        else:
            g[d] = { s : RG[s][d] }
            
    cycles = []
    visited = set()
    for n in g:
        if n not in visited:
            cycle = []
            cycle = _getCycle(n,g,visited, cycle)
            cycles.append(cycle)

    rg = _reverse(g)
    for cycle in cycles:
        if root in cycle:
            continue  
        _mergeCycles(cycle, G, RG, g, rg)

    return g
