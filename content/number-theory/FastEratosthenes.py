"""
 * Author: Jakob Kogler, chilli, pajenegod
 * Date: 2020-04-12
 * License: CC0
 * Description: Prime sieve for generating all primes smaller than LIM.
 * Time: LIM=1e9 $\approx$ 1.5s
 * Status: Stress-tested
 * Details: Despite its n log log n complexity, segmented sieve is still faster
 * than other options, including bitset sieves and linear sieves. This is
 * primarily due to its low memory usage, which reduces cache misses. This
 * implementation skips even numbers.
"""

def eratosthenes(lim):
    """Generate all primes smaller than lim using segmented sieve"""
    if lim <= 2:
        return []
    
    s = int(lim ** 0.5) + 1
    r = lim // 2
    
    # Small sieve up to sqrt(lim)
    sieve = [False] * (s + 1)
    primes = [2]
    cp = []  # (prime, index) pairs
    
    for i in range(3, s + 1, 2):
        if not sieve[i]:
            cp.append([i, i * i // 2])
            for j in range(i * i, s + 1, 2 * i):
                sieve[j] = True
    
    # Segmented sieve
    for L in range(1, r + 1, s):
        block = [False] * s
        for p_idx in range(len(cp)):
            p, idx = cp[p_idx]
            while idx < s + L:
                if idx >= L:
                    block[idx - L] = True
                idx += p
            cp[p_idx][1] = idx
        
        for i in range(min(s, r - L)):
            if not block[i]:
                primes.append((L + i) * 2 + 1)
    
    return primes

# Example usage:
# primes = eratosthenes(1000000)  # All primes < 1 million
