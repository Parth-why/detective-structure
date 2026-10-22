/**
 * SOCIAL DETECTIVE — INVESTIGATION BOARD & RUNTIME STATE JS
 * Handles Stack Backtracking, Circular Queue CCTV cycling, Theory Board, and Final Accusation.
 */

// Backtrack (Stack Pop)
async function backtrackInvestigation() {
  SoundEffects.pop();
  try {
    const res = await fetch('/api/backtrack', { method: 'POST' });
    const data = await res.json();

    if (!data.success) {
      showToast(data.message, "warning");
      return;
    }

    showToast(`⏮️ Backtracked to: ${data.current_item.title || data.current_item.id}`, "cyan");
    updateStackUI(data.stack_state);

    // If popped to a specific item, highlight or load it
    if (data.current_item.type === "SUSPECT") {
      highlightActiveCard(`suspect-${data.current_item.id}`);
    } else if (data.current_item.type === "EVIDENCE") {
      highlightActiveCard(`evidence-${data.current_item.id}`);
    }
  } catch (e) {
    showToast("Failed to backtrack.", "danger");
  }
}

// Refresh Stack UI
function updateStackUI(stackState) {
  const container = document.getElementById('investigationStackList');
  if (!container) return;

  if (!stackState.items || stackState.items.length === 0) {
    container.innerHTML = `<span style="color:var(--text-muted); font-size:0.8rem;">Investigation stack is empty.</span>`;
    return;
  }

  container.innerHTML = stackState.items.map((item, idx) => `
    <div class="stack-node ${idx === 0 ? 'top-node' : ''}">
      <div>
        <div style="font-weight:700; font-size:0.85rem;">${idx === 0 ? '▶ [TOP] ' : ''}${item.title || item.id}</div>
        <div style="font-size:0.7rem; color:var(--text-cyan); font-family:var(--text-mono);">${item.type} | ${item.timestamp || 'Active'}</div>
      </div>
      <span style="font-size:0.7rem; color:var(--text-muted); font-family:var(--text-mono);">Depth ${stackState.items.length - idx}</span>
    </div>
  `).join('');
}

// Surveillance Camera (Circular Queue) Cycle Next
async function cycleCCTVFeed() {
  SoundEffects.scan();
  try {
    const res = await fetch('/api/circular-queue/cycle', { method: 'POST' });
    const data = await res.json();

    if (data.current_feed) {
      const feed = data.current_feed;
      const camLabel = document.getElementById('cctvCameraLabel');
      const camNotes = document.getElementById('cctvNotes');
      const camTime = document.getElementById('cctvTimestamp');
      const camBadge = document.getElementById('cctvBadge');

      if (camLabel) camLabel.innerText = `${feed.code}: ${feed.label}`;
      if (camNotes) camNotes.innerText = feed.notes;
      if (camTime) camTime.innerText = `REC TIME: ${feed.timestamp}`;
      if (camBadge) {
        camBadge.innerText = feed.security_level;
        camBadge.style.background = feed.color_hex + '22';
        camBadge.style.color = feed.color_hex;
        camBadge.style.borderColor = feed.color_hex;
      }

      updateCircularQueueSlots(data.state);
      showToast(`📹 Switched to ${feed.code} (${feed.label})`, "cyan");
    }
  } catch (e) {
    showToast("Error cycling surveillance feed.", "danger");
  }
}

function updateCircularQueueSlots(state) {
  const container = document.getElementById('circularQueueSlots');
  if (!container || !state || !state.slots) return;

  container.innerHTML = state.slots.map(slot => `
    <div style="
      flex: 1;
      padding: 0.5rem;
      border: 1px solid ${slot.is_front ? 'var(--accent-blue)' : (slot.is_rear ? 'var(--accent-amber)' : 'var(--border-subtle)')};
      background: ${slot.is_front ? 'rgba(2, 132, 199, 0.12)' : 'var(--bg-inset)'};
      border-radius: var(--radius-sm);
      text-align: center;
      font-family: var(--text-mono);
      font-size: 0.75rem;
    ">
      <div style="font-weight:800; color:${slot.is_front ? 'var(--accent-blue)' : 'var(--text-primary)'};">
        Slot [${slot.index}]
      </div>
      <div style="font-size:0.65rem; color:var(--text-muted); margin-top:2px;">
        ${slot.is_front ? '▲ FRONT' : (slot.is_rear ? '▼ REAR' : 'OCCUPIED')}
      </div>
    </div>
  `).join('');
}

// Toggle Theory Status
async function toggleTheory(type, id, status) {
  SoundEffects.click();
  try {
    const res = await fetch('/api/theory/toggle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, id, status })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`📝 Tagged ${type} '${id}' as ${status}`, "cyan");
    }
  } catch (e) {
    showToast("Failed to update theory.", "danger");
  }
}

// Process Evidence (Queue Dequeue)
async function processNextEvidence() {
  SoundEffects.scan();
  try {
    const res = await fetch('/api/queue/dequeue', { method: 'POST' });
    const data = await res.json();

    if (!data.success) {
      showToast(data.message, "warning");
      return;
    }

    SoundEffects.success();
    const item = data.processed_item;
    showToast(`📋 Processed Evidence #${item.id}: ${item.title} (FIFO Dequeued)`, "success");

    // Open evidence detail or update evidence queue display
    const qCount = document.getElementById('evidenceQueueCount');
    if (qCount) qCount.innerText = data.queue_state.size;
  } catch (e) {
    showToast("Failed to process evidence.", "danger");
  }
}

// Submit Final Accusation
async function submitAccusation() {
  const select = document.getElementById('accusedSuspectSelect');
  if (!select || !select.value) {
    showToast("Please select a suspect to accuse.", "warning");
    return;
  }

  const suspectId = select.value;
  SoundEffects.scan();

  try {
    const res = await fetch('/api/accusation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ suspect_id: suspectId })
    });
    const data = await res.json();

    const modal = document.getElementById('accusationResultModal');
    const title = document.getElementById('accusationResultTitle');
    const msg = document.getElementById('accusationResultMsg');
    const actionBtn = document.getElementById('accusationActionBtn');

    if (data.verdict === "SOLVED") {
      SoundEffects.success();
      if (title) title.innerText = "🏆 CASE CLOSED — CONGRATULATIONS!";
      if (msg) msg.innerText = data.message;
      if (actionBtn) {
        actionBtn.innerText = "VIEW CASE SOLVED REPORT";
        actionBtn.onclick = () => window.location.href = '/case-solved';
      }
    } else {
      SoundEffects.alert();
      if (title) title.innerText = "❌ THEORY CONTRADICTION";
      if (msg) msg.innerText = data.message;
      if (actionBtn) {
        actionBtn.innerText = "CONTINUE INVESTIGATION";
        actionBtn.onclick = () => {
          if (modal) modal.classList.remove('active');
        };
      }
    }

    if (modal) modal.classList.add('active');
  } catch (e) {
    showToast("Error submitting accusation.", "danger");
  }
}

function highlightActiveCard(elementId) {
  const el = document.getElementById(elementId);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    el.classList.add('flash-highlight');
    setTimeout(() => el.classList.remove('flash-highlight'), 1200);
  }
}
