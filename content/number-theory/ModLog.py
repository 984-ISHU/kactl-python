"""
 * Author: Bjorn Martinsson
 * Date: 2020-06-03
 * License: CC0
 * Source: own work
 * Description: Returns the smallest $x > 0$ s.t. $a^x = b \pmod m$, or
 * $-1$ if no such $x$ exists. modLog(a,1,m) can be used to
 * calculate the order of $a$.
 * Time: $O(\sqrt m)$
 * Status: tested for all 0 <= a,x < 500 and 0 < m < 500.
"""

import math
from math import gcd

def mod_log(a, b, m):
    """Baby-step giant-step discrete logarithm"""
    n = int(math.sqrt(m)) + 1
    e = f = 1
    j = 1
    A = {}
    
    # Baby step: build lookup table
    while j <= n:
        e = f = e * a % m
        if e == b % m:
            return j
        A[e * b % m] = j
        j += 1
    
    # Check if solution exists
    if gcd(m, e) != gcd(m, b):
        return -1
    
    # Giant step: find matching entry
    for i in range(2, n + 2):
        e = e * f % m
        if e in A:
            return n * i - A[e]
    
    return -1

# Example usage:
# x = mod_log(2, 10, 1000)  # Find x such that 2^x == 10 (mod 1000)
