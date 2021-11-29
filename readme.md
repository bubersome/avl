#### How a Tree Becomes Unbalanced

The structure of a binary search tree can be quite compact. Indeed, when a binary search tree contains exactly 2k - 1 nodes, it can be stored in a binary tree whose height is k - 1. This tree contains 2**3 - 1 = 7 values.

![Sample Binary Tree](https://www.katacoda.com/embed/orm-george-heineman/ch06-utility-balancing/assets/legend.png)

The *height* of a binary tree is the height of its root node (in this case, the node containing the value 19). 

Define the height of a node to be the distance to that node's most distant *descendant* which can be reached by following *left* or *right* nodes. A leaf node has no children, which means that the height of a leaf node is 0. When a node has children, its height is 1 greater than the maximum height of its children (whether both exist or just one). For example, the node containing the value 14 in the figure above has height of 1, since both of its children each have a height of 0.

Let's start by creating a `BinaryNode`class which stores the height of each node in an attribute `height`. Define the height of a node to be 1 greater than the maximum height of its children. Since the height of a leaf node with no children is 0, this means *the height of a non-existing binary node (that is, `None`) is -1*.

```
Copy to Editorclass BinaryNode:
  def __init__(self, val):
    self.value = val
    self.left  = None
    self.right = None
    self.height = 0

  def compute_height(self):
    leftH = rightH = -1
    if self.left:
      leftH = self.left.height
    if self.right:
      rightH = self.right.height
    self.height = 1 + max(leftH, rightH)
```

To set the `height` for a node, call `compute_height()` on the node. `leftH` and `rightH` are set to the height of the *left* and *right* child. If neither exists, then the value used is -1. The resulting height of the node is set to 1 greater than the max of `leftH` and `rightH`.

If you had 1,048,575 values stored in the most compact way in a binary search tree, it would only have a height of 20 - 1 = 19, since 220 - 1 = 1,048,575. This is incredibly efficient! However, since a binary search tree changes its structure whenever a value is inserted or removed, any compact tree can quickly become *unbalanced*. 

Starting from the binary search tree above, add the value 29 and then the value 27. The result is as follows:

![Sample Unbalanced Binary Tree](https://www.katacoda.com/embed/orm-george-heineman/ch06-utility-balancing/assets/legend_2.png)

This tree no longer has a compact representation. The right subtree, rooted at 53, has a height of 3, but the left subtree, rooted at 14, has a height of 1. You can see visually that the right subtree is "taller" than the left, but I need to have a precise mathematical computation to declare when a node is unbalanced. 

Define `height_difference()` to compute the integer value you get when subtracting the height of a node's left child node from the height of a node's right child node. If neither the left or the right is present, then use -1 as that missing child node's height. Add the function to `BinaryNode`.

```
Copy to Editor  def height_difference(self):
    leftH = rightH = -1
    if self.left:
      leftH = self.left.height
    if self.right:
      rightH = self.right.height
    return leftH - rightH
```

The `height_difference()` of the root node in the figure above is 1 - 3 = -2. You can also see that the `height_difference()` of the node containing the value 53 is 2 - 0 = 2. The order in which these values are subtracted matters, and the result can be either negative or positive. Both of these nodes are unbalanced.

I now describe the first known self-balancing binary tree data structure, called the AVL tree (named after its inventors Adelson-Velsky and Landis). As values are inserted into, or removed from, a binary search tree, weaknesses in the structure of the resulting tree are detected and repaired. An AVL tree guarantees that the *height difference of any node is -1, 0 or +1*. This is known as the *AVL Tree Property*. Whenever a node is inserted into a binary search tree, the height of the affected nodes must be computed *so an unbalanced tree node can be detected immediately*.

Let's start by creating the `BinaryTree`class which contains an `insert()`method for inserting a value into a binary search tree. `insert()` relies on a recursive helper method, `_insert()`whose purpose is to insert `val` into the subtree rooted at `node` and return the root node of the updated subtree. In the base case of `_insert()`, the request is to insert `val` into a non-existing node: the result is just a new `BinaryNode` containing this value. Note that the height of this newly created `BinaryNode` is 0 by definition.

```
Copy to Editorclass BinaryTree:
  def __init__(self):
    self.root = None

  def insert(self, val):
    self.root = self._insert(self.root, val)

  def _insert(self, node, val):
    # base case
    if node is None:
      return BinaryNode(val)

    # recursive case
    if val <= node.value:
      node.left = self._insert(node.left, val)
      node = resolve_left_leaning(node)
    else:
      node.right = self._insert(node.right, val)
      node = resolve_right_leaning(node)

    node.compute_height()
    return node

  # TBA: MORE
```

In the recursive case, the value is either inserted into the left subtree rooted at `node.left` or the right subtree rooted at `node.right`, based on whether `val ≤ node.value`: `_insert()`returns `node` at the end. 

The last statement executed is `node.compute_height()` which properly computes the height of `node`as I showed earlier. Because this method is recursive, when `compute_height()` is called, you know that the heights of that node's left and right child nodes (should they exist) have already been computed.

Now that accurate information is available, it is possible to detect when a tree loses its balance. Specifically, when inserting a value into the left subtree, `node.left`, it is possible that `node`becomes "left-leaning" and out of balance to its left. Similarly, when inserting a value into the right subtree, `node.right`, it is possible that `node`becomes "right-leaning" and out of balance to its right. 

In the next step, I describe a resolution strategy to rebalance the tree upon insert.

#### Balancing an AVL Tree on insert

The designers of the AVL tree invented the concept of a *node rotation*, which is visualized below:

![Node Rotation In Simple Tree](https://www.katacoda.com/embed/orm-george-heineman/ch06-utility-balancing/assets/simple_rotation.png)

Three nodes containing the values 10, 30, and 50 are shaded to present their height. The tree is left-leaning, since the root node, containing the value of 50, has a left subtree whose height is 1. There is no right subtree, which means the non-existent tree has a height of -1. The height difference is 1 - (-1) = +2.

An AVL tree rebalances itself by detecting this imbalance and rotating nodes to reconfigure the tree as shown above. After the rotation, the resulting binary search tree as a height of 1 (which is smaller than original) and the node containing 30 has become the new root.

This particular rotation is a *rotate right*, which you can visualize as placing your hand on the original node containing 30 and rotating your hand to the right, which "lifts up" the node containing 30 while "dropping down" the node containing 50.

This same principle applies even in more complicated trees, as shown below:

![Node Rotation In Complicated Tree](https://www.katacoda.com/embed/orm-george-heineman/ch06-utility-balancing/assets/rotation.png)

The root node, containing 50, has height h. The gray triangles are subtrees whose values conform to the binary search tree property. The left subtree of the node containing 10, for example, is labeled 10L, and it contains values that are all smaller than or equal to 10. All you need to know is that the height of this subtree (and the other three shaded subtrees, 10R, 30R, and 50R) is h-3.

This tree leans to the left: its left subtree has a height of h-1 while its right sub-tree has a smaller height of h-3. The *height difference* is +2: The computation (h-1) - (h-3) = -1 + 3 = +2.

An AVL tree rebalances itself by detecting this imbalance and rotating nodes to reconfigure the tree as shown above. After the rotation, the resulting binary search tree as a height of h-1 (which is smaller than original) and the node containing 30 has become the new root.

As described in Chapter 6 in [Learning Algorithms](https://oreil.ly/learn-algorithms), there are four rotational scenarios that are identified. You can find these implementations in `rotation.py`. Here is the code that shows how to perform a right rotation:

```
def rotate_right(node):
  new_root = node.left
  grandson = new_root.right
  node.left = grandson
  new_root.right = node

  node.compute_height()
  return new_root
```

These implementations are precise. What you should observe is that these rotation methods have no recursive calls or loops of any kind. They each have a fixed number of operations, which means their runtime performance is O(1) in all cases. In the more complicated rotation scenarios, *two rotations* are performed:

![Left Right Rotation](https://www.katacoda.com/embed/orm-george-heineman/ch06-utility-balancing/assets/left_right_rotation.png)

In this case, a *rotate left* on the subtree rooted at node containing 10 "drops down" the 10 node and "lifts up" the 30 node, resulting in a tree that matches the original case where a rotate right balances the tree. This represents the `rotate_left_right()` function in `rotation.py`.

Add the following two functions that detect an imbalance and choose the right strategy to rebalance the subtree rooted at `node`. One common feature of these methods is that they return the new `node` of the reconfigured tree that had been rooted at a different `node`.

```
Copy to Editorfrom rotation import rotate_left, rotate_right
from rotation import rotate_left_right, rotate_right_left

def resolve_left_leaning(node):
  if node.height_difference() == 2:
    if node.left.height_difference() >= 0:
      node = rotate_right(node)
    else:
      node = rotate_left_right(node)
  return node

def resolve_right_leaning(node):
  if node.height_difference() == -2:
    if node.right.height_difference() <= 0:
      node = rotate_left(node)
    else:
      node = rotate_right_left(node)
  return node
```

These methods are invoked within `_insert()`.

The surest way to demonstrate that tree rebalancing works is to insert the values from 1 to N into an empty `BinaryTree`. Once done, the height of the root node describes how compact the structure of the tree is.

```
Copy to Editordef insert_trial(N):
  avl = BinaryTree()
  for i in range(1,N+1):
    avl.insert(i)

  print(avl.root.height)
```

The `insert_trial()` function represents the *worst case* behavior for a standard binary search tree because the values are inserted in ascending order. In a regular binary search tree, the height of the root node would be N - 1, when inserting N values. When you execute this code for N = 2k - 1, the height of the AVL tree is k - 1. Try it out! 

```
python -i avl.py 
insert_trial(16383) 
insert_trial(32767) 

insert_trial(1048575) 

insert_trial(int(2**20))

quit()
```

Note that 16,383 = 2^14 - 1, which is why the height of the first AVL tree is 13. Similarly, 32,767 = 2^15 - 1, which is why the second value printed is 14.

Note, you can try N=1,048,575 and the result (in about 40 seconds) will be 19, which is the most compact representation allowed.

Advance to the next step to see how to modify `remove()` to properly rebalance a tree as values are removed.



#### Balancing an AVL Tree on remove

The AVL tree implementation uses the same approach for removing a value as described in the CHAPTER 6: BINARY TREE scenario. Specifically it locates the `node` containing the value to be deleted. Next, it determines the node, `M`, containing the minimum value in `node`'s right subtree and removes it, ultimately replacing `node` with `M`.

The `_remove_min()` helper method completes the first task.

```
Copy to Editor  def _remove_min(self, node):
    if node.left is None:
      return node.right

    # Might become right-leaning, since deleted from left
    node.left = self._remove_min(node.left)
    node = resolve_right_leaning(node)
    node.compute_height()
    return node

  # TBA: MORE
```

When removing the minimum value from a subtree, the result is that the height of the left subtree *could be reduced*, which means there is a chance that the resulting `node` is now right-leaning, and needs to be rebalanced.

Now comes the complicated `remove()`function, which has three locations where a potentially unbalanced node needs to be rebalanced.

```
Copy to Editor  def remove(self, val):
    self.root = self._remove(self.root, val)

  def _remove(self, node, val):
    if node is None:
      return None

    if val < node.value:
      node.left = self._remove(node.left, val)
      node = resolve_right_leaning(node)
    elif val > node.value:
      node.right = self._remove(node.right, val)
      node = resolve_left_leaning(node)
    else:
      if node.left is None:
        return node.right
      if node.right is None:
        return node.left

      # replace self value with node for smallest value
      original = node

      # find SMALLEST child in right subtree and remove it
      node = node.right
      while node.left:
        node = node.left

      node.right = self._remove_min(original.right)
      node.left = original.left

      # Might have made left-leaning by shrinking right side
      node = resolve_left_leaning(node)

    node.compute_height()
    return node
```

After each recursive invocation to `_remove()`, the resulting `node` could either be right-leaning (if the value being removed was in `node.left`) or left-leaning (if the value being removed was in `node.right`). In the third, and final, code location, the `node` could be left-leaning after removing the smallest value from `node`'s right subtree.

In short, the fundamental logic for insertion and removal stays the same, but there is some clean-up work that must happen whenever an unbalanced node is detected. The following `remove_trial()` creates an AVL binary tree with an odd number of values and then removes the "middle" (N+1)/2 values, leaving the N//4 lowest and highest values. 

```
Copy to Editordef remove_trial(N):
  avl = BinaryTree()
  for i in range(1,N+1):
    avl.insert(i)

  for i in range(N//4+1, N//4+(N+1)//2 + 1):
    avl.remove(i)

  print(avl.root.height)
```

Try this out with 31 values:

```
python -i avl.py remove_trial(31) quit()
```

The resulting tree is shown below, whose height is 3.

![Removing AVL values](https://www.katacoda.com/embed/orm-george-heineman/ch06-utility-balancing/assets/second.svg)

As you can see, the tree maintains a compact representation even though a number of values were deleted.