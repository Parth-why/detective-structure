/**
 * SOCIAL DETECTIVE — TIMELINE (DOUBLY LINKED LIST) JS
 * Interactive Doubly Linked List timeline navigation with forward and backward step players.
 */

class TimelineManager {
  constructor() {
    this.currentIndex = 0;
    this.totalEvents = 11;
    this.isPlaying = false;
    this.timer = null;
    this.init();
  }

  init() {
    this.updateActiveEvent(0);
  }

  async navigate(direction) {
    SoundEffects.hop();
    if (direction === 'next') {
      if (this.currentIndex < this.totalEvents - 1) {
        this.currentIndex++;
      } else {
        showToast("Reached End of Timeline (TAIL -> NULL)", "cyan");
        return;
      }
    } else if (direction === 'prev') {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      } else {
        showToast("Reached Beginning of Timeline (HEAD -> NULL)", "cyan");
        return;
      }
    }
    this.updateActiveEvent(this.currentIndex);
  }

  async updateActiveEvent(index) {
    this.currentIndex = index;

    // Highlight card in DOM
    const allCards = document.querySelectorAll('.timeline-event-card');
    allCards.forEach((card, idx) => {
      if (idx === index) {
        card.classList.add('active-event');
        card.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
      } else {
        card.classList.remove('active-event');
      }
    });

    // Fetch node info with prev/next pointers
    try {
      const res = await fetch(`/api/timeline/event/${index}`);
      const data = await res.json();

      const pointerDisplay = document.getElementById('dllPointerInfo');
      if (pointerDisplay && data.data) {
        pointerDisplay.innerHTML = `
          <div style="display:flex; align-items:center; justify-content:space-between; font-family:var(--text-mono); font-size:0.8rem;">
            <div>
              <span style="color:var(--text-muted);">node.prev:</span> 
              <strong style="color:${data.prev_data ? 'var(--accent-purple)' : 'var(--text-muted)'};">
                ${data.prev_data ? data.prev_data.time_label + ' (' + data.prev_data.id + ')' : 'NULL'}
              </strong>
            </div>
            <div style="color:var(--accent-cyan); font-weight:800; font-size:0.9rem;">
              ▶ CURRENT [Node ${index + 1}/${this.totalEvents}]: ${data.data.time_label}
            </div>
            <div>
              <span style="color:var(--text-muted);">node.next:</span> 
              <strong style="color:${data.next_data ? 'var(--accent-cyan)' : 'var(--text-muted)'};">
                ${data.next_data ? data.next_data.time_label + ' (' + data.next_data.id + ')' : 'NULL'}
              </strong>
            </div>
          </div>
        `;
      }
    } catch (e) {
      console.error(e);
    }
  }

  async traverse(direction) {
    if (this.isPlaying) return;
    this.isPlaying = true;
    SoundEffects.scan();

    const endpoint = direction === 'forward' ? '/api/timeline/forward' : '/api/timeline/backward';
    try {
      const res = await fetch(endpoint);
      const data = await res.json();
      const steps = data.steps;

      showToast(`⏳ Running ${direction.toUpperCase()} Doubly Linked List Traversal...`, "cyan");

      let stepIdx = 0;
      this.timer = setInterval(() => {
        if (stepIdx >= steps.length) {
          clearInterval(this.timer);
          this.isPlaying = false;
          SoundEffects.success();
          showToast(`Completed ${direction.toUpperCase()} Traversal (${steps.length} events)`, "success");
          return;
        }

        const step = steps[stepIdx];
        SoundEffects.hop();

        // Calculate logical index
        const domIndex = direction === 'forward' ? stepIdx : (steps.length - 1 - stepIdx);
        this.updateActiveEvent(domIndex);

        const logEl = document.getElementById('timelineStepLog');
        if (logEl) {
          logEl.innerHTML = `
            <div class="anim-slide-in">
              <strong>Step ${step.step} (${step.direction}):</strong> Visiting '${step.current.title}' at ${step.current.time_label} via <code>${step.pointer_used}</code>
            </div>
          `;
        }

        stepIdx++;
      }, 700);
    } catch (e) {
      this.isPlaying = false;
      showToast("Error traversing timeline.", "danger");
    }
  }
}

let globalTimelineManager = null;
document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.timeline-container')) {
    globalTimelineManager = new TimelineManager();
  }
});
