/**
 * SOCIAL DETECTIVE — ALGORITHM LAB CONTROLLER
 * Interactive playground for college viva demonstrations covering all 12+ DSA structures.
 */

// 1. Hash Table Demo
async function runHashDemo() {
  const query = document.getElementById('hashQueryInput').value.trim() || '@ryan_47';
  SoundEffects.scan();

  try {
    const res = await fetch(`/api/hash/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();

    const output = document.getElementById('hashDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem; display:flex; flex-direction:column; gap:0.4rem;">
          <div style="color:var(--accent-cyan); font-weight:700;">${data.hash_calculation}</div>
          <div>Target Key: <strong>${data.query_key}</strong> | Bucket: <strong>#${data.bucket_index}</strong></div>
          <div>Status: <strong style="color:${data.found ? '#00ff9d' : '#ff3366'}">${data.found ? 'MATCH FOUND' : 'NOT FOUND'}</strong> (Comparisons: ${data.comparisons})</div>
          <div style="background:rgba(0,0,0,0.4); padding:0.5rem; border-radius:4px; font-size:0.75rem;">
            ${data.steps.map(s => `<div>[Step ${s.step}] ${s.action} -> ${s.matched ? '✅ MATCH' : '❌ NO'}</div>`).join('')}
          </div>
        </div>
      `;
    }
  } catch (e) {
    showToast("Error executing Hash Table lookup.", "danger");
  }
}

// 2. BST Inorder Demo (Sorted Retrieval!)
async function runBSTTraversalDemo(mode = 'inorder') {
  SoundEffects.scan();
  try {
    const res = await fetch(`/api/bst/traverse/${mode}`);
    const data = await res.json();

    const output = document.getElementById('bstDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem; display:flex; flex-direction:column; gap:0.4rem;">
          <div style="color:var(--accent-purple); font-weight:700;">${data.traversal_type} (${data.order_pattern})</div>
          <div style="font-size:0.75rem; color:var(--text-secondary);">${data.detective_analogy}</div>
          <div style="color:var(--accent-cyan); font-weight:800; margin-top:0.25rem;">
            Output Sequence: [ ${data.items.map(it => it.key).join(' → ')} ]
          </div>
        </div>
      `;
    }
  } catch (e) {
    showToast("Error running BST traversal.", "danger");
  }
}

// 3. Tree Preorder & Postorder Demo
async function runTreeTraversalDemo(mode = 'preorder') {
  SoundEffects.scan();
  try {
    const res = await fetch(`/api/tree/traverse/${mode}`);
    const data = await res.json();

    const output = document.getElementById('treeDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem; display:flex; flex-direction:column; gap:0.4rem;">
          <div style="color:var(--accent-cyan); font-weight:700;">${data.traversal_type} (${data.order_pattern})</div>
          <div style="font-size:0.75rem; color:var(--text-secondary);">${data.detective_analogy}</div>
          <div style="max-height:140px; overflow-y:auto; background:rgba(0,0,0,0.3); padding:0.5rem; border-radius:4px; font-size:0.75rem;">
            ${data.visited_order.map((name, i) => `<div>${i + 1}. ${name}</div>`).join('')}
          </div>
        </div>
      `;
    }
  } catch (e) {
    showToast("Error running Tree traversal.", "danger");
  }
}

// 4. Max-Heap Extract Demo
async function runHeapExtractDemo() {
  SoundEffects.pop();
  try {
    const res = await fetch('/api/heap/extract', { method: 'POST' });
    const data = await res.json();

    const output = document.getElementById('heapDemoOutput');
    if (output && data.extracted_item) {
      const item = data.extracted_item;
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem; display:flex; flex-direction:column; gap:0.4rem;">
          <div style="color:var(--accent-green); font-weight:700;">🎯 Extracted Max Priority: ${item.priority}% Credibility</div>
          <div>Clue: <strong>${item.data.title || 'Evidence item'}</strong></div>
          <div style="font-size:0.75rem; color:var(--text-muted);">Remaining Heap Size: ${data.remaining_size} items</div>
          <div style="font-size:0.75rem; color:var(--accent-purple);">Bubble Down Swaps: ${data.bubble_down_steps.length}</div>
        </div>
      `;
    }
  } catch (e) {
    showToast("Error extracting from Max-Heap.", "danger");
  }
}

// 5. Singly Linked List Traversal Demo
async function runLinkedListDemo() {
  SoundEffects.scan();
  try {
    const res = await fetch('/api/linked-list/traverse');
    const data = await res.json();

    const output = document.getElementById('linkedListDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem; display:flex; flex-direction:column; gap:0.4rem;">
          <div style="color:var(--accent-cyan); font-weight:700;">Linear Clue Chain Traversal (O(n)):</div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-top:0.25rem;">
            ${data.chain.map((c, i) => `
              <span style="background:rgba(0,240,255,0.15); border:1px solid var(--accent-cyan); padding:2px 6px; border-radius:4px;">
                #${c.id} ${i < data.chain.length - 1 ? '→' : '→ NULL'}
              </span>
            `).join('')}
          </div>
          <div style="font-size:0.75rem; color:var(--text-muted);">Visited ${data.total_nodes} nodes sequentially via next pointer.</div>
        </div>
      `;
    }
  } catch (e) {
    showToast("Error traversing Linked List.", "danger");
  }
}

