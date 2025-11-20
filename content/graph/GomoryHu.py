"""
 * Author: chilli, Takanori MAEHARA
 * Date: 2020-04-03
 * License: CC0
 * Source: https://github.com/spaghetti-source/algorithm/
 * Description: Given a list of edges representing an undirected flow graph,
 * returns edges of the Gomory-Hu tree. The max flow between any pair of
 * vertices is given by minimum edge weight along the Gomory-Hu tree path.
 * Time: $O(V)$ Flow Computations
 * Status: Tested on CERC 2015 J, stress-tested
 *
 * Details: The implementation used here is not actually the original
 * Gomory-Hu, but Gusfield's simplified version.
"""

def gomory_hu(N, edges, flow_algorithm):
    """
    Construct Gomory-Hu tree using Gusfield's algorithm.
    
    Args:
        N: Number of vertices
        edges: List of (u, v, capacity) tuples
        flow_algorithm: Function(N, edges, s, t) that returns max flow from s to t
                       and can check leftOfMinCut(v) for min cut
    
    Returns:
        List of (u, v, flow_value) representing Gomory-Hu tree edges
    """
    tree = []
    par = [0] * N
    
    for i in range(1, N):
        # Compute min cut between i and par[i]
        flow_val = flow_algorithm(N, edges, i, par[i])
        tree.append((i, par[i], flow_val))
        
        # Update parents based on which side of cut they're on
        # (This requires flow_algorithm to provide leftOfMinCut info)
        for j in range(i + 1, N):
            if par[j] == par[i] and flow_algorithm.left_of_min_cut(j):
                par[j] = i
    
    return tree

class GomoryHuBuilder:
    """Helper class for building Gomory-Hu tree with PushRelabel or similar."""
    
    def __init__(self, N, edges):
        """
        Initialize builder.
        
        Args:
            N: Number of vertices
            edges: List of (u, v, capacity) tuples
        """
        self.N = N
        self.edges = edges
    
    def build(self, flow_class):
        """
        Build Gomory-Hu tree using specified flow algorithm.
        
        Args:
            flow_class: Class that implements max flow with leftOfMinCut method
        
        Returns:
            List of tree edges (u, v, flow_value)
        """
        tree = []
        par = [0] * self.N
        
        for i in range(1, self.N):
            # Create flow network
            flow = flow_class(self.N)
            for u, v, cap in self.edges:
                flow.add_edge(u, v, cap, cap)
            
            # Compute max flow = min cut
            flow_val = flow.calc(i, par[i])
            tree.append((i, par[i], flow_val))
            
            # Update parents based on min cut
            for j in range(i + 1, self.N):
                if par[j] == par[i] and flow.left_of_min_cut(j):
                    par[j] = i
        
        return tree

# Example usage:
# edges = [(0, 1, 10), (1, 2, 5), (0, 2, 15)]
# # Assuming PushRelabel class is available:
# builder = GomoryHuBuilder(3, edges)
# tree = builder.build(PushRelabel)
