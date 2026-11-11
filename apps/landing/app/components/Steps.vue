<script setup lang="ts">
import { gmail, whatsapp } from '~/utils/brandIcons'

// Steps (light): from billing file to receipt, four stages down a vertical rail. Each stage carries a small "real-looking"
// mock of the thing it describes (a spreadsheet, the three message previews, a send table, a receipt and activity log),
// drawn in HTML so it stays crisp and compact. No second-person approval: guardrails do the checking instead.
// The finished state is the default markup, so reduced-motion visitors (and no-JS) see every stage complete.

const steps = [
    {
        id: 'upload',
        title: 'Upload your billing file',
        text: 'Fill in our Excel template and upload it. Every row is checked, and mistakes such as a wrong phone number are shown row by row, before anything can be sent.'
    },
    {
        id: 'preview',
        title: 'Preview before you send',
        text: 'See exactly how each bill will look on SMS, WhatsApp and email, with the real names and amounts filled in. Send a test to your own phone and inbox first. Nothing reaches a customer until you confirm.',
        tags: ['Errors block sending', 'Cost shown up front', 'Test to yourself first']
    },
    {
        id: 'send',
        title: 'Messages go out on every channel',
        text: 'Each customer gets the bill by SMS, WhatsApp and email, with a personal payment link. Opt-outs are respected, and you can see the status of every message.'
    },
    {
        id: 'match',
        title: 'Payment is matched and receipted',
        text: 'When a customer pays, the payment is matched to the right bill and a receipt is sent to both your organization and the recipient.'

    }
]

// the spreadsheet in step 1 (row 3 is the bad one)
const sheetCols = ['', 'A', 'B', 'C', 'D']
const sheetRows = [
    { n: 1, head: true, bad: -1, cells: ['Account', 'Customer', 'Phone', 'Amount'] },
    { n: 2, head: false, bad: -1, cells: ['A-014', 'Adesuwa Osagie', '2348012345678', '₦50,000'] },
    { n: 3, head: false, bad: 2, cells: ['A-015', 'Tunde Bello', '0801 23', '₦50,000'] },
    { n: 4, head: false, bad: -1, cells: ['A-016', 'Ibrahim Abubakar', '2348098765432', '₦75,000'] }
]

// the send table in step 3
const sendRows = [
    { name: 'Adesuwa Osagie', s: ['sent', 'Sent'], w: ['sent', 'Sent'], e: ['sent', 'Sent'] },
    { name: 'Tunde Bello', s: ['sent', 'Sent'], w: ['opt', 'Opted out'], e: ['sent', 'Sent'] },
    { name: 'Ibrahim Abubakar', s: ['sent', 'Sent'], w: ['sent', 'Sent'], e: ['none', 'No email'] }
]
const pillCls: Record<string, string> = {
    sent: 'bg-[#E3F4EC] text-[#0B7A52]',
    opt: 'bg-[#FFF3D6] text-[#8A5A00]',
    none: 'bg-[#F2F4F7] text-[#98A2B3]'
}

const logRows = [
    { t: '09:12', text: 'Billing file uploaded' },
    { t: '09:40', text: 'Bills sent to 248 customers' },
    { t: '10:42', text: 'Payment of ₦50,000 matched to A-014' }
]

// shared look for the little "app windows"
const card = 'overflow-hidden rounded-xl border border-solid border-cloud bg-white shadow-[0_1px_2px_rgba(11,11,20,.04),0_12px_28px_-16px_rgba(74,21,164,.25)]'

// step 2: the three previews. Clicking a tab takes over; otherwise they cycle gently while in view.
type Tab = 'sms' | 'whatsapp' | 'email'
const tabs: { id: Tab; label: string }[] = [
    { id: 'sms', label: 'SMS' },
    { id: 'whatsapp', label: 'WhatsApp' },
    { id: 'email', label: 'Email' }
]
const tab = ref<Tab>('sms')
let timer: ReturnType<typeof setInterval> | null = null
const stopCycle = () => { if (timer) { clearInterval(timer); timer = null } }
const startCycle = () => {
    stopCycle()
    timer = setInterval(() => {
        const order = tabs.map((t) => t.id)
        tab.value = order[(order.indexOf(tab.value) + 1) % order.length]!
    }, 3200)
}
const pick = (t: Tab) => { stopCycle(); tab.value = t }

