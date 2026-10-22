"""
General Tree Data Structure for Social Detective.
Used for: Hierarchical Case Structure (Case -> Categories -> Subcategories -> Evidence).
Algorithms:
  - Preorder Traversal (Root -> Children): Top-down case exploration.
  - Postorder Traversal (Children -> Root): Bottom-up evidence branch closure.
  - Level-Order Traversal (BFS breadth): Breadth-wise tier investigation.
Complexity:
  - Traversal: O(n) where n is total nodes
  - Space: O(h) where h is tree height
"""

class TreeNode:
    """A node in a general hierarchical tree."""
    def __init__(self, name, node_type="category", data=None):
        self.name = name
        self.node_type = node_type  # root, category, subcategory, clue
        self.data = data or {}
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        return child_node

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.node_type,
            "data": self.data,
            "children": [child.to_dict() for child in self.children]
        }


class Tree:
    """
    General N-ary tree representing the Case Evidence Hierarchy.
    Demonstrates Preorder (top-down) and Postorder (bottom-up) traversals.
    """
    def __init__(self, root_name="CASE_001_ROOT", root_type="case_root", data=None):
        self.root = TreeNode(root_name, root_type, data)

    def find(self, name, current_node=None):
        """Find node by name. Time: O(n)"""
        if current_node is None:
            current_node = self.root

        if current_node.name == name:
            return current_node

        for child in current_node.children:
            found = self.find(name, child)
            if found:
                return found
        return None

    def add_child(self, parent_name, child_node):
        """Find parent and add child to it."""
        parent = self.find(parent_name)
        if parent:
            parent.add_child(child_node)
            return True
        return False

    def preorder(self):
        """
        Preorder Traversal: Visit Parent before Children.
        Concept in Detective Context: Explore the case from broad categories toward specific clues.
        """
        order = []
        steps = []

        def _traverse(node, depth=0):
            if not node:
                return
            order.append(node.name)
            steps.append({
                "step": len(steps) + 1,
                "node": node.name,
                "type": node.node_type,
                "depth": depth,
                "action": f"Visited node '{node.name}' (Preorder: Root -> Subtrees)",
                "data": node.data
            })
            for child in node.children:
                _traverse(child, depth + 1)

        _traverse(self.root)
        return {
            "traversal_type": "Preorder Traversal",
            "order_pattern": "Parent -> Children (Top-Down)",
            "detective_analogy": "Investigate high-level crime categories first, drilling down into specific leads.",
            "time_complexity": "O(n)",
            "space_complexity": "O(h)",
            "visited_order": order,
            "steps": steps
        }

    def postorder(self):
        """
        Postorder Traversal: Visit Children before Parent.
        Concept in Detective Context: Conclude/close all sub-clues before marking parent category solved.
        """
        order = []
        steps = []

        def _traverse(node, depth=0):
            if not node:
                return
            for child in node.children:
                _traverse(child, depth + 1)
            order.append(node.name)
            steps.append({
                "step": len(steps) + 1,
                "node": node.name,
                "type": node.node_type,
                "depth": depth,
                "action": f"Concluded and verified node '{node.name}' (Postorder: Subtrees -> Root)",
                "data": node.data
            })

        _traverse(self.root)
        return {
            "traversal_type": "Postorder Traversal",
            "order_pattern": "Children -> Parent (Bottom-Up)",
            "detective_analogy": "Verify all individual forensic pieces before synthesizing final branch conclusions.",
            "time_complexity": "O(n)",
            "space_complexity": "O(h)",
            "visited_order": order,
            "steps": steps
        }

    def level_order(self):
        """Level-order (Breadth-First) traversal of the tree."""
        if not self.root:
            return {"visited_order": [], "steps": []}

        order = []
        steps = []
        queue = [(self.root, 0)]

        while queue:
            node, level = queue.pop(0)
            order.append(node.name)
            steps.append({
                "step": len(steps) + 1,
                "node": node.name,
                "type": node.node_type,
                "level": level,
                "action": f"Scanned Tier {level} entity: '{node.name}'",
                "data": node.data
            })
            for child in node.children:
                queue.append((child, level + 1))

        return {
            "traversal_type": "Level-Order Traversal",
            "order_pattern": "Tier by Tier (Breadth-First)",
            "visited_order": order,
            "steps": steps
        }

    def to_hierarchy_dict(self):
        return self.root.to_dict()
