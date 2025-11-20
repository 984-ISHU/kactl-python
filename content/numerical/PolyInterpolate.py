"""
 * Author: Simon Lindholm
 * Date: 2017-05-10
 * License: CC0
 * Source: Wikipedia
 * Description: Given $n$ points (x[i], y[i]), computes an n-1-degree polynomial $p$ that
 * passes through them: $p(x) = a[0]*x^0 + ... + a[n-1]*x^{n-1}$.
 * For numerical precision, pick $x[k] = c*\cos(k/(n-1)*\pi), k=0 \dots n-1$.
 * Time: O(n^2)
"""

def interpolate(x, y):
    """
    Compute polynomial passing through given points using Lagrange interpolation.
    
    Args:
        x: List of x-coordinates
        y: List of y-coordinates
    
    Returns:
        List of polynomial coefficients [a0, a1, ..., a_{n-1}]
    """
    n = len(x)
    res = [0.0] * n
    temp = [0.0] * n
    
    # Compute divided differences
    for k in range(n - 1):
        for i in range(k + 1, n):
            y[i] = (y[i] - y[k]) / (x[i] - x[k])
    
    # Build polynomial
    last = 0.0
    temp[0] = 1.0
    
    for k in range(n):
        for i in range(n):
            res[i] += y[k] * temp[i]
            last, temp[i] = temp[i], temp[i] - last * x[k]
    
    return res

# Example usage:
# x = [0, 1, 2]
# y = [1, 3, 7]
# coeffs = interpolate(x, y)  # Find polynomial through these points
