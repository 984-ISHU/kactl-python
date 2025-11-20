"""
 * Author: Håkan Terelius
 * Date: 2009-09-25
 * License: CC0
 * Source: http://en.wikipedia.org/wiki/Euler's_totient_function
 * Description: Euler's phi function is defined as phi(n):=\# of positive integers <= n that are coprime with n.
 * phi(1)=1, p prime => phi(p\^{}k)=(p-1)p\^{}{k-1}, m,n coprime => phi(mn)=phi(m)phi(n).
 * If n=p\_1\^{}{k\_1}p\_2\^{}{k\_2} ... p\_r\^{}{k\_r} then phi(n) = (p\_1-1)p\_1\^{}{k\_1-1}...(p\_r-1)p\_r\^{}{k\_r-1}.
 * phi(n)=n * product\_{p|n}(1-1/p).
 
 * sum\_{d|n} phi(d) = n, sum\_{1<= k <= n, gcd(k,n)=1} k = n phi(n)/2, n>1
 
 * Euler's thm: a,n coprime => a\^{}{phi(n)} == 1 (mod n).
 
 * Fermat's little thm: p prime => a\^{}{p-1} == 1 (mod p) for all a.
 * Status: Tested
"""

def calculatePhi(LIM):
    phi = list(range(LIM))
    for i in range(0, LIM):
        if i & 1:
            phi[i] = i
        else:
            phi[i] = i // 2
    for i in range(3, LIM, 2):
        if phi[i] == i:  # i is prime
            for j in range(i, LIM, i):
                phi[j] -= phi[j] // i
    return phi

# For single value:
def phi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result
