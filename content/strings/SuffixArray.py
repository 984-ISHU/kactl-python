"""
 * Author: 罗穗骞, chilli
 * Date: 2019-04-11
 * License: Unknown
 * Source: Suffix array - a powerful tool for dealing with strings
 * (Chinese IOI National team training paper, 2009)
 * Description: Builds suffix array for a string.
 * sa[i] is the starting index of the suffix which
 * is i'th in the sorted suffix array.
 * The returned list is of size n+1, and sa[0] = n.
 * The lcp array contains longest common prefixes for
 * neighbouring strings in the suffix array:
 * lcp[i] = lcp(sa[i], sa[i-1]), lcp[0] = 0.
 * The input string must not contain any nul chars.
 * Time: O(n \log n)
 * Status: stress-tested
"""

class SuffixArray:
    def __init__(self, s, lim=256):
        s = s + '\0'
        n = len(s)
        k = 0
        x = [ord(c) for c in s]
        y = [0] * n
        ws = [0] * max(n, lim)
        self.sa = list(range(n))
        self.lcp = [0] * n
        
        j = 0
        p = 0
        while p < n:
            p = j
            y = list(range(n - j, n)) + [0] * j
            p_idx = j
            for i in range(n):
                if self.sa[i] >= j:
                    y[p_idx] = self.sa[i] - j
                    p_idx += 1
            
            ws = [0] * lim
            for i in range(n):
                ws[x[i]] += 1
            for i in range(1, lim):
                ws[i] += ws[i - 1]
            for i in range(n - 1, -1, -1):
                ws[x[y[i]]] -= 1
                self.sa[ws[x[y[i]]]] = y[i]
            
            x, y = y, x
            p = 1
            x[self.sa[0]] = 0
            for i in range(1, n):
                a = self.sa[i - 1]
                b = self.sa[i]
                x[b] = p - 1 if (y[a] == y[b] and 
                                 a + j < n and b + j < n and
                                 y[a + j] == y[b + j]) else p
                if x[b] == p:
                    p += 1
            lim = p
            j = max(1, j * 2)
        
        # Build LCP array
        k = 0
        for i in range(n - 1):
            j_idx = self.sa[x[i] - 1]
            while i + k < n and j_idx + k < n and s[i + k] == s[j_idx + k]:
                k += 1
            self.lcp[x[i]] = k
            if k:
                k -= 1
