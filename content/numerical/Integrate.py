"""
 * Author: Simon Lindholm
 * Date: 2015-02-11
 * License: CC0
 * Source: Wikipedia
 * Description: Simple integration of a function over an interval using
 * Simpson's rule. The error should be proportional to $h^4$, although in
 * practice you will want to verify that the result is stable to desired
 * precision when epsilon changes.
 * Status: mostly untested
"""

def integrate(a, b, f, n=1000):
    """
    Integrate function over [a, b] using Simpson's rule.
    
    Args:
        a, b: Integration bounds
        f: Function to integrate
        n: Number of subdivisions (higher = more accurate)
    
    Returns:
        Approximate integral value
    """
    h = (b - a) / (2 * n)
    v = f(a) + f(b)
    
    for i in range(1, 2 * n):
        weight = 4 if i & 1 else 2
        v += f(a + i * h) * weight
    
    return v * h / 3

# Example usage:
# import math
# result = integrate(0, math.pi, math.sin, n=1000)
# Should give approximately 2.0
