"""
AVL-tree (A self-balancing Binary Search Tree) Implamentation
Commands:
- inisialization AVLTree() | AVLTree(list)
- AVLTree.insert_value(x)
- AVLTree.insert_values(list)
- AVLTree.delete_value(x)
- AVLTree.delete_values(list)
- AVLTree.min_value()
- AVLTree.max_value()
- AVLTree.sum()

* balancing is performed automatically on every insert and delete.
"""
class _Node:
    """Internal node used by AVLTree. Not intended for direct use."""
    __slots__ = ("value", "left", "right", "height")
 
    def __init__(self, value):
        self.value = value
        self.left: "_Node | None" = None
        self.right: "_Node | None" = None
        self.height: int = 1  # leaf height starts at 1
 
 
class AVLTree:
    """
    AVL Self-Balancing Binary Search Tree.
    """
    # Construction
    def __init__(self, values=None):
        """
        Create an AVLTree, optionally pre-populated with *values*.
            * values : iterable of numbers, optional
            * Initial values to insert. Duplicates are ignored.
        """
        self._root: "_Node | None" = None
        self._size: int = 0
 
        if values is not None:
            self.insert_values(values)
 
    # Public API: insert
    def insert_value(self, value) -> None:
        """Insert a single *value*.  Duplicates are silently ignored."""
        new_root, inserted = self._insert(self._root, value)
        self._root = new_root
        if inserted:
            self._size += 1
 
    def insert_values(self, values) -> None:
        """Insert every element in the *values* iterable."""
        for val in values:
            self.insert_value(val)
 
    # Public API: delete
    def delete_value(self, value) -> None:
        """
        Remove *value* from the tree. If the value is not present the call is a no-op.
        """
        new_root, deleted = self._delete(self._root, value)
        self._root = new_root
        if deleted:
            self._size -= 1
 
    def delete_values(self, values) -> None:
        """Remove every element in the *values* iterable."""
        for val in values:
            self.delete_value(val)
 
    # Public API: queries
    def min_value(self):
        """
        Return the minimum value in the tree.
        If the tree is empty. -> Raise ValueError
        """
        if self._root is None:
            raise ValueError("min_value() called on an empty tree")
        return self._min_node(self._root).value
 
    def max_value(self):
        """
        Return the maximum value in the tree. 
        If the tree is empty. -> Raise ValueError
        """
        if self._root is None:
            raise ValueError("max_value() called on an empty tree")
        return self._max_node(self._root).value
 
    def sum(self):
        """Return the sum of all values stored in the tree (0 for empty tree)."""
        return self._sum(self._root)
 
    def __len__(self) -> int:
        """Return the number of nodes in the tree."""
        return self._size
 
    def __contains__(self, value) -> bool:
        """Support 'value in avlt' syntax."""
        return self._search(self._root, value) is not None
 
    def __iter__(self):
        """Iterate over values in sorted (ascending) order."""
        yield from self._inorder(self._root)
 
    def __repr__(self) -> str:
        return f"AVLTree({list(self)})"
 
    def __str__(self) -> str:
        """Return a sorted list representation, e.g. [1, 4, 5, 8, 10, ...]."""
        return str(list(self))
 
    # Internal helpers: height & balance factor
    @staticmethod
    def _height(node: "_Node | None") -> int:
        return node.height if node else 0
 
    def _update_height(self, node: "_Node") -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))
 
    def _balance_factor(self, node: "_Node | None") -> int:
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)
 
    # Internal helpers: rotations
    def _rotate_right(self, z: "_Node") -> "_Node":
        """Right rotation around *z*; returns the new subtree root."""
        y = z.left
        T3 = y.right
 
        y.right = z
        z.left = T3
 
        self._update_height(z)
        self._update_height(y)
        return y
 
    def _rotate_left(self, z: "_Node") -> "_Node":
        """Left rotation around *z*; returns the new subtree root."""
        y = z.right
        T2 = y.left
 
        y.left = z
        z.right = T2
 
        self._update_height(z)
        self._update_height(y)
        return y
 
    # Internal helpers: rebalance
    def _rebalance(self, node: "_Node") -> "_Node":
        """
        Apply the appropriate rotation(s) to restore the AVL property
        for *node* and return the (possibly new) subtree root.
        """
        self._update_height(node)
        bf = self._balance_factor(node)
 
        if bf > 1:      # Left-heavy
            if self._balance_factor(node.left) < 0:          # Left-Right case
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)                   # Left-Left case
 
        if bf < -1:     # Right-heavy
            if self._balance_factor(node.right) > 0:          # Right-Left case
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)                    # Right-Right case
        return node  # already balanced
 
    # Internal helpers: insert
    def _insert(self, node: "_Node | None", value) -> "tuple[_Node, bool]":
        """
        Recursively insert *value* into the subtree rooted at *node*.
        Returns: (new_root, inserted)
            *inserted* is True when a new node was created.
        """
        if node is None:
            return _Node(value), True
        if value < node.value:
            node.left, inserted = self._insert(node.left, value)
        elif value > node.value:
            node.right, inserted = self._insert(node.right, value)
        else:
            return node, False  # ingnore duplicate
        return self._rebalance(node), inserted
 
    # Internal helpers: delete
    @staticmethod
    def _min_node(node: "_Node") -> "_Node":
        current = node
        while current.left:
            current = current.left
        return current
 
    @staticmethod
    def _max_node(node: "_Node") -> "_Node":
        current = node
        while current.right:
            current = current.right
        return current
 
    def _delete(self, node: "_Node | None", value) -> "tuple[_Node | None, bool]":
        """
        Recursively delete *value* from the subtree rooted at *node*.
        Returns: (new_root, deleted) 
            *deleted* is True when the value was found and removed.
        """
        if node is None:
            return None, False  # value not found
 
        if value < node.value:
            node.left, deleted = self._delete(node.left, value)
        elif value > node.value:
            node.right, deleted = self._delete(node.right, value)
        else:
            deleted = True
            # Node to remove found
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            # Node has two children: replace with in-order successor
            successor = self._min_node(node.right)
            node.value = successor.value
            node.right, _ = self._delete(node.right, successor.value)
 
        return self._rebalance(node), deleted
 
    # Internal helpers: traversal
    def _inorder(self, node: "_Node | None"):
        if node is None:
            return
        yield from self._inorder(node.left)
        yield node.value
        yield from self._inorder(node.right)
    
    # Internal helpers: search
    def _search(self, node: "_Node | None", value) -> "_Node | None":
        if node is None or node.value == value:
            return node
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)
    
    # Internal helpers: sum
    def _sum(self, node: "_Node | None") -> int | float:
        if node is None:
            return 0
        return node.value + self._sum(node.left) + self._sum(node.right)



