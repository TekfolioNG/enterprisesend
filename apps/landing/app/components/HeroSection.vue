<script setup lang="ts">
import { gmail, whatsapp } from '~/utils/brandIcons'
import { heroIllustration } from '~/utils/heroIllustration'

// The supplied illustration (hand, phone, disc, rings) is driven frame by frame from GSAP, so the whole story is one
// timeline: it plays, holds on the finished scene, fades, and starts again. It pauses when off screen.
const REST = 2.6
const svgEl = ref<SVGSVGElement | null>(null)
const root = ref<HTMLElement | null>(null)
let tl: any = null
let copyTl: any = null
let io: IntersectionObserver | null = null

onMounted(async () => {
  const s = svgEl.value
  if (!s) return
  s.pauseAnimations()
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduce) { s.setCurrentTime(REST); return }   // still image: the finished scene
  s.setCurrentTime(0)
    ; (window as any).__heroStarted = true

  const [{ gsap }, { MotionPathPlugin }, { DrawSVGPlugin }] = await Promise.all([
    import('gsap'), import('gsap/MotionPathPlugin'), import('gsap/DrawSVGPlugin')
  ])
  gsap.registerPlugin(MotionPathPlugin, DrawSVGPlugin)
  const q = gsap.utils.selector(root.value as HTMLElement)

  // words: once
  copyTl = gsap.timeline({ defaults: { ease: 'power3.out' } })
    .fromTo(q('.kicker-reveal'), { y: 10, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 0.6 }, 0)
    .fromTo(q('.beat-inner'), { yPercent: 110, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 0.9, stagger: 0.14 }, 0.1)
    .fromTo(q('.reveal'), { y: 14, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 0.7, stagger: 0.1 }, 0.5)

  // scene: loops with a calm pause on the finished frame
  const STARTS = [{ x: 90, y: 232 }, { x: 90, y: 282 }, { x: 90, y: 332 }]
  const END = { x: 214, y: 90 }
  const clock = { t: 0 }
  tl = gsap.timeline({ paused: true, repeat: -1, repeatDelay: 0.5 })
  tl.to(clock, { t: REST, duration: 3, ease: 'power1.out', onUpdate: () => s.setCurrentTime(clock.t) }, 0)
  tl.to(q('.scene-hide'), { autoAlpha: 1, duration: 0.3 }, 0.05)
  q('.chip').forEach((el: Element, i: number) => {
    const a = STARTS[i]!; const b = { x: END.x, y: END.y + (i - 1) * 14 }
    const t0 = 1.0 + i * 0.16
    tl.set(el, { x: a.x, y: a.y, scale: 0, autoAlpha: 1 }, t0)
      .to(el, { scale: 1, duration: 0.3, ease: 'back.out(2.2)' }, t0)
      .to(el, { motionPath: { path: [a, { x: (a.x + b.x) / 2 - 8, y: Math.min(a.y, b.y) - 46 }, b], curviness: 1.4 }, duration: 0.95, ease: 'power2.inOut' }, t0 + 0.25)
      .to(el, { scale: 0.25, autoAlpha: 0, duration: 0.22, ease: 'power2.in' }, t0 + 1.05)
  })
  tl.fromTo(q('.card'), { autoAlpha: 0, scale: 0.85, transformOrigin: '0% 100%' }, { autoAlpha: 1, scale: 1, duration: 0.55, ease: 'back.out(1.6)' }, 2.4)
  tl.fromTo(q('.pill'), { autoAlpha: 0, scale: 1.7, transformOrigin: '50% 50%' }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: 'back.out(2)' }, 2.85)
  tl.to(q('.paybtn'), { scale: 0.93, transformOrigin: '50% 50%', duration: 0.12, yoyo: true, repeat: 1 }, 3.6)
  tl.fromTo(q('.toast'), { autoAlpha: 0, y: 16 }, { autoAlpha: 1, y: 0, duration: 0.5, ease: 'power3.out' }, 4.0)
  tl.fromTo(q('.tick'), { drawSVG: '0%' }, { drawSVG: '100%', duration: 0.4, ease: 'power2.out' }, 4.15)
  tl.to(q('.scene-hide'), { autoAlpha: 0, duration: 0.45, ease: 'power1.in' }, 7.2)   // hold ~2.7 s, then reset softly

  // play only while visible (saves battery on phones)
  if ('IntersectionObserver' in window) {
    io = new IntersectionObserver((entries) => {
      entries.forEach((e) => (e.isIntersecting ? tl.play() : tl.pause()))
    }, { threshold: 0.2 })
    io.observe(root.value!.querySelector('.scene') as HTMLElement)
  } else { tl.play() }

  if (location.search.includes('debug')) { (window as any).__heroTL = tl; (window as any).__copyTL = copyTl }
})

