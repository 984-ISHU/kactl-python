"""
 * Author: Emil Lenngren, Simon Lindholm
 * Date: 2011-11-29
 * License: CC0
 * Source: folklore
 * Description: Calculates a valid assignment to boolean variables a, b, c,... to a 2-SAT problem,
 * so that an expression of the type $(a||b)\&\&(!a||c)\&\&(d||!b)\&\&...$
 * becomes true, or reports that it is unsatisfiable.
 * Negated variables are represented by bit-inversions (~x).
 * Usage:
 * ts = TwoSat(number of boolean variables)
 * ts.either(0, \~{}3)  \# Var 0 is true or var 3 is false
 * ts.setValue(2)  \# Var 2 is true
 * ts.atMostOne([0,\~{}1,2])  \# <= 1 of vars 0, \~{}1 and 2 are true
 * ts.solve()  \# Returns True iff it is solvable
 * ts.values[0..N-1] holds the assigned values to the vars
 * ts.values[0..N-1] holds the assigned values to the vars
 * Time: O(N+E), where N is the number of boolean variables, and E is the number of clauses.
 * Status: stress-tested
"""

class TwoSat:
    def __init__(self, n=0):
        self.N = n
        self.gr = [[] for _ in range(2 * n)]
        self.values = []
    
    def addVar(self):
        self.gr.append([])
        self.gr.append([])
        self.N += 1
        return self.N - 1
    
    def either(self, f, j):
        f = max(2*f, -1-2*f)
        j = max(2*j, -1-2*j)
        self.gr[f].append(j ^ 1)
        self.gr[j].append(f ^ 1)
    
    def setValue(self, x):
        self.either(x, x)
    
    def atMostOne(self, li):
        if len(li) <= 1:
            return
        cur = ~li[0]
        for i in range(2, len(li)):
            next_var = self.addVar()
            self.either(cur, ~li[i])
            self.either(cur, next_var)
            self.either(~li[i], next_var)
            cur = ~next_var
        self.either(cur, ~li[1])
    
    def dfs(self, i, val, comp, z, time):
        low = val[i] = time[0] = time[0] + 1
        z.append(i)
        for e in self.gr[i]:
            if not comp[e]:
                if val[e]:
                    low = min(low, val[e])
                else:
                    low = min(low, self.dfs(e, val, comp, z, time))
        if low == val[i]:
            while True:
                x = z.pop()
                comp[x] = low
                if x == i:
                    break
        return low
    
    def solve(self):
        val = [0] * len(self.gr)
        comp = [0] * len(self.gr)
        z = []
        time = [0]
        for i in range(len(self.gr)):
            if not comp[i]:
                self.dfs(i, val, comp, z, time)
        
        self.values = [False] * self.N
        for i in range(self.N):
            if comp[2*i] == comp[2*i + 1]:
                return False
            self.values[i] = comp[2*i] > comp[2*i + 1]
        return True
