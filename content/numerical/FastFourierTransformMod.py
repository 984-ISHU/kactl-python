"""
 * Author: chilli
 * Date: 2019-04-25
 * License: CC0
 * Source: http://neerc.ifmo.ru/trains/toulouse/2017/fft2.pdf
 * Description: Higher precision FFT, can be used for convolutions modulo arbitrary integers
 * as long as $N\log_2N\cdot \text{mod} < 8.6 \cdot 10^{14}$ (in practice $10^{16}$ or higher).
 * Inputs must be in $[0, \text{mod})$.
 * Time: O(N log N), where N = |A|+|B| (twice as slow as NTT or FFT)
 * Status: stress-tested
"""

import cmath

def fft_conv_mod(a, b, mod):
    """
    Convolve two sequences modulo an arbitrary integer using FFT.
    
    Args:
        a, b: Lists of integers in [0, mod)
        mod: Modulus
    
    Returns:
        Convolution result modulo mod
    """
    if not a or not b:
        return []
    
    from FastFourierTransform import fft
    
    res_len = len(a) + len(b) - 1
    B = (res_len - 1).bit_length()
    n = 1 << B
    cut = int(mod ** 0.5) + 1
    
    # Split numbers into high and low parts
    L = [complex(a[i] // cut if i < len(a) else 0, 
                 a[i] % cut if i < len(a) else 0) for i in range(n)]
    R = [complex(b[i] // cut if i < len(b) else 0,
                 b[i] % cut if i < len(b) else 0) for i in range(n)]
    
    fft(L)
    fft(R)
    
    # Multiply components
    outs = [0] * n
    outl = [0] * n
    
    for i in range(n):
        j = (-i) & (n - 1)
        outl[j] = (L[i] + L[j].conjugate()) * R[i] / (2.0 * n)
        outs[j] = (L[i] - L[j].conjugate()) * R[i] / (2.0 * n) / 1j
    
    fft(outl)
    fft(outs)
    
    # Reconstruct result
    res = []
    for i in range(res_len):
        av = int(outl[i].real + 0.5)
        bv = int(outl[i].imag + 0.5) + int(outs[i].real + 0.5)
        cv = int(outs[i].imag + 0.5)
        res.append(((av % mod * cut + bv) % mod * cut + cv) % mod)
    
    return res

# Example usage:
# a = [1, 2, 3]
# b = [4, 5, 6]
# result = fft_conv_mod(a, b, 1000000007)
