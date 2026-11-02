<!-- components/herosection.vue -->
<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { heroIllustration } from '../utils/heroIllustration'

// The supplied illustration (hand, phone, indigo disc, ripple rings) is driven frame by frame from GSAP, so the
// whole story is one timeline that plays once, can be replayed, and rests on its final frame.
const REST = 2.6
const svgEl = ref<SVGSVGElement | null>(null)
const root = ref<HTMLElement | null>(null)
const canReplay = ref(false)

let tl: any = null
let copyTl: any = null
let io: IntersectionObserver | null = null
let narrow: MediaQueryList | null = null
let frame: (() => void) | null = null

function replay() {
  if (!tl) return
  canReplay.value = false
  tl.restart()
}

onMounted(async () => {
  const s = svgEl.value
  if (!s) return
  s.pauseAnimations()

  // on phones, crop the empty left margin so the artwork fills the width
  narrow = window.matchMedia('(max-width: 900px)')
  frame = () => s.setAttribute('viewBox', narrow!.matches ? '58 20 362 326' : '12 20 408 326')
  frame()
  narrow.addEventListener('change', frame)

  // reduced motion: show the finished scene, and never apply the hidden "anim" state
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduce) {
    s.setCurrentTime(REST)
    return
  }

  s.setCurrentTime(0)
    ; (window as any).__heroStarted = true

  // Activate the hidden start state from site.css (.anim .reveal, .anim .beat-inner, ...)
  document.documentElement.classList.add('anim')

  let gsap: any
  try {
    const [g, { MotionPathPlugin }, { DrawSVGPlugin }] = await Promise.all([
      import('gsap'), import('gsap/MotionPathPlugin'), import('gsap/DrawSVGPlugin')
    ])
    gsap = g.gsap
    gsap.registerPlugin(MotionPathPlugin, DrawSVGPlugin)
  } catch (err) {
    // If GSAP fails to load, never leave the content hidden
    document.documentElement.classList.remove('anim')
    s.setCurrentTime(REST)
    return
  }

  const q = gsap.utils.selector(root.value as HTMLElement)

  // words
  copyTl = gsap.timeline({ defaults: { ease: 'power3.out' } })
    .fromTo(q('.kicker-reveal'), { y: 10, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 0.6 }, 0)
    .fromTo(q('.beat-inner'), { yPercent: 110, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 0.9, stagger: 0.14 }, 0.1)
    .fromTo(q('.reveal'), { y: 14, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 0.7, stagger: 0.1 }, 0.5)

  // scene
  const STARTS = [{ x: 34, y: 236 }, { x: 34, y: 284 }, { x: 34, y: 332 }]
  const END = { x: 220, y: 92 }
  const clock = { t: 0 }

  tl = gsap.timeline({ paused: true })
  tl.to(clock, { t: REST, duration: 3, ease: 'power1.out', onUpdate: () => s.setCurrentTime(clock.t) }, 0)
  tl.to(q('.scene-hide'), { autoAlpha: 1, duration: 0.25 }, 0.05)

  q('.msg-chip').forEach((el: Element, i: number) => {
    const a = STARTS[i]
    const b = { x: END.x, y: END.y + (i - 1) * 12 }
    const t0 = 1.0 + i * 0.14
    tl.set(el, { x: a.x, y: a.y, scale: 0, autoAlpha: 1 }, t0)
      .to(el, { scale: 1, duration: 0.3, ease: 'back.out(2.2)' }, t0)
      .to(el, {
        motionPath: { path: [a, { x: (a.x + b.x) / 2 - 10, y: Math.min(a.y, b.y) - 50 }, b], curviness: 1.4 },
        duration: 0.95, ease: 'power2.inOut'
      }, t0 + 0.25)
      .to(el, { scale: 0.25, autoAlpha: 0, duration: 0.22, ease: 'power2.in' }, t0 + 1.05)
  })

  tl.fromTo(q('.card'), { autoAlpha: 0, scale: 0.85, transformOrigin: '0% 100%' }, { autoAlpha: 1, scale: 1, duration: 0.55, ease: 'back.out(1.6)' }, 2.3)
  tl.fromTo(q('.pill'), { autoAlpha: 0, scale: 1.7, transformOrigin: '50% 50%' }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: 'back.out(2)' }, 2.75)
  tl.to(q('.paybtn'), { scale: 0.93, transformOrigin: '50% 50%', duration: 0.12, yoyo: true, repeat: 1 }, 3.5)
  tl.fromTo(q('.toast'), { autoAlpha: 0, y: 16 }, { autoAlpha: 1, y: 0, duration: 0.5, ease: 'power3.out' }, 3.9)
  tl.fromTo(q('.tick'), { drawSVG: '0%' }, { drawSVG: '100%', duration: 0.4, ease: 'power2.out' }, 4.05)
  tl.call(() => { canReplay.value = true })

  // start the scene when it is actually on screen (on a phone it sits below the text)
  const sceneEl = root.value!.querySelector('.scene') as HTMLElement
  if ('IntersectionObserver' in window) {
    io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) {
        io?.disconnect()
        tl.play()
      }
    }, { threshold: 0.3 })
    io.observe(sceneEl)
  } else {
    tl.play()
  }

  if (location.search.includes('debug')) {
    ; (window as any).__heroTL = tl
      ; (window as any).__copyTL = copyTl
  }
})

