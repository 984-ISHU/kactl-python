"""
 * Author: Max Bennedich
 * Date: 2004-02-08
 * Description: Invert matrix $A$. Returns rank; result is stored in $A$ unless singular (rank < n).
 * Can easily be extended to prime moduli; for prime powers, repeatedly
 * set $A^{-1} = A^{-1} (2I - AA^{-1}) (\text{mod }p^k)$ where $A^{-1}$ starts as
 * the inverse of A mod p, and k is doubled in each step.
 * Time: O(n^3)
 * Status: Slightly tested
"""

def matrix_inverse(A):
    """
    Invert matrix A in-place using Gauss-Jordan elimination.
    
    Args:
        A: Square matrix (list of lists). Will contain inverse if successful.
    
    Returns:
        Rank of matrix (n if invertible, < n if singular)
    """
    n = len(A)
    col = list(range(n))
    
    # Create augmented matrix [A | I]
    tmp = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    for i in range(n):
        # Find pivot
        r, c = i, i
        for j in range(i, n):
            for k in range(i, n):
                if abs(A[j][k]) > abs(A[r][c]):
                    r, c = j, k
        
        # Check if singular
        if abs(A[r][c]) < 1e-12:
            return i
        
        # Swap rows
        A[i], A[r] = A[r], A[i]
        tmp[i], tmp[r] = tmp[r], tmp[i]
        
        # Swap columns
        for j in range(n):
            A[j][i], A[j][c] = A[j][c], A[j][i]
            tmp[j][i], tmp[j][c] = tmp[j][c], tmp[j][i]
        
        col[i], col[c] = col[c], col[i]
        
        # Eliminate
        v = A[i][i]
        for j in range(i + 1, n):
            f = A[j][i] / v
            A[j][i] = 0
            for k in range(i + 1, n):
                A[j][k] -= f * A[i][k]
            for k in range(n):
                tmp[j][k] -= f * tmp[i][k]
        
        # Scale pivot row
        for j in range(i + 1, n):
            A[i][j] /= v
        for j in range(n):
            tmp[i][j] /= v
        A[i][i] = 1
    
    # Back substitution
    for i in range(n - 1, 0, -1):
        for j in range(i):
            v = A[j][i]
            for k in range(n):
                tmp[j][k] -= v * tmp[i][k]
    
    # Reorder columns
    for i in range(n):
        for j in range(n):
            A[col[i]][col[j]] = tmp[i][j]
    
    return n

# Example usage:
# A = [[1, 2], [3, 4]]
# rank = matrix_inverse(A)
# if rank == len(A):
#     print("Inverse:", A)
# else:
#     print("Matrix is singular")
