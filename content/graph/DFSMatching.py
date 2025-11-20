"""
 * Author: Lukas Polacek
 * Date: 2009-10-28
 * License: CC0
 * Source:
 * Description: Simple bipartite matching algorithm. Graph g should be a list
 * of neighbors of the left partition, and btoa should be a list full of
 * -1's of the same size as the right partition. Returns the size of
 * the matching. btoa[i] will be the match for vertex i on the right side,
 * or -1 if it's not matched.
 * Time: O(VE)
 * Usage: btoa = [-1] * m; dfsMatching(g, btoa)
 * Status: works
"""

def dfsMatching(g, btoa):
    def find(j, vis):
        if btoa[j] == -1:
            return True
        vis[j] = True
        di = btoa[j]
        for e in g[di]:
            if not vis[e] and find(e, vis):
                btoa[e] = di
                return True
        return False
    
    for i in range(len(g)):
        vis = [False] * len(btoa)
        for j in g[i]:
            if find(j, vis):
                btoa[j] = i
                break
    
    return len(btoa) - btoa.count(-1)
