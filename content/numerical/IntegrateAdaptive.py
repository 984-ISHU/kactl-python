"""
 * Author: Simon Lindholm
 * Date: 2015-02-11
 * License: CC0
 * Source: Wikipedia
 * Description: Fast integration using an adaptive Simpson's rule.
 * Usage:
 * sphere\_volume = quad\_adaptive(-1, 1, lambda x: 
 *     quad\_adaptive(-1, 1, lambda y:
 *         quad\_adaptive(-1, 1, lambda z:
 *             int(x*x + y*y + z*z < 1))))
 * Status: mostly untested
"""

def _simpson(f, a, b):
    """Simpson's rule for interval [a, b]."""
    return (f(a) + 4 * f((a + b) / 2) + f(b)) * (b - a) / 6

def _adaptive_rec(f, a, b, eps, S):
    """Recursive adaptive integration."""
    c = (a + b) / 2
    S1 = _simpson(f, a, c)
    S2 = _simpson(f, c, b)
    T = S1 + S2
    
    if abs(T - S) <= 15 * eps or b - a < 1e-10:
        return T + (T - S) / 15
    
    return _adaptive_rec(f, a, c, eps / 2, S1) + _adaptive_rec(f, c, b, eps / 2, S2)

def quad_adaptive(a, b, f, eps=1e-8):
    """
    Integrate function adaptively using Simpson's rule.
    
    Args:
        a, b: Integration bounds
        f: Function to integrate
        eps: Desired precision
    
    Returns:
        Approximate integral value
    """
    return _adaptive_rec(f, a, b, eps, _simpson(f, a, b))

# Example usage:
# import math
# result = quad_adaptive(0, math.pi, math.sin, eps=1e-8)
