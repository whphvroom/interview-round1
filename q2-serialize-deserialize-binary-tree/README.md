# Q2: Serialize and Deserialize Binary Tree

**Difficulty:** Hard

---

## Problem

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Implement the `Codec` class:

- `serialize(root)` — Encodes a tree to a single string.
- `deserialize(data)` — Decodes your encoded data to the original tree.

---

## Examples

### Example 1

```
Input:  root = [1, 2, 3, null, null, 4, 5]
Output: [1, 2, 3, null, null, 4, 5]
```

```
      1
     / \
    2   3
       / \
      4   5
```

The tree must survive a serialize → deserialize roundtrip intact.

### Example 2

```
Input:  root = []
Output: []
```

---

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-1000 <= Node.val <= 1000`

---

## Testing Your Solution

Your solution goes in `solution_template.py`. Once you've implemented `serialize` and `deserialize` inside the `Codec` class, run:

```bash
# Install pytest if you don't have it
pip install pytest

# Run all tests
pytest test_solution.py -v
```

All tests must pass for a complete solution.
