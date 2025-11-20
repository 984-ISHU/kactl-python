"""
 * Author: Stjepan Glavina
 * License: Unlicense
 * Source: https://github.com/stjepang/snippets/blob/master/min_rotation.cpp
 * Description: Finds the lexicographically smallest rotation of a string.
 * Time: O(N)
 * Status: Stress-tested
"""

def min_rotation(s):
    """
    Find starting index of lexicographically smallest rotation.
    Use s = s[i:] + s[:i] to get the actual rotation.
    """
    n = len(s)
    s = s + s  # Duplicate string
    a = 0
    
    b = 0
    while b < n:
        k = 0
        while k < n:
            if a + k == b or s[a + k] < s[b + k]:
                b += max(0, k - 1)
                break
            if s[a + k] > s[b + k]:
                a = b
                break
            k += 1
        else:
            break
        b += 1
    
    return a

# Example usage:
# s = "bcaab"
# i = min_rotation(s)
# rotated = s[i:] + s[:i]  # "aabbc"
