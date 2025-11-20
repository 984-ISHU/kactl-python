"""
 * Author: chilli, Takanori MAEHARA, Benq, Simon Lindholm
 * Date: 2019-05-10
 * License: CC0
 * Source: https://github.com/spaghetti-source/algorithm/
 * Description: Finds a minimum spanning tree/arborescence of a directed graph,
 * given a root node. If no MST exists, returns -1.
 * Time: $O(E \log V)$
 * Status: Stress-tested
"""

class Edge:
    def __init__(self, a, b, w):
        self.a = a  # From
        self.b = b  # To
        self.w = w  # Weight

class LazySkewHeap:
    """Lazy skew heap node for efficient minimum maintenance."""
    
    def __init__(self, edge):
        self.key = edge
        self.left = None
        self.right = None
        self.delta = 0
    
    def propagate(self):
        """Apply lazy delta to key and children."""
        self.key.w += self.delta
        if self.left:
            self.left.delta += self.delta
        if self.right:
            self.right.delta += self.delta
        self.delta = 0
    
    def top(self):
        """Get minimum element."""
        self.propagate()
        return self.key

def merge_heaps(a, b):
    """Merge two skew heaps."""
    if not a or not b:
        return a or b
    
    a.propagate()
    b.propagate()
    
    if a.key.w > b.key.w:
        a, b = b, a
    
    a.right = merge_heaps(b, a.right)
    a.left, a.right = a.right, a.left
    return a

def directed_mst(n, root, edges):
    """
    Find minimum spanning arborescence (directed MST).
    
    Args:
        n: Number of vertices
        root: Root vertex for the arborescence
        edges: List of Edge objects
    
    Returns:
        Tuple (cost, parent) where:
            cost: Total cost of MST (-1 if no MST exists)
            parent: parent[i] = parent of node i in MST
    """
    # Create heaps for each vertex (incoming edges)
    heap = [None] * n
    for e in edges:
        heap[e.b] = merge_heaps(heap[e.b], LazySkewHeap(e))
    
    result = 0
    seen = [-1] * n
    path = [0] * n
    parent = [0] * n
    seen[root] = root
    Q = [None] * n
    in_edge = [Edge(-1, -1, 0)] * n
    
    # Find cycles and contract
    uf_parent = list(range(n))
    uf_rank = [0] * n
    
    def uf_find(x):
        if uf_parent[x] != x:
            uf_parent[x] = uf_find(uf_parent[x])
        return uf_parent[x]
    
    def uf_union(x, y):
        x, y = uf_find(x), uf_find(y)
        if x == y:
            return False
        if uf_rank[x] < uf_rank[y]:
            x, y = y, x
        uf_parent[y] = x
        if uf_rank[x] == uf_rank[y]:
            uf_rank[x] += 1
        return True
    
    for s in range(n):
        u = s
        qi = 0
        
        while seen[u] < 0:
            if not heap[u]:
                return -1, []
            
            e = heap[u].top()
            heap[u].delta -= e.w
            heap[u] = merge_heaps(heap[u].left, heap[u].right)
            
            Q[qi] = e
            path[qi] = u
            qi += 1
            seen[u] = s
            result += e.w
            u = uf_find(e.a)
            
            # Found cycle
            if seen[u] == s:
                cyc_heap = None
                w = 0
                
                while True:
                    qi -= 1
                    w = path[qi]
                    cyc_heap = merge_heaps(cyc_heap, heap[w])
                    if not uf_union(u, w):
                        break
                
                u = uf_find(u)
                heap[u] = cyc_heap
                seen[u] = -1
        
        # Record incoming edges
        for i in range(qi):
            in_edge[uf_find(Q[i].b)] = Q[i]
    
    # Build parent array
    for i in range(n):
        parent[i] = in_edge[i].a
    
    return result, parent

# Example usage:
# edges = [Edge(0, 1, 5), Edge(0, 2, 3), Edge(1, 2, 2)]
# cost, parents = directed_mst(3, 0, edges)
