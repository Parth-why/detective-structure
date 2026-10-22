"""
Doubly Linked List Implementation for Social Detective.
Used for: Case Timeline navigation (forward & backward event tracking).
Complexity:
  - Forward Traversal: O(n)
  - Backward Traversal: O(n)
  - Insert at head / tail: O(1)
  - Delete given node reference: O(1)
  - Search: O(n)
"""

class DoublyNode:
    """A node in a doubly linked list."""
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

    def to_dict(self):
        return {
            "data": self.data,
            "has_prev": self.prev is not None,
            "has_next": self.next is not None
        }


class DoublyLinkedList:
    """
    Doubly Linked List managing bi-directional chronological timeline events.
    Academic demonstration features:
      - append, prepend, insert, delete, search
      - traverse_forward, traverse_backward
      - Detailed step snapshots for UI animation
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    def length(self):
        return self._size

    def append(self, data):
        """Append node at end of list. Time: O(1) using tail pointer"""
        new_node = DoublyNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1
        return new_node

    def prepend(self, data):
        """Insert node at beginning of list. Time: O(1)"""
        new_node = DoublyNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1
        return new_node

    def insert(self, index, data):
        """Insert node at 0-based index. Time: O(n)"""
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")
        if index == 0:
            return self.prepend(data)
        if index == self._size:
            return self.append(data)

        new_node = DoublyNode(data)
        curr = self.head
        for _ in range(index):
            curr = curr.next

        new_node.prev = curr.prev
        new_node.next = curr
        curr.prev.next = new_node
        curr.prev = new_node
        self._size += 1
        return new_node

    def delete(self, key_func=None, value=None):
        """Delete first matching node. Time: O(n)"""
        if self.head is None:
            return False

        def matches(data):
            if key_func is not None:
                return key_func(data)
            return data == value

        curr = self.head
        while curr and not matches(curr.data):
            curr = curr.next

        if curr is None:
            return False

        if curr == self.head and curr == self.tail:
            self.head = None
            self.tail = None
        elif curr == self.head:
            self.head = self.head.next
            self.head.prev = None
        elif curr == self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            curr.prev.next = curr.next
            curr.next.prev = curr.prev

        self._size -= 1
        return True

    def get_node_at(self, index):
        """Get data at index with prev/next context. Time: O(n)"""
        if index < 0 or index >= self._size:
            return None
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return {
            "index": index,
            "data": curr.data,
            "prev_data": curr.prev.data if curr.prev else None,
            "next_data": curr.next.data if curr.next else None,
            "has_prev": curr.prev is not None,
            "has_next": curr.next is not None
        }

    def traverse_forward(self):
        """Traverse from head to tail. Time: O(n)"""
        items = []
        curr = self.head
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items

    def traverse_backward(self):
        """Traverse from tail to head. Time: O(n)"""
        items = []
        curr = self.tail
        while curr:
            items.append(curr.data)
            curr = curr.prev
        return items

    def get_forward_steps(self):
        """Step-by-step forward traversal records for UI visualizer."""
        steps = []
        curr = self.head
        step_idx = 0
        while curr:
            steps.append({
                "step": step_idx + 1,
                "current": curr.data,
                "prev": curr.prev.data if curr.prev else None,
                "next": curr.next.data if curr.next else None,
                "direction": "FORWARD",
                "pointer_used": "node.next",
                "is_head": curr == self.head,
                "is_tail": curr == self.tail
            })
            curr = curr.next
            step_idx += 1
        return steps

    def get_backward_steps(self):
        """Step-by-step backward traversal records for UI visualizer."""
        steps = []
        curr = self.tail
        step_idx = 0
        while curr:
            steps.append({
                "step": step_idx + 1,
                "current": curr.data,
                "prev": curr.prev.data if curr.prev else None,
                "next": curr.next.data if curr.next else None,
                "direction": "BACKWARD",
                "pointer_used": "node.prev",
                "is_head": curr == self.head,
                "is_tail": curr == self.tail
            })
            curr = curr.prev
            step_idx += 1
        return steps

    def to_list(self):
        return self.traverse_forward()
