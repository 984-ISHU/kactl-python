"""
 * Author: Johan Sannemo, Simon Lindholm
 * Date: 2016-12-15
 * License: CC0
 * Description: Finds a minimum vertex cover in a bipartite graph.
 *  The size is the same as the size of a maximum matching, and
 *  the complement is a maximum independent set.
 * Status: stress-tested
"""

def minimum_vertex_cover(g, n, m, dfs_matching):
    """
    Find minimum vertex cover in bipartite graph.
    
    Args:
        g: Adjacency list for left partition (list of lists)
        n: Number of nodes in left partition
        m: Number of nodes in right partition
        dfs_matching: Function that computes maximum matching
    
    Returns:
        List of vertex indices in the minimum cover (0..n-1 for left, n..n+m-1 for right)
    """
    match = [-1] * m
    res = dfs_matching(g, match)
    
    lfound = [True] * n
    seen = [False] * m
    
    # Mark matched left nodes as not found
    for it in match:
        if it != -1:
            lfound[it] = False
    
    # BFS from unmatched left nodes
    q = [i for i in range(n) if lfound[i]]
    
    while q:
        i = q.pop()
        lfound[i] = True
        for e in g[i]:
            if not seen[e] and match[e] != -1:
                seen[e] = True
                q.append(match[e])
    
    # Build cover: unvisited left nodes + visited right nodes
    cover = []
    for i in range(n):
        if not lfound[i]:
            cover.append(i)
    for i in range(m):
        if seen[i]:
            cover.append(n + i)
    
    assert len(cover) == res
    return cover

# Example usage:
# from DFSMatching import dfs_matching
# g = [[0, 1], [1, 2], [0, 2]]  # Left partition adjacency
# cover = minimum_vertex_cover(g, 3, 3, dfs_matching)
