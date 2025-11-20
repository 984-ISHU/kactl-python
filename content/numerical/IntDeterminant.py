"""
 * Author: Unknown
 * Date: 2014-11-27
 * Source: somewhere on github
 * Description: Calculates determinant using modular arithmetics.
 * Modulos can also be removed to get a pure-integer version.
 * Time: O(N^3)
 * Status: bruteforce-tested for N <= 3, mod <= 7
"""

MOD = 12345

def int_determinant(a, mod=MOD):
    """
    Calculate determinant using integer/modular arithmetic.
    
    Args:
        a: Square matrix (list of lists). Will be modified.
        mod: Modulus (set to None for pure integer version)
    
    Returns:
        Determinant value (mod mod if mod is provided)
    """
    n = len(a)
    ans = 1
    
    for i in range(n):
        # GCD-based elimination
        for j in range(i + 1, n):
            while a[j][i] != 0:
                # Euclidean algorithm step
                t = a[i][i] // a[j][i]
                if t != 0:
                    for k in range(i, n):
                        a[i][k] = (a[i][k] - a[j][k] * t)
                        if mod:
                            a[i][k] %= mod
                
                # Swap rows
                a[i], a[j] = a[j], a[i]
                ans *= -1
        
        if mod:
            ans = ans * a[i][i] % mod
        else:
            ans = ans * a[i][i]
        
        if ans == 0:
            return 0
    
    if mod:
        return (ans + mod) % mod
    return ans

# Example usage:
# mat = [[1, 2], [3, 4]]
# det = int_determinant(mat, mod=1000000007)
