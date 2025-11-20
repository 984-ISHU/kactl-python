"""
 * Author: Simon Lindholm
 * Date: 2015-05-13
 * Source: Wikipedia
 * Description: After running max-flow, the left side of a min-cut from s to t is given
 * by all vertices reachable from s, only traversing edges with positive residual capacity.
 * Status: works
"""

def minCut(graph, s, maxflow_result=None):
    """
    Given a flow graph after running maxflow, returns vertices on the left side of min-cut.
    graph: adjacency list where graph[u][v] represents residual capacity
    s: source vertex
    Returns: set of vertices reachable from s
    """
    n = len(graph)
    visited = [False] * n
    stack = [s]
    visited[s] = True
    left_side = {s}
    
    while stack:
        u = stack.pop()
        for v in graph[u]:
            if not visited[v] and graph[u].get(v, 0) > 0:
                visited[v] = True
                left_side.add(v)
                stack.append(v)
    
    return left_side
