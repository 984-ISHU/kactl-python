"""
 * Author: Simon Lindholm
 * Date: 2015-02-24
 * License: CC0
 * Source: Wikipedia, tinyKACTL
 * Description: Push-relabel using the highest label selection rule and the gap heuristic. Quite fast in practice.
 * To obtain the actual flow, look at positive values only.
 * Time: O(V^2\sqrt E)
 * Status: Tested on Kattis and SPOJ, and stress-tested
"""

class Edge:
    def __init__(self, dest, back, f, c):
        self.dest = dest
        self.back = back
        self.f = f
        self.c = c

class PushRelabel:
    def __init__(self, n):
        self.g = [[] for _ in range(n)]
        self.ec = [0] * n
        self.cur = [0] * n
        self.hs = [[] for _ in range(2 * n)]
        self.H = [0] * n
    
    def addEdge(self, s, t, cap, rcap=0):
        if s == t:
            return
        self.g[s].append(Edge(t, len(self.g[t]), 0, cap))
        self.g[t].append(Edge(s, len(self.g[s]) - 1, 0, rcap))
    
    def addFlow(self, e, f):
        back = self.g[e.dest][e.back]
        if not self.ec[e.dest] and f:
            self.hs[self.H[e.dest]].append(e.dest)
        e.f += f
        e.c -= f
        self.ec[e.dest] += f
        back.f -= f
        back.c += f
        self.ec[back.dest] -= f
    
    def calc(self, s, t):
        v = len(self.g)
        self.H[s] = v
        self.ec[t] = 1
        co = [0] * (2 * v)
        co[0] = v - 1
        for i in range(v):
            self.cur[i] = 0
        for e in self.g[s]:
            self.addFlow(e, e.c)
        
        hi = 0
        while True:
            while not self.hs[hi]:
                hi -= 1
                if hi < 0:
                    return -self.ec[s]
            u = self.hs[hi].pop()
            while self.ec[u] > 0:  # discharge u
                if self.cur[u] == len(self.g[u]):
                    self.H[u] = 10**9
                    for e in self.g[u]:
                        if e.c and self.H[u] > self.H[e.dest] + 1:
                            self.H[u] = self.H[e.dest] + 1
                            self.cur[u] = self.g[u].index(e)
                    co[self.H[u]] += 1
                    co[hi] -= 1
                    if co[hi] == 0 and hi < v:
                        for i in range(v):
                            if hi < self.H[i] < v:
                                co[self.H[i]] -= 1
                                self.H[i] = v + 1
                    hi = self.H[u]
                elif (self.g[u][self.cur[u]].c and 
                      self.H[u] == self.H[self.g[u][self.cur[u]].dest] + 1):
                    self.addFlow(self.g[u][self.cur[u]], 
                                min(self.ec[u], self.g[u][self.cur[u]].c))
                else:
                    self.cur[u] += 1
    
    def leftOfMinCut(self, a):
        return self.H[a] >= len(self.g)