onBeforeUnmount(() => {
  tl?.kill()
  copyTl?.kill()
  io?.disconnect()
  if (narrow && frame) narrow.removeEventListener('change', frame)
  // Remove the hidden start state so other pages' .reveal elements are never hidden
  document.documentElement.classList.remove('anim')
})
</script>

<template>
  <section ref="root" class="hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <p class="hero-kicker kicker-reveal">SECURE AUTOMATED BILLINGS &amp; COLLECTIONS</p>
        <h1 class="hero-title">
          <span class="beat"><span class="beat-inner">Verified billing.</span></span>
          <span class="beat"><span class="beat-inner">Fast payments.</span></span>
          <span class="beat"><span class="beat-inner">No arguments.</span></span>
        </h1>
        <p class="hero-lead reveal">Upload your bulk bills file to reach every customer at once across SMS, WhatsApp,
          and email, with personalized messaging and payment link. Our smart AI automatically
          verifies entries to match incoming remittance.</p>

        <div class="cta-row reveal">
          <NuxtLink to="/apply" class="btn btn-indigo">Start Secure Billing</NuxtLink>
          <NuxtLink to="/#how" class="btn-outlined">See how it works</NuxtLink>
        </div>

        <p class="hero-aud reveal">For public utilities, corporate organizations, gated estates, schools, and churches.
        </p>
      </div>

      <div class="scene scene-hide" aria-hidden="true">
        <svg ref="svgEl" viewBox="12 20 408 326" xmlns="http://www.w3.org/2000/svg" focusable="false">
          <defs>
            <filter id="soft" x="-20%" y="-20%" width="140%" height="160%">
              <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#4A15A4" flood-opacity=".14" />
            </filter>
            <linearGradient id="discGrad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stop-color="#75138C" />
              <stop offset="1" stop-color="#4A15A4" />
            </linearGradient>
          </defs>

          <g transform="translate(60 30)" v-html="heroIllustration"></g>

          <g transform="translate(208 34)">
            <g class="card ov">
              <rect width="208" height="104" rx="14" fill="#FFFFFF" stroke="#E5E8ED" filter="url(#soft)" />
              <circle cx="18" cy="19" r="8" fill="#4A15A4" />

              <text class="scene-text name-label" x="32" y="23" font-size="11" font-weight="700" fill="#0B0B14">To:
                Adaeze Ishola</text>

              <g class="pill ov">
                <rect x="146" y="10" width="54" height="18" rx="9" fill="#E3F4EC" />
                <path d="M153 19l2.5 2.5 4.4-4.8" fill="none" stroke="#0B7A52" stroke-width="1.8" stroke-linecap="round"
                  stroke-linejoin="round" />
                <text class="scene-text" x="163" y="22.6" font-size="8.5" font-weight="600"
                  fill="#0B7A52">Verified</text>
              </g>

              <text class="scene-text" x="14" y="46" font-size="10" font-weight="700" fill="#0B0B14">Silverwood
                Estate</text>

              <text class="scene-text" x="14" y="58" font-size="9" font-weight="500" fill="#4A15A4">Dear Adaeze, your
                service charge</text>
              <text class="scene-text" x="14" y="69" font-size="9" font-weight="500" fill="#4A15A4">for December 20XX is
                due</text>

              <text class="scene-text" x="14" y="81" font-size="8.5" font-weight="600" fill="#2D3142">Amount:
                ₦50,000</text>
              <text class="scene-text" x="14" y="93" font-size="8.5" font-weight="500" fill="#667085">Deadline: 31
                December</text>

              <g class="paybtn" transform="translate(132, 82)">
                <rect width="64" height="15" rx="7.5" fill="#4A15A4" />
                <text class="scene-text" x="32" y="10.5" text-anchor="middle" font-size="7.5" font-weight="700"
                  fill="#FFFFFF">Pay Securely</text>
              </g>
            </g>
          </g>

          <g transform="translate(206 262)">
            <g class="toast ov">
              <rect width="206" height="44" rx="22" fill="#E3F4EC" stroke="#BFE6D3" filter="url(#soft)" />
              <circle cx="24" cy="22" r="10" fill="#0B7A52" />
              <path class="tick" d="M19.5 22.5l3.2 3.2 6-6.8" fill="none" stroke="#FFFFFF" stroke-width="2.4"
                stroke-linecap="round" stroke-linejoin="round" />
              <text class="scene-text" x="42" y="21" font-size="12" font-weight="700" fill="#0B7A52">Payment
                Completed</text>
              <text class="scene-text" x="42" y="34" font-size="10" fill="#0B7A52" font-weight="500">Receipt
                Generated</text>
            </g>
          </g>

          <g class="msg-chip">
            <circle r="18" fill="#FFFFFF" stroke="#E5E8ED" stroke-width="1.5" />
            <g transform="translate(-9 -9) scale(.75)" fill="none" stroke="#4A15A4" stroke-width="1.8"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 5h16v11H9l-5 4V5z" />
              <path d="M8 9h8M8 12h5" />
            </g>
          </g>
          <g class="msg-chip">
            <circle r="18" fill="#FFFFFF" stroke="#E5E8ED" stroke-width="1.5" />
            <g transform="translate(-9 -9) scale(.75)" fill="none" stroke="#4A15A4" stroke-width="1.8"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 5h16v11H9l-5 4V5z" />
              <path d="M8 9h8M8 12h5" />
            </g>
          </g>
        </svg>

        <button type="button" class="replay" :class="{ on: canReplay }" @click="replay">↻ Replay</button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  background-color: #F9FBFF;
  padding: 8.5rem 0 4rem 0;
  overflow: hidden;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  align-items: center;
  gap: 2.5rem;
}

