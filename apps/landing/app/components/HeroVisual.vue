<!-- components/HeroVisuals.vue -->
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import gsap from 'gsap'

const containerRef = ref<HTMLElement | null>(null)

onMounted(() => {
  if (!containerRef.value) return

  // GSAP continuous loop for text bubbles & auto-match pill
  const tl = gsap.timeline({ repeat: -1, repeatDelay: 1 })

  // Slide & fade in notification cards
  tl.fromTo(
    '.msg-card',
    { opacity: 0, y: 15, scale: 0.97 },
    { opacity: 1, y: 0, scale: 1, duration: 0.6, stagger: 0.25, ease: 'power2.out' }
  )

  // Animate SVG path pipeline
  tl.fromTo(
    '.n',
    { strokeDasharray: 50, strokeDashoffset: 50 },
    { strokeDashoffset: 0, duration: 0.7, stagger: 0.15, ease: 'power1.inOut' },
    '-=0.2'
  )

  // Reveal matched payment badge & pulse
  tl.fromTo('.disc', { scale: 0, transformOrigin: 'center' }, { scale: 1, duration: 0.4, ease: 'back.out(1.7)' })
  tl.fromTo('.tick', { strokeDasharray: 40, strokeDashoffset: 40 }, { strokeDashoffset: 0, duration: 0.4 })
  tl.fromTo('.matched-pill', { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.4 })
  tl.to('.matched-pill .dot', { scale: 1.4, yoyo: true, repeat: 3, duration: 0.3 })

  // Pause before seamlessly looping
  tl.to({}, { duration: 3.5 })
})
</script>

<template>
  <div ref="containerRef" class="hero-visual-card">

    <!-- Lottie Background Animation (Continuous Auto-Loop) -->
    <client-only>
      <div class="lottie-bg">
        <script src="[suspicious link removed]" type="module"></script>
        <dotlottie-player src="https://lottie.host/dbb77b07-a063-4b04-990d-410ee890bb8a/EVbV9g0uVB.json"
          background="transparent" speed="1" style="width: 100%; height: 100%;" loop autoplay>
        </dotlottie-player>
      </div>
    </client-only>

    <!-- Multi-Channel Notification Cards Stack -->
    <div class="notifications-stack">

      <!-- 1. SMS Card -->
      <div class="msg-card sms-card">
        <div class="card-header">
          <span class="badge sms-bg">
            <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" />
            </svg>
            SMS
          </span>
          <span class="sender font-bold">Silverwood Estate</span>
          <span class="verified">✓ Verified</span>
        </div>
        <p class="card-text">
          Dear Adaeze Ishola, your service charge for Dec 2026 is due. Pay securely via your personal link below.
        </p>
        <div class="card-link">Pay ₦45,000</div>
      </div>

      <!-- 2. WhatsApp Card -->
      <div class="msg-card wa-card">
        <div class="card-header">
          <span class="badge wa-bg">
            <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.84 9.84 0 0012.04 2z" />
            </svg>
            WhatsApp
          </span>
          <span class="sender">Silverwood Accounts</span>
        </div>
        <p class="card-text">
          Hello Adaeze, your instant receipt for invoice #INV-8921 is available.
        </p>
      </div>

      <!-- 3. Gmail Card -->
      <div class="msg-card gmail-card">
        <div class="card-header">
          <span class="badge gmail-bg">
            <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" />
            </svg>
            Gmail
          </span>
          <span class="sender">billing@silverwood.ng</span>
        </div>
        <p class="card-text">
          Statement of Account & Utility Receipt attached.
        </p>
      </div>

    </div>

    <!-- Animated Payment Reconciliation SVG & Pill -->
    <div class="reconciliation-bar">
      <svg class="path" viewBox="0 0 200 60" role="img">
        <g fill="none" stroke="#6366F1" stroke-width="5" stroke-linecap="round">
          <circle class="n n1" cx="14" cy="30" r="10" />
          <path class="n n1" d="M24 30H44" />
          <circle class="n n2" cx="54" cy="30" r="10" />
          <path class="n n2" d="M64 30H84" />
          <circle class="n n3" cx="94" cy="30" r="10" />
          <path class="n n3" d="M104 30H140" />
        </g>
        <circle class="disc" cx="168" cy="30" r="24" fill="#4A15A4" />
        <path class="tick" d="M158 30L165 37L179 22" fill="none" stroke="#FFFFFF" stroke-width="4.5"
          stroke-linecap="round" stroke-linejoin="round" />
      </svg>

      <div class="matched-pill">
        <span class="dot"></span> Payment Completed. Ledger updated.
      </div>
    </div>

  </div>
</template>

<style scoped>
/* Main Visual Wrapper Card */
.hero-visual-card {
  position: relative;
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 24px;
  padding: 1.25rem;
  box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.08);
  overflow: hidden;
}

/* Lottie Background Overlay */
.lottie-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.35;
  pointer-events: none;
  z-index: 0;
}

/* Notification Cards Stack */
.notifications-stack {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Individual Message Card */
.msg-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 0.85rem 1rem;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
  box-sizing: border-box;
  max-width: 100%;
  word-break: break-word;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.35rem;
  font-size: 0.825rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.7rem;
  color: #FFFFFF;
}

.badge .icon {
  width: 12px;
  height: 12px;
}

.sms-bg {
  background-color: #4A15A4;
}

.wa-bg {
  background-color: #25D366;
}

.gmail-bg {
  background-color: #EA4335;
}

.sender {
  font-weight: 700;
  color: #1E293B;
}

.verified {
  color: #059669;
  font-weight: 600;
  font-size: 0.725rem;
  margin-left: auto;
}

.card-text {
  font-size: 0.825rem;
  line-height: 1.4;
  color: #475569;
  margin: 0 0 0.35rem 0;
}

.card-link {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #4A15A4;
  background-color: #F3E8FF;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
}

/* Reconciliation Bar */
.reconciliation-bar {
  position: relative;
  z-index: 1;
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.path {
  width: 100%;
  max-width: 220px;
  height: auto;
}

.matched-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  font-weight: 700;
  color: #0B7A52;
  background-color: #E3F4EC;
  padding: 0.4rem 0.95rem;
  border-radius: 9999px;
  border: 1px solid #BFE6D3;
}

.matched-pill .dot {
  width: 7px;
  height: 7px;
  background-color: #059669;
  border-radius: 50%;
}
</style>