"""
 * Author: Simon Lindholm
 * Date: 2016-07-24
 * License: CC0
 * Source: Russian page
 * Description: Pre-computation of modular inverses. Assumes LIM $\le$ mod and that mod is a prime.
 * Status: Works
"""

def precompute_inverses(mod, lim):
    """Precompute modular inverses from 1 to lim-1 modulo mod (prime)"""
    inv = [0, 1]  # inv[0] is undefined, inv[1] = 1
    for i in range(2, lim):
        inv.append(mod - (mod // i) * inv[mod % i] % mod)
    return inv

# Example usage:
# mod = 1000000007
# lim = 200000
# inv = precompute_inverses(mod, lim)
# Now inv[i] is the modular inverse of i modulo mod
