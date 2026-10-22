"""
Graph Implementation (Adjacency List) for Social Detective.
Used for: Social Network investigation, connection tracing, shortest path, mutual friends.
Algorithms:
  - Breadth-First Search (BFS) using Queue: Time O(V + E), Space O(V)
  - Depth-First Search (DFS) using Stack / Recursion: Time O(V + E), Space O(V)
  - Shortest Path (BFS on unweighted graph): Time O(V + E)
  - Degree Centrality & Mutual Connections
"""

class Graph:
    """
    Undirected / Directed Graph using Adjacency List representation.
    Includes rich step traces for educational visualization during gameplay.
    """
    def __init__(self):
        self.adjacency_list = {}
        self.vertices_data = {}

    def add_vertex(self, vertex, data=None):
        """Add a vertex (suspect/node) to the graph."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            self.vertices_data[vertex] = data or {"id": vertex, "name": str(vertex)}
        elif data is not None:
            self.vertices_data[vertex] = data

    def add_edge(self, u, v, weight=1, bidirectional=True):
        """Add an edge between u and v."""
        if u not in self.adjacency_list:
            self.add_vertex(u)
        if v not in self.adjacency_list:
            self.add_vertex(v)

        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        if bidirectional and u not in self.adjacency_list[v]:
            self.adjacency_list[v].append(u)

    def remove_edge(self, u, v, bidirectional=True):
        """Remove edge between u and v."""
        if u in self.adjacency_list and v in self.adjacency_list[u]:
            self.adjacency_list[u].remove(v)
        if bidirectional and v in self.adjacency_list and u in self.adjacency_list[v]:
            self.adjacency_list[v].remove(u)

    def get_neighbors(self, vertex):
        """Return list of adjacent neighbors."""
        return self.adjacency_list.get(vertex, [])

    def has_edge(self, u, v):
        """Check if edge exists between u and v."""
        return v in self.adjacency_list.get(u, [])

    def degree(self, vertex):
        """Return degree (number of connections) of a vertex."""
        return len(self.adjacency_list.get(vertex, []))

    def find_highest_degree(self):
        """Find the most connected node(s) in the social network."""
        if not self.adjacency_list:
            return None, 0
        max_deg = -1
        top_vertices = []
        for v in self.adjacency_list:
            deg = self.degree(v)
            if deg > max_deg:
                max_deg = deg
                top_vertices = [v]
            elif deg == max_deg:
                top_vertices.append(v)
        return top_vertices, max_deg

    def mutual_connections(self, u, v):
        """
        Find mutual connections between two suspects (Set intersection of neighbors).
        Time: O(deg(u) + deg(v))
        """
        neighbors_u = set(self.get_neighbors(u))
        neighbors_v = set(self.get_neighbors(v))
        mutual_ids = list(neighbors_u.intersection(neighbors_v))
        return {
            "user_a": u,
            "user_b": v,
            "mutual_count": len(mutual_ids),
            "mutual_suspect_ids": mutual_ids,
            "mutual_suspects": [self.vertices_data.get(mid, {"id": mid}) for mid in mutual_ids]
        }

    def bfs(self, start, target=None):
        """
        Breadth-First Search (BFS) using a FIFO Queue.
        Generates step-by-step trace snapshots for front-end queue animation.
        Returns:
          - visited_order: list of nodes in order visited
          - shortest_path: list of nodes from start to target (if target found)
          - distance: number of hops to target
          - steps: step-by-step trace snapshots with live queue contents
        """
        if start not in self.adjacency_list:
            return {"error": f"Start node '{start}' not found in graph."}

        steps = []
        visited = set([start])
        queue = [start]  # Conceptual FIFO Queue
        parent = {start: None}
        visited_order = []
        target_found = False

        step_idx = 1
        steps.append({
            "step": step_idx,
            "action": "INIT",
            "current_node": start,
            "queue_state": list(queue),
            "visited": list(visited),
            "description": f"Initialized BFS at starting node '{start}'. Enqueued into Queue."
        })

        while queue:
            current = queue.pop(0)  # Dequeue from front
            visited_order.append(current)

            step_idx += 1
            steps.append({
                "step": step_idx,
                "action": "DEQUEUE_VISIT",
                "current_node": current,
                "queue_state": list(queue),
                "visited": list(visited),
                "description": f"Dequeued '{current}' from front of queue. Exploring its neighbors."
            })

            if target and current == target:
                target_found = True
                steps.append({
                    "step": step_idx + 1,
                    "action": "TARGET_FOUND",
                    "current_node": current,
                    "queue_state": list(queue),
                    "visited": list(visited),
                    "description": f"🎯 Target '{target}' reached successfully!"
                })
                break

            unvisited_neighbors = []
            for neighbor in self.adjacency_list.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)  # Enqueue to rear
                    unvisited_neighbors.append(neighbor)

            if unvisited_neighbors:
                step_idx += 1
                steps.append({
                    "step": step_idx,
                    "action": "ENQUEUE_NEIGHBORS",
                    "current_node": current,
                    "added_neighbors": unvisited_neighbors,
                    "queue_state": list(queue),
                    "visited": list(visited),
                    "description": f"Enqueued unvisited neighbors of '{current}': {', '.join(unvisited_neighbors)}"
                })

        # Reconstruct path if target specified
        path = []
        distance = -1
        if target and target in parent:
            curr = target
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            distance = len(path) - 1

        return {
            "algorithm": "Breadth-First Search (BFS)",
            "data_structure_used": "Queue (FIFO)",
            "time_complexity": "O(V + E)",
            "space_complexity": "O(V)",
            "start": start,
            "target": target,
            "target_found": target_found if target else None,
            "visited_order": visited_order,
            "shortest_path": path if target else None,
            "distance": distance if target else None,
            "steps": steps
        }

    def dfs(self, start, target=None):
        """
        Depth-First Search (DFS) using LIFO Stack / Recursion.
        Generates step-by-step trace snapshots with Call Stack / Stack states.
        """
        if start not in self.adjacency_list:
            return {"error": f"Start node '{start}' not found in graph."}

        steps = []
        visited = set()
        visited_order = []
        call_stack = []
        parent = {}
        target_found = False

        def _dfs_recursive(current, prev=None):
            nonlocal target_found
            if target_found:
                return

            visited.add(current)
            visited_order.append(current)
            call_stack.append(current)  # Push to call stack
            if prev:
                parent[current] = prev

            steps.append({
                "step": len(steps) + 1,
                "action": "PUSH_VISIT",
                "current_node": current,
                "stack_state": list(call_stack),
                "visited": list(visited),
                "description": f"PUSH '{current}' onto DFS Call Stack. Exploring deepest adjacent branch."
            })

            if target and current == target:
                target_found = True
                steps.append({
                    "step": len(steps) + 1,
                    "action": "TARGET_FOUND",
                    "current_node": current,
                    "stack_state": list(call_stack),
                    "visited": list(visited),
                    "description": f"🎯 Target '{target}' found by DFS!"
                })
                return

            for neighbor in self.adjacency_list.get(current, []):
                if neighbor not in visited:
                    _dfs_recursive(neighbor, current)
                    if target_found:
                        return

            # Backtracking
            popped = call_stack.pop()
            steps.append({
                "step": len(steps) + 1,
                "action": "POP_BACKTRACK",
                "current_node": popped,
                "stack_state": list(call_stack),
                "visited": list(visited),
                "description": f"POP '{popped}' from stack. Backtracking to explore alternative branches."
            })

        _dfs_recursive(start)

        path = []
        if target and target in parent:
            curr = target
            while curr != start:
                path.append(curr)
                curr = parent.get(curr, start)
            path.append(start)
            path.reverse()

        return {
            "algorithm": "Depth-First Search (DFS)",
            "data_structure_used": "Stack / Recursion (LIFO)",
            "time_complexity": "O(V + E)",
            "space_complexity": "O(V)",
            "start": start,
            "target": target,
            "visited_order": visited_order,
            "path": path if target else visited_order,
            "steps": steps
        }

    def shortest_path(self, start, target):
        """Find shortest connection path using BFS."""
        bfs_res = self.bfs(start, target)
        return {
            "start": start,
            "target": target,
            "path": bfs_res.get("shortest_path", []),
            "distance": bfs_res.get("distance", -1),
            "trace_steps": bfs_res.get("steps", [])
        }

    def radius_search(self, start, max_hops=2):
        """Find all suspects within 1, 2, or 3 hops of the start suspect."""
        if start not in self.adjacency_list:
            return {}

        distances = {start: 0}
        queue = [(start, 0)]
        results_by_hop = {i: [] for i in range(1, max_hops + 1)}

        while queue:
            curr, dist = queue.pop(0)
            if dist < max_hops:
                for neighbor in self.adjacency_list.get(curr, []):
                    if neighbor not in distances:
                        distances[neighbor] = dist + 1
                        results_by_hop[dist + 1].append({
                            "id": neighbor,
                            "data": self.vertices_data.get(neighbor, {}),
                            "hops": dist + 1
                        })
                        queue.append((neighbor, dist + 1))

        return {
            "center": start,
            "max_hops": max_hops,
            "results_by_hop": results_by_hop,
            "all_reachable": list(distances.keys())
        }

    def connected_components(self):
        """Find all connected social clusters in the network."""
        visited = set()
        components = []

        for vertex in self.adjacency_list:
            if vertex not in visited:
                comp = []
                queue = [vertex]
                visited.add(vertex)
                while queue:
                    curr = queue.pop(0)
                    comp.append(curr)
                    for n in self.adjacency_list.get(curr, []):
                        if n not in visited:
                            visited.add(n)
                            queue.append(n)
                components.append(comp)
        return components

    def to_dict(self):
        """Export graph for D3 / Vis / Canvas rendering."""
        nodes = []
        for vid, vdata in self.vertices_data.items():
            nodes.append({
                "id": vid,
                "label": vdata.get("name", vid),
                "role": vdata.get("role", "Suspect"),
                "risk_score": vdata.get("risk_score", 0),
                "avatar": vdata.get("avatar_initials", vid[:2].upper()),
                "degree": self.degree(vid)
            })

        edges = []
        seen_edges = set()
        for u in self.adjacency_list:
            for v in self.adjacency_list[u]:
                edge_pair = tuple(sorted([u, v]))
                if edge_pair not in seen_edges:
                    seen_edges.add(edge_pair)
                    edges.append({
                        "source": u,
                        "target": v,
                        "id": f"{u}--{v}"
                    })

        return {
            "nodes": nodes,
            "edges": edges,
            "total_vertices": len(nodes),
            "total_edges": len(edges)
        }
