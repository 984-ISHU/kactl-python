"""
 * Author: Simon Lindholm
 * Date: 2016-01-14
 * License: CC0
 * Description: Given a rooted tree and a subset S of nodes, compute the minimal
 * subtree that contains all the nodes by adding all (at most $|S|-1$)
 * pairwise LCA's and compressing edges.
 * Returns a list of (par, orig\_index) representing a tree rooted at 0.
 * The root points to itself.
 * Time: $O(|S| \log |S|)$
 * Status: Tested at CodeForces
"""

def compress_tree(lca, subset):
    """
    Compress a tree to contain only nodes in subset and their LCAs.
    
    Args:
        lca: LCA object with lca() method and time[] array
        subset: List of node indices to include
    
    Returns:
        List of (parent_index, original_node) tuples representing compressed tree
    """
    n = len(lca.time)
    rev = [0] * n
    
    # Sort by time (DFS order)
    li = sorted(subset, key=lambda x: lca.time[x])
    
    # Add LCAs of consecutive nodes
    m = len(li) - 1
    for i in range(m):
        a, b = li[i], li[i + 1]
        li.append(lca.lca(a, b))
    
    # Sort and remove duplicates
    li = sorted(set(li), key=lambda x: lca.time[x])
    
    # Build reverse mapping
    for i, node in enumerate(li):
        rev[node] = i
    
    # Build compressed tree
    ret = [(0, li[0])]  # Root points to itself
    for i in range(len(li) - 1):
        a, b = li[i], li[i + 1]
        parent = rev[lca.lca(a, b)]
        ret.append((parent, b))
    
    return ret

# Example usage:
# Assuming you have an LCA object and want to compress tree to subset
# compressed = compress_tree(lca_obj, [1, 3, 5, 7])
