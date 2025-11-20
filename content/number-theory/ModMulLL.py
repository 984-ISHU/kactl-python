"""
 * Author: chilli, Ramchandra Apte, Noam527, Simon Lindholm
 * Date: 2019-04-24
 * License: CC0
 * Source: https://github.com/RamchandraApte/OmniTemplate/blob/master/src/number_theory/modulo.hpp
 * Description: Calculate $a \cdot b \bmod c$ (or $a^b \bmod c$) for $0 \le a, b \le c \le 7.2 \cdot 10^{18}$.
 * Time: O(1) for modmul, $O(\log b)$ for modpow
 * Status: stress-tested, proven correct
 * Details:
 * Python's built-in pow(a, b, c) is efficient, but this provides explicit modmul.
 * For very large numbers, Python handles arbitrary precision natively.
"""

def modmul(a, b, m):
    """Fast modular multiplication: (a * b) % m"""
    return (a * b) % m

def modpow(b, e, mod):
    """Fast modular exponentiation: b^e % mod"""
    return pow(b, e, mod)  # Python's built-in is optimized

# Example usage:
# result = modmul(123456789012345, 987654321098765, 1000000007)
# power = modpow(2, 100, 1000000007)
