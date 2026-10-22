# 🕵️‍♂️ SOCIAL DETECTIVE — Every Connection Is Evidence.

> **A Full-Stack Detective Mystery Web Application Powered by Authentic Data Structures & Algorithms (DSA)**  
> *Developed for Academic Demonstration, College Viva Presentations & Interactive Learning.*

---

## 🌟 1. Project Overview

**SOCIAL DETECTIVE** is an interactive cyber forensics mystery game where the player assumes the role of a digital detective investigating a confidential research theft inside a connected social network. 

The application's core innovation is that **every single investigative mechanic is directly powered by custom-built Data Structures and Algorithms in Python**.
- The **Social Network** is a custom **Graph (Adjacency List)**.
- Tracing connection hops uses **Breadth-First Search (BFS via FIFO Queue)**.
- Deep conspiracy exploration uses **Depth-First Search (DFS via LIFO Stack / Recursion)**.
- Fast detective lookups run in $O(1)$ on a **Hash Table with Separate Chaining**.
- Investigation navigation and backtracking run on a **LIFO Stack**.
- Sequential clue pipelines run on a **Singly Linked List**.
- The Incident Timeline operates on a **Doubly Linked List** with bi-directional pointer traversal.
- Case hierarchy exploration utilizes **Preorder (Top-Down)** and **Postorder (Bottom-Up)** Tree traversals.
- Forensic evidence is indexed in a **Binary Search Tree (BST)**, where **Inorder Traversal** yields all evidence IDs in sorted ascending order.
- Forensics prioritization runs on a **Max-Heap Priority Queue**.
- Rotating CCTV surveillance monitors operate on a **Circular Queue** with modulo arithmetic.
- Suspect rankings run on manual **Merge Sort** and **Quick Sort** implementations.
- Evidence lookups run on **Binary Search** and **Linear Search**.

---

## 🚀 2. Quick Start & Installation

### Prerequisites
- Python 3.8+ installed.

### Installation
```bash
# 1. Clone repository or navigate to project directory
cd "d:/CLG/DS project"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the automated test suite
pytest tests/test_all_structures.py

# 4. Start the Social Detective web application
python app.py
```

Open your web browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📊 3. Data Structures & Algorithms Complexity Table

| Data Structure / Algorithm | Operation | Average Time Complexity | Worst-Case Time | Space Complexity | Practical Detective Use-Case in Game |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hash Table** (Separate Chaining) | `search(key)` | $O(1)$ | $O(n)$ | $O(C + n)$ | Fast query for usernames, Evidence IDs, and Keycards |
| **Graph** (Adjacency List) | `add_edge()`, `get_neighbors()` | $O(1)$ | $O(1)$ | $O(V + E)$ | Suspect social network relationships |
| **Breadth-First Search (BFS)** | `bfs(start, target)` | $O(V + E)$ | $O(V + E)$ | $O(V)$ | Finding shortest connection path from victim to suspect |
| **Depth-First Search (DFS)** | `dfs(start)` | $O(V + E)$ | $O(V + E)$ | $O(V)$ | Deep conspiracy exploration with backtrack snapshots |
| **Stack (LIFO)** | `push(item)`, `pop()`, `peek()` | $O(1)$ | $O(1)$ | $O(n)$ | Navigation history and instant Backtracking (Pop) |
| **Queue (FIFO)** | `enqueue()`, `dequeue()` | $O(1)$ | $O(1)$ | $O(n)$ | Chronological forensic evidence processing pipeline |
| **Circular Queue** | `enqueue()`, `dequeue()`, `cycle()`| $O(1)$ | $O(1)$ | $O(\text{cap})$ | Fixed-capacity surveillance camera rotating buffer |
| **Singly Linked List** | `append()`, `traverse()` | $O(n)$ | $O(n)$ | $O(n)$ | Sequential linear clue chain (`Clue 1 -> Clue 2 -> ...`) |
| **Doubly Linked List** | `traverse_forward()`, `backward()`| $O(n)$ | $O(n)$ | $O(n)$ | Timeline navigation (`prev` / `next` event traversal) |
| **Binary Search Tree (BST)** | `search(key)` | $O(\log n)$ | $O(n)$ | $O(n)$ | Fast Evidence ID lookup with Left/Right decisions |
| **BST Inorder Traversal** | `inorder()` | $O(n)$ | $O(n)$ | $O(n)$ | Retrieves evidence records sorted in ascending order |
| **Tree Preorder Traversal** | `preorder()` | $O(n)$ | $O(n)$ | $O(h)$ | Top-down case category exploration |
| **Tree Postorder Traversal** | `postorder()` | $O(n)$ | $O(n)$ | $O(h)$ | Bottom-up conclusion of forensic sub-leads |
| **Max-Heap (Priority Queue)** | `extract_max()`, `insert()` | $O(\log n)$ | $O(\log n)$ | $O(n)$ | Extract highest-credibility forensic clues first |
| **Merge Sort** | `merge_sort(arr)` | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Stable sorting of suspects by threat/risk score |
| **Quick Sort** | `quick_sort(arr)` | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | Pivot-based partition sorting of evidence |
| **Binary Search** | `binary_search(arr, id)` | $O(\log n)$ | $O(\log n)$ | $O(1)$ | Logarithmic search on sorted evidence IDs |

---

## 🏗️ 4. Project Architecture

