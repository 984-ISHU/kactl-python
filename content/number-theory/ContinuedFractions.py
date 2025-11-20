"""
 * Author: Unknown
 * Date: 2002-09-15
 * Source: predates tinyKACTL
 * Description: Computes the continued fraction representation of a number, i.e., the sequence $\{a_1,a_2,a_3,\dots\}$ such that $x = a_1+1/(a_2+1/(a_3+\dots))$.
 * Usage: convergent(a, n) computes the $n$'th convergent, i.e. $a_1 + 1/(a_2 + 1/(\dots + 1/a_n))$.
 * Time: $O(N\log M)$ where $N$ is the length of the continued fraction and $M$ is the largest value.
 * Status: Tested on SPOJ FACT0/FACT1, stress-tested
"""

from fractions import Fraction

def to_continued_fraction(x, y):
    """
    Returns the continued fraction representation [a0, a1, a2, ...]
    for the rational number x/y.
    """
    result = []
    while y != 0:
        result.append(x // y)
        x, y = y, x % y
    return result

def convergent(a, n):
    """
    Compute the nth convergent of continued fraction a.
    Returns a Fraction object representing the convergent.
    a is a list of continued fraction coefficients.
    """
    if n < 0 or n >= len(a):
        return None
    
    # Compute convergent using recurrence relation
    # p_-1 = 1, p_0 = a_0
    # q_-1 = 0, q_0 = 1
    # p_n = a_n * p_{n-1} + p_{n-2}
    # q_n = a_n * q_{n-1} + q_{n-2}
    
    if n == 0:
        return Fraction(a[0], 1)
    
    p_prev2, p_prev1 = 1, a[0]
    q_prev2, q_prev1 = 0, 1
    
    for i in range(1, n + 1):
        p = a[i] * p_prev1 + p_prev2
        q = a[i] * q_prev1 + q_prev2
        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q
    
    return Fraction(p_prev1, q_prev1)

# Example usage:
# cf = to_continued_fraction(649, 200)  # [3, 4, 12, 4]
# c = convergent(cf, 2)  # Fraction(649/200) approximation using first 3 terms
