<script setup lang="ts">
import { Check, Gift, WalletCards } from 'lucide-vue-next';

// Hero art for the Pricing page: what you see before you send, and what a collected payment costs.
// Sample figures only (a ₦8,432 send, a ₦50,000 payment at 1%). Decorative, so hidden from screen readers.
</script>

<template>
    <div class="art relative mx-auto h-[25rem] w-full max-w-[28rem] max-tablet:h-[24rem] max-tablet:max-w-[22rem]"
        aria-hidden="true">
        <!-- faint rising line behind -->
        <svg class="absolute inset-0 h-full w-full" viewBox="0 0 448 400" fill="none">
            <defs>
                <linearGradient id="riseG" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0" stop-color="#75138C" stop-opacity=".35" />
                    <stop offset="1" stop-color="#4A15A4" stop-opacity=".35" />
                </linearGradient>
            </defs>
            <path d="M36 340 L120 270 L226 304 L330 200 L412 118" stroke="url(#riseG)" stroke-width="2"
                stroke-linecap="round" stroke-dasharray="2 8" />
            <circle cx="36" cy="340" r="8" fill="url(#riseG)" />
            <circle cx="120" cy="270" r="8" fill="url(#riseG)" />
            <circle cx="226" cy="304" r="8" fill="url(#riseG)" />
            <circle cx="330" cy="200" r="8" fill="url(#riseG)" />
            <circle cx="412" cy="118" r="17" fill="url(#riseG)" />
            <path d="M404 118l5 5 9-10" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
        </svg>

        <!-- wallet card: cost shown before sending -->
        <div class="art-in absolute top-0 left-0 w-[72%] rounded-2xl border border-solid border-cloud bg-white p-4 shadow-[0_1px_2px_rgba(11,11,20,.04),0_18px_36px_-18px_rgba(74,21,164,.35)]"
            style="animation-delay: .05s">
            <div class="flex items-center justify-between gap-2">
                <div class="flex items-center gap-2">
                    <span class="grid size-7 place-items-center rounded-lg bg-[#EEE8FA] text-brand-indigo">
                        <WalletCards class="size-4" :stroke-width="2" />
                    </span>
                    <span class="text-[.84rem] font-semibold text-ink">Messaging wallet</span>
                </div>
                <span class="text-[.7rem] text-[#667085]">December batch</span>
            </div>
            <dl
                class="m-0 mt-3 grid grid-cols-[1fr_auto] gap-x-4 gap-y-1.5 border-t border-solid border-[#EEF0F3] pt-3 text-[.78rem]">
                <dt class="text-[#667085]">Balance</dt>
                <dd class="m-0 text-right font-semibold text-ink">₦150,000</dd>
                <dt class="text-[#667085]">Cost of this send (248 bills)</dt>
                <dd class="m-0 text-right font-semibold text-ink">₦8,432</dd>
                <dt class="text-[#667085]">Balance after sending</dt>
                <dd class="m-0 text-right font-semibold text-brand-indigo">₦141,568</dd>
            </dl>
        </div>

        <!-- pilot chip -->
        <div class="art-in art-float absolute top-[8.5rem] right-0 z-10 flex items-center gap-2 rounded-xl border border-solid border-cloud bg-white px-3 py-2 shadow-[0_14px_28px_-14px_rgba(74,21,164,.4)]"
            style="animation-delay: .3s">
            <Gift class="size-5 text-brand-indigo" :stroke-width="2" />
            <div class="leading-tight">
                <div class="text-[.7rem] font-semibold text-ink">Founding pilot</div>
                <div class="text-[.62rem] tracking-wide text-[#667085]">FIRST CYCLE FREE</div>
            </div>
        </div>

        <!-- collections card -->
        <div class="art-in absolute right-0 bottom-0 w-[78%] rounded-2xl border border-solid border-cloud bg-white p-4 shadow-[0_1px_2px_rgba(11,11,20,.04),0_18px_36px_-18px_rgba(74,21,164,.35)]"
            style="animation-delay: .18s">
            <div class="flex items-center justify-between">
                <span class="text-[.66rem] font-bold tracking-wide text-[#667085]">PAYMENT RECEIVED</span>
                <span
                    class="inline-flex items-center gap-1 rounded-full bg-[#E3F4EC] px-2 py-0.5 text-[.68rem] font-semibold text-[#0B7A52]">
                    <Check class="size-3" :stroke-width="3" />Matched
                </span>
            </div>
            <div class="mt-2 font-display text-[1.6rem] leading-none font-bold text-ink">₦50,000</div>
            <div class="mt-1 text-[.76rem] text-[#667085]">Adesuwa Osagie · December service charge</div>
            <dl
                class="m-0 mt-3 grid grid-cols-[1fr_auto] gap-x-4 border-t border-dashed border-[#CBD0D8] pt-3 text-[.78rem]">
                <dt class="text-[#667085]">Collection fee (1%)</dt>
                <dd class="m-0 text-right font-semibold text-ink">₦500</dd>
            </dl>
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