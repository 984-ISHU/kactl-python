"""
 * Author: chilli, SJTU, Janez Konc
 * Date: 2019-05-10
 * License: GPL3+
 * Source: https://en.wikipedia.org/wiki/MaxCliqueDyn\_maximum\_clique\_algorithm
 * Description: Quickly finds a maximum clique of a graph (given as symmetric bitset
 * matrix; self-edges not allowed). Can be used to find a maximum independent
 * set by finding a clique of the complement graph.
 * Time: Runs in about 1s for n=155 and worst case random graphs (p=.90). Runs
 * faster for sparse graphs.
 * Status: stress-tested
"""

class MaximumClique:
    def __init__(self, adj_matrix):
        """
        Initialize maximum clique finder.
        
        Args:
            adj_matrix: 2D list/bitset matrix representing graph adjacency
        """
        self.e = adj_matrix
        self.n = len(adj_matrix)
        self.qmax = []
        self.q = []
        self.limit = 0.025
        self.pk = 0
        self.S = [0] * (self.n + 1)
        self.old = [0] * (self.n + 1)
        self.C = [[] for _ in range(self.n + 1)]
    
    def init_vertices(self, vertices):
        """Initialize vertices with degree information."""
        # Count degrees
        for v in vertices:
            v['d'] = sum(1 for u in vertices if self.e[v['i']][u['i']])
        
        # Sort by degree descending
        vertices.sort(key=lambda v: v['d'], reverse=True)
        
        # Update degree bounds
        max_d = vertices[0]['d']
        for i, v in enumerate(vertices):
            v['d'] = min(i, max_d) + 1
    
    def expand(self, R, lev=1):
        """Recursively expand clique candidates."""
        self.S[lev] += self.S[lev - 1] - self.old[lev]
        self.old[lev] = self.S[lev - 1]
        
        while R:
            # Prune if can't beat current best
            if len(self.q) + R[-1]['d'] <= len(self.qmax):
                return
            
            # Add vertex to current clique
            v = R.pop()
            self.q.append(v['i'])
            
            # Find neighbors of v that are in R
            T = [{'i': u['i']} for u in R if self.e[v['i']][u['i']]]
            
            if T:
                # Coloring-based pruning
                if self.S[lev] / (self.pk + 1) < self.limit:
                    self.init_vertices(T)
                    self.pk += 1
                
                # Color vertices
                j = 0
                mxk = 1
                mnk = max(len(self.qmax) - len(self.q) + 1, 1)
                self.C[1] = []
                self.C[2] = []
                
                for vertex in T:
                    k = 1
                    # Find smallest color not used by neighbors
                    while any(self.e[vertex['i']][c] for c in self.C[k]):
                        k += 1
                    
                    if k > mxk:
                        mxk = k
                        self.C[mxk + 1] = []
                    
                    if k < mnk:
                        T[j] = vertex
                        j += 1
                    
                    self.C[k].append(vertex['i'])
                
                # Add vertices with colors >= mnk
                if j > 0:
                    T[j - 1]['d'] = 0
                
                for k in range(mnk, mxk + 1):
                    for i in self.C[k]:
                        T[j] = {'i': i, 'd': k}
                        j += 1
                
                T = T[:j]
                self.expand(T, lev + 1)
            
            elif len(self.q) > len(self.qmax):
                # Found larger clique
                self.qmax = self.q[:]
            
            self.q.pop()
    
    def max_clique(self):
        """Find maximum clique in the graph."""
        V = [{'i': i} for i in range(self.n)]
        self.init_vertices(V)
        self.expand(V)
        return self.qmax

# Example usage:
# adj = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]  # Triangle
# mc = MaximumClique(adj)
# max_clique = mc.max_clique()  # Returns [0, 1, 2] or similar
