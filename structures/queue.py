"""
Queue (FIFO - First In, First Out) Implementation for Social Detective.
Used for: Evidence Processing Pipeline, BFS frontier queue.
Complexity:
  - Enqueue: O(1)
  - Dequeue: O(1)
  - Front: O(1)
  - Rear: O(1)
  - Space: O(n)
"""

class QueueNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Queue:
    """
    Custom Node-based FIFO Queue.
    Maintains front and rear pointers for O(1) operations.
    """
    def __init__(self):
        self.front_node = None
        self.rear_node = None
        self._size = 0

    def is_empty(self):
        return self.front_node is None

    def size(self):
        return self._size

    def enqueue(self, item):
        """Enqueue item at rear of queue. Time: O(1)"""
        new_node = QueueNode(item)
        if self.rear_node is None:
            self.front_node = new_node
            self.rear_node = new_node
        else:
            self.rear_node.next = new_node
            self.rear_node = new_node
        self._size += 1
        return {
            "action": "ENQUEUE",
            "item": item,
            "size": self._size,
            "front": self.front(),
            "rear": self.rear()
        }

    def dequeue(self):
        """Dequeue item from front of queue. Time: O(1)"""
        if self.is_empty():
            return None
        dequeued_item = self.front_node.data
        self.front_node = self.front_node.next
        if self.front_node is None:
            self.rear_node = None
        self._size -= 1
        return dequeued_item

    def front(self):
        """View front item without removing it. Time: O(1)"""
        if self.is_empty():
            return None
        return self.front_node.data

    def rear(self):
        """View rear item without removing it. Time: O(1)"""
        if self.is_empty():
            return None
        return self.rear_node.data

    def clear(self):
        self.front_node = None
        self.rear_node = None
        self._size = 0

    def to_list(self):
        """Return items from FRONT to REAR."""
        items = []
        curr = self.front_node
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items

    def get_state(self):
        """Return full state representation for UI."""
        return {
            "type": "Queue (FIFO)",
            "size": self._size,
            "is_empty": self.is_empty(),
            "front": self.front(),
            "rear": self.rear(),
            "items": self.to_list(),
            "complexity": {
                "enqueue": "O(1)",
                "dequeue": "O(1)",
                "front": "O(1)"
            }
        }
