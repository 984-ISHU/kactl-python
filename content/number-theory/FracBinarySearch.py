"""
 * Author: Simon Lindholm
 * Date: 2015-02-11
 * License: CC0
 * Source: marian's code from NWERC 2014
 * Description: Given $f$ and $N$, finds the smallest fraction $p/q \in [0, 1]$ such that $f(p/q)$ is true, and $p \le N$ (or $q \le N$ if `dir$ is 1).
 * You must have $f(0) = \text{false}$, $f(1) = \text{true}$, and $f$ monotonic. The fraction is given as the last $(num, den)$ pair seen by $f$.
 * Usage: to find a rational approximation of a real number $x$, set $f = \text{lambda } p, q: p \ge q \cdot x$.
 * Time: $O(\log N)$
 * Status: stress-tested for $N \le 300$
"""

def frac_binary_search(f, N, dir=0):
    """
    Find smallest fraction p/q in [0, 1] satisfying f(p, q) = True.
    
    Args:
        f: Function taking (p, q) returning boolean
        N: Maximum value for p (if dir=0) or q (if dir=1)
        dir: 0 to limit p, 1 to limit q
    
    Returns:
        Tuple (num, den) - the last fraction checked by f
    """
    if dir == 1:
        # Swap to limit q instead of p
        result = frac_binary_search(lambda q, p: f(p, q), N, 0)
        return (result[1], result[0])
    
    # Binary search in Stern-Brocot tree
    # We maintain two fractions a/b and c/d with property that
    # all fractions in search space are between them
    a, b = 0, 1  # Left bound
    c, d = 1, 1  # Right bound
    num, den = 0, 1
    
    while True:
        # Mediant of a/b and c/d is (a+c)/(b+d)
        p = a + c
        q = b + d
        
        if p > N:
            break
        
        num, den = p, q
        
        if f(p, q):
            # Fraction too large, search left half
            c, d = p, q
        else:
            # Fraction too small, search right half
            a, b = p, q
    
    return (num, den)

# Example usage:
# Find rational approximation of pi with denominator <= 1000:
# import math
# result = frac_binary_search(lambda p, q: p >= q * math.pi, 1000)
# This gives 355/113, a famous pi approximation
