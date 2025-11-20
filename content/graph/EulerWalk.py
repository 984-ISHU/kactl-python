"""
 * Author: Simon Lindholm
 * Date: 2019-12-31
 * License: CC0
 * Source: folklore
 * Description: Eulerian undirected/directed path/cycle algorithm.
 * Input should be a list of (dest, global edge index), where
 * for undirected graphs, forward/backward edges have the same index.
 * Returns a list of nodes in the Eulerian path/cycle with src at both start and end, or
 * empty list if no cycle/path exists.
 * To get edge indices back, modify to track edge indices.
 * Time: O(V + E)
 * Status: stress-tested
"""

def eulerWalk(gr, nedges, src=0):
    n = len(gr)
    D = [0] * n
    its = [0] * n
    eu = [0] * nedges
    ret = []
    s = [src]
    D[src] += 1  # to allow Euler paths, not just cycles
    
    while s:
        x = s[-1]
        it = its[x]
        end = len(gr[x])
        if it == end:
            ret.append(x)
            s.pop()
            continue
        y, e = gr[x][it]
        its[x] += 1
        if not eu[e]:
            D[x] -= 1
            D[y] += 1
            eu[e] = 1
            s.append(y)
    
    for x in D:
        if x < 0 or len(ret) != nedges + 1:
            return []
    return ret[::-1]
