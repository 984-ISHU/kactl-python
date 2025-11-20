"""
 * Author: Chen Xing
 * Date: 2009-10-13
 * License: CC0
 * Source: N/A
 * Description: Flow algorithm with guaranteed complexity O(VE\^{}2). To get edge flow values, compare
 * capacities before and after, and take the positive values only.
 * Status: stress-tested
"""

from collections import defaultdict

def edmondsKarp(graph, source, sink):
    assert source != sink
    flow = 0
    n = len(graph)
    
    while True:
        par = [-1] * n
        par[source] = source
        q = [source]
        ptr = 0
        
        while ptr < len(q):
            x = q[ptr]
            if x == sink:
                break
            for e, cap in graph[x].items():
                if par[e] == -1 and cap > 0:
                    par[e] = x
                    q.append(e)
            ptr += 1
        
        if par[sink] == -1:
            return flow
        
        # Find bottleneck
        inc = float('inf')
        y = sink
        while y != source:
            p = par[y]
            inc = min(inc, graph[p][y])
            y = p
        
        # Update flow
        flow += inc
        y = sink
        while y != source:
            p = par[y]
            graph[p][y] -= inc
            if graph[p][y] == 0:
                del graph[p][y]
            if y not in graph:
                graph[y] = {}
            graph[y][p] = graph[y].get(p, 0) + inc
            y = p
    
    return flow