const root = ref<HTMLElement | null>(null)
let ctx: any = null
let io: IntersectionObserver | null = null

onMounted(async () => {
    const el = root.value
    if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const { gsap } = await import('gsap')
    ctx = gsap.context(() => {
        const q = gsap.utils.selector(el)
        const head = q('.s-head')[0] as HTMLElement
        const stages = q('.stage') as HTMLElement[]

        // "before" states
        gsap.set(head, { autoAlpha: 0, y: 18 })
        gsap.set(q('.node'), { scale: 0 })
        gsap.set(q('.seg-fill'), { scaleY: 0, transformOrigin: '50% 0%' })
        gsap.set(q('.s-text, .s-mock'), { autoAlpha: 0, y: 18 })
        gsap.set(q('.bad-hl'), { scaleX: 0, transformOrigin: '0% 50%' })
        gsap.set(q('.flag'), { autoAlpha: 0, y: 8 })
        gsap.set(q('.pv-chip'), { autoAlpha: 0, y: 6 })
        gsap.set(q('.bar-fill'), { scaleX: 0, transformOrigin: '0% 50%' })
        gsap.set(q('.pill-s'), { scale: 0.6, autoAlpha: 0 })
        gsap.set(q('.log-row'), { autoAlpha: 0, x: -8 })
        gsap.set(q('.verify'), { scale: 0, transformOrigin: '50% 50%' })

        const scenes: Record<string, (tl: any, s: (sel: string) => Element[]) => void> = {
            upload: (tl, s) => {
                tl.to(s('.bad-hl'), { scaleX: 1, duration: 0.4 }, 0.8)
                    .to(s('.flag'), { autoAlpha: 1, y: 0, duration: 0.4 }, 1.05)
            },
            preview: (tl, s) => {
                tl.to(s('.pv-chip'), { autoAlpha: 1, y: 0, duration: 0.4, stagger: 0.12 }, 0.6)
                    .call(startCycle, [], 1.6)
            },
            send: (tl, s) => {
                const n = { v: 0 }
                const count = s('.count')[0] as HTMLElement | undefined
                tl.to(s('.bar-fill'), { scaleX: 1, duration: 1.2, ease: 'power1.inOut' }, 0.5)
                    .to(n, { v: 248, duration: 1.2, ease: 'power1.inOut', onUpdate: () => { if (count) count.textContent = `${Math.round(n.v)} of 248 sent` } }, 0.5)
                    .to(s('.pill-s'), { scale: 1, autoAlpha: 1, duration: 0.3, stagger: 0.07, ease: 'back.out(2.4)' }, 0.7)
            },
            match: (tl, s) => {
                tl.to(s('.log-row'), { autoAlpha: 1, x: 0, duration: 0.4, stagger: 0.16 }, 0.7)
                    .to(s('.verify'), { scale: 1, duration: 0.4, ease: 'back.out(2.4)' }, 1.3)
            }
        }

        const play = (node: HTMLElement) => {
            if (node === head) return gsap.to(head, { autoAlpha: 1, y: 0, duration: 0.7, ease: 'power3.out' })
            const s = gsap.utils.selector(node)
            const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })
            tl.to(s('.node'), { scale: 1, duration: 0.45, ease: 'back.out(1.8)' }, 0)
                .to(s('.seg-fill'), { scaleY: 1, duration: 0.8, ease: 'power1.inOut' }, 0.3)
                .to(s('.s-text'), { autoAlpha: 1, y: 0, duration: 0.6 }, 0.1)
                .to(s('.s-mock'), { autoAlpha: 1, y: 0, duration: 0.7 }, 0.25)
            scenes[node.dataset.stage ?? '']?.(tl, s)
        }

        const targets = [head, ...stages]
        if (!('IntersectionObserver' in window)) return targets.forEach(play)
        io = new IntersectionObserver((entries) => {
            entries.forEach((e) => {
                if (!e.isIntersecting) return
                io!.unobserve(e.target)
                ctx!.add(() => play(e.target as HTMLElement))
            })
        }, { threshold: 0.3 })
        targets.forEach((t) => io!.observe(t))
    }, el)
})

