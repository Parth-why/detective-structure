"""
Automated Test Suite for Social Detective Custom Data Structures and Algorithms.
"""
import pytest
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from structures.linked_list import LinkedList
from structures.doubly_linked_list import DoublyLinkedList
from structures.stack import Stack
from structures.queue import Queue
from structures.circular_queue import CircularQueue
from structures.hash_table import HashTable
from structures.graph import Graph
from structures.tree import Tree, TreeNode
from structures.bst import BinarySearchTree
from structures.heap import MaxHeap
from structures.sorting import merge_sort_with_trace, quick_sort_with_trace
from structures.searching import linear_search_with_trace, binary_search_with_trace
from services.case_engine import CaseEngine

# --- 1. Singly Linked List Tests ---
def test_linked_list():
    ll = LinkedList()
    assert ll.is_empty()
    ll.append({"id": 101, "title": "Clue 1"})
    ll.append({"id": 102, "title": "Clue 2"})
    ll.prepend({"id": 100, "title": "Clue 0"})
    assert ll.length() == 3

    items = ll.to_list()
    assert [item["id"] for item in items] == [100, 101, 102]

    # Search
    search_res = ll.search(lambda x: x["id"] == 101)
    assert search_res["found"] is True
    assert search_res["index"] == 1

    # Steps
    steps = ll.get_step_by_step_traversal()
    assert len(steps) == 3

    # Delete
    deleted = ll.delete(key_func=lambda x: x["id"] == 101)
    assert deleted is True
    assert ll.length() == 2
    assert [item["id"] for item in ll.to_list()] == [100, 102]

# --- 2. Doubly Linked List Tests ---
def test_doubly_linked_list():
    dll = DoublyLinkedList()
    dll.append({"time": "19:00", "event": "Start"})
    dll.append({"time": "19:30", "event": "Middle"})
    dll.append({"time": "20:00", "event": "End"})
    assert dll.length() == 3

    forward = dll.traverse_forward()
    assert [e["time"] for e in forward] == ["19:00", "19:30", "20:00"]

    backward = dll.traverse_backward()
    assert [e["time"] for e in backward] == ["20:00", "19:30", "19:00"]

    # Forward & backward step records
    f_steps = dll.get_forward_steps()
    b_steps = dll.get_backward_steps()
    assert len(f_steps) == 3
    assert len(b_steps) == 3

    # Get node at index
    node_info = dll.get_node_at(1)
    assert node_info["data"]["event"] == "Middle"
    assert node_info["prev_data"]["event"] == "Start"
    assert node_info["next_data"]["event"] == "End"

# --- 3. Stack Tests ---
def test_stack():
    st = Stack()
    assert st.is_empty()
    st.push("Page: Home")
    st.push("Suspect: Maya")
    st.push("Suspect: Ryan")
    assert st.size() == 3
    assert st.peek() == "Suspect: Ryan"

    # LIFO Pop
    popped = st.pop()
    assert popped == "Suspect: Ryan"
    assert st.peek() == "Suspect: Maya"
    assert st.size() == 2

# --- 4. Queue Tests ---
def test_queue():
    q = Queue()
    assert q.is_empty()
    q.enqueue("Clue A")
    q.enqueue("Clue B")
    q.enqueue("Clue C")
    assert q.size() == 3
    assert q.front() == "Clue A"
    assert q.rear() == "Clue C"

    # FIFO Dequeue
    dequeued = q.dequeue()
    assert dequeued == "Clue A"
    assert q.front() == "Clue B"
    assert q.size() == 2

# --- 5. Circular Queue Tests ---
def test_circular_queue():
    cq = CircularQueue(capacity=3)
    assert cq.is_empty()
    cq.enqueue("CAM_1")
    cq.enqueue("CAM_2")
    cq.enqueue("CAM_3")
    assert cq.is_full()

    # Overflow protection
    overflow = cq.enqueue("CAM_4")
    assert overflow["success"] is False

    # Cycle Next (Dequeue + Enqueue)
    assert cq.peek() == "CAM_1"
    res = cq.cycle_next()
    assert res["cycled_item"] == "CAM_1"
    assert cq.peek() == "CAM_2"

# --- 6. Hash Table Tests ---
def test_hash_table():
    ht = HashTable(capacity=5)
    ht.insert("dr_maya", {"role": "Victim"})
    ht.insert("ryan_47", {"role": "Culprit"})
    ht.insert("sam_sys", {"role": "Accomplice"})

    # Search
    res_ryan = ht.search("ryan_47")
    assert res_ryan["found"] is True
    assert res_ryan["value"]["role"] == "Culprit"

    res_missing = ht.search("unknown_user")
    assert res_missing["found"] is False

    # Bucket states
    bstate = ht.get_buckets_state()
    assert bstate["total_items"] == 3