.hero-copy {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.hero-kicker {
  font-size: 0.825rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #4A15A4;
  margin-bottom: 0.65rem;
}

.hero-title {
  font-size: 3.15rem;
  font-weight: 900;
  line-height: 1.12;
  letter-spacing: -0.03em;
  color: #0B0B14;
  margin-bottom: 0.75rem;
}

.beat {
  display: block;
  overflow: hidden;
}

.beat-inner {
  display: block;
}

.hero-lead {
  font-size: 1rem;
  line-height: 1.55;
  color: #2D3142;
  margin-bottom: 0.15rem;
  max-width: 510px;
}

.cta-row {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  margin-bottom: 0.5rem;
}

.btn-indigo {
  background-color: #4A15A4;
  color: #FFFFFF;
  padding: 0.8rem 1.6rem;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 6px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1), background-color 0.2s ease;
}

.btn-indigo:hover {
  background-color: #370f7a;
  transform: scale(0.96);
}

.btn-indigo:active {
  transform: scale(0.94);
}

.btn-outlined {
  color: #4A15A4;
  font-weight: 600;
  border: 1.75px solid #8993A4;
  padding: 0.8rem 1.6rem;
  border-radius: 6px;
  font-size: 0.95rem;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1), border-color 0.2s ease, background-color 0.2s ease;
}

.btn-outlined:hover {
  background-color: #F4F2FF;
  border-color: #4A15A4;
  transform: scale(0.96);
}

.btn-outlined:active {
  transform: scale(0.94);
}

.hero-aud {
  font-size: 0.85rem;
  font-weight: 500;
  color: #667085;
}

.scene {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: -1.5rem;
  width: 100%;
}

.scene-text {
  font-family: system-ui, -apple-system, sans-serif;
}

.ov {
  overflow: visible;
}

@media (max-width: 900px) {
  .hero {
    padding: 6.5rem 0 3.5rem 0;
  }

  .hero-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .hero-copy {
    text-align: center;
    align-items: center;
  }

  .hero-title {
    font-size: 2.35rem;
  }

  .hero-lead {
    text-align: center;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 0.75rem;
  }

  .cta-row {
    justify-content: center;
    width: 100%;
    margin-bottom: 0.65rem;
  }

  .scene {
    margin-top: 0;
    max-width: 100%;
  }
}
</style>