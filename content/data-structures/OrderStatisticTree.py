"""
 * Author: Simon Lindholm
 * Date: 2016-03-22
 * License: CC0
 * Source: hacKIT, NWERC 2015
 * Description: A set (not multiset!) with support for finding the n'th
 * element, and finding the index of an element. Python's sortedcontainers
 * library provides similar functionality. Install with: pip install sortedcontainers
 * Time: O(\log N)
"""

from sortedcontainers import SortedList

def example():
    t = SortedList()
    t.add(8)
    t.add(10)
    assert t.bisect_left(9) == 1  # index of first element >= 9
    assert t.index(10) == 1  # index of element 10
    assert t.index(8) == 0
    assert t[0] == 8  # n'th element
    assert t[1] == 10

# Alternative: Use bisect module with a regular list (requires manual sorting)
# import bisect
# t = []
# bisect.insort(t, 8)
# bisect.insort(t, 10)
# idx = bisect.bisect_left(t, 9)