# --- 7. Graph Tests ---
def test_graph_bfs_dfs_shortest_path():
    g = Graph()
    g.add_edge("Maya", "Ryan")
    g.add_edge("Ryan", "Sam")
    g.add_edge("Sam", "Arjun")
    g.add_edge("Maya", "Aisha")
    g.add_edge("Aisha", "Arjun")

    # BFS
    bfs_res = g.bfs("Maya", "Arjun")
    assert bfs_res["target_found"] is True
    assert bfs_res["distance"] == 2  # Maya -> Aisha -> Arjun or Maya -> Ryan (if 2 hops)
    assert len(bfs_res["steps"]) > 0

    # DFS
    dfs_res = g.dfs("Maya", "Arjun")
    assert "Arjun" in dfs_res["visited_order"]

    # Mutual Connections
    mutual = g.mutual_connections("Maya", "Sam")
    assert "Ryan" in mutual["mutual_suspect_ids"]

    # Degree
    assert g.degree("Maya") == 2

# --- 8. Tree Tests ---
def test_hierarchy_tree():
    tree = Tree("CASE_ROOT")
    p = TreeNode("PEOPLE")
    d = TreeNode("DIGITAL")
    tree.root.add_child(p)
    tree.root.add_child(d)
    p.add_child(TreeNode("SUSPECT_RYAN"))

    preorder = tree.preorder()
    assert preorder["visited_order"][0] == "CASE_ROOT"
    assert "SUSPECT_RYAN" in preorder["visited_order"]

    postorder = tree.postorder()
    assert postorder["visited_order"][-1] == "CASE_ROOT"

# --- 9. BST Tests ---
def test_binary_search_tree():
    bst = BinarySearchTree()
    keys = [50, 30, 70, 20, 40, 60, 80]
    for k in keys:
        bst.insert(k, f"Evidence #{k}")

    # Search with decision steps
    search_res = bst.search(40)
    assert search_res["found"] is True
    assert search_res["value"] == "Evidence #40"

    # Inorder Traversal must be perfectly sorted!
    inorder_res = bst.inorder()
    assert inorder_res["sorted_keys"] == [20, 30, 40, 50, 60, 70, 80]

    # Preorder & Postorder
    pre_res = bst.preorder()
    assert pre_res["keys"][0] == 50

# --- 10. Max-Heap Tests ---
def test_max_heap():
    heap = MaxHeap()
    heap.insert(65, "Witness statement")
    heap.insert(95, "CCTV Camera 04")
    heap.insert(80, "Phone log")
    heap.insert(98, "Terminal 04 Exfiltration Log")

    assert heap.peek()["priority"] == 98
    extracted = heap.extract_max()
    assert extracted["extracted_item"]["priority"] == 98
    assert heap.peek()["priority"] == 95

# --- 11. Sorting & Searching Tests ---
def test_sorting_and_searching():
    nums = [{"val": 47}, {"val": 12}, {"val": 99}, {"val": 35}]
    
    # Merge Sort
    ms = merge_sort_with_trace(nums, key_func=lambda x: x["val"], reverse=False)
    assert [x["val"] for x in ms["sorted_items"]] == [12, 35, 47, 99]

    # Quick Sort
    qs = quick_sort_with_trace(nums, key_func=lambda x: x["val"], reverse=False)
    assert [x["val"] for x in qs["sorted_items"]] == [12, 35, 47, 99]

    # Binary Search
    sorted_list = ms["sorted_items"]
    bs = binary_search_with_trace(sorted_list, 47, key_func=lambda x: x["val"])
    assert bs["found"] is True
    assert bs["index"] == 2

    # Linear Search
    ls = linear_search_with_trace(nums, 99, key_func=lambda x: x["val"])
    assert ls["found"] is True
    assert ls["index"] == 2

# --- 12. Case Engine Accusation & Score Tests ---
def test_case_engine():
    engine = CaseEngine()
    summary = engine.get_case_summary()
    assert summary["case_id"] == "CASE_001"
    assert summary["total_suspects"] == 13

    # Wrong accusation test
    wrong_res = engine.verify_accusation("arjun_kulkarni")
    assert wrong_res["success"] is False
    assert wrong_res["verdict"] == "INCORRECT"

    # Correct accusation test
    correct_res = engine.verify_accusation("ryan_mehta")
    assert correct_res["success"] is True
    assert correct_res["verdict"] == "SOLVED"
    assert correct_res["culprit"]["id"] == "ryan_mehta"
