"""
Stack (LIFO - Last In, First Out) Implementation for Social Detective.
Used for: Investigation History & Backtracking, DFS execution state.
Complexity:
  - Push: O(1)
  - Pop: O(1)
  - Peek: O(1)
  - Search: O(n)
  - Space: O(n)
"""

class StackNode:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next = next_node


class Stack:
    """
    Custom Node-based LIFO Stack.
    Maintains investigation navigation breadcrumbs allowing full Backtrack.
    """
    def __init__(self):
        self.top_node = None
        self._size = 0

    def is_empty(self):
        return self.top_node is None

    def size(self):
        return self._size

    def push(self, item):
        """Push item to top of stack. Time: O(1)"""
        new_node = StackNode(item, self.top_node)
        self.top_node = new_node
        self._size += 1
        return {
            "action": "PUSH",
            "item": item,
            "size": self._size,
            "top": self.peek()
        }

    def pop(self):
        """Pop item from top of stack. Time: O(1)"""
        if self.is_empty():
            return None
        popped_item = self.top_node.data
        self.top_node = self.top_node.next
        self._size -= 1
        return popped_item

    def peek(self):
        """View top item without removing it. Time: O(1)"""
        if self.is_empty():
            return None
        return self.top_node.data

    def clear(self):
        self.top_node = None
        self._size = 0

    def to_list(self):
        """Return stack elements from TOP to BOTTOM."""
        items = []
        curr = self.top_node
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items

    def get_state(self):
        """Return full state representation for UI."""
        return {
            "type": "Stack (LIFO)",
            "size": self._size,
            "is_empty": self.is_empty(),
            "top": self.peek(),
            "items": self.to_list(),
            "complexity": {
                "push": "O(1)",
                "pop": "O(1)",
                "peek": "O(1)"
            }
        }
