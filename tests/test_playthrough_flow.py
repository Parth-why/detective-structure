import unittest
import json
from app import app, engine
from services.case_engine import CaseEngine

class TestDynamicStateProgression(unittest.TestCase):
    def setUp(self):
        # Reset engine to clean default state for each test
        global engine
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.client.post('/api/reset')

    def test_initial_case_state(self):
        """Test initial state is Stage 0 with default values."""
        res = self.client.get('/api/case/state')
        self.assertEqual(res.status_code, 200)
        state = res.get_json()

        self.assertEqual(state["current_stage"], 0)
        self.assertEqual(state["max_unlocked_stage"], 0)
        self.assertEqual(state["completed_stages"], [])
        self.assertEqual(state["investigated_count"], 0)
        self.assertFalse(state["connection_traced"])
        self.assertEqual(state["theory_status"], "NOT_STARTED")
        self.assertFalse(state["case_solved"])
        self.assertIn("Briefing", state["stage_name"])

    def test_briefing_completion(self):
        """Test completing briefing advances and unlocks Stage 1 (Suspects)."""
        # Complete Stage 0
        res = self.client.post('/api/case/complete_stage', json={"stage": 0})
        self.assertEqual(res.status_code, 200)
        # Set Stage 1
        res = self.client.post('/api/case/stage', json={"stage": 1})
        self.assertEqual(res.status_code, 200)

        state_res = self.client.get('/api/case/state')
        state = state_res.get_json()
        self.assertEqual(state["current_stage"], 1)
        self.assertIn(0, state["completed_stages"])
        self.assertGreaterEqual(state["max_unlocked_stage"], 1)

    def test_suspect_investigation_progress(self):
        """Test inspecting suspects records state and inspecting Ryan completes Stage 1."""
        self.client.post('/api/case/complete_stage', json={"stage": 0})
        self.client.post('/api/case/stage', json={"stage": 1})

        # Inspect Maya Rao
        res = self.client.get('/api/user/maya_rao')
        self.assertEqual(res.status_code, 200)
        state = self.client.get('/api/case/state').get_json()
        self.assertIn("maya_rao", state["investigated_suspects"])
        self.assertEqual(state["investigated_count"], 1)

        # Inspect Ryan Mehta (Prime Suspect - unlocks Stage 2 Connections)
        res = self.client.get('/api/user/ryan_mehta')
        self.assertEqual(res.status_code, 200)
        state = self.client.get('/api/case/state').get_json()
        self.assertIn("ryan_mehta", state["investigated_suspects"])
        self.assertEqual(state["investigated_count"], 2)
        self.assertIn(1, state["completed_stages"])
        self.assertGreaterEqual(state["max_unlocked_stage"], 2)

    def test_connection_progress(self):
        """Test tracing BFS connection completes Stage 2 and unlocks Timeline."""
        self.client.post('/api/case/complete_stage', json={"stage": 0})
        self.client.post('/api/case/complete_stage', json={"stage": 1})
        self.client.post('/api/case/stage', json={"stage": 2})

        res = self.client.get('/api/graph/bfs?start=maya_rao&target=ryan_mehta')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("target_found"))
        self.assertIn("ryan_mehta", data["path"])

        state = self.client.get('/api/case/state').get_json()
        self.assertTrue(state["connection_traced"])
        self.assertIn(2, state["completed_stages"])
        self.assertGreaterEqual(state["max_unlocked_stage"], 3)

    def test_timeline_progress(self):
        """Test navigating timeline events records events and contradiction unlocks Evidence."""
        self.client.post('/api/case/complete_stage', json={"stage": 0})
        self.client.post('/api/case/complete_stage', json={"stage": 1})
        self.client.post('/api/case/complete_stage', json={"stage": 2})
        self.client.post('/api/case/stage', json={"stage": 3})

        # Event 4 is 19:38 Door #3 (Keycard contradiction)
        res = self.client.get('/api/timeline/event/4')
        self.assertEqual(res.status_code, 200)
        ev_data = res.get_json()
        self.assertEqual(ev_data["data"]["timestamp"], "19:38")

        state = self.client.get('/api/case/state').get_json()
        self.assertIn(4, state["timeline_events_reconstructed"])
        self.assertIn("19:38", state["contradictions_discovered"])
        self.assertIn(3, state["completed_stages"])
        self.assertGreaterEqual(state["max_unlocked_stage"], 4)

    def test_evidence_progress(self):
        """Test searching BST and peeking Max-Heap discovers critical clues and unlocks Theory."""
        self.client.post('/api/case/complete_stage', json={"stage": 0})
        self.client.post('/api/case/complete_stage', json={"stage": 1})
        self.client.post('/api/case/complete_stage', json={"stage": 2})
        self.client.post('/api/case/complete_stage', json={"stage": 3})
        self.client.post('/api/case/stage', json={"stage": 4})

        # Search BST for evidence 1047
        res = self.client.get('/api/bst/search/1047')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()["found"])

        # Fetch evidence 1061
        res = self.client.get('/api/evidence/1061')
        self.assertEqual(res.status_code, 200)

        state = self.client.get('/api/case/state').get_json()
        self.assertIn(1047, state["discovered_evidence"])
        self.assertIn(1061, state["discovered_evidence"])
        self.assertIn(4, state["completed_stages"])
        self.assertGreaterEqual(state["max_unlocked_stage"], 5)

    def test_theory_progress(self):
        """Test categorizing suspects in theory updates theory state."""
        self.client.post('/api/case/complete_stage', json={"stage": 0})
        self.client.post('/api/case/complete_stage', json={"stage": 1})
        self.client.post('/api/case/complete_stage', json={"stage": 2})
        self.client.post('/api/case/complete_stage', json={"stage": 3})
        self.client.post('/api/case/complete_stage', json={"stage": 4})
        self.client.post('/api/case/stage', json={"stage": 5})

        res = self.client.post('/api/theory/update', json={
            "entity_type": "suspect",
            "entity_id": "ryan_mehta",
            "status": "CRITICAL"
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()["success"])

        state = self.client.get('/api/case/state').get_json()
        self.assertEqual(state["suspect_statuses"].get("ryan_mehta"), "CRITICAL")
        self.assertIn(5, state["completed_stages"])
        self.assertGreaterEqual(state["max_unlocked_stage"], 6)

    def test_accusation_unlock(self):
        """Test Stage 6 (Accusation) unlocks once required clues and theory are established."""
        self.client.get('/api/user/ryan_mehta')
        self.client.get('/api/graph/bfs?start=maya_rao&target=ryan_mehta')
        self.client.get('/api/timeline/event/4')
        self.client.get('/api/bst/search/1047')
        self.client.post('/api/theory/update', json={"entity_type": "suspect", "entity_id": "ryan_mehta", "status": "CRITICAL"})

        state = self.client.get('/api/case/state').get_json()
        self.assertGreaterEqual(state["max_unlocked_stage"], 6)
        self.assertIn(5, state["completed_stages"])

    def test_incorrect_accusation(self):
        """Test accusing innocent suspect returns contradiction and adds penalty."""
        res = self.client.post('/api/accusation', json={"suspect_id": "arjun_kulkarni"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertEqual(data["verdict"], "INCORRECT")

        # Case must remain unsolved
        state = self.client.get('/api/case/state').get_json()
        self.assertFalse(state["case_solved"])

    def test_correct_accusation(self):
        """Test accusing Ryan Mehta solves the case and marks case completed."""
        res = self.client.post('/api/accusation', json={"suspect_id": "ryan_mehta"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["verdict"], "SOLVED")

        state = self.client.get('/api/case/state').get_json()
        self.assertTrue(state["case_solved"])
        self.assertIn(6, state["completed_stages"])

        # Case Solved page loads cleanly
        solved_page = self.client.get('/case-solved')
        self.assertEqual(solved_page.status_code, 200)
        self.assertIn(b"CASE SOLVED", solved_page.data)
        self.assertIn(b"RYAN MEHTA WAS RESPONSIBLE", solved_page.data)

    def test_state_persistence(self):
        """Test that state persists across multiple queries and page loads."""
        # Perform series of investigation actions
        self.client.get('/api/user/ryan_mehta')
        self.client.get('/api/graph/bfs?start=maya_rao&target=ryan_mehta')
        self.client.get('/api/timeline/event/4')
        self.client.get('/api/bst/search/1047')

        # Load case board
        board_res = self.client.get('/case-board')
        self.assertEqual(board_res.status_code, 200)
        self.assertIn(b"Case Board Overview", board_res.data)

        # Load case view
        case_res = self.client.get('/case')
        self.assertEqual(case_res.status_code, 200)

        # Check API state still intact
        state = self.client.get('/api/case/state').get_json()
        self.assertIn("ryan_mehta", state["investigated_suspects"])
        self.assertTrue(state["connection_traced"])
        self.assertIn(4, state["timeline_events_reconstructed"])
        self.assertIn(1047, state["discovered_evidence"])

if __name__ == "__main__":
    unittest.main()

