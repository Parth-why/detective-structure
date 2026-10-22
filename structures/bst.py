"""
Binary Search Tree (BST) Implementation for Social Detective.
Used for: Evidence ID Indexing, Sorted Retrieval via Inorder Traversal, O(log n) Search.
Complexity:
  - Search (Average): O(log n)
  - Search (Worst): O(n) (unbalanced tree)
  - Insert (Average): O(log n)
  - Delete (Average): O(log n)
  - Inorder Traversal: O(n) (Yields evidence sorted in ascending order)
"""

class BSTNode:
    """A node in a Binary Search Tree."""
    def __init__(self, key, value=None):
        self.key = int(key)
        self.value = value
        self.left = None
        self.right = None

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }


class BinarySearchTree:
    """
    Binary Search Tree organizing evidence items indexed by numeric Evidence ID.
    Demonstrates:
      - Inorder Traversal producing sorted sequence
      - Preorder & Postorder Traversals
      - Binary Search comparisons (Left/Right decisions)
      - Min and Max queries
    """
    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, key, value=None):
        """Insert key-value pair into BST. Time: O(log n) avg"""
        key = int(key)
        new_node = BSTNode(key, value)
        if self.root is None:
            self.root = new_node
            self._size += 1
            return {"inserted": True, "key": key, "is_root": True}

        curr = self.root
        while True:
            if key < curr.key:
                if curr.left is None:
                    curr.left = new_node
                    self._size += 1
                    return {"inserted": True, "key": key, "parent": curr.key, "branch": "LEFT"}
                curr = curr.left
            elif key > curr.key:
                if curr.right is None:
                    curr.right = new_node
                    self._size += 1
                    return {"inserted": True, "key": key, "parent": curr.key, "branch": "RIGHT"}
                curr = curr.right
            else:
                # Key exists, update value
                curr.value = value
                return {"inserted": False, "updated": True, "key": key}

    def search(self, key):
        """
        Search for key in BST. Returns comparison steps for visualization.
        Time: O(log n) avg
        """
        key = int(key)
        steps = []
        curr = self.root
        step_idx = 1

        while curr:
            comparison = ""
            if key == curr.key:
                comparison = f"{key} == {curr.key} -> MATCH FOUND!"
                steps.append({
                    "step": step_idx,
                    "current_node_key": curr.key,
                    "target_key": key,
                    "decision": "MATCH",
                    "comparison": comparison,
                    "matched": True
                })
                return {
                    "found": True,
                    "key": key,
                    "value": curr.value,
                    "steps": steps,
                    "total_comparisons": step_idx,
                    "time_complexity": "O(log n) average"
                }
            elif key < curr.key:
                comparison = f"{key} < {curr.key} -> Branch LEFT"
                steps.append({
                    "step": step_idx,
                    "current_node_key": curr.key,
                    "target_key": key,
                    "decision": "GO_LEFT",
                    "comparison": comparison,
                    "matched": False
                })
                curr = curr.left
            else:
                comparison = f"{key} > {curr.key} -> Branch RIGHT"
                steps.append({
                    "step": step_idx,
                    "current_node_key": curr.key,
                    "target_key": key,
                    "decision": "GO_RIGHT",
                    "comparison": comparison,
                    "matched": False
                })
                curr = curr.right
            step_idx += 1

        return {
            "found": False,
            "key": key,
            "value": None,
            "steps": steps,
            "total_comparisons": step_idx - 1,
            "time_complexity": "O(log n) average"
        }

    def find_min(self, node=None):
        """Find minimum key node in BST."""
        curr = node if node else self.root
        if curr is None:
            return None
        while curr.left:
            curr = curr.left
        return curr

    def find_max(self, node=None):
        """Find maximum key node in BST."""
        curr = node if node else self.root
        if curr is None:
            return None
        while curr.right:
            curr = curr.right
        return curr

    def delete(self, key):
        """Delete key from BST."""
        key = int(key)
        deleted = False

        def _delete_node(node, k):
            nonlocal deleted
            if node is None:
                return None
            if k < node.key:
                node.left = _delete_node(node.left, k)
            elif k > node.key:
                node.right = _delete_node(node.right, k)
            else:
                deleted = True
                # Case 1: Leaf node or 1 child
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                # Case 2: Two children -> Replace with inorder successor (min of right subtree)
                successor = self.find_min(node.right)
                node.key = successor.key
                node.value = successor.value
                node.right = _delete_node(node.right, successor.key)
            return node

        self.root = _delete_node(self.root, key)
        if deleted:
            self._size -= 1
        return deleted

    def inorder(self):
        """
        Inorder Traversal: Left -> Root -> Right.
        Critically important: Yields evidence records in ascending sorted order!
        """
        order = []
        steps = []

        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            order.append({"key": node.key, "value": node.value})
            steps.append({
                "step": len(steps) + 1,
                "key": node.key,
                "action": f"Inorder Visit: Node ID #{node.key} (Sorted Output)",
                "value": node.value
            })
            _inorder(node.right)

        _inorder(self.root)
        return {
            "traversal_type": "BST Inorder Traversal",
            "order_pattern": "Left Subtree -> Root -> Right Subtree",
            "detective_analogy": "Retrieves all indexed evidence records perfectly sorted by numeric Evidence ID.",
            "time_complexity": "O(n)",
            "sorted_keys": [item["key"] for item in order],
            "items": order,
            "steps": steps
        }

    def preorder(self):
        """Preorder Traversal: Root -> Left -> Right."""
        order = []
        steps = []

        def _preorder(node):
            if not node:
                return
            order.append({"key": node.key, "value": node.value})
            steps.append({
                "step": len(steps) + 1,
                "key": node.key,
                "action": f"Preorder Visit: Root Node #{node.key}",
                "value": node.value
            })
            _preorder(node.left)
            _preorder(node.right)

        _preorder(self.root)
        return {
            "traversal_type": "BST Preorder Traversal",
            "order_pattern": "Root -> Left -> Right",
            "detective_analogy": "Used to serialize and reconstruct the exact BST evidence index tree.",
            "time_complexity": "O(n)",
            "keys": [item["key"] for item in order],
            "items": order,
            "steps": steps
        }

    def postorder(self):
        """Postorder Traversal: Left -> Right -> Root."""
        order = []
        steps = []

        def _postorder(node):
            if not node:
                return
            _postorder(node.left)
            _postorder(node.right)
            order.append({"key": node.key, "value": node.value})
            steps.append({
                "step": len(steps) + 1,
                "key": node.key,
                "action": f"Postorder Visit: Leaf/Subtree before Node #{node.key}",
                "value": node.value
            })

        _postorder(self.root)
        return {
            "traversal_type": "BST Postorder Traversal",
            "order_pattern": "Left -> Right -> Root",
            "detective_analogy": "Bottom-up evidence verification and memory cleanup.",
            "time_complexity": "O(n)",
            "keys": [item["key"] for item in order],
            "items": order,
            "steps": steps
        }

    def to_dict_tree(self):
        return self.root.to_dict() if self.root else None
