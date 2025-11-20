"""
 * Author: chilli
 * Date: 2019-04-26
 * License: CC0
 * Source: https://cp-algorithms.com/graph/dinic.html
 * Description: Flow algorithm with complexity $O(VE\log U)$ where $U = \max |\text{cap}|$.
 * $O(\min(E^{1/2}, V^{2/3})E)$ if $U = 1$; $O(\sqrt{V}E)$ for bipartite matching.
 * Status: Tested on SPOJ FASTFLOW and SPOJ MATCHING, stress-tested
"""

from collections import deque

class Dinic:
    class Edge:
        def __init__(self, to, rev, cap):
            self.to = to
            self.rev = rev
            self.c = cap
            self.oc = cap
        
        def flow(self):
            return max(self.oc - self.c, 0)
    
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.lvl = [0] * n
        self.ptr = [0] * n
    
    def add_edge(self, a, b, cap, rcap=0):
        """Add edge from a to b with capacity cap, reverse capacity rcap"""
        self.adj[a].append(self.Edge(b, len(self.adj[b]), cap))
        self.adj[b].append(self.Edge(a, len(self.adj[a]) - 1, rcap))
    
    def dfs(self, v, t, f):
        """DFS to push flow"""
        if v == t or f == 0:
            return f
        
        while self.ptr[v] < len(self.adj[v]):
            e = self.adj[v][self.ptr[v]]
            if self.lvl[e.to] == self.lvl[v] + 1:
                p = self.dfs(e.to, t, min(f, e.c))
                if p > 0:
                    e.c -= p
                    self.adj[e.to][e.rev].c += p
                    return p
            self.ptr[v] += 1
        return 0
    
    def calc(self, s, t):
        """Calculate max flow from s to t"""
        flow = 0
        
        for L in range(31):
            while True:
                self.lvl = [0] * self.n
                self.ptr = [0] * self.n
                
                # BFS to build level graph
                q = deque([s])
                self.lvl[s] = 1
                
                while q and not self.lvl[t]:
                    v = q.popleft()
                    for e in self.adj[v]:
                        if not self.lvl[e.to] and e.c >> (30 - L):
                            q.append(e.to)
                            self.lvl[e.to] = self.lvl[v] + 1
                
                if not self.lvl[t]:
                    break
                
                # Push flow along augmenting paths
                while True:
                    p = self.dfs(s, t, float('inf'))
                    if p == 0:
                        break
                    flow += p
        
        return flow
    
    def left_of_min_cut(self, a):
        """Check if node a is on source side of min cut"""
        return self.lvl[a] != 0

# Example usage:
# dinic = Dinic(4)
# dinic.add_edge(0, 1, 10)
# dinic.add_edge(1, 3, 10)
# max_flow = dinic.calc(0, 3)
