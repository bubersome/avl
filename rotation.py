def rotate_right(node):
    """Perform right rotation around given node."""
    new_root = node.left
    grandson = new_root.right
    node.left = grandson
    new_root.right = node

    node.compute_height()
    return new_root

def rotate_left(node):
    """Perform left rotation around given node."""
    new_root = node.right
    grandson = new_root.left
    node.right = grandson
    new_root.left = node

    node.compute_height()
    return new_root

def rotate_left_right(node):
    """Perform left, then right rotation around given node."""
    child = node.left
    new_root = child.right
    grand1  = new_root.left
    grand2  = new_root.right
    child.right = grand1
    node.left = grand2

    new_root.left = child
    new_root.right = node

    child.compute_height()
    node.compute_height()
    return new_root

def rotate_right_left(node):
    """Perform right, then left rotation around given node."""
    child = node.right
    new_root = child.left
    grand1  = new_root.left
    grand2  = new_root.right
    child.left = grand2
    node.right = grand1

    new_root.left = node
    new_root.right = child

    child.compute_height()
    node.compute_height()
    return new_root
