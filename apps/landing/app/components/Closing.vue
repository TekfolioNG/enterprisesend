<script setup lang="ts">
// Closing call to action (indigo): the four-node brand device from the logo pack, reversed for a coloured ground
// (the same treatment as hero-strip.svg), "loads" in front of the visitor: each ring lights in turn, the line draws on to the
// next, the disc lands and the check is drawn. Then one headline, one line, one button. It plays once as it scrolls into view.
// The finished device is the default markup, so reduced-motion visitors (and no-JS) simply see it complete.

const appUrl = useRuntimeConfig().public.appUrl

const root = ref<HTMLElement | null>(null)
let ctx: any = null
let io: IntersectionObserver | null = null

onMounted(async () => {
    const el = root.value
    if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const { gsap } = await import('gsap')
    ctx = gsap.context(() => {
        const q = gsap.utils.selector(el)
        const mark = q('.c-mark')[0] as HTMLElement
        const words = q('.c-in')

        // "before" states
        gsap.set(q('.c-ring'), { strokeOpacity: 0.25 })
        gsap.set(q('.c-link'), { strokeDashoffset: 1 })
        gsap.set(q('.c-disc'), { scale: 0, svgOrigin: '170 30' })
        gsap.set(q('.c-tick'), { strokeDashoffset: 1 })
        gsap.set(q('.c-pulse'), { autoAlpha: 0, svgOrigin: '170 30' })
        gsap.set(words, { autoAlpha: 0, y: 18 })

        const play = () => {
            const rings = q('.c-ring')
            const links = q('.c-link')
            const tl = gsap.timeline({ defaults: { ease: 'power2.out' } })
            // ring, then the line to the next, three times
            rings.forEach((r, i) => {
                const t = 0.2 + i * 0.5
                tl.to(r, { strokeOpacity: 1, duration: 0.35 }, t)
                tl.to(links[i]!, { strokeDashoffset: 0, duration: i === 2 ? 0.6 : 0.4, ease: 'power1.inOut' }, t + 0.15)
            })
            // the disc lands, the check is drawn, one soft ring goes out
            tl.to(q('.c-disc'), { scale: 1, duration: 0.5, ease: 'back.out(1.8)' }, 1.75)
                .to(q('.c-tick'), { strokeDashoffset: 0, duration: 0.4 }, 2.0)
                .fromTo(q('.c-pulse'), { scale: 1, autoAlpha: 0.55 }, { scale: 1.9, autoAlpha: 0, duration: 1.1 }, 2.05)
            // the words follow the check
            tl.to(words, { autoAlpha: 1, y: 0, duration: 0.7, stagger: 0.12, ease: 'power3.out' }, 1.9)
        }

        if (!('IntersectionObserver' in window)) return play()
        io = new IntersectionObserver((entries) => {
            if (!entries.some((e) => e.isIntersecting)) return
            io!.disconnect()
            ctx!.add(play)
        }, { threshold: 0.45 })
        io.observe(mark)
    }, el)
})

onBeforeUnmount(() => { io?.disconnect(); ctx?.revert() })
</script>

<template>
    <section id="get-started" ref="root" aria-labelledby="closing-title"
        class="scroll-mt-16 overflow-hidden bg-[#100A26] bg-[image:radial-gradient(60%_70%_at_50%_0%,rgba(180,140,255,.28),transparent_72%)] py-20 max-tablet:py-16">
        <div class="wrap flex flex-col items-center text-center">

            <!-- the four-node device, reversed: white on indigo, as in the hero strip -->
            <div class="c-mark mb-10 w-[min(300px,72vw)] tablet:mb-12 tablet:w-[360px]">
                <svg viewBox="0 0 200 60" class="block h-auto w-full overflow-visible" fill="none" aria-hidden="true"
                    focusable="false">
                    <g stroke="#FFFFFF" stroke-width="6">
                        <circle class="c-ring" cx="14" cy="30" r="11" />
                        <path class="c-link" d="M27 30H43" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0" />
                        <circle class="c-ring" cx="56" cy="30" r="11" />
                        <path class="c-link" d="M69 30H85" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0" />
                        <circle class="c-ring" cx="98" cy="30" r="11" />
                        <path class="c-link" d="M111 30H142" pathLength="1" stroke-dasharray="1"
                            stroke-dashoffset="0" />
                    </g>
                    <circle class="c-pulse" cx="170" cy="30" r="30" stroke="#FFFFFF" stroke-width="2" opacity="0" />
                    <circle class="c-disc" cx="170" cy="30" r="30" fill="#FFFFFF" />
                    <path class="c-tick" d="M157 31L166 40L184 20" stroke="#310CA7" stroke-width="7"
                        stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1"
                        stroke-dashoffset="0" />
                </svg>
            </div>

            <h2 id="closing-title"
                class="c-in mb-4 max-w-[18ch] font-display text-[length:clamp(2rem,4.2vw,3.4rem)] leading-[1.08] font-bold tracking-[-0.025em] text-white tablet:max-w-[22ch]">
                Bill with proof. Get paid without the arguments.
            </h2>
            <p class="c-in mx-auto mb-8 max-w-[54ch] text-[1.05rem] leading-[1.6] text-[#DCD3FF]">
                Tell us about your organisation. We review every application ourselves, so the network stays
                trustworthy for everyone who receives a bill.
            </p>

            <div class="c-in flex flex-col items-center gap-4">
                <NuxtLink to="/apply"
                    class="inline-flex min-h-[52px] items-center justify-center rounded-lg border-[1.5px] border-solid border-white bg-white px-7 py-3 text-[1.02rem] font-semibold whitespace-nowrap text-[#310CA7] no-underline shadow-[0_1px_2px_rgba(11,11,20,.2),0_10px_24px_-10px_rgba(11,11,20,.5)] transition duration-300 ease-[cubic-bezier(.22,1,.36,1)] hover:-translate-y-0.5 hover:bg-[#F3EFFB] hover:shadow-[0_2px_4px_rgba(11,11,20,.2),0_16px_30px_-12px_rgba(11,11,20,.6)] active:translate-y-0 active:scale-[.985] active:duration-100">
                    Start Secure Billing</NuxtLink>
                <p class="m-0 text-[.92rem] text-[#C9C2E8]">
                    Explore the sandbox as soon as you sign up.
                    <a :href="`${appUrl}/login`"
                        class="ml-1 font-semibold text-white underline decoration-white/40 underline-offset-4 transition-colors duration-200 hover:decoration-white">Already
                        approved? Sign in</a>
                </p>
            </div>
        </div>
    </section>
</template>