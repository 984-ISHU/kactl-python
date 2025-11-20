"""
 * Author: Stanford
 * Source: Stanford Notebook
 * License: MIT
 * Description: Solves a general linear maximization problem: maximize $c^T x$ subject to $Ax \le b$, $x \ge 0$.
 * Returns -inf if there is no solution, inf if there are arbitrarily good solutions, or the maximum value of $c^T x$ otherwise.
 * The input vector is set to an optimal $x$ (or in the unbounded case, an arbitrary solution fulfilling the constraints).
 * Numerical stability is not guaranteed. For better performance, define variables such that $x = 0$ is viable.
 * Time: O(NM * #pivots), where a pivot may be e.g. an edge relaxation. O(2^n) in the general case.
 * Status: seems to work?
"""

EPS = 1e-8
INF = float('inf')

class Simplex:
    def __init__(self, A, b, c):
        """
        Initialize LP solver.
        
        Args:
            A: Constraint matrix (m x n)
            b: Right-hand side vector (length m)
            c: Objective coefficients (length n)
        """
        self.m = len(b)
        self.n = len(c)
        self.N = list(range(self.n + 1))
        self.B = [self.n + i for i in range(self.m)]
        self.D = [[0.0] * (self.n + 2) for _ in range(self.m + 2)]
        
        # Fill constraint matrix
        for i in range(self.m):
            for j in range(self.n):
                self.D[i][j] = A[i][j]
            self.D[i][self.n] = -1
            self.D[i][self.n + 1] = b[i]
        
        # Fill objective row
        for j in range(self.n):
            self.D[self.m][j] = -c[j]
        
        self.N[self.n] = -1
        self.D[self.m + 1][self.n] = 1
    
    def pivot(self, r, s):
        """Perform pivot operation."""
        a = self.D[r]
        inv = 1.0 / a[s]
        
        # Update all rows except pivot row
        for i in range(self.m + 2):
            if i != r and abs(self.D[i][s]) > EPS:
                b = self.D[i]
                inv2 = b[s] * inv
                for j in range(self.n + 2):
                    b[j] -= a[j] * inv2
                b[s] = a[s] * inv2
        
        # Scale pivot row
        for j in range(self.n + 2):
            if j != s:
                self.D[r][j] *= inv
        
        # Update pivot column
        for i in range(self.m + 2):
            if i != r:
                self.D[i][s] *= -inv
        
        self.D[r][s] = inv
        self.B[r], self.N[s] = self.N[s], self.B[r]
    
    def simplex(self, phase):
        """Run simplex algorithm for given phase."""
        x = self.m + phase - 1
        
        while True:
            # Select entering variable
            s = -1
            for j in range(self.n + 1):
                if self.N[j] != -phase:
                    if s == -1 or (self.D[x][j], self.N[j]) < (self.D[x][s], self.N[s]):
                        if self.D[x][j] < -EPS or (abs(self.D[x][j]) < EPS and j < s):
                            s = j
            
            if s == -1 or self.D[x][s] >= -EPS:
                return True
            
            # Select leaving variable
            r = -1
            for i in range(self.m):
                if self.D[i][s] <= EPS:
                    continue
                ratio = self.D[i][self.n + 1] / self.D[i][s]
                if r == -1 or (ratio, self.B[i]) < (self.D[r][self.n + 1] / self.D[r][s], self.B[r]):
                    r = i
            
            if r == -1:
                return False
            
            self.pivot(r, s)
    
    def solve(self, x):
        """
        Solve the LP problem.
        
        Args:
            x: Output vector (length n) for solution
        
        Returns:
            Optimal value, or -INF if infeasible, INF if unbounded
        """
        # Phase 1: find feasible solution
        r = 0
        for i in range(1, self.m):
            if self.D[i][self.n + 1] < self.D[r][self.n + 1]:
                r = i
        
        if self.D[r][self.n + 1] < -EPS:
            self.pivot(r, self.n)
            if not self.simplex(2) or self.D[self.m + 1][self.n + 1] < -EPS:
                return -INF
            
            # Remove artificial variable
            for i in range(self.m):
                if self.B[i] == -1:
                    s = 0
                    for j in range(1, self.n + 1):
                        if s == 0 or (self.D[i][j], self.N[j]) < (self.D[i][s], self.N[s]):
                            s = j
                    self.pivot(i, s)
        
        # Phase 2: optimize
        ok = self.simplex(1)
        
        # Extract solution
        for i in range(len(x)):
            x[i] = 0.0
        
        for i in range(self.m):
            if self.B[i] < self.n:
                x[self.B[i]] = self.D[i][self.n + 1]
        
        return INF if not ok else self.D[self.m][self.n + 1]

# Example usage:
# A = [[1, -1], [-1, 1], [-1, -2]]
# b = [1, 1, -4]
# c = [-1, -1]
# x = [0, 0]
# simplex = Simplex(A, b, c)
# val = simplex.solve(x)
