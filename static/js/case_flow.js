/**
 * SOCIAL DETECTIVE — DYNAMIC PLAYTHROUGH CONTROLLER (case_flow.js)
 * Authoritative Case State Synchronization & Progression Engine
 */

class CaseFlowManager {
  constructor() {
    this.currentStage = 0;
    this.maxUnlockedStage = 0;
    this.completedStages = new Set();
    this.investigatedSuspects = new Set();
    this.discoveredEvidence = new Set();
    this.discoveredLeads = [];
    this.contradictions = new Set();
    this.connectionTraced = false;
    this.timelinePosition = 0;
    this.timelineEventsReconstructed = new Set([0]);
    this.theoryStatus = "NOT_STARTED";
    this.nextLead = {
      text: "Start by investigating the lab personnel.",
      action_text: "EXAMINE SUSPECTS →",
      target_stage: 1
    };
    this.caseNotesSummary = "1 lead discovered · 0 contradictions · 1 critical clue";
    this.suspectStatuses = {};

    this.graphVisualizer = null;
    this.currentTimelineIndex = 0;
    this.totalTimelineEvents = 11;
    this.currentClueIndex = 0;
    this.selectedAccusedId = null;
    this.selectedAccusedName = null;

    this.clueChain = [
      {
        id: 1020,
        title: "Encrypted Payout Intercept",
        time: "19:15",
        summary: "Digital trace: Offshore crypto escrow transfer for $150,000 flagged in firewall buffer.",
        takeaway: "Someone inside the lab was offered a massive financial bribe.",
        next: 1047
      },
      {
        id: 1047,
        title: "Rear Fire Escape CCTV Log",
        time: "19:47",
        summary: "Physical camera: A hooded figure carrying an external drive exited via the emergency stairwell.",
        takeaway: "The perpetrator fled the building immediately after the file was copied.",
        next: 1061
      },
      {
        id: 1061,
        title: "Terminal 04 Exfiltration Log",
        time: "19:42",
        summary: "System log: Project Chimera genome sequence was copied via USB on workstation #04.",
        takeaway: "The breach occurred while Dr. Maya was verified in the cafeteria.",
        next: 1095
      },
      {
        id: 1095,
        title: "Keycard KC-9021 Scanner Log",
        time: "19:38",
        summary: "Access record: Keycard KC-9021 unlocked Door #3 at 19:38, minutes before Terminal 04 was accessed.",
        takeaway: "The thief used Dr. Maya's stolen badge to access the terminal room.",
        next: null
      }
    ];

    this.init();
  }

  async init() {
    await this.syncWithServerState();
    this.setupEventListeners();
    this.showActiveStage(this.currentStage);
  }

  setupEventListeners() {
    const steps = document.querySelectorAll('.stepper-step');
    steps.forEach((step) => {
      step.addEventListener('click', () => {
        const stageIdx = parseInt(step.getAttribute('data-stage'), 10);
        if (this.completedStages.has(stageIdx) || stageIdx <= this.maxUnlockedStage || stageIdx === this.currentStage) {
          this.goToStage(stageIdx);
        } else {
          const reason = this.getLockedStageMessage(stageIdx);
          this.showLockedStageToast(reason, stageIdx);
        }
      });
    });
  }

  getLockedStageMessage(stageIdx) {
    switch (stageIdx) {
      case 1: return "Start by reviewing the Case Briefing.";
      case 2: return "Investigate Ryan Mehta's statement and access log first.";
      case 3: return "Timeline is still locked. Finish tracing the connection first.";
      case 4: return "Find the contradiction in the timeline first.";
      case 5: return "Examine the critical forensic evidence records first.";
      case 6: return "Build and review your theory before making the final accusation.";
      default: return "Complete the current investigation lead first.";
    }
  }

