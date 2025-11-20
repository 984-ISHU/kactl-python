"""
 * Author: Simon Lindholm
 * Date: 2015-02-04
 * License: CC0
 * Source: Johan Sannemo
 * Description: Poor man's optimization for unimodal functions.
 * Status: used with great success
"""

def hill_climb(start, f):
    """
    Simple hill climbing optimization for 2D functions.
    
    Args:
        start: Starting point [x, y]
        f: Function to minimize
    
    Returns:
        Tuple (min_value, [x, y])
    """
    cur = (f(start), start[:])
    
    jmp = 1e9
    while jmp > 1e-20:
        for _ in range(100):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    p = [cur[1][0] + dx * jmp, cur[1][1] + dy * jmp]
                    val = f(p)
                    if val < cur[0]:
                        cur = (val, p)
        jmp /= 2
    
    return cur

# Example usage:
# def func(p):
#     return (p[0] - 3)**2 + (p[1] + 2)**2
# min_val, min_point = hill_climb([0, 0], func)
