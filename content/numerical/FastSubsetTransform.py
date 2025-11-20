"""
 * Author: Lucian Bicsi
 * Date: 2015-06-25
 * License: GNU Free Documentation License 1.2
 * Source: csacademy
 * Description: Transform to a basis with fast convolutions of the form
 * $\displaystyle c[z] = \sum\nolimits_{z = x \oplus y} a[x] \cdot b[y]$,
 * where $\oplus$ is one of AND, OR, XOR. The size of $a$ must be a power of two.
 * Time: O(N log N)
 * Status: stress-tested
"""

def fst(a, inv, op='AND'):
    """
    Fast Subset Transform.
    
    Args:
        a: Input array (size must be power of 2). Modified in-place.
        inv: True for inverse transform
        op: 'AND', 'OR', or 'XOR'
    """
    n = len(a)
    step = 1
    
    while step < n:
        for i in range(0, n, 2 * step):
            for j in range(i, i + step):
                u, v = a[j], a[j + step]
                
                if op == 'AND':
                    if inv:
                        a[j], a[j + step] = v - u, u
                    else:
                        a[j], a[j + step] = v, u + v
                elif op == 'OR':
                    if inv:
                        a[j], a[j + step] = v, u - v
                    else:
                        a[j], a[j + step] = u + v, u
                elif op == 'XOR':
                    a[j], a[j + step] = u + v, u - v
        
        step *= 2
    
    # XOR requires division by n for inverse
    if inv and op == 'XOR':
        for i in range(n):
            a[i] //= n

def subset_conv(a, b, op='AND'):
    """
    Compute subset convolution.
    
    Args:
        a, b: Input arrays (size must be power of 2)
        op: 'AND', 'OR', or 'XOR'
    
    Returns:
        Convolution result
    """
    a = a[:]
    b = b[:]
    
    fst(a, False, op)
    fst(b, False, op)
    
    for i in range(len(a)):
        a[i] *= b[i]
    
    fst(a, True, op)
    return a

# Example usage:
# a = [1, 2, 3, 4]  # Size must be power of 2
# b = [5, 6, 7, 8]
# result = subset_conv(a, b, 'XOR')
