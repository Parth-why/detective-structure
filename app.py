"""
Flask Application for SOCIAL DETECTIVE: Every Connection Is Evidence.
A full-stack detective mystery web application powered by custom Data Structures & Algorithms.
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
import os
import json
from services.case_engine import CaseEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.secret_key = "social_detective_secret_key_crypto_2026"

# Global Case Engine instance
engine = CaseEngine()

# ==========================================
# PAGE ROUTES
# ==========================================

@app.route("/")
@app.route("/api/index")
@app.route("/api/index.py")
def index():
    """Landing Page showcasing cyber noir aesthetics & project features."""
    summary = engine.get_case_summary()
    return render_template("landing.html", summary=summary)

@app.route("/dashboard")
def dashboard():
    """Detective Command Station with progress, active missions, and quick tools."""
    summary = engine.get_case_summary()
    stats = engine.get_stats()
    return render_template("dashboard.html", summary=summary, stats=stats)

@app.route("/case")
def case_view():
    """Main guided investigation playthrough."""
    summary = engine.get_case_summary()
    case_meta = engine.case_meta
    users = engine.social_network.get_all_users()
    evidence_list = engine.evidence_mgr.get_all_evidence()
    timeline_events = engine.evidence_mgr.timeline_events
    stats = engine.get_stats()
    theory = engine.investigation.get_theory_state()
    return render_template(
        "case.html",
        summary=summary,
        case=case_meta,
        suspects=users,
        evidence_list=evidence_list,
        events=timeline_events,
        stats=stats,
        theory=theory
    )

@app.route("/case-board")
def case_board():
    """Compact Case Board overview of discovered suspects, connections, timeline, evidence, and theory."""
    summary = engine.get_case_summary()
    case_meta = engine.case_meta
    users = engine.social_network.get_all_users()
    evidence_list = engine.evidence_mgr.get_all_evidence()
    timeline_events = engine.evidence_mgr.timeline_events
    stats = engine.get_stats()
    theory = engine.investigation.get_theory_state()
    return render_template(
        "case_board.html",
        summary=summary,
        case=case_meta,
        suspects=users,
        evidence_list=evidence_list,
        events=timeline_events,
        stats=stats,
        theory=theory
    )

@app.route("/suspects")
def suspects():
    """Suspect dossier with risk ratings, alibis, and connection tools."""
    users = engine.social_network.get_all_users()
    summary = engine.get_case_summary()
    return render_template("suspects.html", suspects=users, summary=summary)

@app.route("/network")
def network():
    """Interactive Social Graph visualization with BFS, DFS, and shortest path tracing."""
    users = engine.social_network.get_all_users()
    summary = engine.get_case_summary()
    return render_template("network.html", suspects=users, summary=summary)

@app.route("/evidence")
def evidence():
    """Forensic Evidence Vault with BST search, Heap priority, and Linked List chains."""
    all_evidence = engine.evidence_mgr.get_all_evidence()
    summary = engine.get_case_summary()
    return render_template("evidence.html", evidence_list=all_evidence, summary=summary)

@app.route("/timeline")
def timeline():
    """Doubly Linked List Chronological Timeline."""
    events = engine.evidence_mgr.timeline_events
    summary = engine.get_case_summary()
    return render_template("timeline.html", events=events, summary=summary)

@app.route("/investigation")
def investigation():
    """Evidence Board, Theory Construction, Backtracking Stack, and CCTV Circular Monitor."""
    users = engine.social_network.get_all_users()
    all_evidence = engine.evidence_mgr.get_all_evidence()
    summary = engine.get_case_summary()
    theory = engine.investigation.get_theory_state()
    return render_template("investigation.html", suspects=users, evidence_list=all_evidence, summary=summary, theory=theory)

@app.route("/algorithm-lab")
def algorithm_lab():
    """Academic Presentation & Viva Lab covering all 12+ custom DSA implementations."""
    summary = engine.get_case_summary()
    return render_template("algorithm_lab.html", summary=summary)

@app.route("/case-solved")
def case_solved():
    """Case Closed debrief and Detective Score verification screen."""
    stats = engine.get_stats()
    summary = engine.get_case_summary()
    return render_template("case_solved.html", stats=stats, summary=summary)

@app.route("/download-report")
def download_report():
    """Download the academic project summary PDF report."""
    pdf_path = os.path.join(os.path.dirname(__file__), "Social_Detective_Project_Report.pdf")
    if not os.path.exists(pdf_path):
        pdf_path = os.path.join("/tmp", "Social_Detective_Project_Report.pdf")
        if not os.path.exists(pdf_path):
            from generate_report_pdf import build_pdf
            build_pdf(pdf_path)
    return send_file(pdf_path, as_attachment=True, download_name="Social_Detective_Project_Report.pdf")

@app.route("/report.pdf")
def view_report_pdf():
    """View the academic project summary PDF in browser."""
    pdf_path = os.path.join(os.path.dirname(__file__), "Social_Detective_Project_Report.pdf")
    if not os.path.exists(pdf_path):
        pdf_path = os.path.join("/tmp", "Social_Detective_Project_Report.pdf")
        if not os.path.exists(pdf_path):
            from generate_report_pdf import build_pdf
            build_pdf(pdf_path)
    return send_file(pdf_path, mimetype="application/pdf")


# ==========================================
# REST API ENDPOINTS
# ==========================================

@app.route("/api/case", methods=["GET"])
def api_case():
    return jsonify(engine.get_case_summary())

@app.route("/api/assets", methods=["GET"])
def api_assets():
    return jsonify(engine.assets.scan_assets())

@app.route("/api/case/state", methods=["GET"])
def api_case_state():
    return jsonify(engine.investigation.get_case_state())

@app.route("/api/case/stage", methods=["POST"])
def api_case_stage():
    data = request.json or {}
    stage_idx = data.get("stage", 0)
    success = engine.investigation.set_stage(stage_idx)
    return jsonify({"success": success, "state": engine.investigation.get_case_state()})

@app.route("/api/case/complete_stage", methods=["POST"])
def api_case_complete_stage():
    data = request.json or {}
    stage_idx = data.get("stage", 0)
    engine.investigation.complete_stage(stage_idx)
    return jsonify({"success": True, "state": engine.investigation.get_case_state()})

@app.route("/api/stats", methods=["GET"])
def api_stats():
    return jsonify(engine.get_stats())

@app.route("/api/users", methods=["GET"])
def api_users():
    return jsonify(engine.social_network.get_all_users())

@app.route("/api/user/<user_id>", methods=["GET"])
def api_user_detail(user_id):
    user = engine.social_network.get_user(user_id)
    if not user:
        return jsonify({"error": f"Suspect '{user_id}' not found."}), 404

    # Automatically mark investigated & push to Stack if requested
    engine.investigation.mark_suspect_investigated(user_id)
    engine.investigation.push_investigation({
        "type": "SUSPECT",
        "id": user["id"],
        "title": user["name"],
        "role": user["role"],
        "risk_score": user["risk_score"]
    })
    return jsonify(user)

@app.route("/api/evidence", methods=["GET"])
def api_evidence():
    return jsonify(engine.evidence_mgr.get_all_evidence())

@app.route("/api/evidence/<int:evidence_id>", methods=["GET"])
def api_evidence_detail(evidence_id):
    ev = engine.evidence_mgr.get_evidence_by_id(evidence_id)
    if not ev:
        return jsonify({"error": f"Evidence #{evidence_id} not found."}), 404

    engine.investigation.mark_evidence_discovered(evidence_id)
    engine.investigation.push_investigation({
        "type": "EVIDENCE",
        "id": ev["id"],
        "title": ev["title"],
        "credibility": ev["credibility_score"]
    })
    return jsonify(ev)

# --- Graph & Social Network APIs ---
@app.route("/api/network/data", methods=["GET"])
def api_network_data():
    return jsonify(engine.social_network.get_graph_data())

@app.route("/api/graph/bfs", methods=["GET"])
def api_graph_bfs():
    start = request.args.get("start", "maya_rao")
    target = request.args.get("target")
    engine.investigation.stats["bfs_runs"] += 1
    engine.investigation.log_operation("BFS_EXECUTE", f"Executed BFS from '{start}'" + (f" searching for '{target}'" if target else ""))
    result = engine.social_network.run_bfs(start, target)
    if "shortest_path" in result and "path" not in result:
        result["path"] = result["shortest_path"] or []
    if result.get("target_found") or not target:
        engine.investigation.mark_connection_traced()
    return jsonify(result)

@app.route("/api/graph/dfs", methods=["GET"])
def api_graph_dfs():
    start = request.args.get("start", "maya_rao")
    target = request.args.get("target")
    engine.investigation.stats["dfs_runs"] += 1
    engine.investigation.log_operation("DFS_EXECUTE", f"Executed DFS deep dive from '{start}'")
    result = engine.social_network.run_dfs(start, target)
    return jsonify(result)

@app.route("/api/graph/shortest-path", methods=["GET"])
def api_graph_shortest_path():
    start = request.args.get("start", "maya_rao")
    target = request.args.get("target", "arjun_kulkarni")
    engine.investigation.stats["bfs_runs"] += 1
    engine.investigation.log_operation("SHORTEST_PATH", f"Calculated shortest path from '{start}' to '{target}' using BFS.")
    result = engine.social_network.find_shortest_path(start, target)
    return jsonify(result)

@app.route("/api/graph/mutual", methods=["GET"])
def api_graph_mutual():
    u = request.args.get("user_a", "maya_rao")
    v = request.args.get("user_b", "sam_verma")
    result = engine.social_network.find_mutual_connections(u, v)
    return jsonify(result)

@app.route("/api/graph/radius", methods=["GET"])
def api_graph_radius():
    start = request.args.get("start", "maya_rao")
    hops = int(request.args.get("hops", 2))
    result = engine.social_network.get_connection_radius(start, hops)
    return jsonify(result)

@app.route("/api/graph/analytics", methods=["GET"])
def api_graph_analytics():
    return jsonify(engine.social_network.get_degree_analytics())

# --- Hash Table APIs ---
@app.route("/api/hash/search", methods=["GET"])
def api_hash_search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Empty search query"}), 400
    engine.investigation.stats["hash_searches"] += 1
    result = engine.evidence_mgr.search_database(query)
    engine.investigation.log_operation("HASH_SEARCH", f"Database lookup for '{query}' -> Bucket {result.get('bucket_index')} ({'FOUND' if result.get('found') else 'NOT FOUND'})")
    return jsonify(result)

@app.route("/api/hash/table", methods=["GET"])
def api_hash_table():
    return jsonify(engine.evidence_mgr.get_hash_table_state())

# --- Stack APIs (Investigation History & Backtracking) ---
@app.route("/api/stack/state", methods=["GET"])
def api_stack_state():
    return jsonify(engine.investigation.get_stack_state())

@app.route("/api/stack/push", methods=["POST"])
def api_stack_push():
    data = request.json or {}
    item = data.get("item", {"title": "Generic Investigation Node", "timestamp": "Now"})
    res = engine.investigation.push_investigation(item)
    return jsonify(res)

@app.route("/api/stack/pop", methods=["POST"])
@app.route("/api/backtrack", methods=["POST"])
def api_stack_pop():
    res = engine.investigation.backtrack_pop()
    return jsonify(res)

# --- Queue APIs (Evidence Processing Pipeline) ---
@app.route("/api/queue/state", methods=["GET"])
def api_queue_state():
    return jsonify(engine.investigation.get_queue_state())

@app.route("/api/queue/enqueue", methods=["POST"])
def api_queue_enqueue():
    data = request.json or {}
    item = data.get("item")
    if not item:
        return jsonify({"error": "Missing evidence item"}), 400
    res = engine.investigation.enqueue_evidence(item)
    return jsonify(res)

@app.route("/api/queue/dequeue", methods=["POST"])
def api_queue_dequeue():
    res = engine.investigation.dequeue_process_evidence()
    return jsonify(res)

# --- Circular Queue APIs (Surveillance Monitor) ---
@app.route("/api/circular-queue/state", methods=["GET"])
def api_circular_queue_state():
    return jsonify(engine.investigation.get_cctv_state())

@app.route("/api/circular-queue/cycle", methods=["POST"])
def api_circular_queue_cycle():
    res = engine.investigation.cycle_cctv_feed()
    return jsonify(res or {})

# --- Singly Linked List APIs (Evidence Chain) ---
@app.route("/api/linked-list/traverse", methods=["GET"])
def api_linked_list_traverse():
    return jsonify(engine.evidence_mgr.traverse_evidence_chain())

# --- Doubly Linked List APIs (Case Timeline) ---
@app.route("/api/timeline/forward", methods=["GET"])
def api_timeline_forward():
    return jsonify(engine.evidence_mgr.get_timeline_forward())

@app.route("/api/timeline/backward", methods=["GET"])
def api_timeline_backward():
    return jsonify(engine.evidence_mgr.get_timeline_backward())

@app.route("/api/timeline/event/<int:index>", methods=["GET"])
def api_timeline_event_at(index):
    node = engine.evidence_mgr.get_timeline_event_at(index)
    if not node:
        return jsonify({"error": "Index out of bounds"}), 404
    engine.investigation.record_timeline_event_viewed(index, node.get("data") if node else None)
    return jsonify(node)

# --- Tree APIs (Hierarchy & Preorder/Postorder) ---
@app.route("/api/tree/hierarchy", methods=["GET"])
def api_tree_hierarchy():
    return jsonify(engine.evidence_mgr.get_case_tree_hierarchy())

@app.route("/api/tree/traverse/<mode>", methods=["GET"])
def api_tree_traverse(mode):
    engine.investigation.stats["tree_traversals"] += 1
    if mode.lower() == "preorder":
        res = engine.evidence_mgr.tree_preorder()
    elif mode.lower() == "postorder":
        res = engine.evidence_mgr.tree_postorder()
    elif mode.lower() == "level_order":
        res = engine.evidence_mgr.tree_level_order()
    else:
        return jsonify({"error": f"Invalid traversal mode '{mode}'"}), 400
    engine.investigation.log_operation("TREE_TRAVERSAL", f"Executed {mode.upper()} traversal on Case Tree ({len(res.get('visited_order', []))} nodes)")
    return jsonify(res)

# --- Binary Search Tree (BST) APIs ---
@app.route("/api/bst/state", methods=["GET"])
def api_bst_state():
    return jsonify({
        "tree": engine.evidence_mgr.get_bst_tree_dict(),
        "total_nodes": engine.evidence_mgr.bst._size
    })

@app.route("/api/bst/search/<int:key>", methods=["GET"])
def api_bst_search(key):
    engine.investigation.stats["bst_lookups"] += 1
    res = engine.evidence_mgr.bst_search(key)
    if res.get("found"):
        engine.investigation.mark_evidence_discovered(key)
        if "evidence" not in res:
            res["evidence"] = res.get("value")
    engine.investigation.log_operation("BST_SEARCH", f"BST searched for Evidence #{key} -> {'MATCH FOUND' if res.get('found') else 'NOT FOUND'} ({res.get('total_comparisons')} comparisons)")
    return jsonify(res)

@app.route("/api/bst/traverse/<mode>", methods=["GET"])
def api_bst_traverse(mode):
    engine.investigation.stats["tree_traversals"] += 1
    if mode.lower() == "inorder":
        res = engine.evidence_mgr.bst_inorder()
    elif mode.lower() == "preorder":
        res = engine.evidence_mgr.bst_preorder()
    elif mode.lower() == "postorder":
        res = engine.evidence_mgr.bst_postorder()
    else:
        return jsonify({"error": f"Invalid BST traversal mode '{mode}'"}), 400
    return jsonify(res)

# --- Max-Heap APIs (Priority Forensics) ---
@app.route("/api/heap/state", methods=["GET"])
def api_heap_state():
    return jsonify(engine.evidence_mgr.get_heap_state())

@app.route("/api/heap/peek", methods=["GET"])
def api_heap_peek():
    peek_res = engine.evidence_mgr.heap_peek_strongest()
    if peek_res and "evidence" not in peek_res:
        peek_res["evidence"] = peek_res.get("data")
    return jsonify(peek_res or {})

@app.route("/api/heap/extract", methods=["POST"])
def api_heap_extract():
    engine.investigation.stats["heap_extractions"] += 1
    res = engine.evidence_mgr.heap_extract_strongest()
    if res and res.get("extracted_item"):
        item = res["extracted_item"]["data"]
        engine.investigation.mark_evidence_discovered(item["id"])
        engine.investigation.log_operation("HEAP_EXTRACT_MAX", f"Extracted highest-credibility evidence #{item['id']} ('{item['title']}', Priority: {res['extracted_item']['priority']})")
    return jsonify(res or {})

# --- Sorting & Searching APIs ---
@app.route("/api/sort", methods=["GET"])
def api_sort():
    target_type = request.args.get("type", "suspects")
    sort_by = request.args.get("by", "risk_score" if target_type == "suspects" else "credibility_score")
    algo = request.args.get("algo", "merge_sort")
    reverse = request.args.get("reverse", "true").lower() == "true"

    if target_type == "suspects":
        res = engine.sort_suspects(sort_by=sort_by, algorithm=algo, reverse=reverse)
    else:
        res = engine.sort_evidence(sort_by=sort_by, algorithm=algo, reverse=reverse)

    engine.investigation.log_operation("SORT_EXECUTE", f"Executed {algo.upper()} on {target_type} by '{sort_by}' ({len(res.get('sorted_items', []))} items)")
    return jsonify(res)

@app.route("/api/search", methods=["GET"])
def api_search():
    target_id = request.args.get("id", "1047")
    algo = request.args.get("algo", "binary_search")

    try:
        num_id = int(target_id)
    except ValueError:
        return jsonify({"error": "Target ID must be numeric"}), 400

    if algo == "binary_search":
        res = engine.search_evidence_binary(num_id)
    else:
        res = engine.search_evidence_linear(num_id)

    engine.investigation.log_operation("SEARCH_EXECUTE", f"Executed {algo.upper()} for Evidence #{target_id} -> {'FOUND' if res.get('found') else 'NOT FOUND'}")
    return jsonify(res)

# --- Theory & Accusation APIs ---
@app.route("/api/theory/toggle", methods=["POST"])
@app.route("/api/theory/update", methods=["POST"])
def api_theory_toggle():
    data = request.json or {}
    entity_type = data.get("type") or data.get("entity_type")  # "suspect" or "evidence"
    entity_id = data.get("id") or data.get("entity_id")
    status = data.get("status")

    if entity_type == "suspect":
        res = engine.investigation.toggle_suspect_theory(entity_id, status)
    elif entity_type == "evidence":
        res = engine.investigation.toggle_evidence_theory(entity_id, status)
    else:
        return jsonify({"error": "Invalid entity type"}), 400

    return jsonify({"success": True, "theory": res})

@app.route("/api/theory/state", methods=["GET"])
def api_theory_state():
    return jsonify(engine.investigation.get_theory_state())

@app.route("/api/hint", methods=["POST"])
def api_hint():
    data = request.json or {}
    hint_id = data.get("hint_id", 1)
    hint = engine.missions.use_hint(hint_id)
    if hint:
        engine.investigation.stats["hints_used"] += 1
        engine.investigation.log_operation("HINT_USED", f"Used Hint #{hint_id} (Score penalty: -{hint['cost_score']} pts)")
        return jsonify({"success": True, "hint": hint})
    return jsonify({"error": "Hint not found"}), 404

@app.route("/api/accusation", methods=["POST"])
@app.route("/api/accuse", methods=["POST"])
def api_accusation():
    data = request.json or {}
    accused_id = data.get("suspect_id")
    if not accused_id:
        return jsonify({"error": "No suspect selected for accusation", "success": False}), 400

    result = engine.verify_accusation(accused_id)
    return jsonify(result)

@app.route("/api/reset", methods=["POST"])
def api_reset():
    global engine
    engine = CaseEngine()
    return jsonify({"success": True, "message": "Investigation state reset successfully."})

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" [ONLINE] SOCIAL DETECTIVE - Every Connection Is Evidence.")
    print(" [SERVER] Local Server: http://127.0.0.1:5000")
    print(" [DSA]    DSA Engine Active (12+ Custom Data Structures & Algorithms)")
    print("="*60 + "\n")
    app.run(debug=True, host="127.0.0.1", port=5000)