```
social-detective/
├── app.py                      # Flask application routes & REST APIs
├── requirements.txt            # Python package dependencies
├── README.md                   # Comprehensive academic documentation
├── data/                       # Offline JSON game data storage
│   ├── cases.json              # Mystery narrative, victim, motive, and solution
│   ├── users.json              # 13 suspects with full profile attributes
│   ├── evidence.json           # 15 forensic clues with hash keys & credibility
│   ├── timeline.json           # 11 chronological timeline events
│   ├── tree_data.json          # Case hierarchy tree data
│   ├── missions.json           # Detective objectives, hints, achievements
│   └── cctv_feeds.json         # Rotating surveillance camera feeds
├── structures/                 # 100% Custom Python DSA Implementations
│   ├── __init__.py             # Module exports
│   ├── linked_list.py          # Singly Linked List (Evidence Chain)
│   ├── doubly_linked_list.py   # Doubly Linked List (Timeline Navigation)
│   ├── stack.py                # LIFO Stack (Backtracking)
│   ├── queue.py                # FIFO Queue (Evidence Pipeline)
│   ├── circular_queue.py       # Circular Queue with Modulo Arithmetic
│   ├── hash_table.py           # Hash Table with Separate Chaining
│   ├── graph.py                # Adjacency List Graph with BFS & DFS
│   ├── tree.py                 # N-Ary Hierarchy Tree & Traversals
│   ├── bst.py                  # Binary Search Tree & Inorder Sorting
│   ├── heap.py                 # Max-Heap Priority Queue
│   ├── sorting.py              # Merge Sort & Quick Sort
│   └── searching.py            # Binary Search & Linear Search
├── services/                   # Business Logic & Facades
│   ├── case_engine.py          # Master coordinator, accusations, scoring
│   ├── social_network.py       # Graph service & network analytics
│   ├── evidence_manager.py     # Evidence DSA coordination service
│   ├── investigation_engine.py # Runtime stack, queue, theory, and operation log
│   └── mission_manager.py      # Missions, achievements, hints
├── templates/                  # HTML5 Templates
│   ├── base.html               # Master layout with top status, toast, & ticker
│   ├── landing.html            # Cyber noir landing page & DSA cards
│   ├── dashboard.html          # Detective Command Station
│   ├── case.html               # Case 001 Dossier & Red Herrings
│   ├── suspects.html           # Suspect roster with Merge/Quick Sort
│   ├── network.html            # 2D Canvas Graph with live Queue/Stack
│   ├── evidence.html           # Evidence Vault with BST, Heap, & Linked List
│   ├── timeline.html           # Doubly Linked List interactive timeline
│   ├── investigation.html      # Case Board, Backtracking Stack, & Accusation
│   ├── algorithm_lab.html      # Academic Viva Presentation Hub (12 modules)
│   └── case_solved.html        # Victory debrief & score breakdown
├── static/                     # CSS and Vanilla JavaScript
│   ├── css/
│   │   ├── style.css           # Cyber noir design system & glassmorphism
│   │   └── animations.css      # Keyframe pulses, sliding nodes, glow effects
│   └── js/
│       ├── main.js             # Web Audio synthesizer, toasts, viva modal
│       ├── network.js          # Interactive canvas graph & animated BFS/DFS
│       ├── investigation.js    # Stack backtracking & CCTV cycling
│       ├── timeline.js         # Doubly linked list step player
│       └── algorithms.js       # Algorithm Lab interactive demo controller
└── tests/
    └── test_all_structures.py  # Comprehensive automated pytest test suite
```

---

## 🎓 5. College Viva / Presentation Q&A Guide ("Explain This")

### Q1: Why use an Adjacency List for the social graph instead of an Adjacency Matrix?
> **Answer:** Social networks are typically sparse graphs where $|E| \ll |V|^2$. An Adjacency List requires only $O(V + E)$ space compared to $O(V^2)$ for an Adjacency Matrix, and allows iterating over a suspect's direct neighbors in $O(\text{degree}(v))$ time.

### Q2: Why does BFS guarantee the shortest path between the victim and suspect?
> **Answer:** BFS explores nodes level-by-level in order of their hop distance from the start node using a **FIFO Queue**. In an unweighted graph, the first time a target vertex is reached, the path taken is guaranteed to have the minimum number of edges.

### Q3: Why is a Doubly Linked List used for the Case Timeline?
> **Answer:** Timeline investigation requires moving both forward in time (`node.next`) to observe subsequent events and backward in time (`node.prev`) to verify alibis. A Doubly Linked List enables $O(1)$ bi-directional step transitions without rebuilding the event chain.

### Q4: How does Inorder Traversal on a Binary Search Tree (BST) produce sorted output?
> **Answer:** By definition, a BST maintains the invariant: $\text{Left Subtree Keys} < \text{Root Key} < \text{Right Subtree Keys}$. Inorder traversal recursively visits the Left Subtree, then Root, then Right Subtree, inherently processing keys in strictly ascending numerical order ($O(n)$ time).

### Q5: How does the Circular Queue prevent buffer memory shifting?
> **Answer:** By using modulo arithmetic: $\text{next\_index} = (\text{index} + 1) \pmod{\text{capacity}}$, the pointers wrap around from the end of the fixed array back to index 0, allowing continuous rotation in $O(1)$ time without memory reallocation.

---

## 🧪 6. Automated Testing

To run the automated unit test suite covering all 12 custom data structures and gameplay logic:
```bash
pytest tests/test_all_structures.py -v
```
All 12 test suites pass in **0.02 seconds** with 100% assertions verified.

To verify all 10 HTML page routes and 26+ REST API endpoints:
```bash
python tests/verify_routes.py
```
*Result:* 10/10 HTML Pages & 26/26 REST APIs return Status 200 (100% Pass).

---

## 📜 7. License & Academic Use
Built for educational demonstration and computer science data structures & algorithms curriculum coursework.
All characters, locations, and scenarios in Case 001 are fictional.
