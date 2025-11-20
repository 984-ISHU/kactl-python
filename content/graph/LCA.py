"""
 * Author: chilli, pajenegod
 * Date: 2020-02-20
 * License: CC0
 * Source: Folklore
 * Description: Data structure for computing lowest common ancestors in a tree
 * (with 0 as root). C should be an adjacency list of the tree, either directed
 * or undirected.
 * Time: O(N \log N + Q)
 * Status: stress-tested
"""

class LCA:
    def __init__(self, C):
        self.T = 0
        self.time = [0] * len(C)
        self.path = []
        self.ret = []
        self.dfs(C, 0, -1)
        from bisect import bisect_left
        # Simple RMQ using sparse table
        self.rmq = self._build_rmq(self.ret)
    
    def dfs(self, C, v, par):
        self.time[v] = self.T
        self.T += 1
        for y in C[v]:
            if y != par:
                self.path.append(v)
                self.ret.append(self.time[v])
                self.dfs(C, y, v)
    
    def _build_rmq(self, V):
        # Build sparse table for RMQ
        n = len(V)
        if n == 0:
            return []
        LOG = n.bit_length()
        st = [[0] * n for _ in range(LOG)]
        for i in range(n):
            st[0][i] = i
        
        j = 1
        while (1 << j) <= n:
            i = 0
            while i + (1 << j) - 1 < n:
                if V[st[j-1][i]] < V[st[j-1][i + (1 << (j-1))]]:
                    st[j][i] = st[j-1][i]
                else:
                    st[j][i] = st[j-1][i + (1 << (j-1))]
                i += 1
            j += 1
        return st
    
    def _query_rmq(self, L, R):
        # Query minimum in range [L, R)
        if L >= R:
            return 0
        length = R - L
        k = (length).bit_length() - 1
        if self.ret[self.rmq[k][L]] <= self.ret[self.rmq[k][R - (1 << k)]]:
            return self.rmq[k][L]
        else:
            return self.rmq[k][R - (1 << k)]
    
    def lca(self, a, b):
        if a == b:
            return a
        ta, tb = self.time[a], self.time[b]
        if ta > tb:
            ta, tb = tb, ta
        idx = self._query_rmq(ta, tb)
        return self.path[idx] if idx < len(self.path) else a
