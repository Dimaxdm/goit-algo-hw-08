# Task 1 

## The problem statement
Write an algorithm (function) that finds the minimum value in a AVL tree.

## Solution to task 1
The file ***avl_tree.py*** contains the Python implementation of Tasks 1 and 2

### Explanation to the `min_value()` and its helper `_min_value()` 

```python
def min_value(self):
    if self._root is None:
        raise ValueError("min_value() called on an empty tree")
    return self._min_node(self._root).value

@staticmethod
def _min_node(node: "_Node") -> "_Node":
    current = node
    while current.left:
        current = current.left
    return current
```

The logic exploits the fundamental **BST property**: in any Binary Search Tree, every left child is strictly smaller that its parent.This means the mininum value is always the leftmost node in the entire tree.

Step by step on a example $\textendash$ given the final tree `[1, 3, 5, 11, 13, 15, 20]`, the internal structure looks like roughly like this: 
```
       11
     /    \
    3      15
  /  \    /  \
 1    5  13   20
```
1. `min_value()` checks the tree isn't emtpy, then calls `_min_node(root)` where `root` is the node `11`
2. `current = 11` $\rightarrow$ has a left child (`3`) $\rightarrow$ move left
3. `current = 3`  $\rightarrow$ has a left child (`1`) $\rightarrow$ move left
4. `current = 1` $\rightarrow$ has no left child $\rightarrow$ stop
5. Return `current.value` $\rightarrow$ 1

#### ***Iterative appoach*** 
The iterative `while` loop is a deliberate choise $\textendash$ it uses $O(1)$ space instead of $O(log n)$ stack frames. Since the goal is to chasing a single path (always left), there's nothing to gain from recursion. 

#### Complexity 
* Time $O(\log{}n)$ $\textemdash$ number of iterations equals the tree height, which is $O(\log{}n)$ in a balanced AVL tree.
* Space $O(1)$


# Task 2

## The problem statement
Write an algorithm (function) that calculates the sum of all values in a AVL tree.

## Solution to task 2
The file ***avl_tree.py*** contains the Python implementation of Tasks 1 and 2

### Explanation to the `sum()` and its helper `_sum()` 

```python
def sum(self):
    return self._sum(self._root)

def _sum(self, node: "_Node | None") -> int | float:
    if node is None:
        return 0
    return node.value + self._sum(node.left) + self._sum(node.right)
```
#### ***Recursive appoach***
`_sum` performs a **full post-order traversal** $\textendash$ it visits every single node in the tree and accumulates their values bottom-up. 
Cases:
* **Base case**: `node is None` $\rightarrow$ return `0`. This is the recursion's termination condition. Every leaf's missing children hit this, contibuting nothing to the sum.
* **Recursive case**: return the current node's value **plus** the sum of everything in the left subtree **plus** the sum of everything in the right subtree.

#### Complexity:
* Time $O(n)$ $\textendash$ every node is visited exactly once, since to get a correct sum you must read every value.
* Space $O(\log{}n)$ $\textendash$ the recursion depth equals the tree height, which is $O(\log{}n)$ in a balanced AVL tree.



# Task 3
## The problem statement 
Imagine that during a technical interview you are given the following problem, which should be solved using a heap.

There are several network cables of different lengths. They need to be connected two at a time into a single cable using connectors, in an order that results in the lowest possible cost. The cost of connecting two cables is equal to the sum of their lengths, and the total cost is the sum of the costs of all cable connections.

The task is to find the order of connections that minimizes the total cost.

## Solution to task 3
The file ***min_cables_cost.py*** contains the Python implementation of Task 3

### The Key Insight
When two cable connected, their combined lenghth becomes part of *every subsequent connection* they're involved in. So shorter cables should be merged first $\textendash$ they contribute to fewer total additions. 

### Min-Heap approach
| Need | How the heap hepls |
|---|---|
| Always pick the two shortest cables | `heappop` gives the minimum in $O(\log{}n)$ | 
| Re-insert the merged cable | `heappush` in $O(\log{}n)$ |
| No sorting after each merge | The heap maintains order automatically | 

#### Complexity
* **Time**: $O(n \log{}n)$ $\textendash$ $n - 1$ merges, each doing $2$ pops $+ 1$ push at $O(\log{}n)$
* **Space**: $O(n)$ $\textendash$ the heap holds at most n elements


#### Demo of cables lengths list `[9, 12, 4, 5, 13, 12]`

<img width="449" height="205" alt="image" src="https://github.com/user-attachments/assets/b1eab944-7a7e-4c4d-a7c6-36702a7b2d85" />
