"""
 * Author: Ulf Lundstrom
 * Date: 2009-04-17
 * License: CC0
 * Source: Numeriska algoritmer med matlab, Gerd Eriksson, NADA, KTH
 * Description: Finds the argument minimizing the function $f$ in the interval $[a,b]$
 * assuming $f$ is unimodal on the interval, i.e. has only one local minimum and no local
 * maximum. The maximum error in the result is $\epsilon$. Works equally well for maximization
 * with a small change in the code.
 * Usage:
 * def func(x): return 4+x+.3*x*x
 * xmin = golden\_section\_search(-1000,1000,func)
 * Time: O(log((b-a) / eps))
 * Status: tested
"""

import math

def golden_section_search(a, b, f, eps=1e-7):
    """
    Find minimum of unimodal function using golden section search.
    
    Args:
        a, b: Search interval [a, b]
        f: Function to minimize
        eps: Desired precision
    
    Returns:
        x value that minimizes f(x) in [a, b]
    """
    r = (math.sqrt(5) - 1) / 2  # Golden ratio conjugate
    
    x1 = b - r * (b - a)
    x2 = a + r * (b - a)
    f1 = f(x1)
    f2 = f(x2)
    
    while b - a > eps:
        if f1 < f2:  # Change to > to find maximum
            b = x2
            x2 = x1
            f2 = f1
            x1 = b - r * (b - a)
            f1 = f(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + r * (b - a)
            f2 = f(x2)
    
    return a

# Example usage:
# def func(x):
#     return 4 + x + 0.3 * x * x
# xmin = golden_section_search(-1000, 1000, func)
