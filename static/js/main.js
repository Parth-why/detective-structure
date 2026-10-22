/**
 * SOCIAL DETECTIVE — MAIN JAVASCRIPT CONTROLLER
 * Handles global audio synthesizer, toast alerts, viva explanation modals,
 * presentation mode, and live operation log updates.
 */

// Global Audio Synthesizer (Zero external dependencies, purely Web Audio API)
const SoundEffects = {
  ctx: null,
  enabled: true,

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.ctx = new AudioContext();
      }
    }
  },

  playTone(freq, type = 'sine', duration = 0.15, vol = 0.05) {
    if (!this.enabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(vol, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {
      // Audio autoplay policy fallback
    }
  },

  click() { this.playTone(800, 'sine', 0.05, 0.03); },
  scan() { this.playTone(1200, 'triangle', 0.12, 0.05); },
  hop() { this.playTone(600, 'sine', 0.08, 0.04); },
  pop() { this.playTone(350, 'sawtooth', 0.1, 0.04); },
  success() {
    this.playTone(587.33, 'sine', 0.1, 0.05);
    setTimeout(() => this.playTone(880, 'sine', 0.25, 0.06), 100);
  },
  alert() {
    this.playTone(220, 'square', 0.15, 0.04);
    setTimeout(() => this.playTone(180, 'square', 0.2, 0.04), 120);
  }
};

// Viva Explanation Dictionary (Academic Viva Explanations for all DSA concepts)
const VivaDictionary = {
  graph: {
    title: "Graph & Adjacency List",
    dsa: "Graph (V, E) via Adjacency List",
    time_complexity: "Storage: O(V + E), Traversal: O(V + E)",
    space_complexity: "O(V + E)",
    why_used: "The suspects, victim, and witnesses have complex social relationships and mutual contacts. An Adjacency List is optimal because social networks are sparse (E << V^2).",
    viva_tip: "Be ready to explain why Adjacency List is preferred over Adjacency Matrix for sparse networks."
  },
  bfs: {
    title: "Breadth-First Search (BFS)",
    dsa: "Queue (FIFO) based level-order traversal",
    time_complexity: "O(V + E)",
    space_complexity: "O(V)",
    why_used: "BFS visits vertices level-by-level in increasing distance. In an unweighted social network, BFS is guaranteed to find the SHORTEST PATH (minimum number of connection hops) between the victim and suspect.",
    viva_tip: "Queue enforces First-In, First-Out order: earlier discovered neighbors are explored before deeper ones."
  },
  dfs: {
    title: "Depth-First Search (DFS)",
    dsa: "Stack (LIFO) / Recursion based branch traversal",
    time_complexity: "O(V + E)",
    space_complexity: "O(V)",
    why_used: "DFS investigates deeply along a single path of contacts before backtracking. Used for discovering deep conspiracy chains and connected components.",
    viva_tip: "Stack stores the active recursion trail; backtracking occurs when a node has no more unvisited neighbors."
  },
  hash_table: {
    title: "Hash Table with Separate Chaining",
    dsa: "Hash Table (Array of Linked Lists)",
    time_complexity: "Search / Insert: Average O(1), Worst Case O(n)",
    space_complexity: "O(capacity + n)",
    why_used: "Detectives need instant O(1) query capabilities when searching suspect usernames, Evidence IDs, or Keycard codes without scanning through all records linearly.",
    viva_tip: "Separate chaining resolves hash collisions by maintaining a linked list of nodes at each bucket index."
  },
  stack: {
    title: "Stack (LIFO - Last In, First Out)",
    dsa: "Node-based LIFO Stack",
    time_complexity: "Push: O(1), Pop: O(1), Peek: O(1)",
    space_complexity: "O(n)",
    why_used: "Investigation navigation naturally follows a breadcrumb trail. When a detective wants to BACKTRACK to their previous lead, the most recently visited card (Top of Stack) is popped in O(1) time.",
    viva_tip: "Stack is the fundamental data structure powering the 'Back' button in browsers and undo history in editors."
  },
  queue: {
    title: "Queue (FIFO - First In, First Out)",
    dsa: "Node-based FIFO Queue",
    time_complexity: "Enqueue: O(1), Dequeue: O(1), Front: O(1)",
    space_complexity: "O(n)",
    why_used: "Digital and physical evidence items arrive sequentially at the laboratory intake. A FIFO Queue ensures clues are analyzed strictly in chronological order of arrival without starvation.",
    viva_tip: "Pointers at both front and rear allow O(1) additions and O(1) removals."
  },
  circular_queue: {
    title: "Circular Queue (Surveillance Feeds)",
    dsa: "Array with Modulo Pointer Arithmetic: (index + 1) % capacity",
    time_complexity: "Enqueue / Dequeue: O(1)",
    space_complexity: "O(capacity)",
    why_used: "Surveillance monitors rotate through a fixed set of cameras (CAM 1 -> CAM 5 -> CAM 1). A Circular Queue wraps around without needing to shift memory elements.",
    viva_tip: "Modulo arithmetic eliminates memory fragmentation in fixed buffer management."
  },
  linked_list: {
    title: "Singly Linked List (Evidence Chain)",
    dsa: "Singly Linked List with next pointers",
    time_complexity: "Traversal: O(n), Prepend: O(1), Search: O(n)",
    space_complexity: "O(n)",
    why_used: "Forensic clues form an ordered sequence where clue 1 leads to clue 2, which leads to clue 3. A linked list models pointer-based linear exploration.",
    viva_tip: "Each node contains data and a pointer to the next node; the chain terminates at NULL."
  },
  doubly_linked_list: {
    title: "Doubly Linked List (Case Timeline)",
    dsa: "Doubly Linked List with prev and next pointers",
    time_complexity: "Forward Traversal: O(n), Backward Traversal: O(n), Insert: O(1)",
    space_complexity: "O(n)",
    why_used: "Detectives must reconstruct events chronologically (Next Event via next) and reverse-engineer alibis (Previous Event via prev). Doubly linked lists provide bi-directional navigation.",
    viva_tip: "Two pointers per node enable moving both forward and backward in O(1) per step."
  },
  tree: {
    title: "General N-Ary Tree (Case Hierarchy)",
    dsa: "Hierarchical Tree (Root -> Categories -> Clues)",
    time_complexity: "Preorder / Postorder / Level-order: O(n)",
    space_complexity: "O(h) where h is tree height",
    why_used: "A complex criminal case is organized into People, Digital Evidence, Physical Traces, and Locations. Preorder explores top-down; Postorder closes sub-leads before concluding parent branches.",
    viva_tip: "Preorder visits root before subtrees; Postorder visits all children before the parent."
  },
  bst: {
    title: "Binary Search Tree (BST)",
    dsa: "Binary Tree with BST invariant (Left < Node < Right)",
    time_complexity: "Search / Insert: Average O(log n), Inorder: O(n)",
    space_complexity: "O(n)",
    why_used: "Evidence items indexed by numeric ID can be retrieved in O(log n) time. Running INORDER TRAVERSAL on a BST yields all evidence IDs in perfectly sorted ascending order!",
    viva_tip: "Inorder traversal of any valid BST always produces sorted keys."
  },
  heap: {
    title: "Max-Heap Priority Queue (Strongest Evidence)",
    dsa: "Complete Binary Tree in Array with Max-Heap property",
    time_complexity: "Insert: O(log n), Extract-Max: O(log n), Peek: O(1)",
    space_complexity: "O(n)",
    why_used: "Detectives need to prioritize highest-credibility forensic items first (e.g. 98% credibility CCTV before 60% hearsay). A Max-Heap ensures the maximum priority element is always at the root in O(1).",
    viva_tip: "Bubble-up restores heap order after insertion; Bubble-down (heapify) restores order after extraction."
  },
  sorting: {
    title: "Merge Sort (Divide & Conquer)",
    dsa: "Recursive Merge Sort",
    time_complexity: "Best, Average, Worst: O(n log n)",
    space_complexity: "O(n)",
    why_used: "Guaranteed stable O(n log n) sorting for ranking suspects by risk score or evidence by credibility without the worst-case degradation of simple algorithms.",
    viva_tip: "Divides list into halves until base case of size 1, then merges sorted halves."
  },
  searching: {
    title: "Binary Search",
    dsa: "Divide & Conquer on Sorted Collection",
    time_complexity: "O(log n)",
    space_complexity: "O(1)",
    why_used: "Halves search space at each comparison. When evidence IDs are sorted, Binary Search locates the target clue in logarithmic time.",
    viva_tip: "Requires pre-sorted collection. Uses low, mid, high boundary pointers."
  }
};

// UI Toast Notification helper
function showToast(message, type = 'cyan') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  SoundEffects.click();

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(25px)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Global Viva Explanation Modal Controller
function openExplainModal(key) {
  const item = VivaDictionary[key];
  if (!item) return;

  const modal = document.getElementById('explainModal');
  const title = document.getElementById('explainModalTitle');
  const dsa = document.getElementById('explainModalDSA');
  const time = document.getElementById('explainModalTime');
  const space = document.getElementById('explainModalSpace');
  const why = document.getElementById('explainModalWhy');
  const tip = document.getElementById('explainModalTip');

  if (title) title.innerText = item.title;
  if (dsa) dsa.innerText = item.dsa;
  if (time) time.innerText = item.time_complexity;
  if (space) space.innerText = item.space_complexity;
  if (why) why.innerText = item.why_used;
  if (tip) tip.innerText = item.viva_tip;

  modal.classList.add('active');
  SoundEffects.scan();
}

function closeExplainModal() {
  const modal = document.getElementById('explainModal');
  if (modal) modal.classList.remove('active');
}

// Presentation Mode Toggle
function togglePresentationMode() {
  document.body.classList.toggle('presentation-mode');
  const isPres = document.body.classList.contains('presentation-mode');
  showToast(isPres ? "🎓 Presentation Mode Activated" : "Normal Detective Mode", "cyan");
}

// Reset Case Handler
async function confirmResetCase() {
  if (confirm("Reset the entire investigation? All discoveries, theory tags, and suspect notes will be reset to the beginning.")) {
    try {
      const res = await fetch('/api/reset', { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        showToast("🔄 Case reset to beginning.", "cyan");
        if (typeof localStorage !== 'undefined') {
          localStorage.removeItem('social_detective_stage');
          localStorage.removeItem('social_detective_unlocked');
        }
        setTimeout(() => {
          window.location.href = '/case';
        }, 400);
      }
    } catch (e) {
      showToast("Error resetting case.", "danger");
    }
  }
}

// Global Quick Database Search
async function executeGlobalSearch() {
  const input = document.getElementById('globalSearchInput');
  if (!input || !input.value.trim()) return;

  const q = input.value.trim();
  SoundEffects.scan();

  try {
    const res = await fetch(`/api/hash/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();

    if (data.found) {
      SoundEffects.success();
      showToast(`🎯 Found: ${data.query_key} in Bucket ${data.bucket_index} (Comparisons: ${data.comparisons})`, "success");
      // If user, direct to suspects or open modal
      if (data.value && data.value.type === "user") {
        setTimeout(() => { window.location.href = `/suspects#${data.value.data.id}`; }, 600);
      } else if (data.value && data.value.type === "evidence") {
        setTimeout(() => { window.location.href = `/evidence#ev-${data.value.data.id}`; }, 600);
      }
    } else {
      SoundEffects.alert();
      showToast(`❌ Query '${q}' not found in Hash Table.`, "warning");
    }
  } catch (e) {
    showToast("Network error performing search.", "danger");
  }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  // Global search enter listener
  const searchInput = document.getElementById('globalSearchInput');
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') executeGlobalSearch();
    });
  }

  // Modal close listeners
  const closeBtn = document.getElementById('modalCloseBtn');
  if (closeBtn) closeBtn.addEventListener('click', closeExplainModal);

  const modal = document.getElementById('explainModal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeExplainModal();
    });
  }
});
