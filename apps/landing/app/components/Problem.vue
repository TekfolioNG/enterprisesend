<script setup lang="ts">
// Problem section (home-page background): three everyday frustrations, each a line drawing that does one small thing.
// The drawings sit on the same dark panel as the "How it works" section, so their strokes, fills and text are reversed for dark.
// The finished drawings are the default markup, so reduced-motion visitors (and no-JS) see them as they are.
// With motion allowed, each card is set to its "before" state on mount and plays once as it scrolls into view.

const cards = [
    { id: 'sms', quote: '“Sorry, I didn’t get the SMS.”', note: 'Nobody can show who actually received the bill, so every late payment turns into a string of phone calls.' },
    { id: 'proof', quote: '“Here’s my payment screenshot.”', note: 'A screenshot can be edited, forwarded or faked, and someone still has to check each one against the bank.' },
    { id: 'account', quote: '“Which account was this paid into?”', note: 'If money lands in the wrong account or hands, nobody can say who paid, who received it or where it went.' }
]

// transfer screenshots: final fan positions, centre one on top
const shots = [
    { x: -46, y: 6, rotation: -11, amount: '₦27,500' },
    { x: 46, y: 6, rotation: 11, amount: '₦72,000' },
    { x: 0, y: 0, rotation: 0, amount: '₦50,000' }
]

type Sel = (q: string) => Element[]
const scenes: Record<string, (tl: gsap.core.Timeline, s: Sel) => void> = {
    sms: (tl, s) => {
        tl.to(s('.bubble'), { scale: 1, duration: 0.5, ease: 'back.out(2.2)' }, 0.4)
            .to(s('.badge'), { scale: 1, duration: 0.35, ease: 'back.out(3)' }, 0.8)
    },
    proof: (tl, s) => {
        s('.shot').forEach((el, k) => tl.to(el, { ...shots[k]!, duration: 0.7, ease: 'power2.out' }, 0.4))
    },
    account: (tl, s) => {
        tl.to(s('.link'), { strokeDashoffset: 0, duration: 0.7, ease: 'power2.inOut' }, 0.5)
            .to(s('.flag'), { scale: 1, duration: 0.35, ease: 'back.out(3)' }, 1.15)
    }
}

const root = ref<HTMLElement | null>(null)
let ctx: gsap.Context | null = null
let io: IntersectionObserver | null = null

onMounted(async () => {
    const el = root.value
    if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const { gsap } = await import('gsap')
    ctx = gsap.context(() => {
        const q = gsap.utils.selector(el)
        const targets = q('.p-head, .p-card, .p-next') as HTMLElement[]   // document order: head, cards, next
        const cardEls = targets.filter((t) => t.classList.contains('p-card'))

        // "before" states
        gsap.set(targets, { autoAlpha: 0, y: 20 })
        gsap.set(q('.bubble'), { scale: 0, svgOrigin: '125 94' })
        gsap.set(q('.badge'), { scale: 0, svgOrigin: '196 56' })
        gsap.set(q('.shot'), { x: 0, y: 0, rotation: 0 })
        gsap.set(q('.link'), { strokeDasharray: 100, strokeDashoffset: 100 })
        gsap.set(q('.flag'), { scale: 0, svgOrigin: '160 100' })

        // cards share a row on wider screens: stagger them. Stacked on phones: each plays as it scrolls in.
        const sameRow = cardEls.length > 1 && cardEls[0]!.offsetTop === cardEls[1]!.offsetTop
        const STEP = 0.8

        const play = (node: HTMLElement) => {
            const i = cardEls.indexOf(node)
            const isNext = node.classList.contains('p-next')
            const delay = !sameRow ? 0 : isNext ? cardEls.length * STEP : Math.max(i, 0) * STEP
            const tl = gsap.timeline({ delay, defaults: { ease: 'power3.out' } })
            tl.to(node, { autoAlpha: 1, y: 0, duration: 0.65 }, 0)
            scenes[node.dataset.scene ?? '']?.(tl, gsap.utils.selector(node))
        }

        if (!('IntersectionObserver' in window)) return targets.forEach(play)
        io = new IntersectionObserver((entries) => {
            entries.forEach((e) => {
                if (!e.isIntersecting) return
                io!.unobserve(e.target)
                ctx!.add(() => play(e.target as HTMLElement))
            })
        }, { threshold: 0.25 })
        targets.forEach((t) => io!.observe(t))
    }, el)
})

