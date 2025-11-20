"""
 * Author: Simon Lindholm
 * Date: 2017-04-20
 * License: CC0
 * Source: own work
 * Description: Container where you can add lines of the form kx+m, and query maximum values at points x.
 * Useful for dynamic programming (convex hull trick).
 * Time: O(\log N)
 * Status: stress-tested
"""

from collections import deque

class LineContainer:
    def __init__(self):
        self.lines = deque()  # (k, m, p) tuples
    
    def _div(self, a, b):
        # Floored division
        return a // b - (1 if (a ^ b) < 0 and a % b else 0)
    
    def _isect(self, idx):
        # Calculate intersection point for line at idx
        if idx + 1 >= len(self.lines):
            self.lines[idx] = (self.lines[idx][0], self.lines[idx][1], float('inf'))
            return False
        k1, m1, _ = self.lines[idx]
        k2, m2, _ = self.lines[idx + 1]
        if k1 == k2:
            p = float('inf') if m1 > m2 else float('-inf')
        else:
            p = self._div(m2 - m1, k1 - k2)
        self.lines[idx] = (k1, m1, p)
        if idx + 1 < len(self.lines):
            return p >= self.lines[idx + 1][2]
        return False
    
    def add(self, k, m):
        # Add line kx + m
        # Insert maintaining sorted order by slope k
        idx = len(self.lines)
        for i in range(len(self.lines)):
            if self.lines[i][0] > k:
                idx = i
                break
        self.lines.insert(idx, (k, m, 0))
        
        # Fix intersections
        i = idx
        while i + 1 < len(self.lines) and self._isect(i):
            self.lines.pop(i + 1)
        
        if i > 0:
            self._isect(i - 1)
            if i > 0 and self.lines[i - 1][2] >= self.lines[i][2]:
                self.lines.pop(i)
                i -= 1
        
        while i > 0 and self.lines[i - 1][2] >= self.lines[i][2]:
            self.lines.pop(i)
            i -= 1
            if i > 0:
                self._isect(i - 1)
    
    def query(self, x):
        # Query maximum value at point x
        assert len(self.lines) > 0
        # Binary search for the right line
        left, right = 0, len(self.lines) - 1
        while left < right:
            mid = (left + right) // 2
            if self.lines[mid][2] < x:
                left = mid + 1
            else:
                right = mid
        k, m, _ = self.lines[left]
        return k * x + m