// 6. Sorting Demo (Merge Sort vs Quick Sort)
async function runSortDemo(algo = 'merge_sort') {
  SoundEffects.scan();
  try {
    const res = await fetch(`/api/sort?type=suspects&by=risk_score&algo=${algo}&reverse=true`);
    const data = await res.json();

    const output = document.getElementById('sortDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem; display:flex; flex-direction:column; gap:0.4rem;">
          <div style="color:var(--accent-amber); font-weight:700;">Algorithm: ${data.algorithm} (${data.time_complexity})</div>
          <div>Total Steps Logged: <strong>${data.total_steps}</strong></div>
          <div style="max-height:120px; overflow-y:auto; background:rgba(0,0,0,0.3); padding:0.5rem; border-radius:4px; font-size:0.75rem;">
            ${data.sorted_items.map((s, i) => `<div>${i + 1}. ${s.name} — Risk: ${s.risk_score}</div>`).join('')}
          </div>
        </div>
      `;
    }
  } catch (e) {
    showToast("Error executing sort demo.", "danger");
  }
}

// 7. Searching Demo (Binary Search vs Linear Search)
async function runSearchDemo(algo = 'binary_search') {
  const targetId = document.getElementById('searchTargetInput')?.value || '1047';
  SoundEffects.scan();
  try {
    const res = await fetch(`/api/search?id=${targetId}&algo=${algo}`);
    const data = await res.json();

    const output = document.getElementById('searchDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem; display:flex; flex-direction:column; gap:0.4rem;">
          <div style="color:var(--accent-cyan); font-weight:700;">${data.algorithm} (${data.time_complexity})</div>
          <div>Status: <strong style="color:${data.found ? '#00ff9d' : '#ff3366'}">${data.found ? 'TARGET FOUND at Index ' + data.index : 'NOT FOUND'}</strong></div>
          <div>Total Comparisons: <strong>${data.total_comparisons}</strong></div>
          <div style="background:rgba(0,0,0,0.3); padding:0.5rem; border-radius:4px; font-size:0.75rem; max-height:120px; overflow-y:auto;">
            ${data.steps.map(st => `<div>[Step ${st.step}] ${st.action || st.description} ${st.decision ? '-> ' + st.decision : ''}</div>`).join('')}
          </div>
        </div>
      `;
    }
  } catch (e) {
    showToast("Error executing search demo.", "danger");
  }
}

