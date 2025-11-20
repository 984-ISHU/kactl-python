"""
 * Author: Lukas Polacek
 * Date: 2009-10-28
 * License: CC0
 * Source: Czech graph algorithms book, by Demel. (Tarjan's algorithm)
 * Description: Finds strongly connected components in a
 * directed graph. If vertices u, v belong to the same component,
 * we can reach u from v and vice versa.
 * Usage: scc(graph, lambda v: ...) visits all components
 * in reverse topological order. comp[i] holds the component
 * index of a node (a component only has edges to components with
 * lower index). Returns (comp, ncomps).
 * Time: O(E + V)
 * Status: Bruteforce-tested for N <= 5
"""

def scc(g, f=None):
    n = len(g)
    val = [0] * n
    comp = [-1] * n
    z = []
    cont = []
    Time = [0]
    ncomps = [0]
    
    def dfs(j):
        low = val[j] = Time[0] = Time[0] + 1
        z.append(j)
        for e in g[j]:
            if comp[e] < 0:
                if val[e]:
                    low = min(low, val[e])
                else:
                    low = min(low, dfs(e))
        
        if low == val[j]:
            while True:
                x = z.pop()
                comp[x] = ncomps[0]
                cont.append(x)
                if x == j:
                    break
            if f:
                f(cont[:])
            cont.clear()
            ncomps[0] += 1
        return low
    
    for i in range(n):
        if comp[i] < 0:
            dfs(i)
    
    return comp, ncomps[0]
