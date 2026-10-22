"""
Max-Heap (Priority Queue) Implementation for Social Detective.
Used for: Strongest Evidence Priority Queue (Highest credibility/priority clues extracted first).
Complexity:
  - Insert: O(log n)
  - Extract-Max: O(log n)
  - Peek (Get Max): O(1)
  - Space: O(n)
"""

class HeapItem:
    def __init__(self, priority, data=None):
        self.priority = float(priority)
        self.data = data or {}

    def to_dict(self):
        return {
            "priority": self.priority,
            "data": self.data
        }


class MaxHeap:
    """
    Binary Max-Heap managing priority evidence items.
    Demonstrates:
      - Bubble Up on insertion
      - Bubble Down (Heapify) on extraction
      - Highest priority evidence retrieved first
    """
    def __init__(self):
        self.heap = []

    def size(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * i + 2

    def insert(self, priority, data=None):
        """Insert element into heap and bubble up. Time: O(log n)"""
        item = HeapItem(priority, data)
        self.heap.append(item)
        steps = self._bubble_up(len(self.heap) - 1)
        return {
            "action": "HEAP_INSERT",
            "priority": priority,
            "data": data,
            "steps": steps,
            "heap_size": len(self.heap)
        }

    def _bubble_up(self, index):
        steps = []
        while index > 0 and self.heap[index].priority > self.heap[self._parent(index)].priority:
            p_idx = self._parent(index)
            steps.append({
                "action": "SWAP_BUBBLE_UP",
                "child_idx": index,
                "child_priority": self.heap[index].priority,
                "parent_idx": p_idx,
                "parent_priority": self.heap[p_idx].priority,
                "reason": f"{self.heap[index].priority} > {self.heap[p_idx].priority}"
            })
            self.heap[index], self.heap[p_idx] = self.heap[p_idx], self.heap[index]
            index = p_idx
        return steps

    def peek(self):
        """Return highest priority item without removing. Time: O(1)"""
        if self.is_empty():
            return None
        return self.heap[0].to_dict()

    def extract_max(self):
        """Remove and return highest priority item. Time: O(log n)"""
        if self.is_empty():
            return None

        max_item = self.heap[0]
        last_item = self.heap.pop()

        steps = []
        if self.heap:
            self.heap[0] = last_item
            steps = self._bubble_down(0)

        return {
            "extracted_item": max_item.to_dict(),
            "bubble_down_steps": steps,
            "remaining_size": len(self.heap)
        }

    def _bubble_down(self, index):
        steps = []
        n = len(self.heap)
        while True:
            largest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < n and self.heap[left].priority > self.heap[largest].priority:
                largest = left
            if right < n and self.heap[right].priority > self.heap[largest].priority:
                largest = right

            if largest != index:
                steps.append({
                    "action": "SWAP_BUBBLE_DOWN",
                    "parent_idx": index,
                    "parent_priority": self.heap[index].priority,
                    "largest_child_idx": largest,
                    "largest_child_priority": self.heap[largest].priority
                })
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
            else:
                break
        return steps

    def to_list(self):
        return [item.to_dict() for item in self.heap]

    def get_tree_representation(self):
        """Generates hierarchical tree dict for heap visualizer."""
        if not self.heap:
            return None

        def _build_node(i):
            if i >= len(self.heap):
                return None
            return {
                "index": i,
                "priority": self.heap[i].priority,
                "label": self.heap[i].data.get("title", f"P:{self.heap[i].priority}"),
                "data": self.heap[i].data,
                "left": _build_node(self._left_child(i)),
                "right": _build_node(self._right_child(i))
            }

        return _build_node(0)
