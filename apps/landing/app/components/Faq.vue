<script setup lang="ts">
// FAQ (light): the questions are sorted into three short groups so only a few show at a time. On the left, a heading,
// the three groups as a quiet menu, and one closing nudge towards the sandbox; on the right, the answers as a plain
// accordion with the first one open. Answers state what exists today and avoid promises we cannot yet measure.

const groups = [
    {
        id: 'start',
        label: 'Getting started',
        items: [
            {
                q: 'Who can use EnterpriseSend?',
                a: 'Registered organisations that pass our verification: a CAC registration and an authorised contact. It keeps the network trustworthy for everyone who receives a bill or a message.'
            },
            {
                q: 'Can we try it before we commit?',
                a: 'Yes. Create an account and you can explore a sandbox straight away: upload a file, see the checks, preview every message and send a test to your own phone and email. Sending to real customers unlocks once you are verified and the setup fee is paid.'
            },
            {
                q: 'How long until we can send?',
                a: 'The sandbox is instant. After that it depends on our review and on sender-name and WhatsApp approvals, which are outside our control. We give you a date once your application has been reviewed.'
            },
            {
                q: 'How does pricing work?',
                a: 'A one-time setup and verification fee based on your size, a prepaid wallet that pays for messages, and a small commission on payments collected through your links. The Pricing section has the detail.'
            }
        ]
    },
    {
        id: 'sending',
        label: 'Sending',
        items: [
            {
                q: 'Do we need our own SMS or WhatsApp account?',
                a: 'No. We send through approved providers on your behalf, and we set up your sender names as part of onboarding.'
            },
            {
                q: 'What can we send?',
                a: 'Bills, receipts, reminders, notices and invitations to people you already have a relationship with. Unsolicited promotion and misleading messages are not allowed. Every message carries an opt-out, and we stop messaging anyone who asks.'
            },
            {
                q: 'Can you guarantee delivery?',
                a: 'No one honestly can, because the last step belongs to the phone networks and the apps. What we do is send through approved providers and show you the status of each message, by customer and channel, so you know who still needs a follow-up.'
            }
        ]
    },
    {
        id: 'trust',
        label: 'Trust and data',
        items: [
            {
                q: 'How do my customers know a bill is genuine?',
                a: 'Bills come only from verified organisations, under your registered sender name, with a personal payment link. Every bill and every payment names who sent it and who it was meant for.'
            },
            {
                q: 'Do you hold our money?',
                a: 'No. Payments go through a licensed payment provider, not through us. We match each payment to its bill and send the receipt, and we never hold or move customer funds. Your prepaid wallet pays for messages only.'
            },
            {
                q: 'How is personal data handled?',
                a: 'We process your customers\u2019 data only on your instructions, and each client\u2019s data is kept separate. A data processing agreement is part of onboarding, and the platform is designed to support NDPA obligations.'
            }
        ]
    }
]

const group = ref(groups[0]!.id)
const open = ref(0)
const current = computed(() => groups.find((g) => g.id === group.value)!)

const pickGroup = (id: string) => { group.value = id; open.value = 0 }
const toggle = (i: number) => { open.value = open.value === i ? -1 : i }

// arrow keys move between the groups, as a menu of tabs should
const root = ref<HTMLElement | null>(null)
const onTabKey = (e: KeyboardEvent, i: number) => {
    const keys: Record<string, number> = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }
    const step = keys[e.key]
    if (!step) return
    e.preventDefault()
    const n = (i + step + groups.length) % groups.length
    pickGroup(groups[n]!.id)
    nextTick(() => (root.value?.querySelectorAll('[role="tab"]')[n] as HTMLElement | undefined)?.focus())
}

let ctx: any = null
onMounted(async () => {
    const el = root.value
    if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return
    const { gsap } = await import('gsap')
    ctx = gsap.context(() => {
        const q = gsap.utils.selector(el)
        const parts = [...q('.f-left'), ...q('.f-right')] as HTMLElement[]
        gsap.set(parts, { autoAlpha: 0, y: 22 })
        const io = new IntersectionObserver((entries) => {
            if (!entries.some((e) => e.isIntersecting)) return
            io.disconnect()
            ctx!.add(() => gsap.to(parts, { autoAlpha: 1, y: 0, duration: 0.7, stagger: 0.15, ease: 'power3.out' }))
        }, { threshold: 0.2 })
        io.observe(el)
    }, el)
})
onBeforeUnmount(() => { ctx?.revert() })
</script>

