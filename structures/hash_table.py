"""
Hash Table Implementation with Separate Chaining for Social Detective.
Used for: Detective Database (Fast O(1) suspect, evidence, log lookups).
Complexity:
  - Search (Average): O(1)
  - Search (Worst): O(n) (when all keys hash to the same bucket)
  - Insert (Average): O(1)
  - Delete (Average): O(1)
  - Space: O(capacity + n)
"""

class HashNode:
    """Linked list node used for separate chaining collision resolution."""
    def __init__(self, key, value, next_node=None):
        self.key = str(key)
        self.value = value
        self.next = next_node

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "has_next": self.next is not None
        }


class HashTable:
    """
    Hash Table with separate chaining collision resolution.
    Demonstrates:
      - Custom polynomial / ASCII hash function
      - Collision handling via bucket linked lists
      - Visible bucket states & step-by-step lookup traces for academic viva
    """
    def __init__(self, capacity=11):
        # A prime number capacity for better distribution
        self.capacity = capacity
        self.buckets = [None] * capacity
        self.size = 0

    def hash_function(self, key):
        """
        Calculates bucket index:
        hash_code = sum(ord(c) * 31^i) % capacity
        """
        key_str = str(key)
        hash_code = 0
        for char in key_str:
            hash_code = (hash_code * 31 + ord(char))
        return hash_code % self.capacity

    def insert(self, key, value):
        """
        Insert or update key-value pair.
        Returns insertion trace details.
        """
        key_str = str(key)
        bucket_index = self.hash_function(key_str)
        head = self.buckets[bucket_index]

        # Check if key already exists in the chain to update
        curr = head
        while curr:
            if curr.key == key_str:
                old_val = curr.value
                curr.value = value
                return {
                    "action": "UPDATE",
                    "key": key_str,
                    "bucket_index": bucket_index,
                    "collision": head != curr
                }
            curr = curr.next

        # Key not found, insert new node at the head of the bucket chain (O(1))
        new_node = HashNode(key_str, value, head)
        self.buckets[bucket_index] = new_node
        self.size += 1

        is_collision = head is not None

        return {
            "action": "INSERT",
            "key": key_str,
            "bucket_index": bucket_index,
            "collision": is_collision,
            "chain_length": self._get_bucket_chain_length(bucket_index)
        }

    def _get_bucket_chain_length(self, index):
        count = 0
        curr = self.buckets[index]
        while curr:
            count += 1
            curr = curr.next
        return count

    def search(self, key):
        """
        Search for key and return detailed step trace for frontend animation.
        """
        key_str = str(key)
        bucket_index = self.hash_function(key_str)
        curr = self.buckets[bucket_index]

        trace = {
            "query_key": key_str,
            "hash_calculation": f"hash('{key_str}') % {self.capacity} = {bucket_index}",
            "bucket_index": bucket_index,
            "steps": [],
            "found": False,
            "value": None,
            "comparisons": 0,
            "complexity_note": "Average: O(1), Worst Case: O(n)"
        }

        step_num = 1
        while curr:
            trace["comparisons"] += 1
            is_match = (curr.key.lower() == key_str.lower())
            trace["steps"].append({
                "step": step_num,
                "current_node_key": curr.key,
                "target_key": key_str,
                "matched": is_match,
                "action": f"Comparing node key '{curr.key}' with query '{key_str}'"
            })
            if is_match:
                trace["found"] = True
                trace["value"] = curr.value
                return trace
            curr = curr.next
            step_num += 1

        return trace

    def delete(self, key):
        """Delete key from hash table. Time: O(1) avg"""
        key_str = str(key)
        bucket_index = self.hash_function(key_str)
        curr = self.buckets[bucket_index]
        prev = None

        while curr:
            if curr.key == key_str:
                if prev is None:
                    self.buckets[bucket_index] = curr.next
                else:
                    prev.next = curr.next
                self.size -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def contains(self, key):
        res = self.search(key)
        return res["found"]

    def get_buckets_state(self):
        """Return visual state of all buckets for UI display."""
        bucket_list = []
        for i in range(self.capacity):
            nodes = []
            curr = self.buckets[i]
            while curr:
                nodes.append({
                    "key": curr.key,
                    "value": curr.value
                })
                curr = curr.next
            bucket_list.append({
                "bucket_index": i,
                "count": len(nodes),
                "is_empty": len(nodes) == 0,
                "nodes": nodes
            })
        return {
            "capacity": self.capacity,
            "total_items": self.size,
            "load_factor": round(self.size / self.capacity, 2),
            "buckets": bucket_list
        }
