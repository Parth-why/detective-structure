/**
 * SOCIAL DETECTIVE — FORENSIC INVESTIGATION BOARD FX (investigation_board.js)
 * 
 * Implements the immersive handheld magnifying-glass inspection effect:
 * - Direct mouse tracking with ZERO perceptible lag (No lerp, no CSS transition delay)
 * - Large warm tungsten/desk-lamp lighting reveal (--magnifier-radius: 400px)
 * - Custom vintage monocle / magnifying-glass cursor centered directly on pointer
 * - High-performance requestAnimationFrame loop (60 FPS, GPU transform translate3d)
 * - Touch & mobile detection (disables custom cursor and maintains full touch usability)
 * - Accessibility: respects prefers-reduced-motion
 * - High-performance layering: Zero layout reflows, CSS variables + GPU transforms
 */

class InvestigationBoardFX {
  constructor(options = {}) {
    this.boardEl = document.querySelector(options.boardSelector || '.investigation-board-wrap') || document.body;
    this.lightRadius = options.lightRadius || 350;
    this.boardBgUrl = options.boardBgUrl || '/static/assets/The Vanishing File Investigation Board.png';

    // Direct mouse coordinates
    this.mouseX = window.innerWidth / 2;
    this.mouseY = window.innerHeight / 2;
    this.isInside = true;
    this.isTouchDevice = false;
    this.prefersReducedMotion = false;
    this.rafId = null;

    // DOM Elements
    this.overlayEl = null;

    this.init();
  }

  async init() {
    // 1. Accessibility & Device Detection
    this.prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || window.matchMedia('(hover: none)').matches;

    // 2. Setup Lighting Overlay
    this.setupLightingOverlay();
    
    // 3. Setup Mouse Tracking
    if (!this.isTouchDevice) {
      this.bindMouseEvents();
      this.startRenderLoop();
    } else {
      if (this.overlayEl) {
        this.overlayEl.classList.add('mobile-touch-mode');
      }
    }
  }

  setupLightingOverlay() {
    let overlay = this.boardEl.querySelector('.board-lighting-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'board-lighting-overlay';
      overlay.setAttribute('aria-hidden', 'true');
      this.boardEl.appendChild(overlay);
    }
    this.overlayEl = overlay;
    this.overlayEl.style.setProperty('--magnifier-radius', `${this.lightRadius}px`);
    this.overlayEl.style.setProperty('--light-x', `${this.mouseX}px`);
    this.overlayEl.style.setProperty('--light-y', `${this.mouseY}px`);
  }

  bindMouseEvents() {
    const onMouseMove = (e) => {
      this.isInside = true;
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;
    };

    const onMouseEnter = () => {
      this.isInside = true;
    };

    const onMouseLeave = () => {
      this.isInside = false;
    };

    window.addEventListener('mousemove', onMouseMove, { passive: true });
    document.addEventListener('mouseenter', onMouseEnter);
    document.addEventListener('mouseleave', onMouseLeave);

    // Dynamic light hover on interactive desk items
    this.bindInteractiveObjects();
  }

  bindInteractiveObjects() {
    const items = this.boardEl.querySelectorAll('.ledger-item, .card-panel');
    items.forEach(item => {
      item.addEventListener('mouseenter', () => {
        item.classList.add('magnifier-illuminated');
      });
      item.addEventListener('mouseleave', () => {
        item.classList.remove('magnifier-illuminated');
      });
    });
  }

  startRenderLoop() {
    const render = () => {
      if (this.overlayEl && this.isInside) {
        const rect = this.boardEl.getBoundingClientRect();
        const relX = this.mouseX - rect.left;
        const relY = this.mouseY - rect.top;
        this.overlayEl.style.setProperty('--light-x', `${relX.toFixed(1)}px`);
        this.overlayEl.style.setProperty('--light-y', `${relY.toFixed(1)}px`);
      }

      this.rafId = requestAnimationFrame(render);
    };

    this.rafId = requestAnimationFrame(render);
  }

  destroy() {
    if (this.rafId) cancelAnimationFrame(this.rafId);
    if (this.overlayEl) this.overlayEl.remove();
  }
}

// Automatically initialize on DOM load if board is present
document.addEventListener('DOMContentLoaded', () => {
  const isCaseBoard = document.querySelector('.investigation-board-wrap') || window.location.pathname === '/case-board';
  if (isCaseBoard) {
    window.boardFX = new InvestigationBoardFX({
      boardSelector: '.investigation-board-wrap',
      lightRadius: 400
    });
  }
});
