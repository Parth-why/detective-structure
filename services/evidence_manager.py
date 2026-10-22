"""
Evidence Manager Service for Social Detective.
Integrates custom Data Structures:
  - HashTable (Detective Database lookups)
  - LinkedList (Evidence Clue Chain)
  - DoublyLinkedList (Case Timeline)
  - BinarySearchTree (Indexed Evidence & Inorder Sort)
  - MaxHeap (Priority Forensics)
  - Tree (Case Hierarchy)
"""
import json
import os
from structures.hash_table import HashTable
from structures.linked_list import LinkedList
from structures.doubly_linked_list import DoublyLinkedList
from structures.bst import BinarySearchTree
from structures.heap import MaxHeap
from structures.tree import Tree, TreeNode

class EvidenceManagerService:
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir

        self.hash_table = HashTable(capacity=13)
        self.evidence_chain = LinkedList()
        self.timeline_list = DoublyLinkedList()
        self.bst = BinarySearchTree()
        self.max_heap = MaxHeap()
        self.case_tree = Tree(root_name="CASE_001_THE_VANISHING_FILE", root_type="case_root")

        self.evidence_items = []
        self.timeline_events = []
        self.load_all_data()

    def load_all_data(self):
        self._load_evidence()
        self._load_timeline()
        self._load_users_into_hash()
        self._load_tree()

    def _load_evidence(self):
        ev_file = os.path.join(self.data_dir, "evidence.json")
        with open(ev_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
            self.evidence_items = raw.get("evidence", [])

        # 1. Populate Hash Table with various search keys (ID, HashKey, Title keyword)
        for ev in self.evidence_items:
            # Hash by numeric ID and hash_key
            self.hash_table.insert(str(ev["id"]), {"type": "evidence", "data": ev})
            if "hash_key" in ev:
                self.hash_table.insert(ev["hash_key"], {"type": "evidence", "data": ev})

            # 2. Populate BST (Indexed by integer Evidence ID)
            self.bst.insert(ev["id"], ev)

            # 3. Populate MaxHeap (Prioritized by Credibility Score)
            self.max_heap.insert(ev["credibility_score"], ev)

        # 4. Populate LinkedList Evidence Chain (Sequential linking of primary clues)
        chain_order = [1020, 1047, 1061, 1075, 1120, 1160, 1190]
        ev_map = {ev["id"]: ev for ev in self.evidence_items}
        for eid in chain_order:
            if eid in ev_map:
                self.evidence_chain.append(ev_map[eid])

    def _load_timeline(self):
        tl_file = os.path.join(self.data_dir, "timeline.json")
        with open(tl_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
            self.timeline_events = raw.get("events", [])

        for evt in self.timeline_events:
            self.timeline_list.append(evt)
            # Index event ID in Hash Table as well
            self.hash_table.insert(evt["id"], {"type": "timeline_event", "data": evt})

    def _load_users_into_hash(self):
        user_file = os.path.join(self.data_dir, "users.json")
        with open(user_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
            users = raw.get("users", [])

        for u in users:
            # Index username (@ryan_47), user ID (ryan_mehta), keycard (KC-4410)
            self.hash_table.insert(u["username"].lower(), {"type": "user", "data": u})
            self.hash_table.insert(u["id"].lower(), {"type": "user", "data": u})
            if "keycard_id" in u:
                self.hash_table.insert(u["keycard_id"].lower(), {"type": "keycard", "data": u})

    def _load_tree(self):
        tree_file = os.path.join(self.data_dir, "tree_data.json")
        with open(tree_file, "r", encoding="utf-8") as f:
            tree_raw = json.load(f)

        def _build_nodes(parent_name, children_list):
            for ch in children_list:
                node = TreeNode(ch["name"], ch.get("type", "node"), ch.get("data", {}))
                self.case_tree.add_child(parent_name, node)
                if "children" in ch and ch["children"]:
                    _build_nodes(ch["name"], ch["children"])

        if "children" in tree_raw:
            _build_nodes(self.case_tree.root.name, tree_raw["children"])

    # --- Hash Table Operations ---
    def search_database(self, query):
        """Search Detective Database using custom HashTable with collision resolution."""
        return self.hash_table.search(query.strip().lower())

    def get_hash_table_state(self):
        return self.hash_table.get_buckets_state()

    # --- Linked List Operations ---
    def traverse_evidence_chain(self):
        """Step-by-step traversal of the Singly Linked List clue chain."""
        return {
            "chain": self.evidence_chain.to_list(),
            "steps": self.evidence_chain.get_step_by_step_traversal(),
            "total_nodes": self.evidence_chain.length(),
            "time_complexity": "O(n)",
            "space_complexity": "O(1)"
        }

    # --- Doubly Linked List Operations ---
    def get_timeline_forward(self):
        return {
            "events": self.timeline_list.traverse_forward(),
            "steps": self.timeline_list.get_forward_steps(),
            "direction": "FORWARD",
            "pointer": "next",
            "time_complexity": "O(n)"
        }

    def get_timeline_backward(self):
        return {
            "events": self.timeline_list.traverse_backward(),
            "steps": self.timeline_list.get_backward_steps(),
            "direction": "BACKWARD",
            "pointer": "prev",
            "time_complexity": "O(n)"
        }

    def get_timeline_event_at(self, index):
        return self.timeline_list.get_node_at(index)

    def get_timeline_length(self):
        return self.timeline_list.length()

    # --- BST Operations ---
    def bst_search(self, evidence_id):
        return self.bst.search(evidence_id)

    def bst_inorder(self):
        return self.bst.inorder()

    def bst_preorder(self):
        return self.bst.preorder()

    def bst_postorder(self):
        return self.bst.postorder()

    def get_bst_tree_dict(self):
        return self.bst.to_dict_tree()

    # --- Max-Heap Operations ---
    def heap_peek_strongest(self):
        return self.max_heap.peek()

    def heap_extract_strongest(self):
        return self.max_heap.extract_max()

    def get_heap_state(self):
        return {
            "size": self.max_heap.size(),
            "items": self.max_heap.to_list(),
            "tree": self.max_heap.get_tree_representation()
        }

    # --- Tree Traversals ---
    def tree_preorder(self):
        return self.case_tree.preorder()

    def tree_postorder(self):
        return self.case_tree.postorder()

    def tree_level_order(self):
        return self.case_tree.level_order()

    def get_case_tree_hierarchy(self):
        return self.case_tree.to_hierarchy_dict()

    # --- General getters ---
    def get_all_evidence(self):
        return self.evidence_items

    def get_evidence_by_id(self, eid):
        for ev in self.evidence_items:
            if ev["id"] == int(eid):
                return ev
        return None
