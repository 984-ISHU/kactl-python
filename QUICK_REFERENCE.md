# KACTL Python - Quick Reference

## Files You Can Use RIGHT NOW ✅

### Data Structures (100% Complete)
```python
from FenwickTree import FenwickTree
from SegmentTree import SegmentTree
from LazySegmentTree import LazySegmentTree
from Matrix import Matrix
from RMQ import RMQ
from Treap import Node, split, merge
from UnionFindRollback import UnionFindRollback
```

### Graph Algorithms (Core Algorithms)
```python
from BellmanFord import bellmanFord
from FloydWarshall import floydWarshall
from TopoSort import topoSort
from SCC import scc
from EdmondsKarp import edmondsKarp
from DFSMatching import dfsMatching
from LCA import LCA
```

### Number Theory
```python
from euclid import euclid
from ModPow import modpow
from Eratosthenes import eratosthenesSieve
from MillerRabin import isPrime
```

### Geometry (Basics)
```python
from Point import Point
from ConvexHull import convexHull
```

### Contest Template
```python
# See content/contest/template.py for complete template
```

## Common Usage Examples

### Fenwick Tree
```python
ft = FenwickTree(1000)
ft.update(10, 5)  # Add 5 to position 10
print(ft.query(20))  # Sum of [0, 20)
```

### Segment Tree
```python
st = SegmentTree(1000, 0)
st.update(5, 100)
print(st.query(0, 10))  # Max in range [0, 10)
```

### Shortest Paths
```python
# Bellman-Ford
nodes = [Node() for _ in range(n)]
edges = [Edge(u, v, w) for ...]
bellmanFord(nodes, edges, source)

# Floyd-Warshall
dist = [[INF]*n for _ in range(n)]
floydWarshall(dist)
```

### Topological Sort
```python
graph = [[] for _ in range(n)]  # adjacency list
order = topoSort(graph)
```

### Strongly Connected Components
```python
graph = [[] for _ in range(n)]
comp, ncomps = scc(graph)
```

### Max Flow
```python
graph = [{}  for _ in range(n)]  # list of dicts
graph[u][v] = capacity
flow = edmondsKarp(graph, source, sink)
```

### Bipartite Matching
```python
g = [[] for _ in range(n)]  # left partition adjacency
btoa = [-1] * m  # right partition size
matching_size = dfsMatching(g, btoa)
```

### Lowest Common Ancestor
```python
tree = [[] for _ in range(n)]  # adjacency list
lca_ds = LCA(tree)
ancestor = lca_ds.lca(u, v)
```

### Prime Sieve
```python
primes = eratosthenesSieve(1000000)
```

### Primality Test
```python
if isPrime(n):
    print("Prime")
```

### Modular Exponentiation
```python
result = modpow(base, exp, mod)
# Or use Python built-in:
result = pow(base, exp, mod)
```

### Extended Euclidean
```python
gcd, x, y = euclid(a, b)
# ax + by = gcd
# x is modular inverse of a (mod b) if gcd == 1
```

### Convex Hull
```python
points = [Point(x, y) for ...]
hull = convexHull(points)
```

### Matrix Exponentiation
```python
m = Matrix(3)
m.d = [[1,1,0], [1,0,1], [0,1,0]]
result = m ** n
```

### Range Minimum Query
```python
arr = [3, 1, 4, 1, 5, 9, 2, 6]
rmq = RMQ(arr)
minimum = rmq.query(2, 6)  # min in [2, 6)
```

### Treap
```python
root = None
for val in values:
    root = ins(root, Node(val), position)

left, right = split(root, k)
root = merge(left, right)
```

## Files Still TODO

See `CONVERSION_STATUS.md` for complete list.

**High Priority:**
- Graph: PushRelabel, MinCostMaxFlow, HLD, LinkCutTree
- Strings: KMP, SuffixArray, Hashing
- Number Theory: CRT, Factor, ModularArithmetic

**Medium Priority:**
- Geometry: Most algorithms (48+ files)
- Numerical: FFT, Determinant, Polynomial

## Quick Commands

```bash
# Test a single algorithm
cd content/data-structures
python3 -c "from FenwickTree import FenwickTree; ft = FenwickTree(10); ft.update(5, 10); print(ft.query(6))"

# Generate templates for remaining files in a chapter
python3 batch_convert.py content graph

# Update chapter.tex
python3 batch_convert.py content --update-tex data-structures

# Try to build PDF (requires LaTeX)
make kactl.pdf
```

## Tips for Using Converted Algorithms

1. **Import Path**: Make sure Python can find the modules
   ```python
   import sys
   sys.path.append('path/to/content/chapter')
   ```

2. **Type Hints**: Add if needed for clarity
   ```python
   def func(arr: list[int]) -> int:
   ```

3. **Testing**: Always test with small examples first

4. **Performance**: Python is slower than C++, but:
   - Usually fast enough for CP (especially with PyPy)
   - Cleaner code often beats micro-optimizations
   - Focus on algorithm correctness first

5. **Debugging**: Python's error messages are helpful
   ```python
   import traceback
   try:
       # your code
   except Exception as e:
       traceback.print_exc()
   ```

## Contributing

To help complete the conversion:
1. Pick an algorithm from CONVERSION_STATUS.md
2. Follow patterns in CONVERSION_GUIDE.md
3. Test your implementation
4. Submit a PR or update files directly

---

**Happy Competitive Programming! 🐍🏆**
