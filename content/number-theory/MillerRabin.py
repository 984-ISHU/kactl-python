"""
 * Author: chilli, c1729, Simon Lindholm
 * Date: 2019-03-28
 * License: CC0
 * Source: Wikipedia, https://miller-rabin.appspot.com/
 * Description: Deterministic Miller-Rabin primality test.
 * Guaranteed to work for numbers up to $7 \cdot 10^{18}$; for larger numbers, use Python's built-in or extend A randomly.
 * Time: 7 times the complexity of $a^b \bmod c$.
 * Status: Stress-tested
"""

def modmul(a, b, mod):
    return (a * b) % mod

def modpow(a, b, mod):
    res = 1
    a %= mod
    while b:
        if b & 1:
            res = modmul(res, a, mod)
        a = modmul(a, a, mod)
        b >>= 1
    return res

def isPrime(n):
    if n < 2 or (n % 6) % 4 != 1:
        return (n | 1) == 3
    A = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    s = (n - 1) & -(n - 1)  # count trailing zeroes
    s = s.bit_length() - 1
    d = (n - 1) >> s
    for a in A:
        p = modpow(a % n, d, n)
        i = s
        while p != 1 and p != n - 1 and a % n and i:
            p = modmul(p, p, n)
            i -= 1
        if p != n - 1 and i != s:
            return False
    return True

# Note: Python 3.8+ has math.gcd and for primality testing,
# sympy.isprime() or gmpy2.is_prime() are also available
