"""
 * Author: Simon Lindholm
 * Date: 2019-05-22
 * License: CC0
 * Description: Chinese Remainder Theorem.
 
 * crt(a, m, b, n) computes x such that x == a (mod m), x == b (mod n).
 * If |a| < m and |b| < n, x will obey 0 <= x < lcm(m, n).
 * Time: O(\log(n))
 * Status: Works
"""

def euclid(a, b):
    if not b:
        return a, 1, 0
    d, y, x = euclid(b, a % b)
    y -= (a // b) * x
    return d, x, y

def crt(a, m, b, n):
    if n > m:
        a, b = b, a
        m, n = n, m
    g, x, y = euclid(m, n)
    assert (a - b) % g == 0, "No solution exists"
    x = (b - a) % n * x % n // g * m + a
    return x if x >= 0 else x + m * n // g
