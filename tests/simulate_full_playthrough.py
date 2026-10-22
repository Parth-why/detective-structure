"""
End-to-End Simulation of Full Dynamic Playthrough
Verifies the exact Action -> State Change -> Discovery -> Next Lead pipeline
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app, engine
import json

def run_simulation():
    client = app.test_client()
    client.post('/api/reset')
    print("="*70)
    print("  SOCIAL DETECTIVE — DYNAMIC PLAYTHROUGH VERIFICATION")
    print("="*70)

    # 1. INITIAL STATE (Briefing)
    print("\n[STEP 1] INITIAL CASE BRIEFING")
    res = client.get('/api/case/state')
    state = res.get_json()
    print(f"  Stage: {state['current_stage']} ({state['stage_name']})")
    print(f"  Completed Stages: {state['completed_stages']}")
    print(f"  Memory Strip: '{state['case_notes_summary']}'")
    print(f"  Next Lead: '{state['next_lead']['text']}' -> [{state['next_lead'].get('action_label', 'NEXT')}]")
    assert state['current_stage'] == 0
    assert len(state['completed_stages']) == 0

    # 2. START INVESTIGATION -> STAGE 1 (Suspects)
    print("\n[STEP 2] PLAYER CLICKS 'EXAMINE SUSPECTS'")
    client.post('/api/case/complete_stage', json={"stage": 0})
    client.post('/api/case/stage', json={"stage": 1})
    state = client.get('/api/case/state').get_json()
    print(f"  Stage: {state['current_stage']} ({state['stage_name']})")
    print(f"  Completed Stages: {state['completed_stages']} (Briefing checked [OK])")
    print(f"  Next Lead: '{state['next_lead']['text']}'")
    assert 0 in state['completed_stages']
    assert state['current_stage'] == 1

    # 3. INVESTIGATE RYAN MEHTA
    print("\n[STEP 3] PLAYER EXAMINES RYAN MEHTA")
    res = client.get('/api/user/ryan_mehta')
    user = res.get_json()
    print(f"  Investigated: {user['name']} (Keycard: {user['keycard_id']}, Role: {user['role']})")
    state = client.get('/api/case/state').get_json()
    print(f"  Suspects Investigated: {state['investigated_count']}/13 (Ryan: {state['suspect_statuses'].get('ryan_mehta')})")
    print(f"  Completed Stages: {state['completed_stages']} (Suspects checked [OK])")
    print(f"  Next Lead: '{state['next_lead']['text']}' -> [{state['next_lead'].get('action_label', 'NEXT')}]")
    assert "ryan_mehta" in state['investigated_suspects']
    assert 1 in state['completed_stages']

    # 4. TRACE BFS CONNECTION (Stage 2)
    print("\n[STEP 4] PLAYER RUNS BFS GRAPH TRACE (Maya Rao -> Ryan Mehta)")
    client.post('/api/case/stage', json={"stage": 2})
    res = client.get('/api/graph/bfs?start=maya_rao&target=ryan_mehta')
    bfs_data = res.get_json()
    print(f"  BFS Shortest Path: {' -> '.join(bfs_data['path'])}")
    state = client.get('/api/case/state').get_json()
    print(f"  Connection Traced: {state['connection_traced']}")
    print(f"  Completed Stages: {state['completed_stages']} (Connections checked [OK])")
    print(f"  Next Lead: '{state['next_lead']['text']}' -> [{state['next_lead'].get('action_label', 'NEXT')}]")
    assert state['connection_traced'] is True
    assert 2 in state['completed_stages']

    # 5. RECONSTRUCT TIMELINE CONTRADICTION (Stage 3)
    print("\n[STEP 5] PLAYER RECONSTRUCTS TIMELINE EVENT #4 (19:38 Door #3)")
    client.post('/api/case/stage', json={"stage": 3})
    res = client.get('/api/timeline/event/4')
    ev_data = res.get_json()
    print(f"  Timestamp: {ev_data['data']['timestamp']} | {ev_data['data']['actor_name']} at {ev_data['data']['location']}")
    print(f"  Description: {ev_data['data']['description']}")
    state = client.get('/api/case/state').get_json()
    print(f"  Contradictions Discovered: {state['contradictions_discovered']}")
    print(f"  Memory Strip: '{state['case_notes_summary']}'")
    print(f"  Completed Stages: {state['completed_stages']} (Timeline checked [OK])")
    print(f"  Next Lead: '{state['next_lead']['text']}' -> [{state['next_lead'].get('action_label', 'NEXT')}]")
    assert "19:38" in state['contradictions_discovered']
    assert 3 in state['completed_stages']

    # 6. EXAMINE FORENSIC EVIDENCE (Stage 4)
    print("\n[STEP 6] PLAYER SEARCHES BST & EXPLORES EVIDENCE CHAIN")
    client.post('/api/case/stage', json={"stage": 4})
    bst_res = client.get('/api/bst/search/1047').get_json()
    print(f"  BST Search #1047: {bst_res['evidence']['title']} (Comparisons: {bst_res['total_comparisons']})")
    heap_res = client.get('/api/heap/peek').get_json()
    print(f"  Max-Heap Priority Clue: #{heap_res['evidence']['id']} {heap_res['evidence']['title']} ({heap_res['evidence']['credibility']}% Cred)")
    state = client.get('/api/case/state').get_json()
    print(f"  Discovered Evidence: {state['discovered_evidence']}")
    print(f"  Completed Stages: {state['completed_stages']} (Evidence checked [OK])")
    print(f"  Next Lead: '{state['next_lead']['text']}' -> [{state['next_lead'].get('action_label', 'NEXT')}]")
    assert 1047 in state['discovered_evidence']
    assert 4 in state['completed_stages']

    # 7. BUILD THEORY (Stage 5)
    print("\n[STEP 7] PLAYER MARKS RYAN MEHTA AS 'CRITICAL'")
    client.post('/api/case/stage', json={"stage": 5})
    client.post('/api/theory/update', json={"entity_type": "suspect", "entity_id": "ryan_mehta", "status": "CRITICAL"})
    state = client.get('/api/case/state').get_json()
    print(f"  Theory Status: {state['theory_status']}")
    print(f"  Suspect Status (Ryan): {state['suspect_statuses'].get('ryan_mehta')}")
    print(f"  Completed Stages: {state['completed_stages']} (Theory checked [OK])")
    print(f"  Next Lead: '{state['next_lead']['text']}' -> [{state['next_lead'].get('action_label', 'NEXT')}]")
    assert state['suspect_statuses'].get('ryan_mehta') == 'CRITICAL'
    assert 5 in state['completed_stages']

    # 8. SUBMIT FINAL ACCUSATION (Stage 6)
    print("\n[STEP 8] PLAYER SUBMITS FINAL ACCUSATION FOR RYAN MEHTA")
    client.post('/api/case/stage', json={"stage": 6})
    res = client.post('/api/accusation', json={"suspect_id": "ryan_mehta"})
    verdict_data = res.get_json()
    print(f"  Verdict: {verdict_data['verdict']} | Message: {verdict_data['message']}")
    print(f"  Final Detective Score: {verdict_data['score']} pts")
    state = client.get('/api/case/state').get_json()
    print(f"  Case Solved: {state['case_solved']}")
    print(f"  Completed Stages: {state['completed_stages']} (All 7 Stages Complete [OK])")
    assert verdict_data['verdict'] == "SOLVED"
    assert state['case_solved'] is True
    assert 6 in state['completed_stages']

    # 9. CHECK PERSISTENCE & CASE-SOLVED PAGE
    print("\n[STEP 9] REFRESH & PERSISTENCE VERIFICATION")
    solved_res = client.get('/case-solved')
    assert solved_res.status_code == 200
    assert b"CASE SOLVED" in solved_res.data
    assert b"RYAN MEHTA WAS RESPONSIBLE" in solved_res.data

    board_res = client.get('/case-board')
    assert board_res.status_code == 200
    assert b"100%" in board_res.data

    print("\n" + "="*70)
    print(" [PASSED] ALL ACTIONS PRODUCED DYNAMIC STATE CHANGES AND DISCOVERIES!")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_simulation()
