"""
 * Author: Per Austrin
 * Date: 2004-02-08
 * License: CC0
 * Description: Finds the real roots to a polynomial.
 * Usage: poly\_roots(p, xmin, xmax)
 * Time: O(n^2)
"""

def poly_roots(p, xmin, xmax):
    """
    Find all real roots of polynomial in interval [xmin, xmax].
    
    Args:
        p: Polynomial object
        xmin, xmax: Search interval
    
    Returns:
        List of roots
    """
    # Base case: linear polynomial
    if len(p.a) == 2:
        return [-p.a[0] / p.a[1]]
    
    ret = []
    
    # Find derivative roots
    der = Polynomial(p.a[:])
    der.differentiate()
    dr = poly_roots(der, xmin, xmax)
    
    # Add boundary points
    dr.append(xmin - 1)
    dr.append(xmax + 1)
    dr.sort()
    
    # Check each interval between critical points
    for i in range(len(dr) - 1):
        l, h = dr[i], dr[i + 1]
        sign = p(l) > 0
        
        # If signs differ, there's a root
        if sign != (p(h) > 0):
            # Binary search for root
            for _ in range(60):  # Sufficient for double precision
                m = (l + h) / 2
                f = p(m)
                if (f <= 0) != sign:
                    l = m
                else:
                    h = m
            ret.append((l + h) / 2)
    
    return ret

# Example usage (requires Polynomial class):
# from Polynomial import Polynomial
# p = Polynomial([2, -3, 1])  # x^2 - 3x + 2
# roots = poly_roots(p, -1e9, 1e9)
