"""
 * Author: Simon Lindholm, chilli
 * Date: 2018-07-23
 * License: CC0
 * Source: http://codeforces.com/blog/entry/60737
 * Description: Hash map with good performance. In Python, the built-in dict is already
 * highly optimized with similar performance characteristics. This is included for reference.
 * For competitive programming, simply use Python's dict.
"""

# Python's built-in dict is already highly optimized
# and uses a similar hashing strategy.
# Simply use: h = {}
# or for default values: from collections import defaultdict; h = defaultdict(int)

# Example usage:
def example():
    h = {}
    h[42] = 1
    h[100] = 2
    print(h.get(42, 0))  # 1
    print(h.get(50, 0))  # 0 (default)
