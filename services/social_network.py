"""
Social Network Service for Social Detective.
Manages the Custom Graph data structure representing suspect connections,
BFS/DFS executions, and social graph metrics.
"""
import json
import os
from structures.graph import Graph

class SocialNetworkService:
    def __init__(self, data_path=None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.json")
        self.data_path = data_path
        self.graph = Graph()
        self.users_data = {}
        self.load_data()

    def load_data(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            users = raw.get("users", [])

        for u in users:
            uid = u["id"]
            self.users_data[uid] = u
            self.graph.add_vertex(uid, u)

        for u in users:
            uid = u["id"]
            for friend_id in u.get("friends", []):
                self.graph.add_edge(uid, friend_id, bidirectional=True)

    def get_graph_data(self):
        """Returns node/edge dictionary for visual graph rendering."""
        return self.graph.to_dict()

    def get_user(self, user_id):
        return self.users_data.get(user_id)

    def get_all_users(self):
        return list(self.users_data.values())

    def run_bfs(self, start_id, target_id=None):
        """Execute BFS connection trace with step-by-step queue snapshots."""
        return self.graph.bfs(start_id, target_id)

    def run_dfs(self, start_id, target_id=None):
        """Execute DFS deep investigation trace with call stack snapshots."""
        return self.graph.dfs(start_id, target_id)

    def find_shortest_path(self, start_id, target_id):
        """Find the shortest connection path between two suspects."""
        return self.graph.shortest_path(start_id, target_id)

    def find_mutual_connections(self, user_a, user_b):
        """Find mutual friends between two suspects."""
        return self.graph.mutual_connections(user_a, user_b)

    def get_connection_radius(self, start_id, hops=2):
        """Find suspects within 1, 2, or 3 hops."""
        return self.graph.radius_search(start_id, hops)

    def get_degree_analytics(self):
        """Analyze degrees and find the most connected suspects."""
        top_suspects, max_deg = self.graph.find_highest_degree()
        degrees = {uid: self.graph.degree(uid) for uid in self.users_data}
        return {
            "top_connected_ids": top_suspects,
            "max_degree": max_deg,
            "degrees": degrees,
            "connected_components": self.graph.connected_components()
        }
