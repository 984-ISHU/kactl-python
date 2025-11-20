# KACTL Python Conversion Guide

This document provides a comprehensive guide for converting the remaining KACTL algorithms from C++ to Python.

## Current Status

**Completed: ~35 files across 5 chapters**
**Remaining: ~150 files across 6 chapters**

See `CONVERSION_STATUS.md` for detailed progress.

## Quick Start

### Option 1: Manual Conversion (Recommended for Quality)

1. Choose a chapter to work on
2. Read the C++ file
3. Convert to Python following the patterns below
4. Test the implementation
5. Update the chapter.tex file

### Option 2: Semi-Automated

```bash
# Generate templates for all files in a chapter
python batch_convert.py content graph

# Then manually implement each template
# Finally update chapter.tex
python batch_convert.py content --update-tex graph
```

## Conversion Patterns

### 1. Comment Blocks
```cpp
// C++
/**
 * Author: Name
 * Description: Description text
 * Time: O(N)
 */
```

```python
# Python
"""
Author: Name
Description: Description text
Time: O(N)
"""
```

### 2. Data Types
```cpp
// C++
ll x;                    // long long
vi arr;                  // vector<int>
vector<pii> pairs;       // vector<pair<int,int>>
unordered_map<int,int> m;
```

```python
# Python
x = 0                    # int (arbitrary precision)
arr = []                 # list
pairs = []               # list of tuples
m = {}                   # dict
```

### 3. Common Constructs

#### Loops
```cpp
// C++
rep(i,0,n) { ... }
for(int x : vec) { ... }
```

```python
# Python
for i in range(n):
for x in vec:
```

#### Sorting
```cpp
// C++
sort(all(v));
sort(all(v), greater<int>());
```

```python
# Python
v.sort()
v.sort(reverse=True)
```

#### Binary Search
```cpp
// C++
lower_bound(all(v), x) - v.begin()
upper_bound(all(v), x) - v.begin()
```

```python
# Python
from bisect import bisect_left, bisect_right
bisect_left(v, x)
bisect_right(v, x)
```

### 4. Classes and Structs
```cpp
// C++
struct Point {
    int x, y;
    Point(int x, int y) : x(x), y(y) {}
    int dist2() { return x*x + y*y; }
};
```

```python
# Python
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def dist2(self):
        return self.x * self.x + self.y * self.y
```

### 5. Templates
```cpp
// C++
template<class T>
T gcd(T a, T b) {
    return b ? gcd(b, a%b) : a;
}
```

```python
# Python
def gcd(a, b):
    return gcd(b, a % b) if b else a

# Or use built-in:
from math import gcd
```

### 6. Common Algorithms

#### DFS/BFS
```cpp
// C++
void dfs(int v) {
    vis[v] = 1;
    for(int u : g[v])
        if(!vis[u]) dfs(u);
}
```

```python
# Python
def dfs(v):
    vis[v] = True
    for u in g[v]:
        if not vis[u]:
            dfs(u)
```

#### Priority Queue
```cpp
// C++
priority_queue<int> pq;
priority_queue<int, vector<int>, greater<int>> min_pq;
pq.push(x);
int top = pq.top(); pq.pop();
```

```python
# Python
from heapq import heappush, heappop
pq = []
heappush(pq, x)        # min-heap by default
top = heappop(pq)

# For max-heap, negate values
heappush(pq, -x)
top = -heappop(pq)
```

## Priority Order for Completion

### High Priority (Core Algorithms)
1. **Graph** - Network flows, matching, tree algorithms
2. **Number Theory** - Modular arithmetic, factorization
3. **Strings** - KMP, Z-algorithm, suffix structures

### Medium Priority
4. **Geometry** - Advanced geometric algorithms
5. **Numerical** - FFT, linear algebra

### Low Priority
6. **Various** - Miscellaneous utilities

## Testing

After implementing each algorithm:

1. Compare output with C++ version on sample inputs
2. Test edge cases (empty input, single element, etc.)
3. Verify time complexity matches specification

## Chapter-Specific Notes

### Graph
- Many algorithms use adjacency lists: `vector<vi>` → `list of lists`
- Flow algorithms use capacity graphs: `vector<unordered_map<int,int>>` → `list of dicts`
- Be careful with 0-indexed vs 1-indexed

### Geometry
- Use `Point` class consistently
- Python's `math` module for trig functions
- Consider using `complex` numbers for some operations

### Number Theory
- Python integers have arbitrary precision (no overflow!)
- Use `pow(base, exp, mod)` for modular exponentiation
- `math.gcd` is built-in (Python 3.5+)

### Strings
- Python strings are immutable
- Use lists for mutable string operations
- Built-in: `str.find()`, `str.count()`, etc.

### Numerical
- Use `numpy` for matrix operations (optional, add dependency)
- Python's `complex` for FFT
- Careful with floating-point precision

## Common Pitfalls

1. **Integer Division**: `//` in Python 3 (not `/`)
2. **Range**: `range(n)` is `[0, n)` (exclusive end)
3. **Modulo of Negatives**: Python's `%` always returns non-negative
4. **Pass by Reference**: Python passes object references, but numbers/strings are immutable
5. **Recursion Limit**: May need `sys.setrecursionlimit(10**6)` for deep recursion

## LaTeX Integration

After converting a chapter, update `chapter.tex`:
```bash
# Replace all .h with .py
sed -i '' 's/\.h}/.py}/g' content/CHAPTER/chapter.tex

# Or use the batch script:
python batch_convert.py content --update-tex CHAPTER
```

## Final Steps

1. Convert all algorithms
2. Update all chapter.tex files
3. Test PDF compilation: `make kactl.pdf`
4. Verify all algorithms appear correctly in the generated PDF

## Resources

- [Python Official Docs](https://docs.python.org/3/)
- [Python Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python Standard Library](https://docs.python.org/3/library/)
- Original KACTL: https://github.com/kth-competitive-programming/kactl

## Getting Help

If stuck on a conversion:
1. Check similar algorithms already converted
2. Refer to this guide's patterns
3. Test incrementally with small examples
4. Compare with C++ version's behavior

---

Good luck with the conversion! 🐍
