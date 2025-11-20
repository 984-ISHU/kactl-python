"""
 * Author: Simon Lindholm
 * Date: 2017-04-17
 * License: CC0
 * Source: folklore
 * Description: Finds all biconnected components in an undirected graph, and
 * runs a callback for the edges in each. In a biconnected component there
 * are at least two internally disjoint paths between any two nodes (a cycle
 * exists through them). Note that a node can be in several components. An
 * edge which is not in a component is a bridge, i.e., not part of any cycle.
 * Usage:
 * eid = 0; ed = [[] for _ in range(N)]
 * for each edge (a,b):
 * ed[a].append((b, eid))
 * ed[b].append((a, eid)); eid += 1
 * bicomps(lambda edgelist: ...)
 * Time: O(E + V)
 * Status: tested during MIPT ICPC Workshop 2017
"""

num = []
st = []
ed = []
Time = [0]

def dfs(at, par, f):
    global num, st, ed, Time
    me = num[at] = Time[0] = Time[0] + 1
    top = me
    for y, e in ed[at]:
        if e != par:
            if num[y]:
                top = min(top, num[y])
                if num[y] < me:
                    st.append(e)
            else:
                si = len(st)
                up = dfs(y, e, f)
                top = min(top, up)
                if up == me:
                    st.append(e)
                    f(st[si:])
                    st[:] = st[:si]
                elif up < me:
                    st.append(e)
                else:
                    pass  # e is a bridge
    return top

def bicomps(f):
    global num, st, Time
    num = [0] * len(ed)
    st = []
    Time[0] = 0
    for i in range(len(ed)):
        if not num[i]:
            dfs(i, -1, f)
