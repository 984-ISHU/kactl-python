"""
 * Author: Lukas Polacek
 * Date: 2009-09-28
 * License: CC0
 * Source: folklore
 * Description: Operators for modular arithmetic. You need to set mod to
 * some number first and then you can use the structure.
"""

from math import gcd

MOD = 10**9 + 7  # Change to desired modulus

class Mod:
    def __init__(self, x, mod=MOD):
        self.x = x % mod
        self.mod = mod
    
    def __add__(self, other):
        return Mod((self.x + other.x) % self.mod, self.mod)
    
    def __sub__(self, other):
        return Mod((self.x - other.x + self.mod) % self.mod, self.mod)
    
    def __mul__(self, other):
        return Mod((self.x * other.x) % self.mod, self.mod)
    
    def __truediv__(self, other):
        return self * other.invert()
    
    def invert(self):
        # Extended Euclidean algorithm
        def euclid(a, b):
            if not b:
                return a, 1, 0
            d, y, x = euclid(b, a % b)
            y -= (a // b) * x
            return d, x, y
        
        g, x, y = euclid(self.x, self.mod)
        assert g == 1, "No modular inverse"
        return Mod((x + self.mod) % self.mod, self.mod)
    
    def __pow__(self, e):
        if e == 0:
            return Mod(1, self.mod)
        r = self ** (e // 2)
        r = r * r
        return self * r if e & 1 else r
    
    def __repr__(self):
        return f"Mod({self.x}, {self.mod})"

# Alternative: Use Python's built-in pow(base, -1, mod) for modular inverse in Python 3.8+
