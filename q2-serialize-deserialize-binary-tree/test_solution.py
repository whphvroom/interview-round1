"""
Test suite for Q2: Serialize and Deserialize Binary Tree

Run with:  pytest test_solution.py -v

NOTE: The serialization format is not tested — only the roundtrip property:
      deserialize(serialize(tree))  must produce a structurally identical tree.
"""
import pytest
from collections import deque
from solution_template import Codec


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_tree(vals: list) -> TreeNode:
    """Build a tree from a level-order list (None = absent node)."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def trees_equal(a: TreeNode, b: TreeNode) -> bool:
    """Return True iff two trees are structurally identical with equal values (iterative)."""
    stack = [(a, b)]
    while stack:
        x, y = stack.pop()
        if x is None and y is None:
            continue
        if x is None or y is None or x.val != y.val:
            return False
        stack.append((x.left, y.left))
        stack.append((x.right, y.right))
    return True


def roundtrip(vals: list) -> bool:
    """Build a tree, serialize it, deserialize it, and check equality."""
    codec = Codec()
    original = build_tree(vals)
    result = codec.deserialize(codec.serialize(original))
    return trees_equal(original, result)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestCodec:

    # --- Problem statement examples ------------------------------------------

    def test_example1(self):
        assert roundtrip([1, 2, 3, None, None, 4, 5])

    def test_example2_empty_tree(self):
        assert roundtrip([])

    # --- Single node ---------------------------------------------------------

    def test_single_node_positive(self):
        assert roundtrip([42])

    def test_single_node_zero(self):
        assert roundtrip([0])

    def test_single_node_negative(self):
        assert roundtrip([-7])

    def test_single_node_min_value(self):
        assert roundtrip([-1000])

    def test_single_node_max_value(self):
        assert roundtrip([1000])

    # --- Shape variants ------------------------------------------------------

    def test_complete_binary_tree(self):
        assert roundtrip([1, 2, 3, 4, 5, 6, 7])

    def test_left_skewed(self):
        # Linked list going left: 1 -> 2 -> 3 -> 4 -> 5
        assert roundtrip([1, 2, None, 3, None, 4, None, 5])

    def test_right_skewed(self):
        assert roundtrip([1, None, 2, None, 3, None, 4, None, 5])

    def test_only_left_children(self):
        assert roundtrip([1, 2, 3, 4, 5])

    def test_only_right_children(self):
        assert roundtrip([1, None, 2, None, 3])

    def test_left_heavy(self):
        assert roundtrip([1, 2, 3, 4, 5, None, None, 8, 9])

    def test_right_heavy(self):
        assert roundtrip([1, 2, 3, None, None, 6, 7, None, None, None, None, 12, 13])

    def test_root_only_left_child(self):
        assert roundtrip([1, 2])

    def test_root_only_right_child(self):
        assert roundtrip([1, None, 3])

    # --- Value edge cases ----------------------------------------------------

    def test_negative_values(self):
        assert roundtrip([-10, -20, -30, -40, -50])

    def test_mixed_sign_values(self):
        assert roundtrip([0, -1000, 1000, -500, 500])

    def test_duplicate_values(self):
        assert roundtrip([1, 1, 1, 1, 1, 1, 1])

    def test_all_zeros(self):
        assert roundtrip([0, 0, 0, 0, 0])

    # --- Serialize produces a string -----------------------------------------

    def test_serialize_returns_string(self):
        codec = Codec()
        tree = build_tree([1, 2, 3])
        assert isinstance(codec.serialize(tree), str)

    def test_serialize_empty_returns_string(self):
        codec = Codec()
        assert isinstance(codec.serialize(None), str)

    # --- Idempotency ---------------------------------------------------------

    def test_double_roundtrip(self):
        codec = Codec()
        original = build_tree([1, 2, 3, None, None, 4, 5])
        once = codec.deserialize(codec.serialize(original))
        twice = codec.deserialize(codec.serialize(once))
        assert trees_equal(original, twice)

    def test_independent_codec_instances(self):
        # Two separate Codec instances must agree
        c1, c2 = Codec(), Codec()
        tree = build_tree([5, 3, 8, 1, 4, 7, 9])
        serialized = c1.serialize(tree)
        result = c2.deserialize(serialized)
        assert trees_equal(tree, result)

    # --- Large tree ----------------------------------------------------------

    def test_large_right_chain(self):
        # 10^4 nodes in a right-skewed chain
        n = 10_000
        root = TreeNode(0)
        cur = root
        for i in range(1, n):
            cur.right = TreeNode(i % 2001 - 1000)
            cur = cur.right
        codec = Codec()
        result = codec.deserialize(codec.serialize(root))
        assert trees_equal(root, result)

    def test_large_complete_tree(self):
        # ~1000 nodes in a complete binary tree
        vals = [i % 2001 - 1000 for i in range(1000)]
        assert roundtrip(vals)
