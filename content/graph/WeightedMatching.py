"""
 * Author: Benjamin Qi, chilli
 * Date: 2020-04-04
 * License: CC0
 * Source: https://github.com/bqi343/USACO/
 * Description: Given a weighted bipartite graph, matches every node on
 * the left with a node on the right such that no
 * nodes are in two matchings and the sum of the edge weights is minimal. Takes
 * cost[N][M], where cost[i][j] = cost for L[i] to be matched with R[j] and
 * returns (min cost, match), where L[i] is matched with
 * R[match[i]]. Negate costs for max cost. Requires $N \le M$.
 * Time: $O(N^2M)$
 * Status: Tested on kattis:cordonbleu, stress-tested
"""

def hungarian(cost):
    """
    Solve minimum cost bipartite matching using Hungarian algorithm.
    
    Args:
        cost: 2D list where cost[i][j] = cost to match left[i] with right[j]
              Must have len(cost) <= len(cost[0]) (more right nodes than left)
    
    Returns:
        Tuple (min_cost, matches) where matches[i] = right node matched to left[i]
    """
    if not cost:
        return 0, []
    
    n = len(cost) + 1  # Left side (with dummy)
    m = len(cost[0]) + 1  # Right side (with dummy)
    
    u = [0] * n  # Dual variables for left
    v = [0] * m  # Dual variables for right
    p = [0] * m  # p[j] = left node matched to right j
    ans = [0] * (n - 1)
    
    INF = float('inf')
    
    for i in range(1, n):
        p[0] = i
        j0 = 0  # Current right node
        dist = [INF] * m
        pre = [-1] * m
        done = [False] * m
        
        # Dijkstra to find augmenting path
        while True:
            done[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = -1
            
            # Relax edges from i0
            for j in range(1, m):
                if not done[j]:
                    if i0 > 0:
                        cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    else:
                        cur = 0
                    
                    if cur < dist[j]:
                        dist[j] = cur
                        pre[j] = j0
                    
                    if dist[j] < delta:
                        delta = dist[j]
                        j1 = j
            
            # Update potentials
            for j in range(m):
                if done[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    dist[j] -= delta
            
            j0 = j1
            
            # Found augmenting path
            if p[j0] == 0:
                break
        
        # Update matching along augmenting path
        while j0:
            j1 = pre[j0]
            p[j0] = p[j1]
            j0 = j1
    
    # Extract final matching
    for j in range(1, m):
        if p[j]:
            ans[p[j] - 1] = j - 1
    
    return -v[0], ans

# Example usage:
# cost = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# min_cost, matching = hungarian(cost)
# Left node i is matched to right node matching[i]
