"""
 * Author: David Rydh, Per Austrin
 * Date: 2003-03-16
 * Description: Polynomial operations.
"""

class Polynomial:
    def __init__(self, coefficients):
        """
        Initialize polynomial with coefficients.
        
        Args:
            coefficients: List [a0, a1, a2, ...] representing a0 + a1*x + a2*x^2 + ...
        """
        self.a = list(coefficients)
    
    def __call__(self, x):
        """Evaluate polynomial at x using Horner's method."""
        if not self.a:
            return 0.0
        val = 0.0
        for coef in reversed(self.a):
            val = val * x + coef
        return val
    
    def differentiate(self):
        """Compute derivative of polynomial in-place."""
        if len(self.a) <= 1:
            self.a = [0.0]
            return
        
        for i in range(len(self.a) - 1):
            self.a[i] = (i + 1) * self.a[i + 1]
        self.a.pop()
    
    def divide_by_root(self, x0):
        """
        Divide polynomial by (x - x0) in-place using synthetic division.
        
        Args:
            x0: Root to divide by
        """
        if not self.a:
            return
        
        b = self.a[-1]
        self.a[-1] = 0
        
        for i in range(len(self.a) - 2, -1, -1):
            c = self.a[i]
            self.a[i] = self.a[i + 1] * x0 + b
            b = c
        
        self.a.pop()
    
    def degree(self):
        """Return degree of polynomial."""
        return len(self.a) - 1
    
    def __repr__(self):
        terms = []
        for i, coef in enumerate(self.a):
            if coef != 0:
                if i == 0:
                    terms.append(f"{coef}")
                elif i == 1:
                    terms.append(f"{coef}*x")
                else:
                    terms.append(f"{coef}*x^{i}")
        return " + ".join(terms) if terms else "0"

# Example usage:
# p = Polynomial([1, 2, 3])  # 1 + 2x + 3x^2
# print(p(2))  # Evaluate at x=2: 1 + 4 + 12 = 17
# p.differentiate()  # Now p = 2 + 6x
# p.divide_by_root(1)  # Divide by (x-1)
