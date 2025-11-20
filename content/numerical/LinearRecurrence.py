"""
 * Author: Lucian Bicsi
 * Date: 2018-02-14
 * License: CC0
 * Source: Chinese material
 * Description: Generates the $k$'th term of an $n$-order
 * linear recurrence $S[i] = \sum_j S[i-j-1]\text{tr}[j]$,
 * given $S[0 \ldots \ge n-1]$ and $\text{tr}[0 \ldots n-1]$.
 * Faster than matrix multiplication.
 * Useful together with Berlekamp--Massey.
 * Usage: linear\_rec([0, 1], [1, 1], k) returns k'th Fibonacci number
 * Time: O(n^2 log k)
 * Status: bruteforce-tested mod 5 for n <= 5
"""

MOD = 998244353  # Use appropriate modulus

def linear_recurrence(S, tr, k, mod=MOD):
    """
    Compute k'th term of linear recurrence.
    
    Args:
        S: Initial terms [S[0], S[1], ..., S[n-1]]
        tr: Transition coefficients [tr[0], tr[1], ..., tr[n-1]]
            Such that S[i] = sum(S[i-j-1] * tr[j] for j in range(n))
        k: Which term to compute
        mod: Modulus
    
    Returns:
        S[k] mod mod
    """
    n = len(tr)
    
    def combine(a, b):
        """Multiply two polynomials mod the recurrence."""
        res = [0] * (2 * n + 1)
        for i in range(n + 1):
            for j in range(n + 1):
                res[i + j] = (res[i + j] + a[i] * b[j]) % mod
        
        # Reduce using recurrence relation
        for i in range(2 * n, n, -1):
            for j in range(n):
                res[i - 1 - j] = (res[i - 1 - j] + res[i] * tr[j]) % mod
        
        return res[:n + 1]
    
    # Initialize polynomials
    pol = [0] * (n + 1)
    e = [0] * (n + 1)
    pol[0] = 1
    e[1] = 1
    
    k += 1
    
    # Binary exponentiation
    while k > 0:
        if k % 2 == 1:
            pol = combine(pol, e)
        e = combine(e, e)
        k //= 2
    
    # Compute result
    res = 0
    for i in range(n):
        res = (res + pol[i + 1] * S[i]) % mod
    
    return res

# Example usage:
# Fibonacci: S[n] = S[n-1] + S[n-2]
# fib_k = linear_recurrence([0, 1], [1, 1], k)
# This computes the k'th Fibonacci number efficiently
