"""
 * Author: Simon Lindholm
 * Date: 2019-12-28
 * License: CC0
 * Source: https://github.com/hoke-t/tamu-kactl/blob/master/content/data-structures/MoQueries.h
 * Description: Answer interval or tree path queries by finding an approximate TSP through the queries,
 * and moving from one query to the next by adding/removing points at the ends.
 * Time: O(N \sqrt Q)
 * Status: stress-tested
"""

# Global functions to be implemented by user:
# def add(ind, end): ...  # add a[ind] (end = 0 or 1)
# def del_element(ind, end): ...  # remove a[ind]
# def calc(): ...  # compute current answer

def mo(Q, add_fn, del_fn, calc_fn):
    """
    Q: list of (left, right) query pairs
    add_fn, del_fn, calc_fn: callback functions
    Returns: list of answers for each query
    """
    L, R = 0, 0
    blk = 350  # ~N/sqrt(Q)
    s = list(range(len(Q)))
    res = [0] * len(Q)
    
    def K(x):
        return (Q[x][0] // blk, Q[x][1] ^ (-(Q[x][0] // blk & 1)))
    
    s.sort(key=K)
    
    for qi in s:
        q = Q[qi]
        while L > q[0]:
            L -= 1
            add_fn(L, 0)
        while R < q[1]:
            add_fn(R, 1)
            R += 1
        while L < q[0]:
            del_fn(L, 0)
            L += 1
        while R > q[1]:
            R -= 1
            del_fn(R, 1)
        res[qi] = calc_fn()
    
    return res

def moTree(Q, ed, add_fn, del_fn, calc_fn, root=0):
    """
    Q: list of [u, v] tree path queries
    ed: adjacency list
    add_fn, del_fn, calc_fn: callback functions
    Returns: list of answers for each query
    """
    N = len(ed)
    pos = [0, 0]
    blk = 350  # ~N/sqrt(Q)
    s = list(range(len(Q)))
    res = [0] * len(Q)
    I = [0] * N
    L = [0] * N
    R = [0] * N
    in_path = [0] * N
    par = [0] * N
    
    counter = [0]
    add_fn(0, 0)
    in_path[0] = 1
    
    def dfs(x, p, dep):
        par[x] = p
        L[x] = N
        if dep:
            I[x] = counter[0]
            counter[0] += 1
        for y in ed[x]:
            if y != p:
                dfs(y, x, not dep)
        if not dep:
            I[x] = counter[0]
            counter[0] += 1
        R[x] = N
    
    dfs(root, -1, 0)
    
    def K(x):
        return (I[Q[x][0]] // blk, I[Q[x][1]] ^ (-(I[Q[x][0]] // blk & 1)))
    
    s.sort(key=K)
    
    for qi in s:
        for end in range(2):
            a = pos[end]
            b = Q[qi][end]
            path = []
            
            while not (L[b] <= L[a] and R[a] <= R[b]):
                path.append(b)
                b = par[b]
            
            while a != b:
                c = par[a]
                if in_path[c]:
                    del_fn(a, end)
                    in_path[a] = 0
                else:
                    add_fn(c, end)
                    in_path[c] = 1
                a = c
            
            for i in range(len(path) - 1, -1, -1):
                c = path[i]
                if in_path[c]:
                    del_fn(a, end)
                    in_path[a] = 0
                else:
                    add_fn(c, end)
                    in_path[c] = 1
                a = c
            
            pos[end] = a
            if end:
                res[qi] = calc_fn()
    
    return res