  showLockedStageToast(reason, stageIdx) {
    SoundEffects.alert();
    const existing = document.querySelector('.locked-stage-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'discovery-toast-banner locked-stage-toast';
    toast.style.borderLeftColor = 'var(--accent-amber)';
    toast.style.borderColor = 'var(--accent-amber)';

    toast.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-family:var(--text-mono); font-size:0.75rem; color:var(--accent-amber); font-weight:700;">
          ⚠️ STAGE LOCKED
        </span>
        <button onclick="this.closest('.locked-stage-toast').remove()" style="background:none; border:none; color:var(--text-muted); cursor:pointer; font-size:1.1rem; line-height:1;">&times;</button>
      </div>
      <div style="font-size:0.95rem; font-weight:700; color:var(--text-primary); margin-top:2px;">
        This part of the case is not ready yet.
      </div>
      <div style="font-size:0.8rem; color:var(--text-secondary); line-height:1.4;">
        ${reason}
      </div>
      <div style="margin-top:0.6rem; text-align:right;">
        <button class="btn btn-amber btn-sm" id="lockedToastLeadBtn">
          GO TO CURRENT LEAD →
        </button>
      </div>
    `;

    document.body.appendChild(toast);

    const btn = toast.querySelector('#lockedToastLeadBtn');
    if (btn) {
      btn.onclick = () => {
        toast.remove();
        this.goToCurrentLead();
      };
    }

    setTimeout(() => {
      if (toast && toast.parentNode) {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 300);
      }
    }, 5500);
  }

  goToCurrentLead() {
    if (!this.nextLead) return;
    const targetStage = this.nextLead.target_stage !== undefined ? this.nextLead.target_stage : this.currentStage;
    this.goToStage(targetStage);
  }

  async syncWithServerState() {
    try {
      const res = await fetch('/api/case/state');
      const state = await res.json();

      if (state) {
        this.currentStage = state.current_stage !== undefined ? state.current_stage : this.currentStage;
        this.maxUnlockedStage = state.max_unlocked_stage !== undefined ? state.max_unlocked_stage : this.maxUnlockedStage;
        this.completedStages = new Set(state.completed_stages || []);
        this.investigatedSuspects = new Set(state.investigated_suspects || []);
        this.discoveredEvidence = new Set(state.discovered_evidence || []);
        this.discoveredLeads = state.discovered_leads || [];
        this.contradictions = new Set(state.contradictions_discovered || []);
        this.connectionTraced = !!state.connection_traced;
        this.timelinePosition = state.timeline_position || 0;
        this.timelineEventsReconstructed = new Set(state.timeline_events_reconstructed || [0]);
        this.theoryStatus = state.theory_status || "NOT_STARTED";
        this.nextLead = state.next_lead || this.nextLead;
        this.caseNotesSummary = state.case_notes_summary || this.caseNotesSummary;
        this.suspectStatuses = state.suspect_statuses || {};
      }

      // Also sync live score and stats if available
      try {
        const statsRes = await fetch('/api/stats');
        const statsData = await statsRes.json();
        if (statsData && statsData.score !== undefined) {
          this.score = statsData.score;
        }
      } catch (e) {}

    } catch (e) {
      console.warn("Could not sync state with server, using local state:", e);
    }

    this.renderStateUI();
  }

  renderStateUI() {
    this.updateStepperUI();
    this.renderCaseMemoryStrip();
    this.renderSuspectBadges();
    this.renderDynamicNextLeads();
    this.updateHeaderProgress();
  }

  updateHeaderProgress() {
    const headerScore = document.getElementById('headerScoreValue');
    if (headerScore && this.score !== undefined) {
      headerScore.innerText = this.score;
    }
    const pct = Math.min(100, Math.round((this.completedStages.size / 7) * 100));
    const fills = document.querySelectorAll('.progress-bar-fill');
    fills.forEach(f => { f.style.width = `${pct}%`; });
    const progTexts = document.querySelectorAll('.progress-container span:last-child');
    progTexts.forEach(t => { t.innerText = `${pct}%`; });
  }

  updateStepperUI() {
    const steps = document.querySelectorAll('.stepper-step');
    const stageNames = ["Briefing", "Suspects", "Connections", "Timeline", "Evidence", "Theory", "Accusation"];

    steps.forEach((step) => {
      const idx = parseInt(step.getAttribute('data-stage'), 10);
      step.classList.remove('active', 'completed', 'locked');

      const name = stageNames[idx] || "";

      if (idx === this.currentStage) {
        step.classList.add('active');
        step.innerHTML = `<span style="color:var(--accent-blue);">●</span> <strong>${name}</strong>`;
      } else if (this.completedStages.has(idx)) {
        step.classList.add('completed');
        step.innerHTML = `<span style="color:var(--accent-green); font-weight:700;">✓</span> ${name}`;
      } else if (idx <= this.maxUnlockedStage) {
        step.innerHTML = `<span style="color:var(--text-muted);">○</span> ${name}`;
      } else {
        step.classList.add('locked');
        step.innerHTML = `<span style="color:rgba(255,255,255,0.2);">○</span> <span style="color:var(--text-muted);">${name}</span>`;
      }
    });
  }

  renderCaseMemoryStrip() {
    const textEl = document.getElementById('caseNotesSummaryText');
    const badgeEl = document.getElementById('caseMemoryProgressBadge');
    const strip = document.getElementById('caseMemoryStrip');

    if (textEl) {
      textEl.innerText = this.caseNotesSummary;
    }

    if (badgeEl) {
      badgeEl.innerText = `${this.investigatedSuspects.size}/13 Suspects • ${this.discoveredEvidence.size}/15 Clues • ${this.timelineEventsReconstructed.size}/11 Events`;
    }

    if (strip) {
      strip.classList.add('updated');
      setTimeout(() => strip.classList.remove('updated'), 600);
    }
  }

  renderSuspectBadges() {
    Object.keys(this.suspectStatuses).forEach((id) => {
      const status = this.suspectStatuses[id];
      const pill = document.getElementById(`suspect-status-${id}`);
      if (pill) {
        pill.innerText = status;
        if (status === 'INVESTIGATED' || status === 'CLEARED') {
          pill.style.color = "var(--accent-green)";
          pill.style.borderColor = "rgba(63, 185, 80, 0.4)";
        } else if (status === 'CRITICAL') {
          pill.style.color = "var(--accent-red)";
          pill.style.borderColor = "rgba(248, 81, 73, 0.4)";
        } else if (status === 'RELEVANT') {
          pill.style.color = "var(--accent-amber)";
          pill.style.borderColor = "rgba(210, 153, 34, 0.4)";
        } else {
          pill.style.color = "var(--text-muted)";
          pill.style.borderColor = "var(--border-subtle)";
        }
      }
    });
  }

  renderDynamicNextLeads() {
    for (let i = 0; i <= 6; i++) {
      const leadTextEl = document.getElementById(`stage${i}NextLeadText`);
      const actionBtnEl = document.getElementById(`stage${i}ActionBtn`);

      if (leadTextEl && this.nextLead && this.nextLead.text) {
        leadTextEl.innerText = this.nextLead.text;
      }

      if (actionBtnEl && this.nextLead) {
        const actionText = this.nextLead.action_text || this.nextLead.action_label || "CONTINUE →";
        actionBtnEl.innerText = actionText;

        actionBtnEl.onclick = () => {
          const code = this.nextLead.action_code;
          if (code === 'START_BRIEFING' || (code === 'EXAMINE_SUSPECTS' && this.currentStage === 0)) {
            this.startInvestigation();
          } else if (code === 'EXAMINE_SUSPECTS') {
            if (this.currentStage !== 1) this.goToStage(1);
            this.inspectSuspect('ryan_mehta');
          } else if (code === 'TRACE_CONNECTIONS') {
            if (this.currentStage !== 2) this.goToStage(2);
            setTimeout(() => this.traceShortestConnection('maya_rao', 'ryan_mehta'), 200);
          } else if (code === 'RECONSTRUCT_TIMELINE') {
            this.goToStage(3);
          } else if (code === 'EXAMINE_EVIDENCE') {
            this.goToStage(4);
          } else if (code === 'BUILD_THEORY') {
            this.goToStage(5);
          } else if (code === 'MAKE_ACCUSATION') {
            this.goToStage(6);
          } else if (code === 'CASE_SOLVED') {
            window.location.href = '/case-solved';
          } else if (this.nextLead.target_stage !== undefined) {
            this.goToStage(this.nextLead.target_stage);
          }
        };
      }
    }
  }

  showDiscovery(title, message) {
    SoundEffects.success();

    const existing = document.querySelector('.discovery-toast-banner');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'discovery-toast-banner';
    toast.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-family:var(--text-mono); font-size:0.75rem; color:var(--accent-green); font-weight:700;">
          + NEW DISCOVERY
        </span>
        <span style="font-family:var(--text-mono); font-size:0.7rem; color:var(--text-muted);">
          CASE UPDATED
        </span>
      </div>
      <div style="font-size:0.95rem; font-weight:700; color:var(--text-primary); margin-top:2px;">
        ${title}
      </div>
      <div style="font-size:0.8rem; color:var(--text-secondary); line-height:1.4;">
        ${message}
      </div>
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('fade-out');
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  async goToStage(stageIndex) {
    if (stageIndex > this.maxUnlockedStage && !this.completedStages.has(stageIndex)) {
      const msg = this.getLockedStageMessage(stageIndex);
      showToast(msg, "warning");
      return;
    }

    this.currentStage = stageIndex;
    try {
      await fetch('/api/case/stage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stage: stageIndex })
      });
    } catch (e) {}

    SoundEffects.hop();
    this.showActiveStage(stageIndex);
    await this.syncWithServerState();

    if (stageIndex === 2) {
      this.initGraphVisualizer();
    } else if (stageIndex === 3) {
      this.loadTimelineNode(this.currentTimelineIndex);
    } else if (stageIndex === 4) {
      this.renderClueChainNode(this.currentClueIndex);
    } else if (stageIndex === 5) {
      this.loadTheoryStack();
    }

    const mainArea = document.querySelector('.case-playthrough-container');
    if (mainArea) {
      mainArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  showActiveStage(stageIndex) {
    const panels = document.querySelectorAll('.stage-panel');
    panels.forEach((p) => p.classList.remove('active'));

    const activePanel = document.getElementById(`stage-panel-${stageIndex}`);
    if (activePanel) {
      activePanel.classList.add('active');
    }
  }

  advanceToNextStage() {
    if (this.currentStage < 6) {
      this.goToStage(this.currentStage + 1);
    }
  }

  // --- STAGE 0: BRIEFING ---
  async startInvestigation() {
    SoundEffects.click();
    try {
      await fetch('/api/case/complete_stage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stage: 0 })
      });
      await fetch('/api/case/stage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stage: 1 })
      });
    } catch (e) {}

    this.showDiscovery(
      "Investigation Commenced",
      "13 personnel identified with building and network access. Inspect Ryan Mehta's statement."
    );

    this.goToStage(1);
  }

  // --- STAGE 1: SUSPECT INSPECTION ---
  async inspectSuspect(suspectId) {
    SoundEffects.scan();
    try {
      const res = await fetch(`/api/user/${suspectId}`);
      const data = await res.json();

      if (data.error) {
        showToast(data.error, "danger");
        return;
      }

      await this.syncWithServerState();

      const modal = document.getElementById('suspectDetailModal');
      const title = document.getElementById('suspectModalName');
      const role = document.getElementById('suspectModalRole');
      const location = document.getElementById('suspectModalLocation');
      const statement = document.getElementById('suspectModalStatement');
      const connections = document.getElementById('suspectModalConnections');
      const evidence = document.getElementById('suspectModalEvidence');
      const highlight = document.getElementById('suspectContradictionHighlight');
      const nextLeadText = document.getElementById('suspectModalNextLeadText');
      const nextLeadBtn = document.getElementById('suspectModalNextLeadBtn');

      if (title) title.innerText = data.name;
      if (role) role.innerText = data.role;
      if (location) location.innerText = data.location || 'Campus';
      if (statement) statement.innerText = `"${data.bio || data.alibi || 'I was studying.'}"`;

      if (connections) {
        if (suspectId === 'ryan_mehta') {
          connections.innerText = "Direct collaborator with Dr. Maya Rao; frequent communications with Systems Admin Sam Verma.";
        } else if (suspectId === 'maya_rao') {
          connections.innerText = "Principal Investigator; works with Ryan Mehta, Dev Malhotra, and Sarah Chen.";
        } else if (suspectId === 'sam_verma') {
          connections.innerText = "Network Systems Administrator; administrative access to all lab workstations.";
        } else {
          connections.innerText = "General lab research staff.";
        }
      }

      if (evidence && highlight) {
        if (suspectId === 'ryan_mehta') {
          highlight.style.display = 'block';
          evidence.innerHTML = `<strong>Contradiction Detected:</strong> Ryan claimed he was at the university library all evening. However, Keycard KC-9021 access records place his badge at Door #3 at 19:38.`;
        } else if (suspectId === 'maya_rao') {
          highlight.style.display = 'block';
          highlight.style.borderColor = 'var(--accent-green)';
          highlight.style.background = 'rgba(63, 185, 80, 0.08)';
          evidence.innerHTML = `<strong>Exonerated:</strong> Verified in 1st-floor cafeteria from 19:30 to 20:45 by multiple witnesses and timestamped register transactions. Her badge was stolen.`;
        } else {
          highlight.style.display = 'none';
        }
      }

