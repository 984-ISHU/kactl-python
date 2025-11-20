"""
 * Author: Simon Lindholm
 * Date: 2016-07-25
 * Source: https://github.com/ngthanhtrung23/ACM\_Notebook\_new/
 * Description: Represents a forest of unrooted trees. You can add and remove
 * edges (as long as the result is still a forest), and check whether
 * two nodes are in the same tree.
 * Time: All operations take amortized $O(\log N)$.
 * Status: Stress-tested a bit for N <= 20
"""

class LCTNode:
    """Splay tree node for Link-Cut Tree."""
    
    def __init__(self):
        self.parent = None  # Parent in splay tree
        self.path_parent = None  # Path parent (tree edge not in current splay tree)
        self.left = None
        self.right = None
        self.flip = False
    
    def fix(self):
        """Update pointers and aggregates."""
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self
    
    def push_flip(self):
        """Propagate flip operation."""
        if not self.flip:
            return
        self.flip = False
        self.left, self.right = self.right, self.left
        if self.left:
            self.left.flip = not self.left.flip
        if self.right:
            self.right.flip = not self.right.flip
    
    def direction(self):
        """Return 0 if left child, 1 if right child, -1 if root."""
        if not self.parent:
            return -1
        return 1 if self.parent.right == self else 0
    
    def rotate(self):
        """Rotate this node up."""
        p = self.parent
        g = p.parent
        d = self.direction()
        
        if d == 0:  # Left child
            p.left = self.right
            if self.right:
                self.right.parent = p
            self.right = p
        else:  # Right child
            p.right = self.left
            if self.left:
                self.left.parent = p
            self.left = p
        
        self.parent = g
        p.parent = self
        
        if g:
            if g.left == p:
                g.left = self
            else:
                g.right = self
        
        self.path_parent, p.path_parent = p.path_parent, self.path_parent
        p.fix()
        self.fix()
    
    def splay(self):
        """Splay this node to root of its splay tree."""
        while self.parent:
            self.parent.push_flip()
            self.push_flip()
            
            if not self.parent.parent:
                # Zig step
                self.rotate()
            else:
                # Zig-zig or zig-zag
                if (self.parent.direction() == self.direction()):
                    # Zig-zig
                    self.parent.rotate()
                    self.rotate()
                else:
                    # Zig-zag
                    self.rotate()
                    self.rotate()
    
    def first(self):
        """Get leftmost node in splay tree."""
        self.push_flip()
        if self.left:
            return self.left.first()
        self.splay()
        return self

class LinkCutTree:
    """Link-Cut Tree for dynamic tree operations."""
    
    def __init__(self, n):
        """Initialize n isolated nodes."""
        self.nodes = [LCTNode() for _ in range(n)]
    
    def access(self, u):
        """Make path from root to u a single splay tree."""
        node = self.nodes[u]
        node.splay()
        
        while node.path_parent:
            parent = node.path_parent
            parent.splay()
            
            # Detach right child
            if parent.right:
                parent.right.parent = None
                parent.right.path_parent = parent
            
            parent.right = node
            parent.fix()
            node = parent
        
        return node
    
    def make_root(self, u):
        """Make u the root of its tree."""
        node = self.nodes[u]
        self.access(u)
        node.splay()
        
        if node.left:
            node.left.parent = None
            node.left.flip = not node.left.flip
            node.left.path_parent = node
            node.left = None
            node.fix()
    
    def link(self, u, v):
        """Add edge between u and v."""
        self.make_root(u)
        self.nodes[u].path_parent = self.nodes[v]
    
    def cut(self, u, v):
        """Remove edge between u and v."""
        node_u = self.nodes[u]
        node_v = self.nodes[v]
        
        self.make_root(v)
        node_u.splay()
        
        # Check if v is path parent or left child
        if node_u.path_parent:
            node_u.path_parent = None
        else:
            node_u.left = None
            node_v.parent = None
            node_u.fix()
    
    def connected(self, u, v):
        """Check if u and v are in same tree."""
        node_u = self.access(u).first()
        node_v = self.access(v).first()
        return node_u == node_v

# Example usage:
# lct = LinkCutTree(5)
# lct.link(0, 1)
# lct.link(1, 2)
# print(lct.connected(0, 2))  # True
# lct.cut(1, 2)
# print(lct.connected(0, 2))  # False
