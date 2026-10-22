"""
Singly Linked List Implementation for Social Detective.
Used for: Evidence Chain (sequential clue discovery).
Complexity:
  - Traversal: O(n)
  - Search: O(n)
  - Prepend (Insert at head): O(1)
  - Append: O(n) or O(1) with tail pointer
"""

class Node:
    """A node in a singly linked list."""
    def __init__(self, data=None):
        self.data = data
        self.next = None

    def to_dict(self):
        return {
            "data": self.data,
            "has_next": self.next is not None
        }


class LinkedList:
    """
    Singly Linked List managing linear sequential evidence chains.
    Academic demonstration features:
      - append, prepend, insert, delete, search, traverse, length
      - Step-by-step traversal generator for frontend visualization
    """
    def __init__(self):
        self.head = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    def length(self):
        return self._size

    def append(self, data):
        """Append node at end of list. Time: O(n)"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self._size += 1
        return new_node

    def prepend(self, data):
        """Insert node at beginning of list. Time: O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
        return new_node

    def insert(self, index, data):
        """Insert node at 0-based index. Time: O(n)"""
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")
        if index == 0:
            return self.prepend(data)
        
        new_node = Node(data)
        curr = self.head
        for _ in range(index - 1):
            curr = curr.next
        new_node.next = curr.next
        curr.next = new_node
        self._size += 1
        return new_node

    def delete(self, key_func=None, value=None):
        """
        Delete first node matching key_func(node.data) or node.data == value.
        Time: O(n)
        """
        if self.head is None:
            return False

        # Match helper
        def matches(data):
            if key_func is not None:
                return key_func(data)
            return data == value

        if matches(self.head.data):
            self.head = self.head.next
            self._size -= 1
            return True

        curr = self.head
        while curr.next and not matches(curr.next.data):
            curr = curr.next

        if curr.next:
            curr.next = curr.next.next
            self._size -= 1
            return True
        return False

    def search(self, key_func):
        """
        Search for node where key_func(data) is True.
        Returns (index, data, steps_count) or (None, None, steps_count).
        Time: O(n)
        """
        curr = self.head
        index = 0
        steps = []
        while curr:
            steps.append({
                "step": index,
                "data": curr.data,
                "matched": bool(key_func(curr.data))
            })
            if key_func(curr.data):
                return {
                    "found": True,
                    "index": index,
                    "data": curr.data,
                    "steps": steps
                }
            curr = curr.next
            index += 1

        return {
            "found": False,
            "index": -1,
            "data": None,
            "steps": steps
        }

    def traverse(self):
        """Traverse list and return items. Time: O(n)"""
        items = []
        curr = self.head
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items

    def get_step_by_step_traversal(self):
        """
        Returns step-by-step array for frontend animated visualization.
        """
        steps = []
        curr = self.head
        step_idx = 0
        while curr:
            next_val = curr.next.data if curr.next else None
            steps.append({
                "step_number": step_idx + 1,
                "current_node": curr.data,
                "next_node": next_val,
                "is_tail": curr.next is None,
                "pointer_action": f"Following pointer: Node[{step_idx}] -> {'Node[' + str(step_idx+1) + ']' if curr.next else 'NULL'}"
            })
            curr = curr.next
            step_idx += 1
        return steps

    def to_list(self):
        return self.traverse()
