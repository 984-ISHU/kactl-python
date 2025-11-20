"""
 * Author: Lukas Polacek, Simon Lindholm
 * Date: 2019-12-26
 * License: CC0
 * Source: folklore
 * Description: Disjoint-set data structure with undo.
 * If undo is not needed, skip st, time() and rollback().
 * Usage: t = uf.time(); ...; uf.rollback(t)
 * Time: O(\log(N))
 * Status: tested as part of DirectedMST.h
"""

class UnionFindRollback:
    def __init__(self, n):
        self.e = [-1] * n
        self.st = []
    
    def size(self, x):
        return -self.e[self.find(x)]
    
    def find(self, x):
        return x if self.e[x] < 0 else self.find(self.e[x])
    
    def time(self):
        return len(self.st)
    
    def rollback(self, t):
        while len(self.st) > t:
            idx, val = self.st.pop()
            self.e[idx] = val
    
    def join(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.e[a] > self.e[b]:
            a, b = b, a
        self.st.append((a, self.e[a]))
        self.st.append((b, self.e[b]))
        self.e[a] += self.e[b]
        self.e[b] = a
        return True
