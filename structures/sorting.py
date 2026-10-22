"""
Manual Sorting Algorithms Implementation for Social Detective.
Algorithms:
  - Merge Sort (Divide & Conquer): Time O(n log n), Space O(n)
  - Quick Sort (Partitioning): Time O(n log n) avg, O(n^2) worst, Space O(log n)
"""

def merge_sort_with_trace(arr, key_func=None, reverse=False):
    """
    Merge Sort implementation with step trace logging for demonstration.
    """
    if key_func is None:
        key_func = lambda x: x

    steps = []
    
    def _merge(left, right, depth):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            val_l = key_func(left[i])
            val_r = key_func(right[j])
            
            condition = (val_l >= val_r) if reverse else (val_l <= val_r)
            if condition:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        steps.append({
            "action": "MERGE",
            "depth": depth,
            "left_size": len(left),
            "right_size": len(right),
            "merged_size": len(merged),
            "description": f"Merged sorted partitions of sizes {len(left)} and {len(right)}"
        })
        return merged

    def _sort(sub_arr, depth=0):
        if len(sub_arr) <= 1:
            return sub_arr
        
        mid = len(sub_arr) // 2
        left_partition = sub_arr[:mid]
        right_partition = sub_arr[mid:]
        
        steps.append({
            "action": "SPLIT",
            "depth": depth,
            "mid_index": mid,
            "description": f"Divided list of size {len(sub_arr)} into [{len(left_partition)}] and [{len(right_partition)}]"
        })
        
        sorted_left = _sort(left_partition, depth + 1)
        sorted_right = _sort(right_partition, depth + 1)
        
        return _merge(sorted_left, sorted_right, depth)

    sorted_result = _sort(list(arr))
    return {
        "algorithm": "Merge Sort",
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "sorted_items": sorted_result,
        "steps": steps,
        "total_steps": len(steps)
    }


def quick_sort_with_trace(arr, key_func=None, reverse=False):
    """
    Quick Sort implementation with pivot selection and partition tracing.
    """
    if key_func is None:
        key_func = lambda x: x

    steps = []

    def _quick_sort(items, depth=0):
        if len(items) <= 1:
            return items

        pivot = items[len(items) // 2]
        pivot_val = key_func(pivot)

        less = []
        equal = []
        greater = []

        for item in items:
            val = key_func(item)
            if val < pivot_val:
                less.append(item)
            elif val > pivot_val:
                greater.append(item)
            else:
                equal.append(item)

        steps.append({
            "action": "PARTITION",
            "depth": depth,
            "pivot_val": str(pivot_val),
            "less_count": len(less),
            "equal_count": len(equal),
            "greater_count": len(greater),
            "description": f"Partitioned around pivot '{pivot_val}' -> Less: {len(less)}, Equal: {len(equal)}, Greater: {len(greater)}"
        })

        if reverse:
            return _quick_sort(greater, depth + 1) + equal + _quick_sort(less, depth + 1)
        else:
            return _quick_sort(less, depth + 1) + equal + _quick_sort(greater, depth + 1)

    sorted_result = _quick_sort(list(arr))
    return {
        "algorithm": "Quick Sort",
        "time_complexity": "O(n log n) average, O(n^2) worst case",
        "space_complexity": "O(log n)",
        "sorted_items": sorted_result,
        "steps": steps,
        "total_steps": len(steps)
    }
