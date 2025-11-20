"""
 * Author: Simon Lindholm
 * Date: 2020-10-12
 * License: CC0
 * Source: https://en.wikipedia.org/wiki/Misra\_\%26\_Gries\_edge\_coloring\_algorithm
 * https://codeforces.com/blog/entry/75431 for the note about bipartite graphs.
 * Description: Given a simple, undirected graph with max degree $D$, computes a
 * $(D + 1)$-coloring of the edges such that no neighboring edges share a color.
 * ($D$-coloring is NP-hard, but can be done for bipartite graphs by repeated matchings of
 * max-degree nodes.)
 * Time: O(NM)
 * Status: stress-tested, tested on kattis:gamescheduling
"""

def edge_coloring(N, edges):
    """
    Compute edge coloring using Misra & Gries algorithm.
    
    Args:
        N: Number of vertices
        edges: List of (u, v) tuples representing edges
    
    Returns:
        List of colors for each edge (0-indexed)
    """
    # Count degree of each vertex
    cc = [0] * (N + 1)
    for u, v in edges:
        cc[u] += 1
        cc[v] += 1
    
    ncols = max(cc) + 1
    ret = [0] * len(edges)
    
    # adj[v][color] = edge index using that color at vertex v
    adj = [[-1] * ncols for _ in range(N)]
    
    # free[v] = smallest free color at vertex v
    free = [0] * N
    
    for idx, (u, v) in enumerate(edges):
        fan = [v]
        loc = [0] * ncols
        
        c = free[u]  # Color to assign
        ind = 0
        
        # Build fan from u
        d = free[v]
        loc[d] = 0
        while True:
            loc[d] = ind + 1
            if adj[u][d] == -1:
                break
            v = edges[adj[u][d]][1] if edges[adj[u][d]][0] == u else edges[adj[u][d]][0]
            ind += 1
            fan.append(v)
            d = free[v]
        
        cc[loc[d]] = c
        
        # Augment along cd-path
        cd = d
        at = u
        end = u
        while at != -1:
            next_node = adj[at][cd] if adj[at][cd] != -1 else -1
            if next_node != -1:
                other = edges[adj[at][cd]]
                at = other[1] if other[0] == at else other[0]
            else:
                at = -1
            
            # Swap colors along path
            adj[end][cd], adj[end][cd ^ c ^ d] = adj[end][cd ^ c ^ d], adj[end][cd]
            end = at if at != -1 else end
            cd ^= c ^ d
        
        # Shift fan
        i = 0
        while adj[fan[i]][d] != -1:
            left = fan[i]
            right = fan[i + 1]
            i += 1
            e = cc[i]
            adj[u][e] = left
            adj[left][e] = u
            adj[right][e] = -1
            free[right] = e
        
        adj[u][d] = fan[i]
        adj[fan[i]][d] = u
        
        # Update free colors
        for y in [fan[0], u, end]:
            free[y] = 0
            while adj[y][free[y]] != -1:
                free[y] += 1
    
    # Extract colors from adjacency structure
    for i, (u, v) in enumerate(edges):
        ret[i] = 0
        while adj[u][ret[i]] != v:
            ret[i] += 1
    
    return ret

# Example usage:
# edges = [(0, 1), (1, 2), (2, 0)]  # Triangle
# colors = edge_coloring(3, edges)
