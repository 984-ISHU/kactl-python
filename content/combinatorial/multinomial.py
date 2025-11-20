"""
 * Author: Mattias de Zalenski, Fredrik Niemelä, Per Austrin, Simon Lindholm
 * Date: 2002-09-26
 * Source: Max Bennedich
 * Description: Computes {k\_1 + ... + k_n choose k\_1, k\_2, ..., k_n} = (sum k_i)! / (k\_1! k\_2! ... k_n!).
 * Status: Tested on kattis:lexicography
"""

def multinomial(v):
    if not v:
        return 1
    c = 1
    m = v[0]
    for i in range(1, len(v)):
        for j in range(v[i]):
            m += 1
            c = c * m // (j + 1)
    return c
