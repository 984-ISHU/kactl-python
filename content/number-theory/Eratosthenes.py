"""
 * Author: Håkan Terelius
 * Date: 2009-08-26
 * License: CC0
 * Source: http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
 * Description: Prime sieve for generating all primes up to a certain limit.
 * Time: lim=100'000'000 approx 0.8 s. Runs 30% faster if only odd indices are stored.
 * Status: Tested
"""

def eratosthenesSieve(lim):
    if lim <= 2:
        return []
    isprime = [True] * lim
    isprime[0] = isprime[1] = False
    for i in range(4, lim, 2):
        isprime[i] = False
    i = 3
    while i * i < lim:
        if isprime[i]:
            for j in range(i * i, lim, i * 2):
                isprime[j] = False
        i += 2
    pr = [i for i in range(2, lim) if isprime[i]]
    return pr
