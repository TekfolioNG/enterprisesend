<script setup lang="ts">
// Who it's for (white): heading and one line on top, then three portrait photos that start as a single stack with the
// estate on top, centred. As the section scrolls into view the two cards behind it slide out left and right, slowly,
// tied to the scroll position (scrubbed, with a little lag so it glides). Captions fade in once the cards have cleared.
// A quiet row of tags below names the other kinds of organisation this suits.
// The finished row is the default markup, so reduced-motion visitors (and no-JS) simply see the row.

const FRONT = 1   // the middle card (estates) sits on top of the stack

const items = [
    {
        id: 'clinics',
        title: 'Clinics and practices',
        text: 'Invoices, follow-up payments and appointment notices.',
        img: '/home/clinics-es.webp',
        alt: 'A doctor in a white coat pressing a stamp onto a paper form at a clinic desk',
        pos: 'object-[58%_60%]'
    },
    {
        id: 'estates',
        title: 'Estates and property managers',
        text: 'Service charges, levies and power tokens.',
        img: '/home/estates-es.webp',
        alt: 'A gated residential entrance with a keypad intercom and letterboxes set into a timber-clad wall',
        pos: 'object-[38%_50%]'
    },
    {
        id: 'utilities',
        title: 'Utilities and fintechs',
        text: 'High-volume bills and receipts with a full audit trail.',
        img: '/home/utils-es.webp',
        alt: 'An engineer in a hard hat and high-visibility jacket checking a control panel while holding a tablet',
        pos: 'object-[62%_40%]'
    }
]

const also = ['Schools', 'Faith groups', 'Corporate bodies', 'Associations', 'Event organisers']

const root = ref<HTMLElement | null>(null)
let ctx: any = null

onMounted(async () => {
    const el = root.value
    if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const [{ gsap }, { ScrollTrigger }] = await Promise.all([import('gsap'), import('gsap/ScrollTrigger')])
    gsap.registerPlugin(ScrollTrigger)

    ctx = gsap.context(() => {
        const q = gsap.utils.selector(el)
        const head = q('.wf-head')[0] as HTMLElement
        const stage = q('.wf-stage')[0] as HTMLElement
        const cards = q('.wf-card') as HTMLElement[]
        const front = cards[FRONT]!

        // layout positions (offset*) ignore transforms, so the stack stays centred on the front card at any width
        const cx = (c: HTMLElement) => c.offsetLeft + c.offsetWidth / 2
        const cy = (c: HTMLElement) => c.offsetTop + c.offsetHeight / 2

        gsap.from(head, { autoAlpha: 0, y: 20, duration: 0.7, ease: 'power3.out', scrollTrigger: { trigger: head, start: 'top 88%', once: true } })
        gsap.from(q('.wf-also'), { autoAlpha: 0, y: 12, duration: 0.7, ease: 'power3.out', scrollTrigger: { trigger: q('.wf-also')[0]!, start: 'top 95%', once: true } })

        // a long scroll distance and a lagging scrub, so the cards glide instead of snapping out
        const tl = gsap.timeline({
            scrollTrigger: { trigger: stage, start: 'top 92%', end: 'top 8%', scrub: 1.6, invalidateOnRefresh: true }
        })

        cards.forEach((c, i) => {
            const d = i - FRONT   // -1 (left), 0 (front), 1 (right)
            gsap.set(c, { zIndex: i === FRONT ? 10 : 8 })
            tl.fromTo(c,
                {
                    x: () => cx(front) - cx(c) + d * 26,
                    y: () => cy(front) - cy(c) + Math.abs(d) * 8,
                    rotation: d * 3.5,
                    scale: 1 - Math.abs(d) * 0.05
                },
                { x: 0, y: 0, rotation: 0, scale: 1, duration: 1, ease: 'sine.inOut' }, 0.08)
        })

        // captions wait until the cards are nearly out
        tl.fromTo(q('.wf-cap'), { autoAlpha: 0, y: 10 }, { autoAlpha: 1, y: 0, duration: 0.3, ease: 'power2.out' }, 0.8)
    }, el)
})

onBeforeUnmount(() => { ctx?.revert() })
</script>

<template>
    <section id="who-for" ref="root" class="scroll-mt-16 overflow-x-clip bg-white py-16 max-tablet:py-12">
        <div class="wrap">
            <div class="wf-head mx-auto mb-10 max-w-[760px] text-center max-tablet:mb-8">
                <h2
                    class="mb-3 font-display text-[length:clamp(1.9rem,3.6vw,3rem)] leading-[1.1] font-bold tracking-[-0.02em] text-ink">
                    Made for any organisation that bills many people
                </h2>
                <p class="mx-auto m-0 max-w-none text-[1.05rem] leading-[1.6] text-[#2D3142]">
                    Estates, clinics and utilities are only the start. If you bill a sizeable number of people
                    weekly, monthly, quarterly, yearly or only now and then, whatever your rhythm,
                    <b class="font-bold text-brand-indigo">EnterpriseSend</b> fits.
                </p>
            </div>

            <ul
                class="wf-stage relative m-0 mx-auto grid max-w-[1040px] list-none grid-cols-2 gap-3 p-0 tablet:grid-cols-3 tablet:gap-5">
                <li v-for="(a, i) in items" :key="a.id"
                    class="wf-card relative aspect-[5/6] overflow-hidden rounded-[20px] bg-[#100A26] shadow-[0_1px_2px_rgba(11,11,20,.08),0_18px_36px_-18px_rgba(11,11,20,.45)] will-change-transform max-tablet:rounded-2xl"
                    :class="i === FRONT ? 'max-tablet:order-first max-tablet:col-span-2 max-tablet:aspect-[16/10]' : 'max-tablet:aspect-[4/5]'">
                    <img :src="a.img" :alt="a.alt" loading="lazy" decoding="async"
                        class="absolute inset-0 h-full w-full object-cover" :class="a.pos">
                    <div class="absolute inset-0 bg-[image:linear-gradient(to_top,rgba(11,11,20,.78),rgba(11,11,20,.2)_42%,transparent_62%)]"
                        aria-hidden="true"></div>
                    <div class="wf-cap absolute right-0 bottom-0 left-0 p-4 max-tablet:p-3">
                        <h3
                            class="m-0 mb-1 font-display text-[1.05rem] leading-tight font-bold text-white max-tablet:text-[.95rem]">
                            {{ a.title }}</h3>
                        <p class="m-0 text-[.82rem] leading-[1.45] text-white/80"
                            :class="i === FRONT ? '' : 'max-tablet:hidden'">{{ a.text }}</p>
                    </div>
                </li>
            </ul>

            <div class="wf-also mt-8 flex flex-wrap items-center justify-center gap-2 max-tablet:mt-6">
                <span class="mr-1 text-[.92rem] text-[#667085]">Also a fit for</span>
                <span v-for="t in also" :key="t"
                    class="rounded-full border border-solid border-cloud bg-[#F9FBFF] px-3.5 py-1.5 text-[.88rem] font-semibold text-[#374151]">{{
                        t }}</span>
            </div>
        </div>
    </section>
</template>