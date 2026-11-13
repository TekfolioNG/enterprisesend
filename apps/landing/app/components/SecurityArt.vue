<script setup lang="ts">
import { BadgeCheck, Check, Link2 } from 'lucide-vue-next';

// Hero art for the Security page: the product's own trust features, drawn in HTML.
// A second person approves a batch, the activity log chains each step with a hash, and the sender is verified.
// A faint chain of linked nodes (the logo's motif) sits behind. Decorative only, so hidden from screen readers.
const log = [
    { t: '09:12', pre: 'Billing file uploaded by ', name: 'Ada O.', h: 'a41f…9c' },
    { t: '09:31', pre: 'Approved by ', name: 'Funke A.', h: '7c0e…2d' },
    { t: '09:40', pre: 'Bills sent to 248 customers', name: '', h: 'e93b…51' }
]
</script>

<template>
    <div class="art relative mx-auto h-[25rem] w-full max-w-[28rem] max-tablet:h-[24rem] max-tablet:max-w-[22rem]"
        aria-hidden="true">
        <!-- faint chain of linked nodes -->
        <svg class="absolute inset-0 h-full w-full" viewBox="0 0 448 400" fill="none">
            <defs>
                <linearGradient id="chainG" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0" stop-color="#75138C" stop-opacity=".35" />
                    <stop offset="1" stop-color="#4A15A4" stop-opacity=".35" />
                </linearGradient>
            </defs>
            <path d="M36 340 L120 262 L226 300 L330 196 L412 118" stroke="url(#chainG)" stroke-width="2"
                stroke-linecap="round" stroke-dasharray="2 8" />
            <circle cx="36" cy="340" r="8" fill="url(#chainG)" />
            <circle cx="120" cy="262" r="8" fill="url(#chainG)" />
            <circle cx="226" cy="300" r="8" fill="url(#chainG)" />
            <circle cx="330" cy="196" r="8" fill="url(#chainG)" />
            <circle cx="412" cy="118" r="17" fill="url(#chainG)" />
            <path d="M404 118l5 5 9-10" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
        </svg>

        <!-- approval card -->
        <div class="art-in absolute top-0 left-0 w-[70%] rounded-2xl border border-solid border-cloud bg-white p-4 shadow-[0_1px_2px_rgba(11,11,20,.04),0_18px_36px_-18px_rgba(74,21,164,.35)]"
            style="animation-delay: .05s">
            <div class="flex items-start justify-between gap-2">
                <div class="min-w-0">
                    <div class="truncate text-[.84rem] font-semibold text-ink">December service charge</div>
                    <div class="text-[.72rem] text-[#667085]">248 bills · ₦12.4M</div>
                </div>
                <span
                    class="inline-flex shrink-0 items-center gap-1 rounded-full bg-[#E3F4EC] px-2 py-0.5 text-[.68rem] font-semibold text-[#0B7A52]">
                    <Check class="size-3" :stroke-width="3" />Approved
                </span>
            </div>
            <div class="mt-3 grid gap-2 border-t border-solid border-[#EEF0F3] pt-3 text-[.76rem]">
                <div class="flex items-center gap-2">
                    <span
                        class="grid size-6 place-items-center rounded-full bg-[#EEE8FA] text-[.62rem] font-bold text-brand-indigo">AO</span>
                    <span class="text-[#667085]">Prepared by <b class="font-semibold text-ink">Ada O.</b></span>
                </div>
                <div class="flex items-center gap-2">
                    <span
                        class="grid size-6 place-items-center rounded-full bg-brand-indigo text-[.62rem] font-bold text-white">FA</span>
                    <span class="text-[#667085]">Approved by <b class="font-semibold text-ink">Funke A.</b> ·
                        09:31</span>
                </div>
            </div>
        </div>

        <!-- verified sender chip -->
        <div class="art-in art-float absolute top-[5.5rem] right-0 z-10 flex items-center gap-2 rounded-xl border border-solid border-cloud bg-white px-3 py-2 shadow-[0_14px_28px_-14px_rgba(74,21,164,.4)]"
            style="animation-delay: .3s">
            <BadgeCheck class="size-5 text-brand-indigo" :stroke-width="2" />
            <div class="leading-tight">
                <div class="text-[.7rem] font-semibold text-ink">Sender verified</div>
                <div class="text-[.62rem] tracking-wide text-[#667085]">SILVERWOOD</div>
            </div>
        </div>

        <!-- activity log -->
        <div class="art-in absolute right-0 bottom-0 w-[78%] rounded-2xl border border-solid border-cloud bg-white shadow-[0_1px_2px_rgba(11,11,20,.04),0_18px_36px_-18px_rgba(74,21,164,.35)]"
            style="animation-delay: .18s">
            <div class="flex items-center gap-1.5 border-b border-solid border-cloud px-4 py-2.5">
                <Link2 class="size-3.5 text-[#667085]" :stroke-width="2.2" />
                <span class="text-[.66rem] font-bold tracking-wide text-[#667085]">ACTIVITY LOG</span>
            </div>
            <ul class="m-0 list-none space-y-2.5 px-4 py-3">
                <li v-for="l in log" :key="l.t" class="flex items-center gap-2.5 text-[.74rem] leading-[1.3]">
                    <span class="w-9 shrink-0 font-mono text-[.68rem] text-[#667085]">{{ l.t }}</span>
                    <span class="min-w-0 flex-1" :class="l.name ? 'text-[#667085]' : 'text-ink'">{{ l.pre }}<b
                            v-if="l.name" class="font-semibold text-ink">{{ l.name }}</b></span>
                    <span class="shrink-0 rounded bg-[#F2F4F7] px-1.5 py-0.5 font-mono text-[.62rem] text-[#667085]">{{
                        l.h }}</span>
                </li>
            </ul>
            <div
                class="mx-4 mb-3 inline-flex items-center gap-1.5 rounded-full bg-[#EEE8FA] px-2.5 py-1 text-[.7rem] font-semibold text-brand-indigo">
                <Check class="size-3" :stroke-width="3" />Integrity check passed
            </div>
        </div>
    </div>
</template>

<style scoped>
@media (prefers-reduced-motion: no-preference) {
    .art-in {
        animation: art-in .7s cubic-bezier(.22, 1, .36, 1) both;
    }

    .art-float {
        animation: art-in .7s cubic-bezier(.22, 1, .36, 1) both, art-float 5s ease-in-out 1.2s infinite;
    }
}

@keyframes art-in {
    from {
        opacity: 0;
        transform: translateY(12px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes art-float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-5px);
    }
}
</style>