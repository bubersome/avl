from rotation import rotate_left, rotate_right
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


class BinaryNode:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None
        self.height = 0

    def compute_height(self):
        leftH = rightH = -1
        if self.left:
            leftH = self.left.height
        if self.right:
            rightH = self.right.height
        self.height = 1 + max(leftH, rightH)

    def height_difference(self):
        leftH = rightH = -1
        if self.left:
            leftH = self.left.height
        if self.right:
            rightH = self.right.height
        return leftH - rightH


class BinaryTree:
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

    def _remove_min(self, node):
        if node.left is None:
            return node.right

        # Might become right-leaning, since deleted from left
        node.left = self._remove_min(node.left)
        node = resolve_right_leaning(node)
        node.compute_height()
        return node

    def remove(self, val):
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


def insert_trial(N):
    avl = BinaryTree()
    for i in range(1, N + 1):
        avl.insert(i)

    print(avl.root.height)


def remove_trial(N):
    avl = BinaryTree()
    for i in range(1, N + 1):
        avl.insert(i)

    for i in range(N // 4 + 1, N // 4 + (N + 1) // 2 + 1):
        avl.remove(i)

    print(avl.root.height)
