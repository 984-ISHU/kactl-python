"""
 * Author: Simon Lindholm
 * Date: 2015-06-23
 * License: CC0
 * Source: own work
 * Description: Sums of mod'ed arithmetic progressions.
 * modsum(to, c, k, m) = sum of (k*i+c) % m for i=0 to to-1.
 * divsum is similar but for floored division.
 * Time: $O(\log m)$, with a large constant.
 * Status: Tested for all |k|,|c|,to,m <= 50, and on kattis:aladin
"""

def sumsq(to):
    """Sum of 0..to-1, handling overflow"""
    return to // 2 * ((to - 1) | 1)

def divsum(to, c, k, m):
    """Sum of (k*i+c)//m for i in range(to)"""
    res = k // m * sumsq(to) + c // m * to
    k %= m
    c %= m
    if not k:
        return res
    to2 = (to * k + c) // m
    return res + (to - 1) * to2 - divsum(to2, m - 1 - c, m, k)

def modsum(to, c, k, m):
    """Sum of (k*i+c) % m for i in range(to)"""
    c = ((c % m) + m) % m
    k = ((k % m) + m) % m
    return to * c + k * sumsq(to) - m * divsum(to, c, k, m)

# Example usage:
# result = modsum(100, 5, 3, 17)  # Sum of (3*i+5) % 17 for i=0..99
