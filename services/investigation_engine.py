"""
Investigation Engine Service for Social Detective.
Manages player runtime state:
  - Stack: Navigation History & Backtracking (LIFO)
  - Queue: Evidence Processing Queue (FIFO)
  - Circular Queue: Surveillance Camera Rotation
  - Theory Board: Suspects and Evidence tagged as relevant/irrelevant
  - Operation Log: Real-time DSA action timestamps for academic demonstration
"""
import json
import os
import datetime
from structures.stack import Stack
from structures.queue import Queue
from structures.circular_queue import CircularQueue

class InvestigationEngineService:
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir

        self.navigation_stack = Stack()
        self.evidence_queue = Queue()
        self.cctv_queue = CircularQueue(capacity=5)

        self.operation_log = []
        self.theory = {
            "suspects": {},       # {suspect_id: "RELEVANT" | "CLEARED" | "UNMARKED"}
            "evidence": {},       # {evidence_id: "CRITICAL" | "DISMISSED" | "UNMARKED"}
            "notes": []
        }
        self.discovered_evidence = set([1020])  # Initial intercept clue is known
        self.investigated_suspects = set()
        
        # Authoritative Walkthrough Progression State
        self.current_stage = 0
        self.completed_stages = set()
        self.max_unlocked_stage = 0
        self.connection_traced = False
        self.timeline_position = 0
        self.timeline_events_reconstructed = set([0])
        self.contradictions_discovered = set()
        self.discovered_leads = ["Dr. Maya Rao's research file missing from Apex Bio-Lab."]
        self.theory_status = "NOT_STARTED"
        self.accusation_made = False
        self.case_solved = False

        self.stats = {
            "bfs_runs": 0,
            "dfs_runs": 0,
            "hash_searches": 0,
            "stack_pushes": 0,
            "stack_pops": 0,
            "queue_enqueues": 0,
            "queue_dequeues": 0,
            "tree_traversals": 0,
            "bst_lookups": 0,
            "heap_extractions": 0,
            "hints_used": 0,
            "wrong_accusations": 0
        }

        self._init_default_state()

    def _init_default_state(self):
        # Push initial root location onto stack
        self.navigation_stack.push({
            "type": "LOCATION",
            "title": "Detective Command Station",
            "id": "HQ",
            "timestamp": "19:00"
        })

        # Populate initial FIFO evidence processing queue
        ev_file = os.path.join(self.data_dir, "evidence.json")
        with open(ev_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
            # Queue 5 initial incoming clues into FIFO queue
            for ev in raw.get("evidence", [])[:5]:
                self.evidence_queue.enqueue(ev)

        # Populate CCTV Circular Queue with 5 camera feeds
        cctv_file = os.path.join(self.data_dir, "cctv_feeds.json")
        with open(cctv_file, "r", encoding="utf-8") as f:
            cctv_raw = json.load(f)
            for feed in cctv_raw.get("feeds", []):
                self.cctv_queue.enqueue(feed)

        self.log_operation("SYSTEM_INIT", "Social Detective DSA Investigation Engine initialized.")

    def log_operation(self, op_type, details):
        """Append timecoded action to the persistent DSA operation log."""
        now = datetime.datetime.now().strftime("%H:%M:%S")
        entry = {
            "timestamp": now,
            "type": op_type,
            "details": details
        }
        self.operation_log.insert(0, entry)  # Most recent first
        if len(self.operation_log) > 50:
            self.operation_log.pop()
        return entry

    # --- State & Stage Progression Methods ---
    def set_stage(self, stage_idx):
        """Change stage if within unlocked bounds."""
        stage_idx = int(stage_idx)
        if stage_idx <= self.max_unlocked_stage or stage_idx == 0:
            self.current_stage = stage_idx
            return True
        return False

    def complete_stage(self, stage_idx):
        """Mark stage complete and unlock next stage if conditions met."""
        stage_idx = int(stage_idx)
        self.completed_stages.add(stage_idx)
        self.max_unlocked_stage = max(self.max_unlocked_stage, stage_idx + 1)
        if self.current_stage <= stage_idx:
            self.current_stage = stage_idx + 1

    def mark_suspect_investigated(self, suspect_id):
        self.investigated_suspects.add(suspect_id)
        if suspect_id == "ryan_mehta":
            self.discovered_leads.append("Ryan's statement conflicts with the access log.")
            self.completed_stages.add(1)
            self.max_unlocked_stage = max(self.max_unlocked_stage, 2)
        elif len(self.investigated_suspects) >= 2:
            self.completed_stages.add(1)
            self.max_unlocked_stage = max(self.max_unlocked_stage, 2)

    def mark_connection_traced(self):
        self.connection_traced = True
        self.discovered_leads.append("Ryan is connected directly to Server Admin Sam Verma.")
        self.completed_stages.add(2)
        self.max_unlocked_stage = max(self.max_unlocked_stage, 3)

    def record_timeline_event_viewed(self, event_idx, event_data=None):
        self.timeline_position = int(event_idx)
        self.timeline_events_reconstructed.add(int(event_idx))
        if event_data and (event_data.get("timestamp") in ["19:38", "19:42", "19:47"] or event_data.get("is_critical")):
            self.contradictions_discovered.add(event_data.get("timestamp", f"EVT_{event_idx}"))
            self.completed_stages.add(3)
            self.max_unlocked_stage = max(self.max_unlocked_stage, 4)

    def mark_evidence_discovered(self, evidence_id):
        eid = int(evidence_id)
        self.discovered_evidence.add(eid)
        if len(self.discovered_evidence) >= 2:
            self.completed_stages.add(4)
            self.max_unlocked_stage = max(self.max_unlocked_stage, 5)

    def toggle_suspect_theory(self, suspect_id, status):
        """Set suspect status: RELEVANT, CLEARED, CRITICAL, UNMARKED"""
        self.theory["suspects"][suspect_id] = status
        self.log_operation("THEORY_UPDATE", f"Marked suspect '{suspect_id}' as {status}.")
        
        # Check if theory has enough markings
        critical_count = sum(1 for v in self.theory["suspects"].values() if v == "CRITICAL")
        marked_count = len(self.theory["suspects"])
        if critical_count >= 1 or marked_count >= 3:
            self.theory_status = "FORMED"
            self.completed_stages.add(5)
            self.max_unlocked_stage = max(self.max_unlocked_stage, 6)
        elif marked_count >= 1:
            self.theory_status = "IN_PROGRESS"

        return self.theory

    def get_case_state(self):
        """Authoritative single source of truth for case progress."""
        leads_count = len(self.discovered_leads)
        contradictions_count = len(self.contradictions_discovered)
        critical_clues = [eid for eid in self.discovered_evidence if eid in [1020, 1047, 1061, 1095, 1120, 1160]]
        
        # Dynamic Next Lead calculation matching exact investigation progression
        if self.case_solved:
            next_lead = {
                "text": "Case Closed. Review full case dossier and algorithm lab.",
                "action_label": "VIEW SOLUTION →",
                "action_text": "VIEW SOLUTION →",
                "target_stage": 6,
                "action_code": "CASE_SOLVED"
            }
        elif 5 in self.completed_stages or self.theory_status == "FORMED":
            next_lead = {
                "text": "You have enough evidence to make a decision.",
                "action_label": "MAKE YOUR ACCUSATION →",
                "action_text": "MAKE YOUR ACCUSATION →",
                "target_stage": 6,
                "action_code": "MAKE_ACCUSATION"
            }
        elif 4 in self.completed_stages or len(self.discovered_evidence) >= 2:
            next_lead = {
                "text": "The evidence now points strongly toward one suspect.",
                "action_label": "BUILD YOUR THEORY →",
                "action_text": "BUILD YOUR THEORY →",
                "target_stage": 5,
                "action_code": "BUILD_THEORY"
            }
        elif 3 in self.completed_stages or contradictions_count >= 1:
            next_lead = {
                "text": "Ryan was still inside the facility after claiming he had left.",
                "action_label": "EXAMINE THE EVIDENCE →",
                "action_text": "EXAMINE THE EVIDENCE →",
                "target_stage": 4,
                "action_code": "EXAMINE_EVIDENCE"
            }
        elif 2 in self.completed_stages or self.connection_traced:
            next_lead = {
                "text": "Ryan wasn't as disconnected from Maya as he claimed.",
                "action_label": "RECONSTRUCT THE NIGHT →",
                "action_text": "RECONSTRUCT THE NIGHT →",
                "target_stage": 3,
                "action_code": "RECONSTRUCT_TIMELINE"
            }
        elif "ryan_mehta" in self.investigated_suspects or 1 in self.completed_stages:
            next_lead = {
                "text": "Ryan's statement conflicts with the access log.",
                "action_label": "TRACE HIS CONNECTION →",
                "action_text": "TRACE HIS CONNECTION →",
                "target_stage": 2,
                "action_code": "TRACE_CONNECTIONS"
            }
        else:
            next_lead = {
                "text": "Start by finding out who had access to Maya's research.",
                "action_label": "EXAMINE SUSPECTS →",
                "action_text": "EXAMINE SUSPECTS →",
                "target_stage": 1,
                "action_code": "EXAMINE_SUSPECTS"
            }

        # Format dynamic case notes summary
        parts = []
        if leads_count > 0:
            parts.append(f"{leads_count} lead{'s' if leads_count != 1 else ''} discovered")
        else:
            parts.append("0 leads discovered")

        if contradictions_count > 0:
            parts.append(f"{contradictions_count} contradiction{'s' if contradictions_count != 1 else ''}")

        if len(critical_clues) > 0:
            parts.append(f"{len(critical_clues)} critical clue{'s' if len(critical_clues) != 1 else ''}")

        case_notes_text = " · ".join(parts)

        stage_names = ["Briefing", "Suspects", "Connections", "Timeline", "Evidence", "Theory", "Accusation"]
        stage_name = stage_names[self.current_stage] if self.current_stage < len(stage_names) else "Completed"

        # Build dynamic suspect_statuses map
        suspect_statuses = {}
        for s_id in self.investigated_suspects:
            suspect_statuses[s_id] = "INVESTIGATED"
        for s_id, tag in self.theory.get("suspects", {}).items():
            if tag and tag != "UNMARKED":
                suspect_statuses[s_id] = tag

        return {
            "current_stage": self.current_stage,
            "stage_name": stage_name,
            "completed_stages": list(self.completed_stages),
            "max_unlocked_stage": self.max_unlocked_stage,
            "investigated_suspects": list(self.investigated_suspects),
            "investigated_count": len(self.investigated_suspects),
            "suspect_statuses": suspect_statuses,
            "discovered_evidence": list(self.discovered_evidence),
            "discovered_count": len(self.discovered_evidence),
            "connection_traced": self.connection_traced,
            "timeline_position": self.timeline_position,
            "timeline_events_reconstructed": list(self.timeline_events_reconstructed),
            "timeline_reconstructed_count": len(self.timeline_events_reconstructed),
            "contradictions_discovered": list(self.contradictions_discovered),
            "contradictions_count": contradictions_count,
            "discovered_leads": self.discovered_leads,
            "leads_count": leads_count,
            "theory_status": self.theory_status,
            "theory": self.theory,
            "case_notes_summary": case_notes_text,
            "next_lead": next_lead,
            "case_solved": self.case_solved
        }

    # --- Stack Operations (Investigation History & Backtracking) ---
    def push_investigation(self, item):
        """Push suspect/evidence/location card onto investigation stack."""
        self.stats["stack_pushes"] += 1
        res = self.navigation_stack.push(item)
        self.log_operation("STACK_PUSH", f"Pushed '{item.get('title', item.get('id', 'item'))}' onto Stack (Size: {self.navigation_stack.size()})")
        return res

    def backtrack_pop(self):
        """Pop top investigation item to backtrack to previous state. Time: O(1)"""
        if self.navigation_stack.size() <= 1:
            return {
                "success": False,
                "message": "Cannot backtrack further. Reached initial Command Station root.",
                "current_item": self.navigation_stack.peek(),
                "stack_state": self.navigation_stack.get_state()
            }

        self.stats["stack_pops"] += 1
        popped_item = self.navigation_stack.pop()
        current_top = self.navigation_stack.peek()
        self.log_operation("STACK_POP", f"Popped '{popped_item.get('title', popped_item.get('id', 'item'))}' from Stack. Backtracked to '{current_top.get('title', 'item')}'.")
        return {
            "success": True,
            "popped_item": popped_item,
            "current_item": current_top,
            "stack_state": self.navigation_stack.get_state()
        }

    def get_stack_state(self):
        return self.navigation_stack.get_state()

    # --- Queue Operations (Evidence Processing) ---
    def enqueue_evidence(self, ev_item):
        self.stats["queue_enqueues"] += 1
        res = self.evidence_queue.enqueue(ev_item)
        self.log_operation("QUEUE_ENQUEUE", f"Enqueued evidence #{ev_item.get('id', 'item')} to processing queue.")
        return res

    def dequeue_process_evidence(self):
        """Process the first available evidence item FIFO."""
        if self.evidence_queue.is_empty():
            return {"success": False, "message": "Evidence processing queue is empty."}

        self.stats["queue_dequeues"] += 1
        processed = self.evidence_queue.dequeue()
        self.mark_evidence_discovered(processed["id"])
        self.log_operation("QUEUE_DEQUEUE", f"Processed evidence #{processed.get('id')} ('{processed.get('title')}') via FIFO queue.")
        return {
            "success": True,
            "processed_item": processed,
            "queue_state": self.evidence_queue.get_state()
        }

    def get_queue_state(self):
        return self.evidence_queue.get_state()

    # --- Circular Queue Operations (Surveillance Monitor) ---
    def cycle_cctv_feed(self):
        """Rotate next camera feed in the circular buffer."""
        result = self.cctv_queue.cycle_next()
        if result:
            feed = result.get("current_feed", {})
            self.log_operation("CIRCULAR_QUEUE_ROTATE", f"Rotated CCTV monitor to {feed.get('code', 'CAM')} ({feed.get('label', '')})")
        return result

    def get_cctv_state(self):
        return self.cctv_queue.get_state()

    def toggle_evidence_theory(self, evidence_id, status):
        """Set evidence status: CRITICAL, DISMISSED, UNMARKED"""
        self.theory["evidence"][str(evidence_id)] = status
        self.log_operation("THEORY_UPDATE", f"Marked evidence #{evidence_id} as {status}.")
        return self.theory

    def get_theory_state(self):
        return self.theory

    def get_operation_log(self):
        return self.operation_log
