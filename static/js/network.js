/**
 * SOCIAL DETECTIVE — NETWORK GRAPH & BFS/DFS VISUALIZER
 * Interactive 2D canvas network visualizer with live BFS Queue and DFS Stack animations.
 */

class NetworkGraphVisualizer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    this.nodes = [];
    this.edges = [];
    this.nodeMap = {};

    this.nodeStates = {}; // { nodeId: "UNVISITED" | "QUEUED" | "VISITING" | "VISITED" | "TARGET" | "PATH" }
    this.animationTimer = null;
    this.isPlaying = false;

    this.selectedNode = null;
    this.draggedNode = null;
    this.offset = { x: 0, y: 0 };

    this.setupCanvas();
    this.setupEventListeners();
    this.loadGraphData();
  }

  setupCanvas() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = rect.height || 550;
  }

  setupEventListeners() {
    let isDragging = false;
    let dragStartX = 0;
    let dragStartY = 0;

    this.canvas.addEventListener('mousedown', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      // Check if clicking a node
      for (const node of this.nodes) {
        const dx = node.x - mouseX;
        const dy = node.y - mouseY;
        if (Math.sqrt(dx * dx + dy * dy) <= node.radius) {
          this.draggedNode = node;
          this.selectedNode = node;
          isDragging = true;
          this.onNodeClicked(node);
          SoundEffects.click();
          this.render();
          return;
        }
      }

      isDragging = true;
      dragStartX = mouseX;
      dragStartY = mouseY;
    });

    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      if (this.draggedNode) {
        this.draggedNode.x = mouseX;
        this.draggedNode.y = mouseY;
        this.render();
      }
    });

    window.addEventListener('mouseup', () => {
      this.draggedNode = null;
      isDragging = false;
    });

    window.addEventListener('resize', () => {
      this.setupCanvas();
      this.render();
    });
  }

  async loadGraphData() {
    try {
      const res = await fetch('/api/network/data');
      const data = await res.json();
      this.initNodes(data.nodes, data.edges);
      this.render();
    } catch (e) {
      console.error("Failed to load network data", e);
    }
  }

  initNodes(rawNodes, rawEdges) {
    const width = this.canvas.width;
    const height = this.canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.38;

    this.nodes = [];
    this.edges = rawEdges;
    this.nodeMap = {};

    const count = rawNodes.length;
    rawNodes.forEach((n, idx) => {
      // Place in initial circular layout
      const angle = (idx / count) * 2 * Math.PI;
      const nodeObj = {
        ...n,
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
        radius: 22,
        initialX: centerX + radius * Math.cos(angle),
        initialY: centerY + radius * Math.sin(angle)
      };
      this.nodes.push(nodeObj);
      this.nodeMap[n.id] = nodeObj;
      this.nodeStates[n.id] = "UNVISITED";
    });

    // Populate dropdowns if present on page
    this.populateSelects();
  }

  populateSelects() {
    const startSelect = document.getElementById('bfsStartSelect');
    const targetSelect = document.getElementById('bfsTargetSelect');

    if (startSelect && targetSelect && startSelect.options.length <= 1) {
      startSelect.innerHTML = '';
      targetSelect.innerHTML = '';

      this.nodes.forEach(n => {
        const opt1 = document.createElement('option');
        opt1.value = n.id;
        opt1.innerText = `${n.label} (${n.role.split(' ')[0]})`;
        if (n.id === 'maya_rao') opt1.selected = true;
        startSelect.appendChild(opt1);

        const opt2 = document.createElement('option');
        opt2.value = n.id;
        opt2.innerText = `${n.label} (${n.role.split(' ')[0]})`;
        if (n.id === 'ryan_mehta') opt2.selected = true;
        targetSelect.appendChild(opt2);
      });
    }
  }

  onNodeClicked(node) {
    const infoPanel = document.getElementById('selectedNodeInfo');
    if (infoPanel) {
      infoPanel.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
          <div class="suspect-avatar" style="width:40px; height:40px; font-size:0.9rem;">${node.avatar}</div>
          <div>
            <h4 style="color:var(--text-primary); font-size:0.95rem; font-weight:700;">${node.label}</h4>
            <span style="color:var(--accent-blue); font-size:0.75rem; font-family:var(--text-mono);">${node.role}</span>
          </div>
        </div>
        <div style="font-size:0.8rem; color:var(--text-secondary); display:flex; flex-direction:column; gap:0.25rem;">
          <div>Risk Level: <strong style="color:${node.risk_score > 70 ? '#ff3366' : '#00ff9d'}">${node.risk_score}/100</strong></div>
          <div>Direct Connections: <strong style="color:var(--accent-cyan)">${node.degree}</strong></div>
        </div>
      `;
    }
  }

  resetStates() {
    if (this.animationTimer) clearInterval(this.animationTimer);
    this.isPlaying = false;
    for (const nid in this.nodeStates) {
      this.nodeStates[nid] = "UNVISITED";
    }
    this.render();

    const qDisplay = document.getElementById('liveQueuePanel');
    if (qDisplay) qDisplay.innerHTML = '<span style="color:var(--text-muted); font-size:0.8rem;">Queue is empty</span>';
    const sDisplay = document.getElementById('liveStackPanel');
    if (sDisplay) sDisplay.innerHTML = '<span style="color:var(--text-muted); font-size:0.8rem;">Stack is empty</span>';
  }

  // --- Run BFS with Step-by-Step Queue Animation ---
  async runBFSAnimation() {
    const startSelect = document.getElementById('bfsStartSelect');
    const targetSelect = document.getElementById('bfsTargetSelect');
    const start = startSelect ? startSelect.value : 'maya_rao';
    const target = targetSelect ? targetSelect.value : 'ryan_mehta';

    this.resetStates();
    SoundEffects.scan();

    try {
      const res = await fetch(`/api/graph/bfs?start=${start}&target=${target}`);
      const data = await res.json();
      if (data.error) {
        showToast(data.error, "danger");
        return;
      }

      this.playBFSSteps(data.steps, data.shortest_path);
    } catch (e) {
      showToast("Error executing BFS.", "danger");
    }
  }

  playBFSSteps(steps, shortestPath) {
    let stepIndex = 0;
    this.isPlaying = true;

    this.animationTimer = setInterval(() => {
      if (stepIndex >= steps.length) {
        clearInterval(this.animationTimer);
        this.isPlaying = false;
        // Highlight shortest path
        if (shortestPath && shortestPath.length > 0) {
          shortestPath.forEach(nid => this.nodeStates[nid] = "PATH");
          SoundEffects.success();
          showToast(`🎯 BFS Shortest Path Found (${shortestPath.length - 1} hops): ${shortestPath.join(' → ')}`, "success");
        }
        this.render();
        return;
      }

      const step = steps[stepIndex];
      SoundEffects.hop();

      // Update node states based on step
      if (step.action === "INIT" || step.action === "ENQUEUE_NEIGHBORS") {
        (step.added_neighbors || [step.current_node]).forEach(nid => {
          if (this.nodeStates[nid] !== "VISITED" && this.nodeStates[nid] !== "PATH") {
            this.nodeStates[nid] = "QUEUED";
          }
        });
      } else if (step.action === "DEQUEUE_VISIT") {
        this.nodeStates[step.current_node] = "VISITING";
        setTimeout(() => {
          if (this.nodeStates[step.current_node] === "VISITING") {
            this.nodeStates[step.current_node] = "VISITED";
          }
          this.render();
        }, 300);
      } else if (step.action === "TARGET_FOUND") {
        this.nodeStates[step.current_node] = "TARGET";
      }

      // Update Live Queue display panel
      this.updateQueuePanel(step.queue_state, step.current_node);

      // Log description
      const logEl = document.getElementById('algorithmStepLog');
      if (logEl) {
        logEl.innerHTML = `<div class="anim-slide-in"><strong>Step ${step.step}:</strong> ${step.description}</div>`;
      }

      this.render();
      stepIndex++;
    }, 600);
  }

  updateQueuePanel(queueItems, currentNode) {
    const panel = document.getElementById('liveQueuePanel');
    if (!panel) return;

    if (!queueItems || queueItems.length === 0) {
      panel.innerHTML = `<span style="color:var(--text-muted); font-size:0.75rem;">Queue is empty</span>`;
      return;
    }

    panel.innerHTML = `
      <div style="font-size:0.65rem; color:var(--accent-cyan); font-family:var(--text-mono); margin-bottom:2px;">
        FRONT ─── FIFO QUEUE ─── REAR
      </div>
      <div style="display:flex; gap:0.4rem; overflow-x:auto;">
        ${queueItems.map((item, idx) => `
          <div class="queue-node" style="${idx === 0 ? 'border-color:var(--accent-amber); background:rgba(255,184,0,0.2);' : ''}">
            ${idx === 0 ? '▶ ' : ''}${this.nodeMap[item]?.label || item}
          </div>
        `).join('')}
      </div>
    `;
  }

  // --- Run DFS with Step-by-Step Stack Animation ---
  async runDFSAnimation() {
    const startSelect = document.getElementById('bfsStartSelect');
    const targetSelect = document.getElementById('bfsTargetSelect');
    const start = startSelect ? startSelect.value : 'maya_rao';
    const target = targetSelect ? targetSelect.value : 'ryan_mehta';

    this.resetStates();
    SoundEffects.scan();

    try {
      const res = await fetch(`/api/graph/dfs?start=${start}&target=${target}`);
      const data = await res.json();
      if (data.error) {
        showToast(data.error, "danger");
        return;
      }

      this.playDFSSteps(data.steps, data.path);
    } catch (e) {
      showToast("Error executing DFS.", "danger");
    }
  }

  playDFSSteps(steps, path) {
    let stepIndex = 0;
    this.isPlaying = true;

    this.animationTimer = setInterval(() => {
      if (stepIndex >= steps.length) {
        clearInterval(this.animationTimer);
        this.isPlaying = false;
        SoundEffects.success();
        showToast("⚡ DFS Deep Investigation Complete!", "success");
        this.render();
        return;
      }

      const step = steps[stepIndex];
      SoundEffects.hop();

      if (step.action === "PUSH_VISIT") {
        this.nodeStates[step.current_node] = "VISITING";
      } else if (step.action === "POP_BACKTRACK") {
        this.nodeStates[step.current_node] = "VISITED";
      } else if (step.action === "TARGET_FOUND") {
        this.nodeStates[step.current_node] = "TARGET";
      }

      this.updateStackPanel(step.stack_state);

      const logEl = document.getElementById('algorithmStepLog');
      if (logEl) {
        logEl.innerHTML = `<div class="anim-slide-in"><strong>Step ${step.step}:</strong> ${step.description}</div>`;
      }

      this.render();
      stepIndex++;
    }, 600);
  }

  updateStackPanel(stackItems) {
    const panel = document.getElementById('liveStackPanel');
    if (!panel) return;

    if (!stackItems || stackItems.length === 0) {
      panel.innerHTML = `<span style="color:var(--text-muted); font-size:0.75rem;">Call Stack is empty</span>`;
      return;
    }

    const reversed = [...stackItems].reverse();
    panel.innerHTML = `
      <div style="font-size:0.65rem; color:var(--accent-purple); font-family:var(--text-mono); margin-bottom:4px;">
        TOP (Current Node) ─── LIFO STACK
      </div>
      <div style="display:flex; flex-direction:column; gap:0.3rem;">
        ${reversed.map((item, idx) => `
          <div class="stack-node ${idx === 0 ? 'top-node' : ''}">
            <span>${idx === 0 ? '⚡ ' : ''}${this.nodeMap[item]?.label || item}</span>
            <span style="font-size:0.65rem; opacity:0.7;">Depth ${reversed.length - idx}</span>
          </div>
        `).join('')}
      </div>
    `;
  }

  // --- Rendering Loop ---
  render() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Warm parchment paper canvas background
    this.ctx.fillStyle = '#fdfbf7';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw Edges
    this.edges.forEach(edge => {
      const u = this.nodeMap[edge.source];
      const v = this.nodeMap[edge.target];
      if (!u || !v) return;

      const isPathEdge = (this.nodeStates[u.id] === "PATH" && this.nodeStates[v.id] === "PATH");

      this.ctx.beginPath();
      this.ctx.moveTo(u.x, u.y);
      this.ctx.lineTo(v.x, v.y);

      if (isPathEdge) {
        this.ctx.strokeStyle = '#c2410c';
        this.ctx.lineWidth = 3.5;
        this.ctx.shadowBlur = 0;
      } else {
        this.ctx.strokeStyle = 'rgba(120, 113, 108, 0.3)';
        this.ctx.lineWidth = 1.4;
        this.ctx.shadowBlur = 0;
      }
      this.ctx.stroke();
    });

    // Draw Nodes
    this.nodes.forEach(node => {
      const state = this.nodeStates[node.id] || "UNVISITED";
      let fillColor = '#ffffff';
      let strokeColor = '#a8a29e';
      let glowColor = 'transparent';
      let textColor = '#1c1917';

      if (state === "QUEUED") {
        fillColor = '#fef3c7';
        strokeColor = '#b45309';
        glowColor = 'rgba(245, 158, 11, 0.25)';
      } else if (state === "VISITING") {
        fillColor = '#f3e8ff';
        strokeColor = '#6d28d9';
        glowColor = 'rgba(109, 40, 217, 0.25)';
      } else if (state === "VISITED") {
        fillColor = '#e0f2fe';
        strokeColor = '#0284c7';
        glowColor = 'rgba(2, 132, 199, 0.2)';
      } else if (state === "TARGET") {
        fillColor = '#dcfce7';
        strokeColor = '#15803d';
        glowColor = 'rgba(21, 128, 61, 0.3)';
      } else if (state === "PATH") {
        fillColor = '#ffedd5';
        strokeColor = '#c2410c';
        glowColor = 'rgba(194, 65, 12, 0.3)';
      } else if (node.risk_score > 70) {
        strokeColor = '#b91c1c';
      }

      // Draw outer indicator ring if active
      if (glowColor !== 'transparent') {
        this.ctx.beginPath();
        this.ctx.arc(node.x, node.y, node.radius + 5, 0, 2 * Math.PI);
        this.ctx.fillStyle = glowColor;
        this.ctx.fill();
      }

      // Draw node circle
      this.ctx.beginPath();
      this.ctx.arc(node.x, node.y, node.radius, 0, 2 * Math.PI);
      this.ctx.fillStyle = fillColor;
      this.ctx.fill();
      this.ctx.strokeStyle = strokeColor;
      this.ctx.lineWidth = 2.2;
      this.ctx.stroke();

      // Draw avatar initials
      this.ctx.font = 'bold 11px sans-serif';
      this.ctx.fillStyle = textColor;
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(node.avatar || node.id.substring(0, 2).toUpperCase(), node.x, node.y);

      // Draw label below
      this.ctx.font = '600 11px sans-serif';
      this.ctx.fillStyle = '#44403c';
      this.ctx.fillText(node.label.split(' ')[0], node.x, node.y + node.radius + 14);
    });
  }

  // --- Shortest Path Finder ---
  async findShortestPath() {
    const startSelect = document.getElementById('bfsStartSelect');
    const targetSelect = document.getElementById('bfsTargetSelect');
    const start = startSelect ? startSelect.value : 'maya_rao';
    const target = targetSelect ? targetSelect.value : 'arjun_kulkarni';

    this.resetStates();
    SoundEffects.scan();

    try {
      const res = await fetch(`/api/graph/shortest-path?start=${start}&target=${target}`);
      const data = await res.json();

      if (data.path && data.path.length > 0) {
        data.path.forEach(nid => this.nodeStates[nid] = "PATH");
        SoundEffects.success();
        this.render();

        const logEl = document.getElementById('algorithmStepLog');
        if (logEl) {
          logEl.innerHTML = `<div class="anim-slide-in" style="color:var(--accent-amber);"><strong>Shortest Connection Path (Distance: ${data.distance}):</strong> ${data.path.join(' → ')}</div>`;
        }
        showToast(`🎯 Shortest path: ${data.path.length - 1} hops (${data.path.join(' → ')})`, "success");
      } else {
        showToast("No path found between selected suspects.", "warning");
      }
    } catch (e) {
      showToast("Error computing shortest path.", "danger");
    }
  }

  // --- Mutual Connections Finder ---
  async findMutualConnections() {
    const startSelect = document.getElementById('bfsStartSelect');
    const targetSelect = document.getElementById('bfsTargetSelect');
    const u = startSelect ? startSelect.value : 'maya_rao';
    const v = targetSelect ? targetSelect.value : 'sam_verma';

    this.resetStates();
    SoundEffects.scan();

    try {
      const res = await fetch(`/api/graph/mutual?user_a=${u}&user_b=${v}`);
      const data = await res.json();

      this.nodeStates[u] = "TARGET";
      this.nodeStates[v] = "TARGET";

      if (data.mutual_suspect_ids && data.mutual_suspect_ids.length > 0) {
        data.mutual_suspect_ids.forEach(mid => this.nodeStates[mid] = "VISITING");
        SoundEffects.success();
        this.render();

        const logEl = document.getElementById('algorithmStepLog');
        if (logEl) {
          logEl.innerHTML = `<div class="anim-slide-in" style="color:var(--accent-purple);"><strong>Mutual Contacts (${data.mutual_count}):</strong> ${data.mutual_suspect_ids.join(', ')}</div>`;
        }
        showToast(`Found ${data.mutual_count} mutual connection(s): ${data.mutual_suspect_ids.join(', ')}`, "success");
      } else {
        this.render();
        showToast("No mutual connections found between these suspects.", "warning");
      }
    } catch (e) {
      showToast("Error finding mutual connections.", "danger");
    }
  }

  // --- Connection Radius (1, 2, 3 Hops) ---
  async findRadius(hops = 2) {
    const startSelect = document.getElementById('bfsStartSelect');
    const start = startSelect ? startSelect.value : 'maya_rao';

    this.resetStates();
    SoundEffects.scan();

    try {
      const res = await fetch(`/api/graph/radius?start=${start}&hops=${hops}`);
      const data = await res.json();

      this.nodeStates[start] = "TARGET";
      if (data.results_by_hop) {
        for (const h in data.results_by_hop) {
          data.results_by_hop[h].forEach(item => {
            this.nodeStates[item.id] = (h == 1) ? "VISITED" : "QUEUED";
          });
        }
      }
      SoundEffects.success();
      this.render();

      const logEl = document.getElementById('algorithmStepLog');
      if (logEl) {
        logEl.innerHTML = `<div class="anim-slide-in"><strong>Radius Analysis (${hops} hops from ${start}):</strong> Total reachable suspects: ${data.all_reachable ? data.all_reachable.length : 0}</div>`;
      }
      showToast(`Analyzed ${hops}-hop radius from ${start}`, "cyan");
    } catch (e) {
      showToast("Error computing radius.", "danger");
    }
  }

  // --- Degree Centrality Analytics ---
  async analyzeDegreeCentrality() {
    SoundEffects.scan();
    try {
      const res = await fetch('/api/graph/analytics');
      const data = await res.json();

      this.resetStates();
      if (data.top_connected_ids) {
        data.top_connected_ids.forEach(tid => this.nodeStates[tid] = "TARGET");
      }
      SoundEffects.success();
      this.render();

      const logEl = document.getElementById('algorithmStepLog');
      if (logEl) {
        logEl.innerHTML = `<div class="anim-slide-in" style="color:var(--accent-cyan);"><strong>Highest Degree Centrality:</strong> ${data.top_connected_ids ? data.top_connected_ids.join(', ') : ''} (${data.max_degree} direct connections)</div>`;
      }
      showToast(`Highest degree suspects: ${data.top_connected_ids ? data.top_connected_ids.join(', ') : ''}`, "success");
    } catch (e) {
      showToast("Error analyzing degree centrality.", "danger");
    }
  }
}

// Instantiate graph on page load
let globalNetworkVisualizer = null;
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('networkCanvas')) {
    globalNetworkVisualizer = new NetworkGraphVisualizer('networkCanvas');
  }
});