if __name__ == "__main__":
    print("\n", "#" * 10, " AVL Tree Demo ", "#" * 10, "\n")
    example_list = [5, 9, 10, 12, 13, 8]
    
    avlt = AVLTree(example_list)
    print(f"{"After init with"} \"{example_list}\"  >>> {avlt}")
 
    avlt.insert_values([1, 4])
    print(f"{"After insert_values([1, 4])":<40} >>> {avlt}")
 
    avlt.insert_value(20)
    print(f"{"After insert_value(20)":<40} >>> {avlt}")
 
    avlt.delete_value(9)
    print(f"{"After delete_value(9)":<40} >>> {avlt}")
 
    avlt.delete_values([11, 8])
    print(f"{"After delete_values([11, 8])":<40} >>> {avlt}", "\n")
 
    print(f"{"min_value()":<12} >>> {avlt.min_value()}  {"<--solution to task 01":>25}") 
    print(f"{"max_value()":<12} >>> {avlt.max_value()}")
    print(f"{"sum()":<12} >>> {avlt.sum()} {"<--solution to task 02":>25}")
    print(f"{"len(avlt)":<12} >>> {len(avlt)}")
    print(f"{"10 in avlt":<12} >>> {10 in avlt}")
    print(f"{"99 in avlt":<12} >>> {99 in avlt}")