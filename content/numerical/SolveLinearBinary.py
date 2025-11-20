"""
 * Author: Simon Lindholm
 * Date: 2016-08-27
 * License: CC0
 * Source: own work
 * Description: Solves $Ax = b$ over $\mathbb{F}_2$. If there are multiple solutions, one is returned arbitrarily.
 * Returns rank, or -1 if no solutions. Destroys $A$ and $b$.
 * Time: O(n^2 m)
 * Status: bruteforce-tested for n, m <= 4
"""

def solve_linear_binary(A, b, m):
    """
    Solve linear system over F_2 (binary field).
    
    Args:
        A: List of integers representing bitsets (rows of matrix)
        b: List of bits (0 or 1)
        m: Number of variables
    
    Returns:
        Tuple (rank, solution_bitset) or (-1, None) if no solution
    """
    n = len(A)
    col = list(range(m))
    rank = 0
    
    for i in range(n):
        # Find pivot
        br = None
        for r in range(i, n):
            if A[r] != 0:
                br = r
                break
        
        if br is None:
            # Check if system is inconsistent
            for j in range(i, n):
                if b[j]:
                    return -1, None
            break
        
        # Find first set bit >= i
        bc = i
        while bc < m and not (A[br] & (1 << bc)):
            bc += 1
        
        if bc >= m:
            break
        
        # Swap rows
        A[i], A[br] = A[br], A[i]
        b[i], b[br] = b[br], b[i]
        
        # Swap columns logically
        col[i], col[bc] = col[bc], col[i]
        for j in range(n):
            bit_i = (A[j] >> i) & 1
            bit_bc = (A[j] >> bc) & 1
            if bit_i != bit_bc:
                A[j] ^= (1 << i)
                A[j] ^= (1 << bc)
        
        # Eliminate
        for j in range(i + 1, n):
            if A[j] & (1 << i):
                b[j] ^= b[i]
                A[j] ^= A[i]
        
        rank += 1
    
    # Back substitution
    x = 0
    for i in range(rank - 1, -1, -1):
        if b[i]:
            x |= (1 << col[i])
            for j in range(i):
                if A[j] & (1 << i):
                    b[j] ^= 1
    
    return rank, x

# Example usage:
# A = [0b110, 0b101, 0b011]  # 3x3 binary matrix
# b = [1, 0, 1]
# rank, solution = solve_linear_binary(A, b, 3)
