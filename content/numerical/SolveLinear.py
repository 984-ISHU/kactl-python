"""
 * Author: Per Austrin, Simon Lindholm
 * Date: 2004-02-08
 * License: CC0
 * Description: Solves $A \cdot x = b$. If there are multiple solutions, an arbitrary one is returned.
 * Returns rank, or -1 if no solutions. Data in $A$ and $b$ is lost.
 * Time: O(n^2 m)
 * Status: tested on kattis:equationsolver
"""

EPS = 1e-12

def solve_linear(A, b, x):
    """
    Solve linear system Ax = b using Gaussian elimination.
    
    Args:
        A: Coefficient matrix (n x m). Will be modified.
        b: Right-hand side vector (length n). Will be modified.
        x: Solution vector (length m). Will be filled.
    
    Returns:
        Rank of the system, or -1 if no solution exists
    """
    n = len(A)
    m = len(x)
    
    if n > 0:
        assert len(A[0]) == m
    
    col = list(range(m))
    rank = 0
    
    for i in range(n):
        # Find pivot
        br, bc = i, i
        bv = 0
        
        for r in range(i, n):
            for c in range(i, m):
                v = abs(A[r][c])
                if v > bv:
                    br, bc, bv = r, c, v
        
        # Check if no pivot found
        if bv <= EPS:
            # Check if system is inconsistent
            for j in range(i, n):
                if abs(b[j]) > EPS:
                    return -1
            break
        
        # Swap rows and columns
        A[i], A[br] = A[br], A[i]
        b[i], b[br] = b[br], b[i]
        col[i], col[bc] = col[bc], col[i]
        
        for j in range(n):
            A[j][i], A[j][bc] = A[j][bc], A[j][i]
        
        # Eliminate column
        bv = 1.0 / A[i][i]
        
        for j in range(i + 1, n):
            fac = A[j][i] * bv
            b[j] -= fac * b[i]
            for k in range(i + 1, m):
                A[j][k] -= fac * A[i][k]
        
        rank += 1
    
    # Back substitution
    x[:] = [0] * m
    
    for i in range(rank - 1, -1, -1):
        b[i] /= A[i][i]
        x[col[i]] = b[i]
        
        for j in range(i):
            b[j] -= A[j][i] * b[i]
    
    return rank

# Example usage:
# A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
# b = [8, -11, -3]
# x = [0, 0, 0]
# rank = solve_linear(A, b, x)
# Now x contains the solution
