"""
 * Author: Lucian Bicsi
 * Date: 2017-10-31
 * License: CC0
 * Source: Wikipedia
 * Description: Recovers any $n$-order linear recurrence relation from the first
 * $2n$ terms of the recurrence.
 * Useful for guessing linear recurrences after brute-forcing the first terms.
 * Should work on any field, but numerical stability for floats is not guaranteed.
 * Output will have size $\le n$.
 * Usage: berlekamp\_massey([0, 1, 1, 3, 5, 11]) returns [1, 2]
 * Time: O(N^2)
 * Status: bruteforce-tested mod 5 for n <= 5 and all s
"""

MOD = 998244353  # Use appropriate modulus

def mod_pow(base, exp, mod):
    """Modular exponentiation."""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

def berlekamp_massey(s, mod=MOD):
    """
    Find shortest linear recurrence for sequence s.
    
    Args:
        s: Sequence of values (list)
        mod: Modulus for computation
    
    Returns:
        Coefficients [c0, c1, ...] such that s[i] = sum(c[j] * s[i-j-1])
    """
    n = len(s)
    C = [0] * n
    B = [0] * n
    C[0] = B[0] = 1
    
    L = 0  # Length of LFSR
    m = 0  # Number of iterations since L was updated
    b = 1  # Previous discrepancy
    
    for i in range(n):
        m += 1
        
        # Compute discrepancy
        d = s[i] % mod
        for j in range(1, L + 1):
            d = (d + C[j] * s[i - j]) % mod
        
        if d == 0:
            continue
        
        T = C[:]
        coef = d * mod_pow(b, mod - 2, mod) % mod
        
        for j in range(m, n):
            C[j] = (C[j] - coef * B[j - m]) % mod
        
        if 2 * L <= i:
            L = i + 1 - L
            B = T
            b = d
            m = 0
    
    # Extract coefficients and negate
    C = C[:L + 1]
    result = C[1:]
    for i in range(len(result)):
        result[i] = (mod - result[i]) % mod
    
    return result

# Example usage:
# Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13
# coefs = berlekamp_massey([0, 1, 1, 2, 3, 5, 8, 13])
# Result: [1, 1] meaning s[n] = s[n-1] + s[n-2]
