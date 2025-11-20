"""
 * Author: Simon Lindholm
 * Date: 2016-09-06
 * License: CC0
 * Source: folklore
 * Description: Calculates determinant of a matrix. Destroys the matrix.
 * Time: O(N^3)
 * Status: somewhat tested
"""

def determinant(a):
    """
    Calculate determinant using Gaussian elimination.
    
    Args:
        a: Square matrix (list of lists). Will be modified.
    
    Returns:
        Determinant value
    """
    n = len(a)
    res = 1.0
    
    for i in range(n):
        # Find pivot
        b = i
        for j in range(i + 1, n):
            if abs(a[j][i]) > abs(a[b][i]):
                b = j
        
        # Swap rows
        if i != b:
            a[i], a[b] = a[b], a[i]
            res *= -1
        
        res *= a[i][i]
        if res == 0:
            return 0
        
        # Eliminate column
        for j in range(i + 1, n):
            v = a[j][i] / a[i][i]
            if v != 0:
                for k in range(i + 1, n):
                    a[j][k] -= v * a[i][k]
    
    return res

# Example usage:
# mat = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
# det = determinant(mat)
