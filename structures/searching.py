"""
Manual Searching Algorithms Implementation for Social Detective.
Algorithms:
  - Linear Search: Time O(n), Space O(1)
  - Binary Search (on sorted collection): Time O(log n), Space O(1)
"""

def linear_search_with_trace(arr, target_value, key_func=None):
    """
    Linear search checking each element sequentially.
    """
    if key_func is None:
        key_func = lambda x: x

    steps = []
    for idx, item in enumerate(arr):
        val = key_func(item)
        is_match = (str(val).lower() == str(target_value).lower())
        steps.append({
            "step": idx + 1,
            "index": idx,
            "element_value": str(val),
            "target_value": str(target_value),
            "matched": is_match,
            "description": f"Checked index {idx}: value '{val}' {'== ' + str(target_value) + ' (MATCH)' if is_match else '!= ' + str(target_value)}"
        })
        if is_match:
            return {
                "algorithm": "Linear Search",
                "found": True,
                "index": idx,
                "item": item,
                "steps": steps,
                "total_comparisons": idx + 1,
                "time_complexity": "O(n)"
            }

    return {
        "algorithm": "Linear Search",
        "found": False,
        "index": -1,
        "item": None,
        "steps": steps,
        "total_comparisons": len(arr),
        "time_complexity": "O(n)"
    }


def binary_search_with_trace(sorted_arr, target_value, key_func=None):
    """
    Binary search on a sorted array with low, mid, high pointers.
    Time Complexity: O(log n)
    """
    if key_func is None:
        key_func = lambda x: x

    try:
        target_num = float(target_value)
        is_numeric = True
    except (ValueError, TypeError):
        is_numeric = False
        target_str = str(target_value).lower()

    low = 0
    high = len(sorted_arr) - 1
    steps = []
    step_num = 1

    while low <= high:
        mid = (low + high) // 2
        mid_item = sorted_arr[mid]
        mid_val = key_func(mid_item)

        if is_numeric:
            try:
                mid_num = float(mid_val)
                val_equal = (mid_num == target_num)
                val_less = (mid_num < target_num)
            except (ValueError, TypeError):
                val_equal = (str(mid_val) == str(target_value))
                val_less = (str(mid_val) < str(target_value))
        else:
            mid_str = str(mid_val).lower()
            val_equal = (mid_str == target_str)
            val_less = (mid_str < target_str)

        steps.append({
            "step": step_num,
            "low": low,
            "mid": mid,
            "high": high,
            "mid_value": str(mid_val),
            "target": str(target_value),
            "action": f"Low={low}, Mid={mid} (Val={mid_val}), High={high}"
        })

        if val_equal:
            steps[-1]["result"] = "TARGET FOUND"
            return {
                "algorithm": "Binary Search",
                "found": True,
                "index": mid,
                "item": mid_item,
                "steps": steps,
                "total_comparisons": step_num,
                "time_complexity": "O(log n)"
            }
        elif val_less:
            steps[-1]["decision"] = f"{mid_val} < {target_value} -> Search RIGHT half (low = mid + 1)"
            low = mid + 1
        else:
            steps[-1]["decision"] = f"{mid_val} > {target_value} -> Search LEFT half (high = mid - 1)"
            high = mid - 1

        step_num += 1

    return {
        "algorithm": "Binary Search",
        "found": False,
        "index": -1,
        "item": None,
        "steps": steps,
        "total_comparisons": step_num - 1,
        "time_complexity": "O(log n)"
    }
