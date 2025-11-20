"""
 * Author: Simon Lindholm
 * Date: 2017-05-11
 * License: CC0
 * Source: folklore
 * Description: Computes sums a[i,j] for all i<I, j<J, and increases single elements a[i,j].
 * Requires that the elements to be updated are known in advance (call fakeUpdate() before init()).
 * Time: O(\log^2 N). (Use persistent segment trees for O(\log N).)
 * Status: stress-tested
"""

from bisect import bisect_left

class FenwickTree2D:
    def __init__(self, limx):
        self.ys = [[] for _ in range(limx)]
        self.ft = []
    
    def fakeUpdate(self, x, y):
        while x < len(self.ys):
            self.ys[x].append(y)
            x |= x + 1
    
    def init(self):
        for v in self.ys:
            v.sort()
            self.ft.append(FenwickTree(len(v)))
    
    def ind(self, x, y):
        return bisect_left(self.ys[x], y)
    
    def update(self, x, y, dif):
        while x < len(self.ys):
            self.ft[x].update(self.ind(x, y), dif)
            x |= x + 1
    
    def query(self, x, y):
        sum_val = 0
        while x:
            sum_val += self.ft[x - 1].query(self.ind(x - 1, y))
            x &= x - 1
        return sum_val

class FenwickTree:
    def __init__(self, n):
        self.s = [0] * n
    
    def update(self, pos, dif):
        while pos < len(self.s):
            self.s[pos] += dif
            pos |= pos + 1
    
    def query(self, pos):
        res = 0
        while pos > 0:
            res += self.s[pos - 1]
            pos &= pos - 1
        return res
