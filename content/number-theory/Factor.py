"""
 * Author: chilli, SJTU, pajenegod
 * Date: 2020-03-04
 * License: CC0
 * Source: own
 * Description: Pollard-rho randomized factorization algorithm. Returns prime
 * factors of a number, in arbitrary order (e.g. 2299 -> [11, 19, 11]).
 * Time: $O(n^{1/4})$, less for numbers with small factors.
 * Status: stress-tested
"""

from math import gcd

def mod_mul(a, b, m):
    """Fast modular multiplication for large numbers"""
    return (a * b) % m

def is_prime(n):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Test with witnesses
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def pollard(n):
    """Find a non-trivial factor of n using Pollard's rho"""
    if n % 2 == 0:
        return 2
    
    x = y = 2
    prd = 1
    i = 1
    t = 0
    
    while True:
        t += 1
        if t % 40 == 0 or prd == 0:
            g = gcd(prd, n)
            if g > 1:
                return g
            prd = 1
        
        # Cycle detection
        if x == y:
            i += 1
            x = i
            y = (x * x + i) % n
        
        # Update product
        q = mod_mul(prd, abs(x - y), n)
        if q != 0:
            prd = q
        
        # Advance
        x = (x * x + i) % n
        y = (y * y + i) % n
        y = (y * y + i) % n

def factor(n):
    """Return all prime factors of n (with multiplicity)"""
    if n == 1:
        return []
    if is_prime(n):
        return [n]
    
    x = pollard(n)
    left = factor(x)
    right = factor(n // x)
    return left + right

# Example usage:
# factors = factor(2299)  # Returns [11, 11, 19]
