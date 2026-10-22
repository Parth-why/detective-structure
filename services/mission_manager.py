"""
Mission and Achievement Manager for Social Detective.
Tracks mission completion, hint revelations, and unlockable achievements.
"""
import json
import os

class MissionManagerService:
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir
        self.missions = []
        self.hints = []
        self.achievements = []
        self.load_data()

    def load_data(self):
        missions_file = os.path.join(self.data_dir, "missions.json")
        with open(missions_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
            self.missions = raw.get("missions", [])
            self.hints = raw.get("hints", [])
            self.achievements = raw.get("achievements", [])

    def get_missions(self):
        return self.missions

    def get_hints(self):
        return self.hints

    def get_achievements(self):
        return self.achievements

    def use_hint(self, hint_id):
        for h in self.hints:
            if h["id"] == int(hint_id):
                h["used"] = True
                return h
        return None

    def update_achievements_and_missions(self, stats, discovered_count, theory_state):
        """
        Dynamically evaluate unlocks based on gameplay progress and DSA operations.
        """
        # Missions
        if stats.get("bfs_runs", 0) > 0:
            self._complete_mission("M01")
        if stats.get("hash_searches", 0) > 0:
            self._complete_mission("M02")
        if stats.get("heap_extractions", 0) > 0:
            self._complete_mission("M05")
        if stats.get("tree_traversals", 0) >= 2:
            self._complete_mission("M06")
        if stats.get("bst_lookups", 0) > 0:
            self._complete_mission("M07")

        # Achievements
        if discovered_count >= 1:
            self._unlock_achievement("ACH_FIRST_CLUE")
        if stats.get("bfs_runs", 0) >= 1:
            self._unlock_achievement("ACH_NETWORK_ANALYST")
        if stats.get("dfs_runs", 0) >= 1:
            self._unlock_achievement("ACH_DEEP_DIVE")
        if stats.get("hash_searches", 0) >= 3:
            self._unlock_achievement("ACH_HASH_HUNTER")
        if stats.get("stack_pops", 0) >= 1:
            self._unlock_achievement("ACH_BACKTRACKER")
        if stats.get("queue_dequeues", 0) >= 3:
            self._unlock_achievement("ACH_QUEUE_MASTER")
        if stats.get("tree_traversals", 0) >= 3:
            self._unlock_achievement("ACH_TREE_WALKER")

        return {
            "missions": self.missions,
            "achievements": self.achievements
        }

    def _complete_mission(self, mid):
        for m in self.missions:
            if m["id"] == mid:
                m["completed"] = True

    def _unlock_achievement(self, aid):
        for a in self.achievements:
            if a["id"] == aid:
                a["unlocked"] = True