onBeforeUnmount(() => { stopCycle(); io?.disconnect(); ctx?.revert() })
</script>

<template>
    <section id="steps" ref="root" class="scroll-mt-16 bg-[#F9FBFF] py-16 max-tablet:py-12">
        <div class="wrap">
            <div class="s-head mb-12 text-center max-tablet:mb-10">
                <h2
                    class="mb-3 font-display text-[length:clamp(1.9rem,3.6vw,3rem)] leading-[1.1] font-bold tracking-[-0.02em] text-ink">
                    From billing file to receipt in four steps
                </h2>
                <p class="mx-auto m-0 max-w-none text-[1.05rem] leading-[1.6] text-[#2D3142]">
                    Built-in guardrails check your work at every step, so you stay in control without the paperwork.
                </p>
            </div>

            <ol class="m-0 mx-auto grid max-w-[1000px] list-none grid-cols-1 p-0">
                <li v-for="(s, i) in steps" :key="s.id" :data-stage="s.id"
                    class="stage grid grid-cols-[2.25rem_minmax(0,1fr)] gap-x-4 tablet:grid-cols-[3rem_minmax(0,1fr)] tablet:gap-x-8">
                    <!-- rail: numbered node, then a line that fills down to the next one -->
                    <div class="relative">
                        <span
                            class="node absolute top-0 left-0 flex size-9 items-center justify-center rounded-full bg-brand-indigo font-display text-[1rem] font-bold text-white shadow-[0_0_0_4px_rgba(74,21,164,.12)] tablet:size-12 tablet:text-[1.2rem]">
                            <template v-if="i < steps.length - 1">{{ i + 1 }}</template>
                            <svg v-else class="h-5 w-5 tablet:h-6 tablet:w-6" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"
                                aria-hidden="true">
                                <path d="M5.5 12.5l4.5 4.5 8.5-9.5" />
                            </svg>
                        </span>
                        <div v-if="i < steps.length - 1"
                            class="absolute top-11 bottom-1 left-[17px] w-0.5 overflow-hidden rounded-full bg-[#DAD3EE] tablet:top-[3.75rem] tablet:left-[23px]">
                            <div class="seg-fill h-full w-full bg-brand-indigo"></div>
                        </div>
                    </div>

                    <div
                        class="grid items-center gap-6 pb-14 max-tablet:pb-10 tablet:grid-cols-[minmax(0,.8fr)_minmax(0,1.2fr)] tablet:gap-10">
                        <div class="s-text">
                            <h3
                                class="mb-2 font-display text-[1.3rem] leading-snug font-bold text-ink tablet:text-[1.45rem]">
                                {{ s.title }}</h3>
                            <p class="m-0 text-[1rem] leading-[1.6] text-[#2D3142]">{{ s.text }}</p>
                            <ul v-if="s.tags" class="m-0 mt-4 flex list-none flex-wrap gap-2 p-0">
                                <li v-for="t in s.tags" :key="t"
                                    class="inline-flex items-center gap-1.5 rounded-full bg-[#EEE8FA] px-3 py-1 text-[.82rem] font-semibold text-brand-indigo">
                                    <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                        stroke-width="3" stroke-linecap="round" stroke-linejoin="round"
                                        aria-hidden="true">
                                        <path d="M5.5 12.5l4.5 4.5 8.5-9.5" />
                                    </svg>
                                    {{ t }}
                                </li>
                            </ul>
                        </div>

                        <!-- ============ 1. the spreadsheet ============ -->
                        <div v-if="s.id === 'upload'" class="s-mock" aria-hidden="true">
                            <div :class="card">
                                <div class="flex items-center gap-2 bg-[#217346] px-3 py-2 text-white">
                                    <span
                                        class="grid size-5 place-items-center rounded-[4px] bg-white text-[.7rem] font-extrabold text-[#217346]">X</span>
                                    <span class="text-[.78rem] font-semibold">december_billing.xlsx</span>
                                </div>
                                <div
                                    class="flex items-center gap-2 border-b border-solid border-[#E1E4EA] bg-[#F3F3F3] px-2 py-1 text-[.7rem] text-[#444]">
                                    <span
                                        class="w-10 rounded-[3px] border border-solid border-[#D0D4DA] bg-white px-1 text-center">C3</span>
                                    <span class="font-semibold text-[#217346] italic">fx</span>
                                    <span class="truncate">0801 23</span>
                                </div>
                                <div
                                    class="grid grid-cols-[1.6rem_.8fr_1.2fr_1.45fr_.9fr] text-[.72rem] leading-none text-[#1F2937]">
                                    <div v-for="(c, k) in sheetCols" :key="'h' + k"
                                        class="border-r border-b border-solid border-[#E1E4EA] bg-[#F3F3F3] py-[.4rem] text-center text-[.66rem] font-semibold text-[#666]">
                                        {{ c }}</div>
                                    <template v-for="r in sheetRows" :key="r.n">
                                        <div
                                            class="border-r border-b border-solid border-[#E1E4EA] bg-[#F3F3F3] py-[.5rem] text-center text-[.66rem] text-[#666]">
                                            {{ r.n }}</div>
                                        <div v-for="(cell, k) in r.cells" :key="r.n + '-' + k"
                                            class="relative truncate border-r border-b border-solid border-[#E1E4EA] px-1.5 py-[.5rem]"
                                            :class="[r.head ? 'bg-[#EAF4EE] font-bold' : '', k === 3 && !r.head ? 'text-right' : '']">
                                            <span v-if="r.bad === k"
                                                class="bad-hl absolute inset-0 bg-[#FDECEC] shadow-[inset_0_0_0_2px_#E5484D]"></span>
                                            <span class="relative">{{ cell }}</span>
                                        </div>
                                    </template>
                                </div>
                                <div class="flex items-center bg-[#F3F3F3] px-2 pt-1 text-[.7rem]">
                                    <span
                                        class="border-b-2 border-solid border-[#217346] bg-white px-2.5 py-0.5 font-semibold text-[#217346]">Sheet1</span>
                                </div>
                            </div>
                            <div
                                class="flag mt-3 flex items-start gap-2.5 rounded-lg border border-solid border-[#F5C2C4] bg-[#FDECEC] px-3 py-2.5 text-[.84rem] leading-[1.45] text-[#9B1C1F]">
                                <span
                                    class="mt-px grid size-4 shrink-0 place-items-center rounded-full bg-[#E5484D] text-[.65rem] font-bold text-white">!</span>
                                <span><b>Row 3:</b> phone number must start with 234 and have 13 digits. Fix it and
                                    upload again. Nothing is sent.</span>
                            </div>
                        </div>

                        <!-- ============ 2. preview on every channel ============ -->
                        <div v-else-if="s.id === 'preview'" class="s-mock">
                            <div :class="card">
                                <div aria-hidden="true"
                                    class="flex flex-wrap items-center gap-x-4 gap-y-1.5 border-b border-solid border-cloud px-3.5 py-2.5 text-[.78rem]">
                                    <span class="pv-chip font-semibold text-ink">December service charge</span>
                                    <span class="pv-chip text-[#667085]">248 bills · ₦12.4M</span>
                                    <span
                                        class="pv-chip inline-flex items-center gap-1 rounded-full bg-[#E3F4EC] px-2 py-0.5 font-semibold text-[#0B7A52]">
                                        <svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                            stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M5.5 12.5l4.5 4.5 8.5-9.5" />
                                        </svg>Checks passed</span>
                                    <span class="pv-chip ml-auto text-[#667085]">Est. cost ₦8,432</span>
                                </div>

                                <div role="group" aria-label="Preview channel" class="flex gap-1.5 px-3.5 pt-3">
                                    <button v-for="t in tabs" :key="t.id" type="button" :aria-pressed="tab === t.id"
                                        class="inline-flex min-h-8 cursor-pointer items-center gap-1.5 rounded-full border border-solid px-3 text-[.8rem] font-semibold transition-colors duration-200"
                                        :class="tab === t.id ? 'border-brand-indigo bg-brand-indigo text-white' : 'border-[#CBD0D8] bg-white text-[#374151] hover:border-brand-indigo/55'"
                                        @click="pick(t.id)">
                                        <svg v-if="t.id === 'sms'" class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none"
                                            stroke="currentColor" stroke-width="2.2" stroke-linecap="round"
                                            stroke-linejoin="round" aria-hidden="true">
                                            <path d="M4 5h16v11H9l-5 4V5z" />
                                        </svg>
                                        <svg v-else-if="t.id === 'whatsapp'" class="h-3.5 w-3.5" viewBox="0 0 24 24"
                                            aria-hidden="true">
                                            <path :d="whatsapp.path" :fill="whatsapp.hex" />
                                        </svg>
                                        <svg v-else class="h-3.5 w-3.5" viewBox="0 0 24 24" aria-hidden="true">
                                            <path :d="gmail.path" :fill="gmail.hex" />
                                        </svg>
                                        {{ t.label }}
                                    </button>
                                </div>

                                <!-- the three previews share one fixed-height stage so nothing jumps when they switch -->
                                <div aria-hidden="true" class="relative m-3.5 mb-0 h-[14.5rem]">
                                    <!-- SMS -->
                                    <div class="absolute inset-0 rounded-lg bg-[#F2F2F7] p-3 transition-opacity duration-300"
                                        :class="tab === 'sms' ? 'opacity-100' : 'pointer-events-none opacity-0'">
                                        <div
                                            class="text-center text-[.65rem] leading-[1.4] font-semibold text-[#8E8E93]">
                                            SILVERWOOD<br /><span class="font-normal">Text Message · Today 09:00</span>
                                        </div>
                                        <div
                                            class="mt-3 max-w-[90%] rounded-2xl rounded-bl-md bg-[#E9E9EB] px-3 py-2 text-[.8rem] leading-[1.45] text-[#111]">
                                            Silverwood Estate: Dear Adaeze, your December service charge of ₦50,000 is
                                            due 31 Dec. Pay securely:
                                            <span class="text-[#0A64D8] underline">enterprisesend.com/p/7Kq2</span>
                                            Reply STOP to opt out
                                        </div>
                                        <div class="mt-2 text-[.68rem] text-[#8E8E93]">Sender name: SILVERWOOD</div>
                                    </div>
                                    <!-- WhatsApp -->
                                    <div class="absolute inset-0 rounded-lg bg-[#EFE7DD] p-3 transition-opacity duration-300"
                                        :class="tab === 'whatsapp' ? 'opacity-100' : 'pointer-events-none opacity-0'">
                                        <div
                                            class="max-w-[90%] rounded-lg rounded-tl-none bg-white p-2.5 text-[.8rem] leading-[1.45] text-[#111] shadow-[0_1px_1px_rgba(11,20,26,.13)]">
                                            <div class="mb-1 flex items-center gap-1 font-semibold text-[#128C7E]">
                                                Silverwood Estate
                                                <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="#128C7E">
                                                    <path
                                                        d="M12 2l2.4 1.7 2.9-.1 1 2.7 2.4 1.7-.9 2.8.9 2.8-2.4 1.7-1 2.7-2.9-.1L12 22l-2.4-1.7-2.9.1-1-2.7-2.4-1.7.9-2.8-.9-2.8 2.4-1.7 1-2.7 2.9.1L12 2z" />
                                                    <path d="M8 12.2l2.7 2.7L16 9.4" fill="none" stroke="#fff"
                                                        stroke-width="2" stroke-linecap="round"
                                                        stroke-linejoin="round" />
                                                </svg>
                                            </div>
                                            Dear Adaeze, your December service charge of <b>₦50,000</b> is due 31 Dec.
                                            Tap below to pay securely.
                                            <div class="mt-1 text-right text-[.62rem] text-[#8696A0]">09:00</div>
                                            <div
                                                class="mt-1.5 border-t border-solid border-[#E9EDEF] pt-2 text-center font-semibold text-[#027EB5]">
                                                ↗ Pay securely</div>
                                        </div>
                                    </div>
                                    <!-- Email -->
                                    <div class="absolute inset-0 overflow-hidden rounded-lg border border-solid border-cloud bg-white text-[.78rem] transition-opacity duration-300"
                                        :class="tab === 'email' ? 'opacity-100' : 'pointer-events-none opacity-0'">
                                        <div
                                            class="flex items-center gap-2.5 border-b border-solid border-cloud px-3 py-2">
                                            <span
                                                class="grid size-7 shrink-0 place-items-center rounded-full bg-brand-indigo text-[.75rem] font-bold text-white">S</span>
                                            <div class="min-w-0 leading-[1.3]">
                                                <div class="truncate font-semibold text-ink">Your December service
                                                    charge
                                                </div>
                                                <div class="truncate text-[.68rem] text-[#667085]">Silverwood Estate ·
                                                    to
                                                    Adaeze Ishola</div>
                                            </div>
                                        </div>
                                        <div class="px-3 py-3 text-center">
                                            <div class="text-[.72rem] text-[#667085]">December service charge</div>
                                            <div class="font-display text-[1.6rem] leading-tight font-bold text-ink">
                                                ₦50,000</div>
                                            <div class="mb-2.5 text-[.72rem] text-[#667085]">Due 31 Dec</div>
                                            <span
                                                class="inline-block rounded-md bg-cta px-4 py-1.5 text-[.8rem] font-semibold text-white">Pay
                                                securely</span>
                                            <div class="mt-2.5 text-[.62rem] text-[#98A2B3]">Reply STOP to opt out</div>
                                        </div>
                                    </div>
                                </div>

                                <div aria-hidden="true" class="flex items-center gap-2 px-3.5 py-3">
                                    <span
                                        class="rounded-lg border-[1.5px] border-solid border-[#CBD0D8] bg-white px-3 py-1.5 text-[.8rem] font-semibold text-brand-indigo">Send
                                        test to me</span>
                                    <span
                                        class="ml-auto rounded-lg bg-cta px-3.5 py-1.5 text-[.8rem] font-semibold text-white">Confirm
                                        and send</span>
                                </div>
                            </div>
                        </div>

                        <!-- ============ 3. sent on every channel ============ -->
                        <div v-else-if="s.id === 'send'" class="s-mock" aria-hidden="true">
                            <div :class="card">
                                <div class="border-b border-solid border-cloud px-3.5 py-3">
                                    <div class="mb-2 flex items-center justify-between text-[.8rem]">
                                        <span class="font-semibold text-ink">Sending December bills</span>
                                        <span class="count font-semibold text-[#0B7A52]">248 of 248 sent</span>
                                    </div>
                                    <div class="h-2 overflow-hidden rounded-full bg-[#E5E8ED]">
                                        <div class="bar-fill h-full w-full rounded-full bg-[#0B7A52]"></div>
                                    </div>
                                </div>
                                <div
                                    class="grid grid-cols-[minmax(0,1.1fr)_repeat(3,minmax(0,1fr))] items-center gap-x-2 gap-y-0 px-3.5 py-1 text-[.78rem]">
                                    <div class="py-2 text-[.68rem] font-bold tracking-wide text-[#667085]">CUSTOMER
                                    </div>
                                    <div class="flex items-center gap-1 py-2 text-[.68rem] font-bold text-[#667085]">
                                        <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="#4A15A4"
                                            stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M4 5h16v11H9l-5 4V5z" />
                                        </svg>SMS
                                    </div>
                                    <div class="flex items-center gap-1 py-2 text-[.68rem] font-bold text-[#667085]">
                                        <svg class="h-3.5 w-3.5" viewBox="0 0 24 24">
                                            <path :d="whatsapp.path" :fill="whatsapp.hex" />
                                        </svg>WhatsApp
                                    </div>
                                    <div class="flex items-center gap-1 py-2 text-[.68rem] font-bold text-[#667085]">
                                        <svg class="h-3.5 w-3.5" viewBox="0 0 24 24">
                                            <path :d="gmail.path" :fill="gmail.hex" />
                                        </svg>Email
                                    </div>
                                    <template v-for="r in sendRows" :key="r.name">
                                        <div
                                            class="truncate border-t border-solid border-[#EEF0F3] py-2.5 font-semibold text-ink">
                                            {{ r.name }}</div>
                                        <div v-for="(c, k) in [r.s, r.w, r.e]" :key="r.name + k"
                                            class="border-t border-solid border-[#EEF0F3] py-2">
                                            <span
                                                class="pill-s inline-block rounded-full px-2 py-0.5 text-[.7rem] font-semibold"
                                                :class="pillCls[c[0]!]">{{ c[1] }}</span>
                                        </div>
                                    </template>
                                </div>
                                <div
                                    class="border-t border-solid border-cloud bg-[#F9FBFF] px-3.5 py-2.5 text-[.78rem] text-[#667085]">
                                    Every message carries the customer's own payment link.</div>
                            </div>
                        </div>

                        <!-- ============ 4. receipt and activity log ============ -->
                        <div v-else class="s-mock" aria-hidden="true">
                            <div class="grid gap-4 tablet:grid-cols-2">
                                <div :class="card">
                                    <div class="p-4">
                                        <div class="mb-3 flex items-center justify-between">
                                            <span
                                                class="text-[.7rem] font-bold tracking-wide text-[#667085]">RECEIPT</span>
                                            <span
                                                class="inline-flex items-center gap-1 rounded-full bg-[#E3F4EC] px-2 py-0.5 text-[.7rem] font-semibold text-[#0B7A52]">
                                                <svg class="h-3 w-3" viewBox="0 0 24 24" fill="none"
                                                    stroke="currentColor" stroke-width="3.2" stroke-linecap="round"
                                                    stroke-linejoin="round">
                                                    <path d="M5.5 12.5l4.5 4.5 8.5-9.5" />
                                                </svg>Matched to bill</span>
                                        </div>
                                        <div class="font-display text-[1.7rem] leading-none font-bold text-ink">₦50,000
                                        </div>
                                        <div class="mt-1 text-[.8rem] text-[#374151]">Adesuwa Osagie · December service
                                            charge
                                        </div>
                                        <dl class="m-0 mt-3 grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-[.76rem]">
                                            <dt class="text-[#667085]">Billed by</dt>
                                            <dd class="m-0 text-right font-semibold text-ink">Silverwood Estate</dd>
                                            <dt class="text-[#667085]">Bill</dt>
                                            <dd class="m-0 text-right font-semibold text-ink">A-014</dd>
                                            <dt class="text-[#667085]">Paid</dt>
                                            <dd class="m-0 text-right font-semibold text-ink">10:42 today</dd>
                                        </dl>
                                    </div>
                                    <div
                                        class="flex items-center gap-2 border-t border-dashed border-[#CBD0D8] bg-[#F9FBFF] px-4 py-2.5 text-[.74rem] text-[#667085]">
                                        <svg class="h-3.5 w-3.5 shrink-0" viewBox="0 0 24 24">
                                            <path :d="gmail.path" :fill="gmail.hex" />
                                        </svg>
                                        <svg class="h-3.5 w-3.5 shrink-0" viewBox="0 0 24 24">
                                            <path :d="whatsapp.path" :fill="whatsapp.hex" />
                                        </svg>
                                        Receipt sent
                                    </div>
                                </div>

                                <div :class="card">
                                    <div
                                        class="flex items-center justify-between border-b border-solid border-cloud px-4 py-3">
                                        <span class="text-[.7rem] font-bold tracking-wide text-[#667085]">ACTIVITY
                                            LOG</span>
                                    </div>
                                    <ul class="m-0 list-none space-y-3 p-4">
                                        <li v-for="l in logRows" :key="l.t"
                                            class="log-row flex gap-3 text-[.78rem] leading-[1.4]">
                                            <span class="w-10 shrink-0 font-mono text-[.72rem] text-[#667085]">{{ l.t
                                                }}</span>
                                            <span class="text-ink">{{ l.text }}</span>
                                        </li>
                                    </ul>
                                    <div
                                        class="verify mx-4 mb-4 inline-flex items-center gap-1.5 rounded-full bg-[#EEE8FA] px-3 py-1 text-[.74rem] font-semibold text-brand-indigo">
                                        <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                            stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6l7-3z" />
                                            <path d="M9 12l2.2 2.2L15.5 10" />
                                        </svg>Integrity check passed
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
            </ol>
        </div>
    </section>
</template>