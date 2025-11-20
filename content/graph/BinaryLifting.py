"""
 * Author: Johan Sannemo
 * Date: 2015-02-06
 * License: CC0
 * Source: Folklore
 * Description: Calculate power of two jumps in a tree,
 * to support fast upward jumps and LCAs.
 * Assumes the root node points to itself.
 * Time: construction O(N \log N), queries O(\log N)
 * Status: Tested at Petrozavodsk, also stress-tested via LCA.cpp
"""

def treeJump(P):
    on = 1
    d = 1
    while on < len(P):
        on *= 2
        d += 1
    jmp = [P[:] for _ in range(d)]
    for i in range(1, d):
        for j in range(len(P)):
            jmp[i][j] = jmp[i-1][jmp[i-1][j]]
    return jmp

def jmp(tbl, nod, steps):
    for i in range(len(tbl)):
        if steps & (1 << i):
            nod = tbl[i][nod]
    return nod

def lca(tbl, depth, a, b):
    if depth[a] < depth[b]:
        a, b = b, a
    a = jmp(tbl, a, depth[a] - depth[b])
    if a == b:
        return a
    for i in range(len(tbl) - 1, -1, -1):
        c = tbl[i][a]
        d = tbl[i][b]
        if c != d:
            a, b = c, d
    return tbl[0][a]
