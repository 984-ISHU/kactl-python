"""
 * Author: Ludo Pulles, chilli, Simon Lindholm
 * Date: 2019-01-09
 * License: CC0
 * Source: http://neerc.ifmo.ru/trains/toulouse/2017/fft2.pdf
 * Description: fft(a) computes $\hat f(k) = \sum_x a[x] \exp(2\pi i \cdot k x / N)$ for all $k$. N must be a power of 2.
 * Useful for convolution: conv(a, b) = c, where $c[x] = \sum a[i]b[x-i]$.
 * For convolution of complex numbers or more than two vectors: FFT, multiply
 * pointwise, divide by n, reverse(start+1, end), FFT back.
 * Rounding is safe if $(\sum a_i^2 + \sum b_i^2)\log_2{N} < 9\cdot10^{14}$
 * (in practice $10^{16}$; higher for random inputs).
 * Otherwise, use NTT/FFTMod.
 * Time: O(N log N) with N = |A|+|B|
 * Status: somewhat tested
"""

import cmath
import math

def fft(a):
    """
    Compute Fast Fourier Transform in-place.
    
    Args:
        a: List of complex numbers (length must be power of 2)
    """
    n = len(a)
    if n <= 1:
        return
    
    L = n.bit_length() - 1
    
    # Initialize roots of unity (cached)
    if not hasattr(fft, 'rt') or len(fft.rt) < n:
        fft.rt = [1] * n
        k = 2
        while k < n:
            x = cmath.exp(1j * cmath.pi / k)
            for i in range(k, 2 * k):
                fft.rt[i] = fft.rt[i // 2] * x if i & 1 else fft.rt[i // 2]
            k *= 2
    
    # Bit-reversal permutation
    rev = [0] * n
    for i in range(n):
        rev[i] = (rev[i // 2] | (i & 1) << L) // 2
        if i < rev[i]:
            a[i], a[rev[i]] = a[rev[i]], a[i]
    
    # Cooley-Tukey FFT
    k = 1
    while k < n:
        for i in range(0, n, 2 * k):
            for j in range(k):
                z = fft.rt[j + k] * a[i + j + k]
                a[i + j + k] = a[i + j] - z
                a[i + j] += z
        k *= 2

def conv(a, b):
    """
    Compute convolution of two sequences using FFT.
    
    Args:
        a, b: Lists of real numbers
    
    Returns:
        List where res[x] = sum(a[i] * b[x-i])
    """
    if not a or not b:
        return []
    
    res_size = len(a) + len(b) - 1
    L = (res_size - 1).bit_length()
    n = 1 << L
    
    # Pack a and b into complex array
    in_arr = [complex(a[i] if i < len(a) else 0, 
                     b[i] if i < len(b) else 0) for i in range(n)]
    
    fft(in_arr)
    
    # Pointwise multiplication trick
    for i in range(n):
        in_arr[i] *= in_arr[i]
    
    out = [in_arr[(-i) & (n - 1)] - in_arr[i].conjugate() for i in range(n)]
    
    fft(out)
    
    res = [out[i].imag / (4 * n) for i in range(res_size)]
    return res

# Example usage:
# a = [1, 2, 3]
# b = [4, 5, 6]
# result = conv(a, b)  # Convolution of a and b
