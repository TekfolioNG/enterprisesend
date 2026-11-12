<script setup lang="ts">
// How it works (dark, short): the four safeguards are the four steps. Each one's marker is the EnterpriseSend mark
// (a check in a disc, reversed for dark). The markers light up in turn as the section scrolls into view, joined by a line that fills.
// On wider screens the markers are centred over their text; on phones they sit left with a vertical line.
// The "4" in the heading is stamped into place, then gives a soft pulse now and then.
// The finished state is the default markup, so reduced-motion visitors (and no-JS) see every step complete.
const steps = [
    { title: 'Registered senders only', text: 'Bills come only from verified organisations, so an impersonator cannot send one.' },
    { title: 'Verified sender/receiver', text: 'Every bill and every payment names who sent it and who it was meant for.' },
    { title: 'One source of truth', text: 'The billing sheet, the messages and the payments live in one secure cloud record.' },
    { title: 'Traceable end to end', text: 'Every payment is matched to its original bill and written to a tamper-evident activity log.' }
]

const root = ref<HTMLElement | null>(null)
let ctx: any = null
let io: IntersectionObserver | null = null

onMounted(async () => {
    const el = root.value
    if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const { gsap } = await import('gsap')
    ctx = gsap.context(() => {
        const q = gsap.utils.selector(el)
        const head = q('.h-head')[0] as HTMLElement
        const items = q('.step') as HTMLElement[]
        // four across on wider screens (stagger them), one column on phones (each lights as it scrolls in)
        const horizontal = items.length > 1 && items[0]!.offsetTop === items[1]!.offsetTop

        // "before" states
        gsap.set(head, { autoAlpha: 0, y: 18 })
        gsap.set(q('.stamp-in'), { autoAlpha: 0, scale: 0.4 })
        gsap.set(q('.copy'), { autoAlpha: 0, y: 14 })
        gsap.set(q('.disc'), { scale: 0, transformOrigin: '50% 50%' })
        gsap.set(q('.tick'), { strokeDashoffset: 1 })
        gsap.set(q('.seg-fill'), horizontal ? { scaleX: 0, transformOrigin: '0% 50%' } : { scaleY: 0, transformOrigin: '50% 0%' })

        const play = (node: HTMLElement) => {
            if (node === head) {
                return gsap.timeline({ defaults: { ease: 'power3.out' } })
                    .to(head, { autoAlpha: 1, y: 0, duration: 0.7 }, 0)
                    // the disc pops in; the rings then pulse on their own (CSS, below)
                    .to(q('.stamp-in'), { autoAlpha: 1, scale: 1, duration: 0.5, ease: 'back.out(2)' }, 0.5)
            }
            const s = gsap.utils.selector(node)
            const delay = horizontal ? items.indexOf(node) * 0.6 : 0
            const grow = horizontal ? { scaleX: 1 } : { scaleY: 1 }
            gsap.timeline({ delay, defaults: { ease: 'power3.out' } })
                .to(s('.disc'), { scale: 1, duration: 0.45, ease: 'back.out(1.8)' }, 0)
                .to(s('.tick'), { strokeDashoffset: 0, duration: 0.35 }, 0.2)
                .fromTo(s('.pulse'), { scale: 1, autoAlpha: 0.5 }, { scale: 1.7, autoAlpha: 0, duration: 0.7 }, 0.05)
                .to(s('.copy'), { autoAlpha: 1, y: 0, duration: 0.6 }, 0.1)
                .to(s('.seg-fill'), { ...grow, duration: 0.5, ease: 'power1.inOut' }, 0.35)
        }

        const targets = [head, ...items]
        if (!('IntersectionObserver' in window)) return targets.forEach(play)
        io = new IntersectionObserver((entries) => {
            entries.forEach((e) => {
                if (!e.isIntersecting) return
                io!.unobserve(e.target)
                ctx!.add(() => play(e.target as HTMLElement))
            })
        }, { threshold: 0.4 })
        targets.forEach((t) => io!.observe(t))
    }, el)
})

onBeforeUnmount(() => { io?.disconnect(); ctx?.revert() })
</script>

