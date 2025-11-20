"""
 * Author: Simon Lindholm
 * Date: 2016-10-08
 * License: CC0
 * Source: me
 * Description: Segment tree with ability to add or set values of large intervals, and compute max of intervals.
 * Can be changed to other things.
 * Time: O(\log N).
 * Status: stress-tested a bit
 * Usage: tr = LazySegmentTree(v, 0, len(v))
"""

class LazySegmentTree:
    def __init__(self, v, lo, hi):
        self.lo = lo
        self.hi = hi
        self.l = None
        self.r = None
        self.mset = float('inf')
        self.madd = 0
        self.val = float('-inf')
        
        if isinstance(v, list):  # Initialize from array
            if lo + 1 < hi:
                mid = lo + (hi - lo) // 2
                self.l = LazySegmentTree(v, lo, mid)
                self.r = LazySegmentTree(v, mid, hi)
                self.val = max(self.l.val, self.r.val)
            else:
                self.val = v[lo]
    
    def query(self, L, R):
        if R <= self.lo or self.hi <= L:
            return float('-inf')
        if L <= self.lo and self.hi <= R:
            return self.val
        self.push()
        return max(self.l.query(L, R), self.r.query(L, R))
    
    def set(self, L, R, x):
        if R <= self.lo or self.hi <= L:
            return
        if L <= self.lo and self.hi <= R:
            self.mset = x
            self.val = x
            self.madd = 0
        else:
            self.push()
            self.l.set(L, R, x)
            self.r.set(L, R, x)
            self.val = max(self.l.val, self.r.val)
    
    def add(self, L, R, x):
        if R <= self.lo or self.hi <= L:
            return
        if L <= self.lo and self.hi <= R:
            if self.mset != float('inf'):
                self.mset += x
            else:
                self.madd += x
            self.val += x
        else:
            self.push()
            self.l.add(L, R, x)
            self.r.add(L, R, x)
            self.val = max(self.l.val, self.r.val)
    
    def push(self):
        if not self.l:
            mid = self.lo + (self.hi - self.lo) // 2
            self.l = LazySegmentTree(None, self.lo, mid)
            self.r = LazySegmentTree(None, mid, self.hi)
        if self.mset != float('inf'):
            self.l.set(self.lo, self.hi, self.mset)
            self.r.set(self.lo, self.hi, self.mset)
            self.mset = float('inf')
        elif self.madd:
            self.l.add(self.lo, self.hi, self.madd)
            self.r.add(self.lo, self.hi, self.madd)
            self.madd = 0
