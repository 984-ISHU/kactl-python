"""
 * Author: Simon Lindholm
 * Date: 2016-12-09
 * License: CC0
 * Source: http://www.mimuw.edu.pl/~mucha/pub/mucha\_sankowski\_focs04.pdf
 * Description: Matching for general graphs using Tutte matrix and matrix inverse.
 * Fails with probability $N / \text{mod}$.
 * Time: $O(N^3)$
 * Status: not very well tested
"""

import random

MOD = 998244353  # Large prime for modular arithmetic

def mod_pow(base, exp, mod):
    """Modular exponentiation."""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

def matrix_inverse_mod(A, mod):
    """
    Compute rank of matrix using Gaussian elimination modulo a prime.
    Returns the rank.
    """
    n = len(A)
    m = len(A[0]) if n > 0 else 0
    
    # Create augmented matrix with identity
    aug = [row[:] + [1 if i == j else 0 for j in range(n)] 
           for i, row in enumerate(A)]
    
    rank = 0
    for col in range(min(n, m)):
        # Find pivot
        pivot = -1
        for row in range(rank, n):
            if aug[row][col] % mod != 0:
                pivot = row
                break
        
        if pivot == -1:
            continue
        
        # Swap rows
        aug[rank], aug[pivot] = aug[pivot], aug[rank]
        
        # Scale pivot row
        inv = mod_pow(aug[rank][col], mod - 2, mod)
        for j in range(len(aug[rank])):
            aug[rank][j] = (aug[rank][j] * inv) % mod
        
        # Eliminate column
        for row in range(n):
            if row != rank and aug[row][col] != 0:
                factor = aug[row][col]
                for j in range(len(aug[row])):
                    aug[row][j] = (aug[row][j] - factor * aug[rank][j]) % mod
        
        rank += 1
    
    return rank

def general_matching(N, edges):
    """
    Find maximum matching in general graph using Tutte matrix.
    
    Args:
        N: Number of vertices
        edges: List of (u, v) tuples
    
    Returns:
        List of (u, v) pairs in the matching
    """
    # Build Tutte matrix (skew-symmetric)
    mat = [[0] * N for _ in range(N)]
    for a, b in edges:
        r = random.randint(1, MOD - 1)
        mat[a][b] = r
        mat[b][a] = (MOD - r) % MOD
    
    # Compute rank
    A = [row[:] for row in mat]
    rank = matrix_inverse_mod(A, MOD)
    
    # M = 2N - rank (number of nodes to add for perfect matching)
    M = 2 * N - rank
    assert rank % 2 == 0
    
    # If need to expand, add dummy nodes
    if M != N:
        # Add dummy nodes to make rank = N
        mat = [row + [0] * (M - N) for row in mat]
        for i in range(N, M):
            row = [0] * M
            for j in range(i):
                r = random.randint(1, MOD - 1)
                row[j] = r
                mat[j].append((MOD - r) % MOD)
            mat.append(row)
        
        # Try again with expanded matrix
        A = [row[:] for row in mat]
        new_rank = matrix_inverse_mod(A, MOD)
        if new_rank != M:
            # Randomization failed, try again
            return general_matching(N, edges)
    
    # Extract matching greedily
    has = [True] * M
    ret = []
    
    for _ in range(M // 2):
        # Find an edge in residual graph
        fi, fj = -1, -1
        for i in range(M):
            if not has[i]:
                continue
            for j in range(i + 1, M):
                if not has[j]:
                    continue
                if A[i][j] != 0 and mat[i][j] != 0:
                    fi, fj = i, j
                    break
            if fi != -1:
                break
        
        if fi == -1:
            break
        
        # Add edge to matching if both nodes are original
        if fj < N:
            ret.append((fi, fj))
        
        has[fi] = has[fj] = False
        
        # Update matrix by eliminating fi and fj
        inv = mod_pow(A[fi][fj], MOD - 2, MOD)
        for i in range(M):
            if has[i] and A[i][fj] != 0:
                factor = (A[i][fj] * inv) % MOD
                for j in range(M):
                    A[i][j] = (A[i][j] - A[fi][j] * factor) % MOD
        
        # Symmetric update
        inv = mod_pow(A[fj][fi], MOD - 2, MOD)
        for i in range(M):
            if has[i] and A[i][fi] != 0:
                factor = (A[i][fi] * inv) % MOD
                for j in range(M):
                    A[i][j] = (A[i][j] - A[fj][j] * factor) % MOD
    
    return ret

# Example usage:
# edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
# matching = general_matching(4, edges)
