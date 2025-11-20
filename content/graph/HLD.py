"""
 * Author: Benjamin Qi, Oleksandr Kulkov, chilli
 * Date: 2020-01-12
 * License: CC0
 * Source: https://codeforces.com/blog/entry/53170
 * Description: Decomposes a tree into vertex disjoint heavy paths and light
 * edges such that the path from any leaf to the root contains at most log(n)
 * light edges. Code does additive modifications and max queries, but can
 * support commutative segtree modifications/queries on paths and subtrees.
 * Takes as input the full adjacency list. VALS\_EDGES being true means that
 * values are stored in the edges, as opposed to the nodes. All values
 * initialized to the segtree default. Root must be 0.
 * Time: $O((\log N)^2)$
 * Status: stress-tested against old HLD
"""

class HLD:
    def __init__(self, adj, vals_edges=False):
        """
        Initialize Heavy-Light Decomposition.
        
        Args:
            adj: Adjacency list (list of lists)
            vals_edges: True if values stored in edges, False if in nodes
        """
        self.N = len(adj)
        self.adj = [neighbors[:] for neighbors in adj]
        self.vals_edges = vals_edges
        self.par = [-1] * self.N
        self.siz = [1] * self.N
        self.rt = [0] * self.N
        self.pos = [0] * self.N
        self.tim = 0
        
        # Use a simple list as segment tree for this implementation
        # In practice, use LazySegmentTree for better performance
        self.tree = [0] * self.N
        
        self.dfs_sz(0)
        self.dfs_hld(0)
    
    def dfs_sz(self, v):
        """Compute subtree sizes and reorder adjacency lists."""
        for i, u in enumerate(self.adj[v]):
            # Remove parent edge from child's adjacency list
            if v in self.adj[u]:
                self.adj[u].remove(v)
            
            self.par[u] = v
            self.dfs_sz(u)
            self.siz[v] += self.siz[u]
            
            # Swap to put heavy child first
            if i == 0 or self.siz[u] > self.siz[self.adj[v][0]]:
                self.adj[v][0], self.adj[v][i] = self.adj[v][i], self.adj[v][0]
    
    def dfs_hld(self, v):
        """Assign positions and root of heavy path for each node."""
        self.pos[v] = self.tim
        self.tim += 1
        
        for i, u in enumerate(self.adj[v]):
            # Heavy child inherits root, light child becomes new root
            self.rt[u] = self.rt[v] if i == 0 else u
            self.dfs_hld(u)
    
    def process(self, u, v, op):
        """Process path from u to v by calling op(l, r) on each segment."""
        while True:
            # Ensure u is higher than v
            if self.pos[u] > self.pos[v]:
                u, v = v, u
            
            # If on same heavy path, process and done
            if self.rt[u] == self.rt[v]:
                break
            
            # Process heavy path containing v
            op(self.pos[self.rt[v]], self.pos[v] + 1)
            v = self.par[self.rt[v]]
        
        # Process final segment on same heavy path
        start = self.pos[u] + (1 if self.vals_edges else 0)
        op(start, self.pos[v] + 1)
    
    def modify_path(self, u, v, val):
        """Add val to all nodes/edges on path from u to v."""
        def add_op(l, r):
            for i in range(l, r):
                self.tree[i] += val
        self.process(u, v, add_op)
    
    def query_path(self, u, v):
        """Return maximum value on path from u to v."""
        res = float('-inf')
        def max_op(l, r):
            nonlocal res
            for i in range(l, r):
                res = max(res, self.tree[i])
        self.process(u, v, max_op)
        return res
    
    def query_subtree(self, v):
        """Return maximum value in subtree rooted at v."""
        start = self.pos[v] + (1 if self.vals_edges else 0)
        end = self.pos[v] + self.siz[v]
        res = float('-inf')
        for i in range(start, end):
            res = max(res, self.tree[i])
        return res

# Example usage:
# adj = [[1, 2], [3, 4], [], [], []]  # Tree with root 0
# hld = HLD(adj, vals_edges=False)
# hld.modify_path(3, 4, 5)
# max_val = hld.query_path(3, 4)
