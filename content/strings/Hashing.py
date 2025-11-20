"""
 * Author: Simon Lindholm
 * Date: 2015-03-15
 * License: CC0
 * Source: own work
 * Description: Self-explanatory methods for string hashing.
 * Status: stress-tested
"""

MOD = 2**61 - 1  # Large prime for hashing
C = 10**11 + 3   # Base for hashing

class HashInterval:
    def __init__(self, s):
        self.ha = [0] * (len(s) + 1)
        self.pw = [1] * (len(s) + 1)
        for i in range(len(s)):
            self.ha[i + 1] = (self.ha[i] * C + ord(s[i])) % MOD
            self.pw[i + 1] = (self.pw[i] * C) % MOD
    
    def hashInterval(self, a, b):
        # hash [a, b)
        return (self.ha[b] - self.ha[a] * self.pw[b - a]) % MOD

def getHashes(s, length):
    if len(s) < length:
        return []
    h = 0
    pw = 1
    for i in range(length):
        h = (h * C + ord(s[i])) % MOD
        pw = (pw * C) % MOD
    ret = [h]
    for i in range(length, len(s)):
        h = (h * C + ord(s[i]) - pw * ord(s[i - length])) % MOD
        ret.append(h)
    return ret