<template>
    <section id="how" ref="root"
        class="scroll-mt-16 bg-[#100A26] bg-[image:radial-gradient(60%_55%_at_50%_0%,rgba(74,21,164,.38),transparent_72%)] py-16 max-tablet:py-12">
        <div class="mx-auto w-[min(1000px,100%-3rem)]">
            <div class="h-head mb-12 text-center max-tablet:mb-10">
                <h2
                    class="mb-3 font-display text-[length:clamp(1.9rem,3.6vw,3rem)] leading-[1.1] font-bold tracking-[-0.02em] text-white">
                    <!-- the "4": a white disc, the number in the section's deep purple, with two slow pulsing rings -->
                    <span
                        class="stamp relative mr-[.35em] inline-flex size-[1.5em] items-center justify-center align-[-.22em]">
                        <span class="stamp-in relative flex size-full items-center justify-center">
                            <span
                                class="ring-loop absolute inset-0 rounded-full border-2 border-solid border-[#B38CF5] opacity-0"></span>
                            <span
                                class="ring-loop ring-late absolute inset-0 rounded-full border-2 border-solid border-[#B38CF5] opacity-0"></span>
                            <span
                                class="absolute inset-0 rounded-full bg-white shadow-[0_0_0_4px_rgba(179,140,245,.25),0_10px_28px_-8px_rgba(179,140,245,.6)]"></span>
                            <span class="relative text-[1.1em] leading-none font-black text-[#100A26]">4</span>
                        </span>
                    </span>safeguards for every transaction
                </h2>
                <p class="mx-auto m-0 max-w-none text-[1.05rem] leading-[1.6] text-[#C9C2E8]">
                    Each one adds to a single trusted, traceable record.
                </p>
            </div>

            <ol class="m-0 grid list-none grid-cols-1 gap-8 p-0 tablet:grid-cols-4">
                <li v-for="(s, i) in steps" :key="s.title"
                    class="step relative pl-12 tablet:pl-0 tablet:pt-14 tablet:text-center">
                    <!-- the mark, reversed for dark: a check in a disc (left on phones, centred over its text on wider screens) -->
                    <svg viewBox="0 0 56 56" aria-hidden="true" fill="none" stroke-linecap="round"
                        stroke-linejoin="round"
                        class="absolute top-0 left-0 block h-9 w-9 overflow-visible tablet:left-1/2 tablet:h-10 tablet:w-10 tablet:-translate-x-1/2">
                        <circle cx="28" cy="28" r="26" stroke-width="3" class="stroke-white/20" />
                        <path d="M17.5 29l7.5 7.5L39.5 20" stroke-width="4.5" class="stroke-white/20" />
                        <circle class="pulse stroke-[#B38CF5]" cx="28" cy="28" r="26" stroke-width="2" opacity="0" />
                        <circle class="disc fill-[#B38CF5]" cx="28" cy="28" r="27" />
                        <path class="tick stroke-[#100A26]" d="M17.5 29l7.5 7.5L39.5 20" stroke-width="4.5"
                            pathLength="1" stroke-dasharray="1" stroke-dashoffset="0" />
                    </svg>

                    <!-- line to the next mark: down on phones; across on wider screens, from this mark's centre-right edge to the next mark's left edge -->
                    <div v-if="i < steps.length - 1"
                        class="absolute top-11 -bottom-6 left-[17px] w-0.5 overflow-hidden rounded-full bg-white/15 tablet:top-[19px] tablet:bottom-auto tablet:left-[calc(50%+1.75rem)] tablet:h-0.5 tablet:w-[calc(100%-1.5rem)]">
                        <div class="seg-fill h-full w-full bg-[#B38CF5]"></div>
                    </div>

                    <div class="copy">
                        <h3 class="mb-1.5 font-display text-[1.1rem] leading-snug font-bold text-white">{{ s.title }}
                        </h3>
                        <p class="m-0 text-[.95rem] leading-[1.6] text-[#C9C2E8]">{{ s.text }}</p>
                    </div>
                </li>
            </ol>
        </div>
    </section>
</template>

<style scoped>
/* Two slow rings ripple out from the "4", the second half a cycle behind. Off for reduced motion (the disc is then a still mark). */
@keyframes ring-pulse {
    0% {
        transform: scale(1);
        opacity: .6;
    }

    75%,
    100% {
        transform: scale(1.9);
        opacity: 0;
    }
}

@media (prefers-reduced-motion: no-preference) {
    .ring-loop {
        animation: ring-pulse 4s ease-out 1.2s infinite;
    }

    .ring-late {
        animation-delay: 3.2s;
    }
}
</style>