      if (nextLeadText && nextLeadBtn) {
        if (suspectId === 'ryan_mehta') {
          nextLeadText.innerText = "Ryan claims he barely knew Maya, but shared access to the high-performance computing cluster.";
          nextLeadBtn.style.display = 'inline-flex';
          nextLeadBtn.innerText = "TRACE HIS CONNECTION →";
          nextLeadBtn.onclick = () => {
            this.closeSuspectModal();
            this.goToStage(2);
            setTimeout(() => {
              this.traceShortestConnection('maya_rao', 'ryan_mehta');
            }, 300);
          };

          this.showDiscovery(
            "Alibi Contradiction: Ryan Mehta",
            "Ryan claimed he was away, but his badge accessed the facility at 19:38. Tracing his network connection is now unlocked."
          );
        } else {
          nextLeadText.innerText = "Inspect Ryan Mehta or trace relationship paths across the laboratory staff.";
          nextLeadBtn.style.display = 'inline-flex';
          nextLeadBtn.innerText = "INVESTIGATE RYAN MEHTA →";
          nextLeadBtn.onclick = () => {
            this.closeSuspectModal();
            this.inspectSuspect('ryan_mehta');
          };
        }
      }

      if (modal) modal.classList.add('active');
    } catch (e) {
      showToast("Error loading suspect dossier.", "danger");
    }
  }

  closeSuspectModal() {
    const modal = document.getElementById('suspectDetailModal');
    if (modal) modal.classList.remove('active');
  }

  // --- STAGE 2: CONNECTIONS (GRAPH BFS) ---
  initGraphVisualizer() {
    if (!this.graphVisualizer) {
      const canvas = document.getElementById('caseNetworkCanvas');
      if (canvas && typeof NetworkGraphVisualizer !== 'undefined') {
        this.graphVisualizer = new NetworkGraphVisualizer('caseNetworkCanvas');
      }
    }
  }

  async traceShortestConnection(start = 'maya_rao', target = 'ryan_mehta') {
    SoundEffects.scan();
    const resultBox = document.getElementById('connectionsResultBox');
    if (resultBox) {
      resultBox.innerHTML = `<span>Finding shortest relationship path between ${start.replace('_', ' ')} and ${target.replace('_', ' ')}...</span>`;
    }

    try {
      const res = await fetch(`/api/graph/bfs?start=${start}&target=${target}`);
      const data = await res.json();

      await this.syncWithServerState();

      if (data.path && data.path.length > 0) {
        SoundEffects.success();
        if (this.graphVisualizer) {
          this.graphVisualizer.highlightPath(data.path, data.visited_order);
        }

        const pathNames = data.path.map(id => id.replace('_', ' ').toUpperCase()).join(' ➔ ');
        const hops = data.path.length - 1;
        if (resultBox) {
          resultBox.innerHTML = `
            <div style="font-family:var(--text-mono); font-size:0.75rem; color:var(--accent-green); font-weight:700; margin-bottom:4px;">
              CONNECTION FOUND : ${hops} DEGREE${hops === 1 ? '' : 'S'} OF SEPARATION (BFS PATH)
            </div>
            <div style="font-size:1rem; font-weight:700; color:var(--text-primary); margin-bottom:4px;">
              ${pathNames}
            </div>
            <div style="font-size:0.85rem; color:var(--text-secondary);">
              ${start === 'maya_rao' && target === 'ryan_mehta' ? "Ryan Mehta is connected to Dr. Maya Rao through Systems Administrator Sam Verma, proving shared access to the server cluster." : "Path traced successfully across network graph edges using FIFO Queue BFS."}
            </div>
          `;
        }

        this.showDiscovery(
          "Network Connection Established",
          "Ryan Mehta is connected to Dr. Maya Rao through Systems Admin Sam Verma. Timeline reconstruction is now unlocked."
        );

        const bannerNextText = document.getElementById('stage2NextLeadText');
        const bannerActionBtn = document.getElementById('stage2ActionBtn');
        if (bannerNextText) {
          bannerNextText.innerText = "Ryan was not as disconnected as he claimed. Reconstruct the night's timeline to check his movements.";
        }
        if (bannerActionBtn) {
          bannerActionBtn.innerText = "RECONSTRUCT THE TIMELINE →";
          bannerActionBtn.onclick = () => this.goToStage(3);
        }
      }
    } catch (e) {
      showToast("Failed to trace connection.", "danger");
    }
  }

  // --- STAGE 3: TIMELINE (ONE EVENT AT A TIME) ---
  async loadTimelineNode(index) {
    SoundEffects.hop();
    this.currentTimelineIndex = Math.max(0, Math.min(index, this.totalTimelineEvents - 1));

    try {
      const res = await fetch(`/api/timeline/event/${this.currentTimelineIndex}`);
      const data = await res.json();

      await this.syncWithServerState();

      const viewer = document.getElementById('timelineSingleEventViewer');
      const contradictionBox = document.getElementById('timelineContradictionCallout');
      const counterEl = document.getElementById('timelineStepCounter');
      if (counterEl) {
        counterEl.innerText = `EVENT ${this.currentTimelineIndex + 1} OF ${this.totalTimelineEvents} (O(1) / STEP)`;
      }

      if (viewer && data.data) {
        const ev = data.data;
        viewer.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; border-bottom:1px solid var(--border-subtle); padding-bottom:0.5rem;">
            <div style="font-family:var(--text-mono); font-size:1.1rem; font-weight:800; color:var(--accent-blue);">
              ${ev.timestamp}
            </div>
            <div style="font-size:0.8rem; color:var(--text-muted); font-family:var(--text-mono);">
              EVENT ${this.currentTimelineIndex + 1} OF ${this.totalTimelineEvents}
            </div>
          </div>
          <div style="font-size:1.05rem; font-weight:700; color:var(--text-primary); margin-bottom:0.25rem;">
            ${ev.actor_name} — ${ev.location}
          </div>
          <div style="font-size:0.9rem; color:var(--text-secondary); line-height:1.6;">
            ${ev.description}
          </div>
        `;

        if (ev.timestamp === "19:38" || ev.timestamp === "19:42" || ev.timestamp === "19:47") {
          if (contradictionBox) {
            contradictionBox.style.display = 'block';
            contradictionBox.innerHTML = `
              <div style="font-family:var(--text-mono); font-size:0.75rem; color:var(--accent-red); font-weight:700; margin-bottom:2px;">
                ⚠️ TIMELINE CONTRADICTION UNCOVERED
              </div>
              <div style="font-size:0.95rem; font-weight:600; color:var(--text-primary);">
                Ryan claimed he left before 19:30. Keycard KC-9021 was scanned at Door #3 at 19:38, and Terminal 04 was accessed at 19:42.
              </div>
            `;
          }

          this.showDiscovery(
            "Timeline Contradiction Confirmed",
            `At ${ev.timestamp}, activity inside the secure lab proves the perpetrator was on-site while Maya was in the cafeteria.`
          );

          const stage3NextLead = document.getElementById('stage3NextLeadText');
          const stage3ActionBtn = document.getElementById('stage3ActionBtn');
          if (stage3NextLead) {
            stage3NextLead.innerText = "Ryan was still inside the facility during the breach. Examine the forensic evidence chain.";
          }
          if (stage3ActionBtn) {
            stage3ActionBtn.innerText = "EXAMINE EVIDENCE →";
            stage3ActionBtn.onclick = () => this.goToStage(4);
          }
        } else {
          if (contradictionBox) contradictionBox.style.display = 'none';
        }
      }
    } catch (e) {}
  }

  prevTimelineEvent() {
    if (this.currentTimelineIndex > 0) {
      this.loadTimelineNode(this.currentTimelineIndex - 1);
    } else {
      showToast("Beginning of timeline reached.", "cyan");
    }
  }

  nextTimelineEvent() {
    if (this.currentTimelineIndex < this.totalTimelineEvents - 1) {
      this.loadTimelineNode(this.currentTimelineIndex + 1);
    } else {
      showToast("End of timeline reached.", "cyan");
    }
  }

  // --- STAGE 4: EVIDENCE ---
  async renderClueChainNode(index) {
    this.currentClueIndex = index;
    const clue = this.clueChain[index];
    const display = document.getElementById('clueChainCurrentDisplay');

    if (display && clue) {
      display.innerHTML = `
        <div style="background:var(--bg-inset); border:1px solid var(--border-primary); border-left:3px solid var(--accent-blue); padding:1rem; border-radius:var(--radius-sm); margin-bottom:0.75rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span style="font-family:var(--text-mono); font-size:0.75rem; color:var(--accent-blue); font-weight:700;">
              EVIDENCE #${clue.id} · ${clue.title.toUpperCase()}
            </span>
            <span style="font-family:var(--text-mono); font-size:0.75rem; color:var(--text-muted);">
              RECORDED: ${clue.time}
            </span>
          </div>
          <div style="font-size:0.95rem; font-weight:600; color:var(--text-primary); margin-bottom:0.5rem;">
            ${clue.summary}
          </div>
          <div style="background:rgba(255,255,255,0.03); padding:0.5rem 0.75rem; border-radius:var(--radius-xs); border:1px solid var(--border-subtle); font-size:0.85rem; color:var(--text-secondary);">
            <strong style="color:var(--text-primary);">What does this tell you?</strong> ${clue.takeaway}
          </div>
        </div>
      `;

      try {
        await fetch(`/api/evidence/${clue.id}`);
        await this.syncWithServerState();
      } catch (e) {}
    }
  }

  advanceClueChain() {
    SoundEffects.scan();
    if (this.currentClueIndex < this.clueChain.length - 1) {
      this.renderClueChainNode(this.currentClueIndex + 1);
    } else {
      this.renderClueChainNode(0);
    }
  }

  async searchEvidenceBST() {
    const input = document.getElementById('playthroughEvidenceSearch');
    const query = input ? input.value.trim() : '1047';
    if (!query) return;

    SoundEffects.scan();
    const output = document.getElementById('bstSearchResultBox');
    if (output) output.innerHTML = "<span>Searching evidence records in BST...</span>";

    try {
      const res = await fetch(`/api/bst/search/${encodeURIComponent(query)}`);
      const data = await res.json();

      await this.syncWithServerState();

      if (data.found && data.evidence) {
        SoundEffects.success();
        const ev = data.evidence;
        if (output) {
          output.innerHTML = `
            <div style="color:var(--accent-green); font-weight:700; margin-bottom:2px; font-size:0.85rem;">
              ✓ EVIDENCE RECORD #${ev.id} DISCOVERED
            </div>
            <div style="font-size:0.95rem; font-weight:700; color:var(--text-primary);">${ev.title}</div>
            <div style="font-size:0.85rem; color:var(--text-secondary); margin-top:2px;">${ev.description}</div>
          `;
        }

        this.showDiscovery(
          `Evidence #${ev.id} Recovered`,
          `${ev.title}: ${ev.description}`
        );

        const stage4NextLead = document.getElementById('stage4NextLeadText');
        const stage4ActionBtn = document.getElementById('stage4ActionBtn');
        if (stage4NextLead) {
          stage4NextLead.innerText = "The evidence links stolen keycard KC-9021, Terminal 04, and the rear fire stairwell. Build your theory.";
        }
        if (stage4ActionBtn) {
          stage4ActionBtn.innerText = "BUILD YOUR THEORY →";
          stage4ActionBtn.onclick = () => this.goToStage(5);
        }
      } else {
        SoundEffects.alert();
        if (output) {
          output.innerHTML = `<span style="color:var(--accent-amber);">Record #${query} not found in BST index. Try #1047 or #1061.</span>`;
        }
      }
    } catch (e) {
      showToast("Error searching evidence.", "danger");
    }
  }

  async extractPriorityHeapClue() {
    SoundEffects.scan();
    const output = document.getElementById('heapPriorityResultBox');
    if (output) output.innerHTML = "<span>Extracting highest-confidence evidence from Max-Heap...</span>";

    try {
      const res = await fetch('/api/heap/peek');
      const data = await res.json();

      await this.syncWithServerState();

      if (data.evidence) {
        SoundEffects.success();
        const ev = data.evidence;
        if (output) {
          output.innerHTML = `
            <div style="color:var(--accent-amber); font-weight:700; margin-bottom:2px; font-size:0.85rem;">
              ★ HIGHEST-CONFIDENCE CLUE (${ev.credibility}% Reliability)
            </div>
            <div style="font-size:0.95rem; font-weight:700; color:var(--text-primary);">#${ev.id}: ${ev.title}</div>
            <div style="font-size:0.85rem; color:var(--text-secondary); margin-top:2px;">${ev.description}</div>
          `;
        }

        this.showDiscovery(
          `Priority Evidence #${ev.id}`,
          `Max-Heap surfaced ${ev.title} (${ev.credibility}% reliability).`
        );
      }
    } catch (e) {
      showToast("Error retrieving priority clue.", "danger");
    }
  }

  // --- STAGE 5: THEORY ---
  async loadTheoryStack() {
    try {
      const res = await fetch('/api/stack/state');
      const data = await res.json();
      const container = document.getElementById('theoryStackContainer');
      if (container && data.items) {
        if (data.items.length === 0) {
          container.innerHTML = `<span style="color:var(--text-muted); font-size:0.8rem;">Investigation history is currently empty.</span>`;
        } else {
          container.innerHTML = data.items.map((item, idx) => `
            <div style="padding:0.4rem 0.6rem; background:var(--bg-inset); border-left:2px solid ${idx === 0 ? 'var(--accent-blue)' : 'var(--border-subtle)'}; margin-bottom:4px; font-size:0.8rem;">
              <div style="font-weight:600; color:var(--text-primary);">${idx === 0 ? '▶ [TOP] ' : ''}${item.title || item.id}</div>
              <div style="font-size:0.7rem; color:var(--text-muted); font-family:var(--text-mono);">${item.type}</div>
            </div>
          `).join('');
        }
      }
    } catch (e) {}
  }

  async setSuspectTag(suspectId, tag) {
    SoundEffects.click();
    try {
      const res = await fetch('/api/theory/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          entity_type: 'suspect',
          entity_id: suspectId,
          status: tag
        })
      });
      const data = await res.json();

      await this.syncWithServerState();

      if (data.success) {
        showToast(`Marked suspect as ${tag}`, "cyan");
        const pill = document.getElementById(`theory-tag-${suspectId}`);
        if (pill) {
          pill.innerText = tag;
          pill.style.color = tag === 'CRITICAL' ? 'var(--accent-red)' : tag === 'CLEARED' ? 'var(--accent-green)' : 'var(--accent-amber)';
        }

        if (suspectId === 'ryan_mehta' && tag === 'CRITICAL') {
          this.showDiscovery(
            "Case Theory Formed",
            "Ryan Mehta marked as CRITICAL. You have enough evidence to proceed to final accusation."
          );

          const stage5ActionBtn = document.getElementById('stage5ActionBtn');
          if (stage5ActionBtn) {
            stage5ActionBtn.innerText = "MAKE FINAL ACCUSATION →";
            stage5ActionBtn.onclick = () => this.goToStage(6);
          }
        }
      }
    } catch (e) {
      showToast("Failed to update theory status.", "danger");
    }
  }

  async backtrackInvestigation() {
    SoundEffects.pop();
    try {
      const res = await fetch('/api/backtrack', { method: 'POST' });
      const data = await res.json();

      if (!data.success) {
        showToast(data.message || "No previous action to undo.", "warning");
        return;
      }

      showToast(`Undid action: Returned to ${data.current_item ? data.current_item.title : 'previous state'}`, "cyan");
      this.loadTheoryStack();
      await this.syncWithServerState();
    } catch (e) {
      showToast("Error undoing action.", "danger");
    }
  }

  // --- STAGE 6: FINAL ACCUSATION ---
  selectAccusedSuspect(suspectId, suspectName) {
    SoundEffects.click();
    this.selectedAccusedId = suspectId;
    this.selectedAccusedName = suspectName;

    const candidates = document.querySelectorAll('.accusation-candidate');
    candidates.forEach((c) => {
      if (c.getAttribute('data-id') === suspectId) {
        c.classList.add('selected');
        const indicator = c.querySelector('.select-indicator');
        if (indicator) {
          indicator.innerText = "SELECTED ✓";
          indicator.style.color = "var(--accent-red)";
        }
      } else {
        c.classList.remove('selected');
        const indicator = c.querySelector('.select-indicator');
        if (indicator) {
          indicator.innerText = "SELECT →";
          indicator.style.color = "var(--text-muted)";
        }
      }
    });

    const banner = document.getElementById('accusationSelectionBanner');
    const submitBtn = document.getElementById('submitAccusationBtn');

    if (banner) {
      banner.style.display = 'block';
      banner.innerHTML = `
        <div style="font-size:0.8rem; color:var(--text-muted); font-family:var(--text-mono); margin-bottom:2px;">ACCUSATION CONFIRMATION</div>
        <div style="font-size:1.1rem; font-weight:700; color:var(--text-primary);">
          You are accusing <strong style="color:var(--accent-red);">${suspectName}</strong> of stealing Project Chimera.
        </div>
        <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:4px;">
          Once submitted, your accusation will be cross-checked against keycard logs, terminal timestamps, and alibis.
        </div>
      `;
    }

    if (submitBtn) {
      submitBtn.removeAttribute('disabled');
      submitBtn.style.opacity = '1';
      submitBtn.style.cursor = 'pointer';
      submitBtn.innerText = `SUBMIT ACCUSATION FOR ${suspectName.toUpperCase()}`;
    }
  }

  async submitFinalAccusation() {
    if (!this.selectedAccusedId) {
      SoundEffects.alert();
      showToast("Please select a suspect before submitting.", "warning");
      return;
    }

    SoundEffects.scan();
    const submitBtn = document.getElementById('submitAccusationBtn');
    if (submitBtn) {
      submitBtn.innerText = "EVALUATING FORENSIC EVIDENCE...";
      submitBtn.setAttribute('disabled', 'true');
    }

    try {
      const res = await fetch('/api/accusation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ suspect_id: this.selectedAccusedId })
      });
      const data = await res.json();

      if (data.success && data.verdict === "SOLVED") {
        SoundEffects.success();
        this.showDiscovery("CASE SOLVED!", "Conviction secured against Ryan Mehta. Generating case report...");
        setTimeout(() => {
          window.location.href = '/case-solved';
        }, 800);
      } else {
        SoundEffects.alert();
        this.showContradictionModal(data);
        await this.syncWithServerState();
        if (submitBtn) {
          submitBtn.removeAttribute('disabled');
          submitBtn.innerText = `SUBMIT ACCUSATION FOR ${this.selectedAccusedName ? this.selectedAccusedName.toUpperCase() : 'SELECTED SUSPECT'}`;
        }
      }
    } catch (e) {
      showToast("Error evaluating accusation.", "danger");
      if (submitBtn) {
        submitBtn.removeAttribute('disabled');
        submitBtn.innerText = "SUBMIT ACCUSATION";
      }
    }
  }

  showContradictionModal(data) {
    const modal = document.getElementById('accusationContradictionModal');
    const reasonText = document.getElementById('contradictionReasonText');
    if (reasonText) {
      if (this.selectedAccusedId === 'maya_rao') {
        reasonText.innerText = "Contradiction: Dr. Maya Rao was verified in the 1st-floor cafeteria from 19:30 to 20:45 by staff and cafeteria records. Her stolen keycard KC-9021 was used by someone else.";
      } else if (this.selectedAccusedId === 'arjun_kulkarni') {
        reasonText.innerText = "Contradiction: Arjun Kulkarni was delivering a lecture in the main Auditorium during the breach window, verified by video footage.";
      } else {
        reasonText.innerText = data.message || "Contradiction: This suspect has a verified alibi. The stolen keycard KC-9021 and Terminal 04 access point toward a different perpetrator.";
      }
    }
    if (modal) modal.classList.add('active');
  }

  closeContradictionModal() {
    const modal = document.getElementById('accusationContradictionModal');
    if (modal) modal.classList.remove('active');
  }
}

// Global toggle for "How This Works" expanders
function toggleHowBox(boxId) {
  const box = document.getElementById(boxId);
  if (box) {
    box.classList.toggle('open');
    const sign = box.querySelector('.how-sign');
    if (sign) {
      sign.innerText = box.classList.contains('open') ? '−' : '+';
    }
    SoundEffects.click();
  }
}

let globalCaseFlow = null;
document.addEventListener('DOMContentLoaded', () => {
  globalCaseFlow = new CaseFlowManager();
});
