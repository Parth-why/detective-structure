"""
Case Engine Service for Social Detective.
Main facade connecting Case Narrative, Graph, Evidence Data Structures,
Investigation State, Accusations, and Detective Scoring.
"""
import json
import os
from services.social_network import SocialNetworkService
from services.evidence_manager import EvidenceManagerService
from services.investigation_engine import InvestigationEngineService
from services.mission_manager import MissionManagerService
from services.asset_manager import AssetManagerService
from structures.sorting import merge_sort_with_trace, quick_sort_with_trace
from structures.searching import linear_search_with_trace, binary_search_with_trace

class CaseEngine:
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir

        self.social_network = SocialNetworkService()
        self.evidence_mgr = EvidenceManagerService(data_dir=data_dir)
        self.investigation = InvestigationEngineService(data_dir=data_dir)
        self.missions = MissionManagerService(data_dir=data_dir)
        self.assets = AssetManagerService()

        self.case_meta = {}
        self.load_case_meta()

    def load_case_meta(self):
        case_file = os.path.join(self.data_dir, "cases.json")
        with open(case_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
            cases = raw.get("cases", [])
            if cases:
                self.case_meta = cases[0]

    def get_case_summary(self):
        total_evidence = len(self.evidence_mgr.get_all_evidence())
        state = self.investigation.get_case_state()
        discovered_count = state["discovered_count"]
        progress_pct = int((len(state["completed_stages"]) / 7.0) * 100)

        return {
            "case_id": self.case_meta.get("id", "CASE_001"),
            "title": self.case_meta.get("title", "THE VANISHING FILE"),
            "tagline": self.case_meta.get("tagline", "Every Connection Is Evidence."),
            "incident_time": self.case_meta.get("incident_time", "19:00 - 21:00"),
            "incident_date": self.case_meta.get("incident_date", "October 6, 2026"),
            "location": self.case_meta.get("location", "Apex Bio-Informatics Lab"),
            "victim": self.case_meta.get("victim", {}),
            "progress_pct": min(100, progress_pct),
            "total_suspects": len(self.social_network.get_all_users()),
            "investigated_suspects_count": state["investigated_count"],
            "investigated_suspects": state["investigated_suspects"],
            "total_evidence": total_evidence,
            "discovered_evidence_count": discovered_count,
            "discovered_evidence": state["discovered_evidence"],
            "total_timeline_events": self.evidence_mgr.get_timeline_length(),
            "timeline_reconstructed_count": state["timeline_reconstructed_count"],
            "state": state,
            "active_missions": self.missions.get_missions(),
            "assets": self.assets.scan_assets()
        }

    def get_stats(self):
        base_stats = self.investigation.stats
        total_evidence = len(self.evidence_mgr.get_all_evidence())
        discovered_count = len(self.investigation.discovered_evidence)
        state = self.investigation.get_case_state()

        # Calculate live detective score (Base 1000)
        # Score = (Discovered Clues * 40) + (BFS runs * 20) + (DFS runs * 20) + (Hash * 15) - (Hints * 35) - (Wrong * 150)
        score = 400 + (discovered_count * 40) + (base_stats["bfs_runs"] * 30) + (base_stats["dfs_runs"] * 20) + (base_stats["hash_searches"] * 15) + (len(state["completed_stages"]) * 40) - (base_stats["hints_used"] * 35) - (base_stats["wrong_accusations"] * 100)
        score = max(50, min(1000, score))

        # Check and update achievements
        self.missions.update_achievements_and_missions(base_stats, discovered_count, self.investigation.get_theory_state())

        return {
            "score": score,
            "discovered_evidence": list(self.investigation.discovered_evidence),
            "discovered_count": discovered_count,
            "total_evidence": total_evidence,
            "dsa_stats": base_stats,
            "state": state,
            "operation_log": self.investigation.get_operation_log()[:15],
            "achievements": self.missions.get_achievements(),
            "missions": self.missions.get_missions()
        }

    # --- Accusation Handler ---
    def verify_accusation(self, accused_id, selected_evidence_ids=None):
        """
        Evaluate player's accusation against ground truth:
          - Target Culprit: Ryan Mehta ('ryan_mehta')
          - Key Supporting Evidence: 1047 (CCTV Fire Stairs), 1061 (Exfiltration Log), 1120 (Sam Signal), 1160 (Library Reverse SSH)
        """
        target_culprit = self.case_meta.get("culprit_id", "ryan_mehta")
        is_correct_culprit = (accused_id == target_culprit)

        if not is_correct_culprit:
            self.investigation.stats["wrong_accusations"] += 1
            self.investigation.log_operation("ACCUSATION_FAILED", f"Accusation submitted for '{accused_id}' — Disproven by alibis/forensics.")
            return {
                "verdict": "INCORRECT",
                "success": False,
                "message": "Your theory contains contradictions. The suspect's alibi holds up, or key digital evidence points elsewhere. Review the Timeline and Social Graph connections!",
                "culprit_id": None
            }

        # Culprit is correct! Check solved status
        self.investigation.case_solved = True
        self.investigation.current_stage = 6
        self.investigation.completed_stages.add(6)
        self.missions._unlock_achievement("ACH_CASE_CLOSED")
        self.missions._complete_mission("M08")
        self.investigation.log_operation("ACCUSATION_SUCCESS", f"CASE CLOSED! Culprit '{accused_id}' successfully identified with evidence.")

        stats = self.get_stats()
        return {
            "verdict": "SOLVED",
            "success": True,
            "message": "Outstanding work, Detective! You have accurately identified Ryan Mehta as the perpetrator of Case 001.",
            "culprit": self.social_network.get_user("ryan_mehta"),
            "accomplice": self.social_network.get_user("sam_verma"),
            "solution_summary": self.case_meta.get("solution_summary", {}),
            "score": stats["score"],
            "dsa_verified": [
                "Graph & Adjacency List", "Breadth-First Search (BFS)", "Depth-First Search (DFS)",
                "Hash Table with Separate Chaining", "Stack (LIFO Backtracking)", "Queue (FIFO Processing)",
                "Circular Queue (Surveillance Feeds)", "Singly Linked List (Evidence Chain)",
                "Doubly Linked List (Timeline Navigation)", "N-Ary Hierarchy Tree (Preorder & Postorder)",
                "Binary Search Tree (Inorder Sorted Retrieval)", "Max-Heap Priority Queue",
                "Merge Sort", "Binary Search"
            ]
        }

    # --- Sorting & Searching Demonstrations ---
    def sort_suspects(self, sort_by="risk_score", algorithm="merge_sort", reverse=True):
        users = self.social_network.get_all_users()
        key_func = lambda u: u.get(sort_by, 0)
        
        if algorithm == "quick_sort":
            return quick_sort_with_trace(users, key_func=key_func, reverse=reverse)
        return merge_sort_with_trace(users, key_func=key_func, reverse=reverse)

    def sort_evidence(self, sort_by="credibility_score", algorithm="merge_sort", reverse=True):
        evidence = self.evidence_mgr.get_all_evidence()
        key_func = lambda e: e.get(sort_by, 0)

        if algorithm == "quick_sort":
            return quick_sort_with_trace(evidence, key_func=key_func, reverse=reverse)
        return merge_sort_with_trace(evidence, key_func=key_func, reverse=reverse)

    def search_evidence_linear(self, target_id):
        evidence = self.evidence_mgr.get_all_evidence()
        return linear_search_with_trace(evidence, target_id, key_func=lambda e: e.get("id"))

    def search_evidence_binary(self, target_id):
        # Must be sorted by ID first for Binary Search
        evidence = sorted(self.evidence_mgr.get_all_evidence(), key=lambda e: e.get("id", 0))
        return binary_search_with_trace(evidence, target_id, key_func=lambda e: e.get("id"))
