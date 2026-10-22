"""
Verification script for all Flask routes and REST API endpoints.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

def test_all_routes():
    client = app.test_client()

    pages = [
        "/",
        "/dashboard",
        "/case",
        "/case-board",
        "/suspects",
        "/network",
        "/evidence",
        "/timeline",
        "/investigation",
        "/algorithm-lab",
        "/case-solved"
    ]

    print("\n--- Verifying HTML Page Routes ---")
    for page in pages:
        res = client.get(page)
        print(f"Page: {page:16} -> Status: {res.status_code}")
        assert res.status_code == 200, f"Failed page: {page}"

    apis = [
        "/api/case",
        "/api/stats",
        "/api/users",
        "/api/evidence",
        "/api/network/data",
        "/api/graph/bfs?start=maya_rao&target=ryan_mehta",
        "/api/graph/dfs?start=maya_rao",
        "/api/graph/shortest-path?start=maya_rao&target=arjun_kulkarni",
        "/api/hash/search?q=@ryan_47",
        "/api/hash/table",
        "/api/stack/state",
        "/api/queue/state",
        "/api/circular-queue/state",
        "/api/linked-list/traverse",
        "/api/timeline/forward",
        "/api/timeline/backward",
        "/api/tree/hierarchy",
        "/api/tree/traverse/preorder",
        "/api/tree/traverse/postorder",
        "/api/bst/state",
        "/api/bst/search/1047",
        "/api/bst/traverse/inorder",
        "/api/heap/state",
        "/api/heap/peek",
        "/api/sort?type=suspects&by=risk_score&algo=merge_sort",
        "/api/search?id=1047&algo=binary_search"
    ]

    print("\n--- Verifying REST API Endpoints ---")
    for api in apis:
        res = client.get(api)
        print(f"API: {api[:35]:35} -> Status: {res.status_code}")
        assert res.status_code == 200, f"Failed API: {api}"

    # Verify POST Accusation
    print("\n--- Verifying POST APIs ---")
    post_res = client.post("/api/accusation", json={"suspect_id": "ryan_mehta"})
    print(f"POST Accusation (Correct) -> Status: {post_res.status_code}, Verdict: {post_res.json.get('verdict')}")
    assert post_res.status_code == 200
    assert post_res.json.get("verdict") == "SOLVED"

    wrong_post = client.post("/api/accusation", json={"suspect_id": "arjun_kulkarni"})
    print(f"POST Accusation (Wrong)   -> Status: {wrong_post.status_code}, Verdict: {wrong_post.json.get('verdict')}")
    assert wrong_post.status_code == 200
    assert wrong_post.json.get("verdict") == "INCORRECT"

    print("\n[SUCCESS] ALL 10 HTML PAGES AND 26+ REST APIS VERIFIED PERFECTLY (100% PASS)!\n")

if __name__ == "__main__":
    test_all_routes()