onBeforeUnmount(() => { io?.disconnect(); ctx?.revert() })
</script>

<template>
    <section ref="root" class="bg-[#F9FBFF] py-16 max-tablet:py-12">
        <div class="wrap">
            <div class="p-head mb-10 text-center max-tablet:mb-8">
                <h2
                    class="mb-3 font-display text-[length:clamp(1.9rem,3.6vw,3rem)] leading-[1.1] font-bold tracking-[-0.02em] text-ink">
                    Every bill and payment, traceable.
                </h2>
                <p class="mx-auto m-0 max-w-none text-[1.05rem] leading-[1.6] text-[#2D3142]">
                    No manual paper trail. You get a clear, digital record of who billed, who paid and where it went.
                </p>
            </div>

            <div class="grid grid-cols-1 gap-6 tablet:grid-cols-3">
                <article v-for="c in cards" :key="c.id" :data-scene="c.id"
                    class="p-card flex flex-col rounded-2xl border border-solid border-cloud bg-white p-5 shadow-[0_1px_2px_rgba(11,11,20,.04),0_12px_28px_-16px_rgba(74,21,164,.25)]">
                    <!-- illustration panel: same dark as the "How it works" section, so everything inside is reversed for dark -->
                    <div class="mb-5 rounded-xl bg-[#100A26] bg-[image:radial-gradient(70%_60%_at_50%_0%,rgba(74,21,164,.38),transparent_75%)] p-3"
                        aria-hidden="true">
                        <svg viewBox="0 0 320 200" class="block h-auto w-full overflow-visible" focusable="false"
                            fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">

                            <!-- 1. the unread message -->
                            <template v-if="c.id === 'sms'">
                                <rect x="115" y="14" width="90" height="172" rx="16"
                                    class="fill-[#1A1238] stroke-[#B38CF5]" />
                                <path d="M146 26h28" class="stroke-[#B38CF5]" />
                                <text x="160" y="46" text-anchor="middle" font-size="9" font-weight="700"
                                    class="fill-[#C9C2E8] font-sans">SMS</text>
                                <g class="bubble">
                                    <path
                                        d="M127 56h66a8 8 0 0 1 8 8v20a8 8 0 0 1-8 8h-56l-12 10v-10a8 8 0 0 1-6-8V64a8 8 0 0 1 8-8z"
                                        class="fill-[#B38CF5]/15 stroke-[#B38CF5]" />
                                    <path d="M135 72h46M135 82h30" class="stroke-[#B38CF5]" />
                                </g>
                                <g class="badge">
                                    <circle cx="196" cy="56" r="10" class="fill-[#F0525A]" />
                                    <text x="196" y="60" text-anchor="middle" font-size="11" font-weight="700"
                                        class="fill-white font-sans">1</text>
                                </g>
                                <path d="M129 122h50M129 136h62M129 150h38" class="stroke-white/20" />
                            </template>

                            <!-- 2. the screenshots -->
                            <g v-else-if="c.id === 'proof'" transform="translate(160 100)">
                                <g v-for="(s, i) in shots" :key="i" class="shot"
                                    :transform="`translate(${s.x} ${s.y}) rotate(${s.rotation})`">
                                    <rect x="-40" y="-62" width="80" height="124" rx="8"
                                        class="fill-[#1A1238] stroke-[#B38CF5]" />
                                    <path d="M-40 -42h80" stroke-width="2" class="stroke-[#B38CF5]" />
                                    <path d="M-30 -52h26" class="stroke-[#B38CF5]" />
                                    <text x="0" y="-8" text-anchor="middle" font-size="13" font-weight="700"
                                        class="fill-white font-sans">{{
                                            s.amount }}</text>
                                    <path d="M-26 8h52M-26 20h34" class="stroke-white/20" />
                                    <circle cx="0" cy="44" r="8" stroke-width="2" class="stroke-[#4FD9A0]" />
                                    <path d="M-4 44l3 3 5.5-6" stroke-width="2" class="stroke-[#4FD9A0]" />
                                </g>
                            </g>

                            <!-- 3. the school bill and an account that does not match -->
                            <template v-else>
                                <!-- bill -->
                                <rect x="10" y="36" width="108" height="128" rx="8"
                                    class="fill-[#1A1238] stroke-[#B38CF5]" />
                                <text x="22" y="58" font-size="8" font-weight="700"
                                    class="fill-[#C9C2E8] font-sans">BILLED BY</text>
                                <text x="22" y="74" font-size="10.5" font-weight="600"
                                    class="fill-white font-sans">Bright Academy</text>
                                <text x="22" y="104" font-size="14" font-weight="700"
                                    class="fill-white font-sans">₦185,000</text>
                                <text x="22" y="120" font-size="8.5" class="fill-[#C9C2E8] font-sans">School fees, Term
                                    2</text>
                                <path d="M22 138h50" class="stroke-white/20" />
                                <!-- bank account -->
                                <rect x="202" y="36" width="108" height="128" rx="8"
                                    class="fill-[#1A1238] stroke-[#B38CF5]" />
                                <text x="214" y="58" font-size="8" font-weight="700"
                                    class="fill-[#C9C2E8] font-sans">PAID INTO</text>
                                <text x="214" y="74" font-size="10.5" font-weight="600"
                                    class="fill-[#FF8A8F] font-sans">Sunday Martins</text>
                                <text x="214" y="104" font-size="12" font-weight="500"
                                    class="fill-[#C9C2E8] font-sans">•••• 4821</text>
                                <path d="M214 124h60M214 138h40" class="stroke-white/20" />
                                <!-- the link that does not add up -->
                                <path class="link stroke-[#F0525A]" pathLength="100" d="M118 100H202" />
                                <g class="flag">
                                    <circle cx="160" cy="100" r="12" class="fill-[#F0525A]" />
                                    <text x="160" y="105" text-anchor="middle" font-size="15" font-weight="700"
                                        class="fill-white font-sans">≠</text>
                                </g>
                            </template>
                        </svg>
                    </div>
                    <blockquote
                        class="m-0 mb-2 font-display text-[length:clamp(.95rem,1.45vw,1.05rem)] leading-snug font-bold text-ink max-tablet:text-[1.05rem]">
                        {{ c.quote }}</blockquote>
                    <p class="m-0 text-[.95rem] leading-[1.55] text-[#374151]">{{ c.note }}</p>
                </article>
            </div>

            <!-- hand-over to the next section -->
            <div class="p-next mt-12 flex flex-col items-center gap-4 text-center max-tablet:mt-9">
                <p class="m-0 font-display text-[1.15rem] font-bold text-ink">It really doesn't have to be this
                    stressful...
                </p>
                <NuxtLink to="/#how"
                    class="group inline-flex min-h-12 items-center justify-center gap-2 rounded-lg border-[1.5px] border-solid border-[#CBD0D8] bg-white px-6 py-3 text-[.98rem] font-semibold whitespace-nowrap text-brand-indigo no-underline shadow-[0_1px_2px_rgba(11,11,20,.06),0_6px_14px_-8px_rgba(11,11,20,.18)] transition duration-300 ease-[cubic-bezier(.22,1,.36,1)] hover:-translate-y-0.5 hover:border-cta hover:bg-cta hover:text-white hover:shadow-[0_2px_4px_rgba(11,11,20,.06),0_14px_26px_-12px_rgba(74,21,164,.45)] active:translate-y-0 active:scale-[.985] active:duration-100">
                    Here's How with EnterpriseSend
                    <svg class="h-4 w-4 transition-transform duration-300 group-hover:translate-y-0.5"
                        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"
                        stroke-linejoin="round" aria-hidden="true">
                        <path d="M12 5v14M6 13l6 6 6-6" />
                    </svg>
                </NuxtLink>
            </div>
        </div>
    </section>
</template>