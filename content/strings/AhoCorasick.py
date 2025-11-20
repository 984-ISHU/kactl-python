"""
 * Author: Simon Lindholm
 * Date: 2015-02-18
 * License: CC0
 * Source: marian's (TC) code
 * Description: Aho-Corasick automaton, used for multiple pattern matching.
 * Initialize with ac = AhoCorasick(patterns); the automaton start node will be at index 0.
 * find(word) returns for each position the index of the longest word that ends there, or -1 if none.
 * findAll(patterns, word) finds all words that start at each position (shortest first).
 * Duplicate patterns are allowed; empty patterns are not.
 * Time: construction takes $O(26N)$, where $N =$ sum of length of patterns.
 * find(x) is $O(N)$, findAll is $O(NM)$.
 * Status: stress-tested
"""

from collections import deque

class AhoCorasick:
    ALPHA = 26
    FIRST = ord('A')
    
    class Node:
        def __init__(self):
            self.back = -1
            self.next = [-1] * AhoCorasick.ALPHA
            self.start = -1
            self.end = -1
            self.nmatches = 0
    
    def __init__(self, patterns):
        self.nodes = [self.Node()]
        self.backp = []
        
        # Insert all patterns
        for j, pattern in enumerate(patterns):
            self._insert(pattern, j)
        
        # Build failure links
        self.nodes[0].back = len(self.nodes)
        self.nodes.append(self.Node())
        self.nodes[-1].back = 0
        
        q = deque([0])
        while q:
            n = q.popleft()
            prev = self.nodes[n].back
            
            for i in range(self.ALPHA):
                ed = self.nodes[n].next[i]
                y = self.nodes[prev].next[i]
                
                if ed == -1:
                    self.nodes[n].next[i] = y
                else:
                    self.nodes[ed].back = y
                    if self.nodes[ed].end == -1:
                        self.nodes[ed].end = self.nodes[y].end
                    else:
                        self.backp[self.nodes[ed].start] = self.nodes[y].end
                    self.nodes[ed].nmatches += self.nodes[y].nmatches
                    q.append(ed)
    
    def _insert(self, s, j):
        """Insert pattern s with index j"""
        n = 0
        for c in s:
            idx = ord(c) - self.FIRST
            if self.nodes[n].next[idx] == -1:
                self.nodes[n].next[idx] = len(self.nodes)
                self.nodes.append(self.Node())
            n = self.nodes[n].next[idx]
        
        if self.nodes[n].end == -1:
            self.nodes[n].start = j
        self.backp.append(self.nodes[n].end)
        self.nodes[n].end = j
        self.nodes[n].nmatches += 1
    
    def find(self, word):
        """Find longest pattern ending at each position"""
        n = 0
        res = []
        for c in word:
            idx = ord(c) - self.FIRST
            n = self.nodes[n].next[idx]
            res.append(self.nodes[n].end)
        return res
    
    def find_all(self, patterns, word):
        """Find all patterns starting at each position"""
        r = self.find(word)
        res = [[] for _ in range(len(word))]
        
        for i in range(len(word)):
            ind = r[i]
            while ind != -1:
                start_pos = i - len(patterns[ind]) + 1
                res[start_pos].append(ind)
                ind = self.backp[ind]
        
        return res

# Example usage:
# patterns = ["SHE", "HE", "HIS", "HERS"]
# ac = AhoCorasick(patterns)
# matches = ac.find_all(patterns, "SHEHISHERE")
