"""
Circular Queue Implementation for Social Detective.
Used for: Surveillance Camera Feed Monitor (rotating CCTV feeds with modulo wrap-around).
Complexity:
  - Enqueue: O(1)
  - Dequeue: O(1)
  - Peek: O(1)
  - Rotate (Cycle Next): O(1)
  - Space: O(capacity)
"""

class CircularQueue:
    """
    Fixed-capacity array-based Circular Queue using modulo arithmetic.
    Demonstrates wrap-around behavior: (index + 1) % capacity.
    """
    def __init__(self, capacity=5):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self.count = 0

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == self.capacity

    def enqueue(self, item):
        """Enqueue item into the circular buffer. Time: O(1)"""
        if self.is_full():
            return {"success": False, "message": "Queue is full (Buffer overflow)"}

        if self.front == -1:
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity

        self.queue[self.rear] = item
        self.count += 1
        return {
            "success": True,
            "action": "ENQUEUE",
            "item": item,
            "front_index": self.front,
            "rear_index": self.rear,
            "count": self.count
        }

    def dequeue(self):
        """Dequeue item from front of circular buffer. Time: O(1)"""
        if self.is_empty():
            return None

        dequeued_item = self.queue[self.front]
        self.queue[self.front] = None

        if self.front == self.rear:
            # Single item was present
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity

        self.count -= 1
        return dequeued_item

    def peek(self):
        """View current front item."""
        if self.is_empty():
            return None
        return self.queue[self.front]

    def cycle_next(self):
        """
        Special Surveillance Camera operation: Dequeue from front and Enqueue to rear!
        Continuously cycles feeds through the circular buffer.
        """
        if self.is_empty():
            return None
        item = self.dequeue()
        self.enqueue(item)
        return {
            "current_feed": self.peek(),
            "cycled_item": item,
            "state": self.get_state()
        }

    def to_list(self):
        """Return logical items in circular order from front to rear."""
        if self.is_empty():
            return []
        items = []
        idx = self.front
        for _ in range(self.count):
            items.append(self.queue[idx])
            idx = (idx + 1) % self.capacity
        return items

    def get_state(self):
        """Return low-level array slots and pointer indexes for visualization."""
        slots = []
        for i in range(self.capacity):
            slots.append({
                "index": i,
                "value": self.queue[i],
                "is_front": (i == self.front and not self.is_empty()),
                "is_rear": (i == self.rear and not self.is_empty()),
                "is_occupied": self.queue[i] is not None
            })
        return {
            "type": "Circular Queue",
            "capacity": self.capacity,
            "count": self.count,
            "front": self.front,
            "rear": self.rear,
            "is_full": self.is_full(),
            "is_empty": self.is_empty(),
            "slots": slots,
            "logical_order": self.to_list(),
            "formula": "next_index = (index + 1) % capacity"
        }