// 1b. Inspect Hash Buckets & Chaining
async function inspectHashBuckets() {
  SoundEffects.scan();
  try {
    const res = await fetch('/api/hash/table');
    const data = await res.json();
    const output = document.getElementById('hashDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.75rem;">
          <div style="color:var(--accent-cyan); font-weight:700; margin-bottom:4px;">
            Hash Table State (Capacity: ${data.capacity}, Total Items: ${data.total_items}, Load Factor: ${data.load_factor})
          </div>
          <div style="max-height:140px; overflow-y:auto; background:rgba(0,0,0,0.3); padding:0.4rem; border-radius:4px; display:flex; flex-direction:column; gap:2px;">
            ${data.buckets.map(b => `
              <div>
                <span style="color:var(--accent-purple); font-weight:700;">Bucket [${b.bucket_index}]:</span> 
                ${b.is_empty ? '<span style="color:var(--text-muted);">Empty</span>' : b.nodes.map(n => `<span style="background:rgba(0,240,255,0.15); border:1px solid var(--accent-cyan); padding:1px 4px; border-radius:3px; margin:0 2px;">${n.key}</span>`).join(' → ')}
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }
  } catch (e) {
    showToast("Error inspecting hash buckets.", "danger");
  }
}

// 8b. Stack Interactive Demo
async function pushStackDemo() {
  const titles = ["Suspect: Ryan Mehta", "Evidence: Terminal Log #1061", "Location: Server Room A", "Evidence: CCTV #1047", "Suspect: Sam Verma"];
  const randomTitle = titles[Math.floor(Math.random() * titles.length)];
  SoundEffects.click();
  try {
    const res = await fetch('/api/stack/push', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item: { type: "DEMO_NODE", title: randomTitle, timestamp: "Now" } })
    });
    const data = await res.json();
    const output = document.getElementById('stackDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem; color:var(--accent-green);">
          ✅ PUSH(item) -> Pushed "${randomTitle}" to TOP (Stack Size: ${data.size})
        </div>
      `;
    }
    showToast(`Pushed to Stack (Size: ${data.size})`, "cyan");
  } catch (e) {
    showToast("Error pushing to stack.", "danger");
  }
}

async function popStackDemo() {
  SoundEffects.pop();
  try {
    const res = await fetch('/api/stack/pop', { method: 'POST' });
    const data = await res.json();
    const output = document.getElementById('stackDemoOutput');
    if (output) {
      if (data.success) {
        output.innerHTML = `
          <div style="font-family:var(--text-mono); font-size:0.8rem; color:var(--accent-purple);">
            ⚡ POP() -> Removed "${data.popped_item.title || data.popped_item.id}". Current Top: "${data.current_item.title || data.current_item.id}"
          </div>
        `;
        showToast(`Popped from Stack: ${data.popped_item.title || data.popped_item.id}`, "purple");
      } else {
        output.innerHTML = `<div style="color:var(--accent-amber); font-size:0.8rem;">${data.message}</div>`;
      }
    }
  } catch (e) {
    showToast("Error popping stack.", "danger");
  }
}

// 9b. Queue Interactive Demo
async function enqueueQueueDemo() {
  const evTitles = ["Packet Capture #1160", "Badge Scan #1075", "DarkWeb Chat #1020", "Dining Receipt #1148"];
  const item = { id: Math.floor(Math.random() * 800 + 1000), title: evTitles[Math.floor(Math.random() * evTitles.length)] };
  SoundEffects.click();
  try {
    const res = await fetch('/api/queue/enqueue', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item })
    });
    const data = await res.json();
    const output = document.getElementById('queueDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem; color:var(--accent-green);">
          ✅ ENQUEUE(item) -> Added "#${item.id}: ${item.title}" to REAR (Size: ${data.size})
        </div>
      `;
    }
    showToast(`Enqueued to Queue (Size: ${data.size})`, "cyan");
  } catch (e) {
    showToast("Error enqueuing.", "danger");
  }
}

async function dequeueQueueDemo() {
  SoundEffects.scan();
  try {
    const res = await fetch('/api/queue/dequeue', { method: 'POST' });
    const data = await res.json();
    const output = document.getElementById('queueDemoOutput');
    if (output) {
      if (data.success) {
        output.innerHTML = `
          <div style="font-family:var(--text-mono); font-size:0.8rem; color:var(--accent-cyan);">
            📋 DEQUEUE() -> Processed FRONT item: "#${data.processed_item.id}: ${data.processed_item.title}" (FIFO)
          </div>
        `;
        showToast(`Dequeued: #${data.processed_item.id}`, "success");
      } else {
        output.innerHTML = `<div style="color:var(--accent-amber); font-size:0.8rem;">${data.message}</div>`;
      }
    }
  } catch (e) {
    showToast("Error dequeuing.", "danger");
  }
}

// 9c. Circular Queue Demo
async function cycleCircularDemo() {
  SoundEffects.scan();
  try {
    const res = await fetch('/api/circular-queue/cycle', { method: 'POST' });
    const data = await res.json();
    const output = document.getElementById('circularDemoOutput');
    if (output && data.current_feed) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem;">
          <div style="color:var(--accent-cyan); font-weight:700;">Rotated: ${data.current_feed.code} (${data.current_feed.label})</div>
          <div style="color:var(--text-muted); font-size:0.75rem;">Wrap-around modulo formula: (index + 1) % 5 = Front: ${data.state.front}, Rear: ${data.state.rear}</div>
        </div>
      `;
      showToast(`CCTV Switched to ${data.current_feed.code}`, "cyan");
    }
  } catch (e) {
    showToast("Error cycling circular queue.", "danger");
  }
}

// 7b. Doubly Linked List Demo
async function traverseDllDemo(dir = 'forward') {
  SoundEffects.scan();
  const endpoint = dir === 'forward' ? '/api/timeline/forward' : '/api/timeline/backward';
  try {
    const res = await fetch(endpoint);
    const data = await res.json();
    const output = document.getElementById('dllDemoOutput');
    if (output) {
      output.innerHTML = `
        <div style="font-family:var(--text-mono); font-size:0.8rem;">
          <div style="color:var(--accent-cyan); font-weight:700;">${data.direction} DLL Traversal via pointer '${data.pointer}':</div>
          <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:2px;">
            ${data.events.map(e => e.time_label + ' (' + e.id + ')').join(dir === 'forward' ? ' ⇄ ' : ' ⇄ ')}
          </div>
        </div>
      `;
      showToast(`Traversed Doubly Linked List (${dir})`, "success");
    }
  } catch (e) {
    showToast("Error traversing DLL.", "danger");
  }
}

