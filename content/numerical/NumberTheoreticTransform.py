"""
 * Author: chilli
 * Date: 2019-04-16
 * License: CC0
 * Source: based on KACTL's FFT
 * Description: ntt(a) computes $\hat f(k) = \sum_x a[x] g^{xk}$ for all $k$, where $g=\text{root}^{(\text{mod}-1)/N}$.
 * N must be a power of 2.
 * Useful for convolution modulo specific nice primes of the form $2^a b+1$,
 * where the convolution result has size at most $2^a$. For arbitrary modulo, see FFTMod.
 * conv(a, b) = c, where $c[x] = \sum a[i]b[x-i]$.
 * For manual convolution: NTT the inputs, multiply
 * pointwise, divide by n, reverse(start+1, end), NTT back.
 * Inputs must be in [0, mod).
 * Time: O(N log N)
 * Status: stress-tested
"""

MOD = (119 << 23) + 1  # 998244353
ROOT = 62
# For p < 2^30 there is also e.g. 5 << 25, 7 << 26, 479 << 21
# and 483 << 21 (same root). The last two are > 10^9.

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

def ntt(a):
    """
    Compute Number Theoretic Transform in-place.
    
    Args:
        a: List of integers in [0, MOD) (length must be power of 2)
    """
    n = len(a)
    if n <= 1:
        return
    
    L = n.bit_length() - 1
    
    # Initialize roots (cached)
    if not hasattr(ntt, 'rt') or len(ntt.rt) < n:
        ntt.rt = [1] * n
        k = 2
        s = 2
        while k < n:
            z = [1, mod_pow(ROOT, MOD >> s, MOD)]
            for i in range(k, 2 * k):
                ntt.rt[i] = ntt.rt[i // 2] * z[i & 1] % MOD
            k *= 2
            s += 1
    
    # Bit-reversal permutation
    rev = [0] * n
    for i in range(n):
        rev[i] = (rev[i // 2] | (i & 1) << L) // 2
        if i < rev[i]:
            a[i], a[rev[i]] = a[rev[i]], a[i]
    
    # Cooley-Tukey NTT
    k = 1
    while k < n:
        for i in range(0, n, 2 * k):
            for j in range(k):
                z = ntt.rt[j + k] * a[i + j + k] % MOD
                a[i + j + k] = (a[i + j] - z + (MOD if z > a[i + j] else 0)) % MOD
                a[i + j] = (a[i + j] + z) % MOD
                if a[i + j] >= MOD:
                    a[i + j] -= MOD
        k *= 2

def ntt_conv(a, b):
    """
    Compute convolution modulo MOD using NTT.
    
    Args:
        a, b: Lists of integers in [0, MOD)
    
    Returns:
        List where res[x] = sum(a[i] * b[x-i]) mod MOD
    """
    if not a or not b:
        return []
    
    s = len(a) + len(b) - 1
    B = (s - 1).bit_length()
    n = 1 << B
    
    inv = mod_pow(n, MOD - 2, MOD)
    
    # Pad to power of 2
    L = list(a) + [0] * (n - len(a))
    R = list(b) + [0] * (n - len(b))
    
    ntt(L)
    ntt(R)
    
    out = [0] * n
    for i in range(n):
        out[(-i) & (n - 1)] = L[i] * R[i] % MOD * inv % MOD
    
    ntt(out)
    
    return out[:s]

# Example usage:
# a = [1, 2, 3]
# b = [4, 5, 6]
# result = ntt_conv(a, b)  # Convolution mod 998244353
