"""
 * Author: Simon Lindholm
 * Date: 2021-01-09
 * License: CC0
 * Source: https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm
 * Description: Find a global minimum cut in an undirected graph, as represented by an adjacency matrix.
 * Time: O(V^3)
 * Status: Stress-tested together with GomoryHu
"""

def global_min_cut(mat):
    """
    Find global minimum cut in undirected graph.
    Returns (cut_weight, vertices_in_one_partition)
    """
    n = len(mat)
    best = (float('inf'), [])
    co = [[i] for i in range(n)]
    
    for ph in range(1, n):
        w = mat[0][:]
        s = t = 0
        
        for _ in range(n - ph):
            w[t] = float('-inf')
            s, t = t, max(range(n), key=lambda i: w[i])
            for i in range(n):
                w[i] += mat[t][i]
        
        if w[t] - mat[t][t] < best[0]:
            best = (w[t] - mat[t][t], co[t][:])
        
        # Merge t into s
        co[s].extend(co[t])
        for i in range(n):
            mat[s][i] += mat[t][i]
        for i in range(n):
            mat[i][s] = mat[s][i]
        mat[0][t] = float('-inf')
    
    return best

# Example usage:
# mat = [[0, 2, 3], [2, 0, 1], [3, 1, 0]]
# weight, partition = global_min_cut(mat)
