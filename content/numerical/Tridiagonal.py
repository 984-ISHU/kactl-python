"""
 * Author: Ulf Lundstrom, Simon Lindholm
 * Date: 2009-08-15
 * License: CC0
 * Source: https://en.wikipedia.org/wiki/Tridiagonal\_matrix\_algorithm
 * Description: Solves tridiagonal system of equations efficiently.
 * Useful for solving problems like $a_i=b_ia_{i-1}+c_ia_{i+1}+d_i$.
 * Time: O(N)
 * Status: Brute-force tested
"""

def tridiagonal(diag, super_diag, sub_diag, b):
    """
    Solve tridiagonal system.
    
    Args:
        diag: Main diagonal
        super_diag: Super-diagonal (above main)
        sub_diag: Sub-diagonal (below main)
        b: Right-hand side
    
    Returns:
        Solution vector
    """
    n = len(b)
    diag = diag[:]
    b = b[:]
    tr = [0] * n
    
    # Forward elimination
    for i in range(n - 1):
        if abs(diag[i]) < 1e-9 * abs(super_diag[i]):
            # Special case: diag[i] ~ 0
            b[i + 1] -= b[i] * diag[i + 1] / super_diag[i]
            if i + 2 < n:
                b[i + 2] -= b[i] * sub_diag[i + 1] / super_diag[i]
            diag[i + 1] = sub_diag[i]
            i += 1
            tr[i] = 1
        else:
            diag[i + 1] -= super_diag[i] * sub_diag[i] / diag[i]
            b[i + 1] -= b[i] * sub_diag[i] / diag[i]
    
    # Back substitution
    for i in range(n - 1, -1, -1):
        if tr[i]:
            b[i], b[i - 1] = b[i - 1], b[i]
            diag[i - 1] = diag[i]
            b[i] /= super_diag[i - 1]
        else:
            b[i] /= diag[i]
            if i > 0:
                b[i - 1] -= b[i] * super_diag[i - 1]
    
    return b

# Example usage:
# diag = [2, 2, 2]
# super_d = [1, 1]
# sub_d = [1, 1]
# b = [1, 2, 1]
# solution = tridiagonal(diag, super_d, sub_d, b)