onBeforeUnmount(() => { tl?.kill(); copyTl?.kill(); io?.disconnect() })
</script>

<template>
  <section ref="root"
    class="hero relative -mt-[72px] overflow-hidden pt-[calc(72px+4rem)] pb-24 max-tablet:pt-[calc(72px+0.5rem)] max-tablet:pb-12">
    <div
      class="wrap grid grid-cols-1 items-center gap-4 tablet:grid-cols-[minmax(0,1fr)_minmax(0,1.02fr)] tablet:gap-[clamp(1rem,2.5vw,2rem)]">
      <div class="hero-copy flex flex-col text-left max-tablet:items-center max-tablet:text-center">
        <p class="kicker-reveal mb-[.9rem] font-display text-[.8rem] font-bold tracking-[.12em] text-brand-indigo">
          SECURE AUTOMATED BILLING &amp; COLLECTIONS</p>
        <h1
          class="mb-4 font-display text-[length:clamp(2.4rem,4.4vw,3.7rem)] leading-[1.05] font-bold tracking-[-0.03em] text-ink max-tablet:text-[length:clamp(2rem,8vw,2.5rem)]">
          <span class="beat -mb-[.12em] block overflow-clip pb-[.12em] whitespace-nowrap"><span
              class="beat-inner block">Verified billing.</span></span>
          <span class="beat -mb-[.12em] block overflow-clip pb-[.12em] whitespace-nowrap"><span
              class="beat-inner block">Fast payments.</span></span>
          <span class="beat -mb-[.12em] block overflow-clip pb-[.12em] whitespace-nowrap"><span
              class="beat-inner block">No arguments.</span></span>
        </h1>
        <p class="reveal mb-[1.1rem] max-w-[56ch] text-[1.02rem] leading-[1.6] text-[#2D3142] max-tablet:mx-auto">Upload
          your bulk bills file to reach every customer at once with personalized
          messages across SMS, WhatsApp, and email, each with a secure payment link. Smart checks catch any errors
          or inconsistencies before anything is sent, and every incoming
          payment is matched to its bill automatically.</p>

        <div class="reveal mb-4 flex flex-wrap items-center gap-[.9rem] max-tablet:w-full max-tablet:justify-center">
          <NuxtLink to="/apply"
            class="inline-flex min-h-12 items-center justify-center rounded-lg border-[1.5px] border-solid border-cta bg-cta px-6 py-3 text-[.98rem] font-semibold whitespace-nowrap text-white no-underline shadow-[0_1px_2px_rgba(117,19,140,.25),0_6px_14px_-6px_rgba(117,19,140,.45)] transition duration-300 ease-[cubic-bezier(.22,1,.36,1)] hover:-translate-y-0.5 hover:border-cta-dark hover:bg-cta-dark hover:shadow-[0_2px_4px_rgba(117,19,140,.25),0_14px_26px_-10px_rgba(117,19,140,.55)] active:translate-y-0 active:scale-[.985] active:duration-100">
            Start Secure Billing</NuxtLink>
          <NuxtLink to="/#how"
            class="inline-flex min-h-12 items-center justify-center rounded-lg border-[1.5px] border-solid border-[#CBD0D8] bg-white px-6 py-3 text-[.98rem] font-semibold whitespace-nowrap text-brand-indigo no-underline shadow-[0_1px_2px_rgba(11,11,20,.06),0_6px_14px_-8px_rgba(11,11,20,.18)] transition duration-300 ease-[cubic-bezier(.22,1,.36,1)] hover:-translate-y-0.5 hover:border-brand-indigo/55 hover:bg-[#F8F6FF] hover:shadow-[0_2px_4px_rgba(11,11,20,.06),0_14px_26px_-12px_rgba(74,21,164,.35)] active:translate-y-0 active:scale-[.985] active:duration-100">
            See how it works</NuxtLink>
        </div>

        <p class="reveal m-0 text-[.88rem] font-medium text-[#667085]"><em>For utilities, estates, schools, faith
            groups,
            clinics, and organizations who want modern, smarter, and foolproof billing and collections system.</em>
        </p>
      </div>

      <div
        class="scene scene-hide relative mx-auto flex w-full max-w-[680px] items-center justify-center max-tablet:order-first max-tablet:max-w-[520px]"
        aria-hidden="true">
        <svg ref="svgEl" class="block h-auto w-full overflow-visible" viewBox="62 16 362 334"
          xmlns="http://www.w3.org/2000/svg" focusable="false">
          <defs>
            <linearGradient id="discGrad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stop-color="#75138C" />
              <stop offset="1" stop-color="#4A15A4" />
            </linearGradient>
          </defs>

          <g transform="translate(60 30)" v-html="heroIllustration"></g>

          <g transform="translate(204 30)">
            <g class="card ov">
              <rect x="-2" y="10" width="220" height="118" rx="18" fill="#4A15A4" opacity=".04" />
              <rect x="-1" y="6" width="218" height="116" rx="16" fill="#4A15A4" opacity=".05" />
              <rect y="3" width="216" height="116" rx="14" fill="#4A15A4" opacity=".06" />
              <rect width="216" height="118" rx="14" fill="#FFFFFF" stroke="#E5E8ED" />
              <circle cx="19" cy="20" r="8" fill="#4A15A4" />
              <text class="font-sans" x="33" y="19" font-size="10.5" font-weight="700" fill="#0B0B14">Silverwood
                Estate</text>
              <text class="font-sans" x="33" y="30" font-size="8" fill="#667085">To: Adaeze Ishola</text>
              <g class="pill ov">
                <rect x="150" y="11" width="54" height="18" rx="9" fill="#E3F4EC" />
                <path d="M157 20l2.5 2.5 4.4-4.8" fill="none" stroke="#0B7A52" stroke-width="1.8" stroke-linecap="round"
                  stroke-linejoin="round" />
                <text class="font-sans" x="167" y="23.4" font-size="8.5" font-weight="600"
                  fill="#0B7A52">Verified</text>
              </g>
              <text class="font-sans" x="14" y="52" font-size="9.5" font-weight="500" fill="#0B0B14">Dear Adaeze, your
                December service</text>
              <text class="font-sans" x="14" y="65" font-size="9.5" font-weight="500" fill="#0B0B14">charge of ₦50,000
                is due 31 Dec.</text>
              <g class="paybtn" transform="translate(14 76)">
                <rect class="fill-cta" width="86" height="22" rx="11" />
                <text class="font-sans" x="43" y="14.6" text-anchor="middle" font-size="9.5" font-weight="600"
                  fill="#FFFFFF">Pay securely</text>
              </g>
              <text class="font-sans" x="14" y="110" font-size="7.5" fill="#667085">Reply STOP to opt out</text>
            </g>
          </g>

          <g transform="translate(206 262)">
            <g class="toast ov">
              <rect x="-2" y="8" width="210" height="44" rx="24" fill="#0B7A52" opacity=".05" />
              <rect y="4" width="206" height="42" rx="22" fill="#0B7A52" opacity=".07" />
              <rect width="206" height="44" rx="22" fill="#E3F4EC" stroke="#BFE6D3" />
              <circle cx="24" cy="22" r="10" fill="#0B7A52" />
              <path class="tick" d="M19.5 22.5l3.2 3.2 6-6.8" fill="none" stroke="#FFFFFF" stroke-width="2.4"
                stroke-linecap="round" stroke-linejoin="round" />
              <text class="font-sans" x="42" y="21" font-size="12" font-weight="700" fill="#0B7A52">Payment
                Completed</text>
              <text class="font-sans" x="42" y="34" font-size="10" font-weight="500" fill="#0B7A52">Receipt
                Generated</text>
            </g>
          </g>

          <!-- the three channels: SMS, WhatsApp, Gmail -->
          <g class="chip opacity-0">
            <circle r="19" fill="#FFFFFF" stroke="#E5E8ED" stroke-width="1.5" />
            <g transform="translate(-9.5 -9.5) scale(.79)" fill="none" stroke="#4A15A4" stroke-width="1.8"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 5h16v11H9l-5 4V5z" />
              <path d="M8 9h8M8 12h5" />
            </g>
          </g>
          <g class="chip opacity-0">
            <circle r="19" fill="#FFFFFF" stroke="#E5E8ED" stroke-width="1.5" />
            <path transform="translate(-10.5 -10.5) scale(.875)" :d="whatsapp.path" :fill="whatsapp.hex" />
          </g>
          <g class="chip opacity-0">
            <circle r="19" fill="#FFFFFF" stroke="#E5E8ED" stroke-width="1.5" />
            <path transform="translate(-10.5 -10.5) scale(.875)" :d="gmail.path" :fill="gmail.hex" />
          </g>
        </svg>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Everything else is Tailwind utilities. Only the soft background glow is kept as CSS. */
.hero {
  background:
    radial-gradient(60% 55% at 82% 38%, #EEE8FA 0%, rgba(238, 232, 250, 0) 72%),
    radial-gradient(40% 40% at 6% 100%, #F3EFFB 0%, rgba(243, 239, 251, 0) 70%),
    #F9FBFF;
}
</style>