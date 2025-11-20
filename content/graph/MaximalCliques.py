"""
 * Author: Simon Lindholm
 * Date: 2018-07-18
 * License: CC0
 * Source: https://en.wikipedia.org/wiki/Bron\%E2\%80\%93Kerbosch\_algorithm
 * Description: Runs a callback for all maximal cliques in a graph (given as a
 * symmetric bitset matrix; self-edges not allowed). Callback is given a bitset
 * representing the maximal clique.
 * Time: $O(3^{n/3})$, much faster for sparse graphs
 * Status: stress-tested
"""

def maximal_cliques(edges, callback, P=None, X=None, R=None):
    """
    Find all maximal cliques using Bron-Kerbosch algorithm.
    
    Args:
        edges: List of sets where edges[i] contains neighbors of node i
        callback: Function to call with each maximal clique (as a set)
        P: Set of candidates (default: all nodes)
        X: Set of already processed nodes (default: empty)
        R: Current clique being built (default: empty)
    """
    n = len(edges)
    if P is None:
        P = set(range(n))
    if X is None:
        X = set()
    if R is None:
        R = set()
    
    # Base case: found maximal clique
    if not P and not X:
        callback(R)
        return
    
    # Choose pivot from P ∪ X with most connections
    pivot_candidates = P | X
    if not pivot_candidates:
        return
    
    # Pick pivot with maximum neighbors in P
    pivot = max(pivot_candidates, key=lambda v: len(edges[v] & P))
    
    # Consider vertices not connected to pivot
    candidates = P - edges[pivot]
    
    for v in list(candidates):
        # Recurse with v added to clique
        new_R = R | {v}
        new_P = P & edges[v]
        new_X = X & edges[v]
        
        maximal_cliques(edges, callback, new_P, new_X, new_R)
        
        # Move v from P to X
        P.remove(v)
        X.add(v)

def cliques_from_adjacency(adj_matrix):
    """
    Helper to convert adjacency matrix to edge sets.
    
    Args:
        adj_matrix: 2D list where adj_matrix[i][j] = 1 if edge exists
    
    Returns:
        List of sets representing edges
    """
    n = len(adj_matrix)
    edges = []
    for i in range(n):
        edge_set = set()
        for j in range(n):
            if adj_matrix[i][j]:
                edge_set.add(j)
        edges.append(edge_set)
    return edges

# Example usage:
# adj = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]  # Triangle
# edges = cliques_from_adjacency(adj)
# cliques = []
# maximal_cliques(edges, lambda c: cliques.append(c))
