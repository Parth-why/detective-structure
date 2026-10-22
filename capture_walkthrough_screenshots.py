"""
Automated High-Resolution Screenshot Capture for Social Detective
Starts the Flask server, simulates each step of the guided playthrough,
and takes pixel-perfect screenshots using headless Chrome for the academic report.
"""
import os
import sys
import time
import json
import threading
import tempfile
import subprocess
import urllib.request
import urllib.parse
from app import app, engine

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def api_post(endpoint, data=None):
    url = f"http://127.0.0.1:5000{endpoint}"
    req_data = json.dumps(data or {}).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def api_get(endpoint):
    url = f"http://127.0.0.1:5000{endpoint}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode('utf-8'))

def take_screenshot(url, output_filename, width=1366, height=820, delay_ms=1500):
    output_path = os.path.join(SCREENSHOT_DIR, output_filename)
    td = tempfile.mkdtemp()
    
    # Chrome headless command with virtual time or wait
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--user-data-dir={td}",
        f"--window-size={width},{height}",
        f"--virtual-time-budget={delay_ms}",
        "--hide-scrollbars",
        f"--screenshot={output_path}",
        url
    ]
    
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"  [OK] Captured: {output_filename} ({size:,} bytes)")
        return output_path
    else:
        print(f"  [FAIL] Failed to capture: {output_filename}")
        return None

def main():
    print("="*70)
    print("  SOCIAL DETECTIVE — AUTOMATED WALKTHROUGH SCREENSHOT CAPTURE")
    print("="*70)

    # 1. Start Flask in daemon thread
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()
    time.sleep(2)
    print("[1] Flask server running on http://127.0.0.1:5000")

    # Reset Engine state
    api_post('/api/reset')
    print("[2] Game state reset to initial Stage 0")

    # -------------------------------------------------------------------------
    # STAGE 0: Briefing & Dossier
    # -------------------------------------------------------------------------
    print("\n--- Capturing Stage 0: Case Briefing ---")
    take_screenshot("http://127.0.0.1:5000/case", "01_stage0_case_briefing.png")

    # -------------------------------------------------------------------------
    # STAGE 1: Suspects Roster (Examine Ryan Mehta)
    # -------------------------------------------------------------------------
    print("\n--- Capturing Stage 1: Suspect Roster ---")
    api_post('/api/case/complete_stage', {"stage": 0})
    api_post('/api/case/stage', {"stage": 1})
    api_get('/api/user/ryan_mehta')
    take_screenshot("http://127.0.0.1:5000/case", "02_stage1_suspects_roster.png")

    # Also capture the dedicated Suspects page
    take_screenshot("http://127.0.0.1:5000/suspects", "02b_suspects_gallery.png")

    # -------------------------------------------------------------------------
    # STAGE 2: Social Graph & BFS
    # -------------------------------------------------------------------------
    print("\n--- Capturing Stage 2: Social Graph & BFS ---")
    api_post('/api/case/complete_stage', {"stage": 1})
    api_post('/api/case/stage', {"stage": 2})
    api_get('/api/graph/bfs?start=maya_rao&target=ryan_mehta')
    take_screenshot("http://127.0.0.1:5000/case", "03_stage2_social_graph_case.png", delay_ms=2500)
    take_screenshot("http://127.0.0.1:5000/network", "03b_stage2_network_explorer.png", delay_ms=2500)

    # -------------------------------------------------------------------------
    # STAGE 3: Timeline & Doubly Linked List
    # -------------------------------------------------------------------------
    print("\n--- Capturing Stage 3: Timeline Stepper ---")
    api_post('/api/case/complete_stage', {"stage": 2})
    api_post('/api/case/stage', {"stage": 3})
    api_get('/api/timeline/event/4')  # 19:38 Door 3 scan
    take_screenshot("http://127.0.0.1:5000/case", "04_stage3_timeline_stepper.png")
    take_screenshot("http://127.0.0.1:5000/timeline", "04b_stage3_timeline_full.png")

    # -------------------------------------------------------------------------
    # STAGE 4: Evidence Vault & BST / Max-Heap
    # -------------------------------------------------------------------------
    print("\n--- Capturing Stage 4: Evidence Vault ---")
    api_post('/api/case/complete_stage', {"stage": 3})
    api_post('/api/case/stage', {"stage": 4})
    api_get('/api/bst/search/1047')
    api_get('/api/heap/peek')
    take_screenshot("http://127.0.0.1:5000/case", "05_stage4_evidence_vault.png")
    take_screenshot("http://127.0.0.1:5000/evidence", "05b_stage4_evidence_full.png")

    # -------------------------------------------------------------------------
    # STAGE 5: Theory Board & LIFO Stack
    # -------------------------------------------------------------------------
    print("\n--- Capturing Stage 5: Theory Case Board ---")
    api_post('/api/case/complete_stage', {"stage": 4})
    api_post('/api/case/stage', {"stage": 5})
    api_post('/api/theory/update', {"entity_type": "suspect", "entity_id": "ryan_mehta", "status": "CRITICAL"})
    api_post('/api/theory/update', {"entity_type": "suspect", "entity_id": "maya_rao", "status": "CLEARED"})
    take_screenshot("http://127.0.0.1:5000/case", "06_stage5_theory_board.png")
    take_screenshot("http://127.0.0.1:5000/investigation", "06b_stage5_investigation_board.png")

    # -------------------------------------------------------------------------
    # STAGE 6: Formal Accusation & Victory Debrief
    # -------------------------------------------------------------------------
    print("\n--- Capturing Stage 6: Case Solved Victory Debrief ---")
    api_post('/api/case/complete_stage', {"stage": 5})
    api_post('/api/case/stage', {"stage": 6})
    verdict = api_post('/api/accusation', {"suspect_id": "ryan_mehta"})
    print(f"  Accusation Result: {verdict.get('verdict')} (Score: {verdict.get('score')} pts)")
    take_screenshot("http://127.0.0.1:5000/case-solved", "07_stage6_case_solved.png")

    # -------------------------------------------------------------------------
    # BONUS: Dashboard & Algorithm Lab
    # -------------------------------------------------------------------------
    print("\n--- Capturing Command Dashboard & Algorithm Lab ---")
    take_screenshot("http://127.0.0.1:5000/dashboard", "08_command_dashboard.png")
    take_screenshot("http://127.0.0.1:5000/algorithm-lab", "09_algorithm_lab_viva.png")

    print("\n" + "="*70)
    print(f" [COMPLETE] All walkthrough screenshots saved in: {SCREENSHOT_DIR}")
    print("="*70)

if __name__ == "__main__":
    main()
