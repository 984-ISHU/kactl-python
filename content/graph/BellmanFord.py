"""
 * Author: Simon Lindholm
 * Date: 2015-02-23
 * License: CC0
 * Source: http://en.wikipedia.org/wiki/Bellman-Ford_algorithm
 * Description: Calculates shortest paths from s in a graph that might have negative edge weights.
 * Unreachable nodes get dist = inf; nodes reachable through negative-weight cycles get dist = -inf.
 * Time: O(VE)
 * Status: Tested on kattis:shortestpath3
"""

class Node:
    def __init__(self):
        self.dist = float('inf')
        self.prev = -1

class Edge:
    def __init__(self, a, b, w):
        self.a = a
        self.b = b
        self.w = w
    
    def s(self):
        return self.a if self.a < self.b else -self.a

def bellmanFord(nodes, edges, s):
    nodes[s].dist = 0
    edges.sort(key=lambda e: e.s())
    
    lim = len(nodes) // 2 + 2  # //3+100 with shuffled vertices
    for i in range(lim):
        for ed in edges:
            cur = nodes[ed.a]
            dest = nodes[ed.b]
            if abs(cur.dist) == float('inf'):
                continue
            d = cur.dist + ed.w
            if d < dest.dist:
                dest.prev = ed.a
                dest.dist = d if i < lim - 1 else float('-inf')
    
    for i in range(lim):
        for e in edges:
            if nodes[e.a].dist == float('-inf'):
                nodes[e.b].dist = float('-inf')