<template>
    <section id="faq" ref="root" class="scroll-mt-16 bg-[#F9FBFF] py-16 max-tablet:py-12">
        <div
            class="wrap mx-auto grid max-w-[1040px] items-start gap-10 tablet:grid-cols-[minmax(0,.8fr)_minmax(0,1.3fr)] tablet:gap-[clamp(2.5rem,6vw,5rem)]">

            <div class="f-left">
                <h2
                    class="mb-3 font-display text-[length:clamp(1.9rem,3.4vw,2.7rem)] leading-[1.1] font-bold tracking-[-0.02em] text-ink">
                    Straight answers
                </h2>
                <p class="mb-6 text-[1.02rem] leading-[1.6] text-[#2D3142]">
                    The things organisations ask before they start.
                </p>

                <div role="tablist" aria-label="Question groups" aria-orientation="vertical"
                    class="-mx-5 flex gap-2 overflow-x-auto px-5 pb-1 tablet:mx-0 tablet:flex-col tablet:gap-1 tablet:overflow-visible tablet:px-0 tablet:pb-0">
                    <button v-for="(g, i) in groups" :key="g.id" type="button" role="tab" :id="`faq-tab-${g.id}`"
                        :aria-selected="group === g.id" :aria-controls="`faq-list-${g.id}`"
                        :tabindex="group === g.id ? 0 : -1"
                        class="flex min-h-11 shrink-0 cursor-pointer items-center justify-between gap-6 rounded-full border border-solid px-4 py-2 text-left text-[.95rem] font-semibold whitespace-nowrap transition-colors duration-200 tablet:rounded-xl tablet:border-transparent"
                        :class="group === g.id
                            ? 'border-brand-indigo bg-[#EEE8FA] text-brand-indigo tablet:border-transparent'
                            : 'border-[#CBD0D8] bg-white text-[#374151] hover:border-brand-indigo/55 tablet:bg-transparent tablet:hover:bg-[#EEF1F6]'"
                        @click="pickGroup(g.id)" @keydown="onTabKey($event, i)">
                        {{ g.label }}
                        <span class="text-[.8rem] font-medium opacity-60 max-tablet:hidden">{{ g.items.length }}</span>
                    </button>
                </div>

                <div
                    class="mt-8 rounded-2xl border border-solid border-cloud bg-white p-5 shadow-[0_1px_2px_rgba(11,11,20,.04),0_12px_28px_-16px_rgba(74,21,164,.25)] max-tablet:mt-6">
                    <p class="m-0 mb-1 font-display text-[1.05rem] font-bold text-ink">Still deciding?</p>
                    <p class="m-0 mb-4 text-[.92rem] leading-[1.55] text-[#374151]">
                        Sign up and explore the sandbox first. Upload a sample file and send a test to yourself.
                    </p>
                    <NuxtLink to="/apply"
                        class="inline-flex min-h-11 items-center justify-center rounded-lg border-[1.5px] border-solid border-cta bg-cta px-5 py-2.5 text-[.95rem] font-semibold whitespace-nowrap text-white no-underline transition duration-300 ease-[cubic-bezier(.22,1,.36,1)] hover:-translate-y-0.5 hover:border-cta-dark hover:bg-cta-dark active:translate-y-0 active:scale-[.985] active:duration-100">
                        Start Secure Billing</NuxtLink>
                </div>
            </div>

            <div class="f-right">
                <Transition name="faq-swap" mode="out-in">
                    <ul :key="current.id" role="tabpanel" :id="`faq-list-${current.id}`"
                        :aria-labelledby="`faq-tab-${current.id}`"
                        class="m-0 list-none border-b border-solid border-cloud p-0">
                        <li v-for="(item, i) in current.items" :key="item.q" class="border-t border-solid border-cloud">
                            <h3 class="m-0">
                                <button type="button" :id="`faq-q-${current.id}-${i}`" :aria-expanded="open === i"
                                    :aria-controls="`faq-a-${current.id}-${i}`"
                                    class="group flex min-h-16 w-full cursor-pointer items-center justify-between gap-5 border-0 bg-transparent py-4 text-left"
                                    @click="toggle(i)">
                                    <span
                                        class="font-display text-[1.1rem] leading-snug font-bold transition-colors duration-300 tablet:text-[1.18rem]"
                                        :class="open === i ? 'text-brand-indigo' : 'text-ink group-hover:text-brand-indigo'">{{
                                            item.q }}</span>
                                    <span
                                        class="grid size-7 shrink-0 place-items-center rounded-full border border-solid transition-colors duration-300"
                                        :class="open === i ? 'border-brand-indigo bg-brand-indigo text-white' : 'border-[#CBD0D8] text-[#667085] group-hover:border-brand-indigo/55'">
                                        <svg class="h-3.5 w-3.5 transition-transform duration-300"
                                            :class="open === i ? 'rotate-45' : ''" viewBox="0 0 24 24" fill="none"
                                            stroke="currentColor" stroke-width="2.6" stroke-linecap="round"
                                            stroke-linejoin="round" aria-hidden="true">
                                            <path d="M12 5v14M5 12h14" />
                                        </svg>
                                    </span>
                                </button>
                            </h3>
                            <div :id="`faq-a-${current.id}-${i}`" role="region"
                                :aria-labelledby="`faq-q-${current.id}-${i}`" :aria-hidden="open !== i"
                                class="grid transition-[grid-template-rows] duration-500 ease-[cubic-bezier(.22,1,.36,1)] motion-reduce:transition-none"
                                :class="open === i ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'">
                                <div class="overflow-hidden">
                                    <p class="m-0 max-w-[58ch] pr-12 pb-5 text-[1rem] leading-[1.65] text-[#2D3142]">{{
                                        item.a }}</p>
                                </div>
                            </div>
                        </li>
                    </ul>
                </Transition>
            </div>
        </div>
    </section>
</template>

<style scoped>
/* the list fades and lifts a little when the group changes */
.faq-swap-enter-active,
.faq-swap-leave-active {
    transition: opacity .25s ease, transform .25s ease;
}

.faq-swap-enter-from,
.faq-swap-leave-to {
    opacity: 0;
    transform: translateY(6px);
}

@media (prefers-reduced-motion: reduce) {

    .faq-swap-enter-active,
    .faq-swap-leave-active {
        transition: none;
    }
}
</style>