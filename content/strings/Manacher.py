"""
 * Author: User adamant on CodeForces
 * Source: http://codeforces.com/blog/entry/12143
 * Description: For each position in a string, computes p[0][i] = half length of
 * longest even palindrome around pos i, p[1][i] = longest odd (half rounded down).
 * Time: O(N)
 * Status: Stress-tested
"""

def manacher(s):
    """
    Find all palindromes in string.
    Returns [even_palindromes, odd_palindromes]
    p[0][i] = half-length of longest even palindrome centered between i-1 and i
    p[1][i] = half-length of longest odd palindrome centered at i
    """
    n = len(s)
    p = [[0] * (n + 1), [0] * n]
    
    for z in range(2):
        l = r = 0
        for i in range(n):
            t = r - i + (1 - z)
            if i < r:
                p[z][i] = min(t, p[z][l + t])
            
            L = i - p[z][i]
            R = i + p[z][i] - (1 - z)
            
            while L >= 1 and R + 1 < n and s[L - 1] == s[R + 1]:
                p[z][i] += 1
                L -= 1
                R += 1
            
            if R > r:
                l, r = L, R
    
    return p

# Example usage:
# even, odd = manacher("abacaba")
# odd[3] gives half-length of palindrome centered at index 3
