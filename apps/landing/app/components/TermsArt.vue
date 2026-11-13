<script setup lang="ts">
import { Check, FileText, Scale } from 'lucide-vue-next';

// Hero art for the Terms page: a clear agreement with the main commitments ticked off.
// Sample content only. Decorative, so hidden from screen readers.
const points = ['Verified organization', 'Lawful basis for every recipient', 'Fees agreed before sending', 'Approval before every batch']
</script>

<template>
    <div class="art relative mx-auto h-[25rem] w-full max-w-[28rem] max-tablet:h-[24rem] max-tablet:max-w-[22rem]"
        aria-hidden="true">
        <svg class="absolute inset-0 h-full w-full" viewBox="0 0 448 400" fill="none">
            <defs>
                <linearGradient id="termsG" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0" stop-color="#75138C" stop-opacity=".35" />
                    <stop offset="1" stop-color="#4A15A4" stop-opacity=".35" />
                </linearGradient>
            </defs>
            <path d="M36 340 L120 270 L226 304 L330 200 L412 118" stroke="url(#termsG)" stroke-width="2"
                stroke-linecap="round" stroke-dasharray="2 8" />
            <circle cx="36" cy="340" r="8" fill="url(#termsG)" />
            <circle cx="120" cy="270" r="8" fill="url(#termsG)" />
            <circle cx="226" cy="304" r="8" fill="url(#termsG)" />
            <circle cx="330" cy="200" r="8" fill="url(#termsG)" />
            <circle cx="412" cy="118" r="17" fill="url(#termsG)" />
            <path d="M404 118l5 5 9-10" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
        </svg>

        <div class="art-in absolute top-0 left-0 w-[76%] rounded-2xl border border-solid border-cloud bg-white p-4 shadow-[0_1px_2px_rgba(11,11,20,.04),0_18px_36px_-18px_rgba(74,21,164,.35)]"
            style="animation-delay: .05s">
            <div class="flex items-center gap-2.5">
                <span class="grid size-8 place-items-center rounded-lg bg-[#EEE8FA] text-brand-indigo">
                    <FileText class="size-[1.1rem]" :stroke-width="2" />
                </span>
                <div class="leading-tight">
                    <div class="text-[.84rem] font-semibold text-ink">Service agreement</div>
                    <div class="text-[.72rem] text-[#667085]">Between EnterpriseSend and your organization</div>
                </div>
            </div>
            <ul class="m-0 mt-3 list-none space-y-2 border-t border-solid border-[#EEF0F3] pt-3">
                <li v-for="p in points" :key="p" class="flex items-center gap-2 text-[.76rem] text-ink">
                    <span class="grid size-4 shrink-0 place-items-center rounded-full bg-[#E3F4EC] text-[#0B7A52]">
                        <Check class="size-2.5" :stroke-width="3.5" />
                    </span>{{ p }}
                </li>
            </ul>
        </div>

        <div class="art-in art-float absolute top-[10.5rem] right-0 z-10 flex items-center gap-2 rounded-xl border border-solid border-cloud bg-white px-3 py-2 shadow-[0_14px_28px_-14px_rgba(74,21,164,.4)]"
            style="animation-delay: .3s">
            <Scale class="size-5 text-brand-indigo" :stroke-width="2" />
            <div class="leading-tight">
                <div class="text-[.7rem] font-semibold text-ink">Nigerian law</div>
                <div class="text-[.62rem] tracking-wide text-[#667085]">GOVERNING LAW</div>
            </div>
        </div>

        <div class="art-in absolute right-0 bottom-0 w-[74%] rounded-2xl border border-solid border-cloud bg-white p-4 shadow-[0_1px_2px_rgba(11,11,20,.04),0_18px_36px_-18px_rgba(74,21,164,.35)]"
            style="animation-delay: .18s">
            <div class="flex items-center justify-between">
                <span class="text-[.66rem] font-bold tracking-wide text-[#667085]">STATUS</span>
                <span
                    class="inline-flex items-center gap-1 rounded-full bg-[#E3F4EC] px-2 py-0.5 text-[.68rem] font-semibold text-[#0B7A52]">
                    <Check class="size-3" :stroke-width="3" />Accepted
                </span>
            </div>
            <div class="mt-2 font-display text-[1.15rem] leading-tight font-bold text-ink">Terms of service</div>
            <div class="mt-1 text-[.74rem] text-[#667085]">Recorded in your activity log</div>
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