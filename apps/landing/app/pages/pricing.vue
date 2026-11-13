<script setup lang="ts">
import { BadgeCheck, Check, Gift, HandCoins, WalletCards } from 'lucide-vue-next'
import { site } from '~/utils/config'
useHead({ title: 'Pricing: EnterpriseSend' })

// Edit the figures here. Setup fee: decide the standard amount, then replace 'Quoted by size'.
const price = {
    walletMarkup: '20%',
    commission: '1%',
    cap: '₦5,000',
    setup: 'Quoted by size',
    enterpriseFrom: '₦1,000,000'
}
const plans = [
    {
        kicker: 'Messaging wallet',
        figure: `Cost + ${price.walletMarkup}`,
        icon: WalletCards,
        text: `Top up a prepaid wallet. Each SMS, WhatsApp or email is charged at the provider’s cost plus ${price.walletMarkup}, and you see the total before you send.`
    },
    {
        kicker: 'Collections',
        figure: price.commission,
        icon: HandCoins,
        text: `On each successful payment made through a payment link, capped at ${price.cap} per payment so large fees stay fair.`
    },
    {
        kicker: 'Setup and verification',
        figure: price.setup,
        icon: BadgeCheck,
        text: `We verify every organization before it can send. Enterprise and NGO setups, including integrations, start from ${price.enterpriseFrom}.`
    }
]
const included = [
    'Row-by-row file checks',
    'Preview on SMS, WhatsApp and email',
    'Two-person approval and a full activity log',
    'Test sends to your own phone and inbox',
    'Personal payment links on every bill',
    'Automatic payment matching and receipts'
]
</script>

<template>
    <PageHero kicker="Pricing" title="Pay for what you send and collect"
        lead="No licence fee per user. You fund a messaging wallet, and pay a small share only on payments collected through your links.">
        <template #art>
            <PricingArt />
        </template>
    </PageHero>

    <section class="bg-white py-14 max-tablet:py-10">
        <div class="wrap">
            <ul class="m-0 mx-auto grid max-w-[1040px] list-none gap-5 p-0 tablet:grid-cols-3">
                <li v-for="p in plans" :key="p.kicker"
                    class="sec-card group rounded-2xl border border-solid border-cloud bg-white p-7 shadow-[0_1px_2px_rgba(11,11,20,.04),0_12px_28px_-18px_rgba(74,21,164,.25)]">
                    <span
                        class="sec-tile mb-5 grid size-14 place-items-center rounded-2xl bg-[#EEE8FA] text-brand-indigo">
                        <component :is="p.icon" class="sec-icon" :size="28" :stroke-width="1.7" aria-hidden="true" />
                    </span>
                    <p class="mb-2 font-display text-[.8rem] font-bold tracking-[.12em] text-brand-indigo uppercase">{{
                        p.kicker }}</p>
                    <p class="m-0 font-display text-[1.9rem] leading-[1.1] font-bold text-ink">{{ p.figure }}</p>
                    <p class="mt-3 mb-0 text-[.95rem] leading-[1.65] text-[#2D3142]">{{ p.text }}</p>
                </li>
            </ul>

            <div
                class="mx-auto mt-6 flex max-w-[1040px] items-start gap-5 rounded-2xl bg-[#2A1066] p-7 text-white tablet:p-9">
                <span
                    class="grid size-14 shrink-0 place-items-center rounded-2xl bg-white/10 text-white max-tablet:hidden">
                    <Gift :size="28" :stroke-width="1.7" aria-hidden="true" />
                </span>
                <div>
                    <p class="mb-2 font-display text-[.8rem] font-bold tracking-[.12em] text-[#DCD3FF] uppercase">
                        Founding
                        pilot offer</p>
                    <h2 class="mb-2 font-display text-[1.5rem] leading-tight font-bold text-white">Your first billing
                        cycle,
                        on us</h2>
                    <p class="m-0 max-w-[62ch] text-[1rem] leading-[1.65] text-[#DCD3FF]">Our first three clients pay no
                        setup fee and no collection commission for their first full billing cycle, with wallet usage
                        only.
                        In return, we ask to publish a short case study.</p>
                </div>
            </div>

            <div class="mx-auto mt-10 max-w-[1040px]">
                <h2 class="mb-4 font-display text-[1.2rem] font-bold text-ink">Included with every account</h2>
                <ul class="m-0 grid list-none gap-x-8 gap-y-3 p-0 tablet:grid-cols-2">
                    <li v-for="i in included" :key="i"
                        class="flex items-start gap-2.5 text-[.98rem] leading-[1.5] text-[#2D3142]">
                        <Check class="mt-0.5 size-4 shrink-0 text-brand-indigo" :stroke-width="3" aria-hidden="true" />
                        {{ i
                        }}
                    </li>
                </ul>
            </div>

            <div class="mx-auto mt-10 flex max-w-[1040px] flex-wrap items-center gap-3">
                <NuxtLink to="/apply" class="btn">Start Secure Billing</NuxtLink>
                <a :href="`mailto:${site.contactEmail}`" class="btn-text">Talk to us about pricing</a>
            </div>
        </div>
    </section>
</template>

<style scoped>
/* Hover: the card lifts, the icon tile grows, and the icon plays a short "tada" once. Off for reduced motion. */
.sec-card {
    transition: transform .35s cubic-bezier(.22, 1, .36, 1), box-shadow .35s;
}

.sec-tile {
    transition: transform .35s cubic-bezier(.22, 1, .36, 1), background-color .35s;
}

@keyframes tada {
    0% {
        transform: scale(1) rotate(0)
    }

    10%,
    20% {
        transform: scale(.92) rotate(-4deg)
    }

    30%,
    50%,
    70% {
        transform: scale(1.12) rotate(4deg)
    }

    40%,
    60% {
        transform: scale(1.12) rotate(-4deg)
    }

    100% {
        transform: scale(1) rotate(0)
    }
}

@media (hover: hover) and (prefers-reduced-motion: no-preference) {
    .sec-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 2px 4px rgba(11, 11, 20, .05), 0 22px 40px -22px rgba(74, 21, 164, .4);
    }

    .sec-card:hover .sec-tile {
        transform: scale(1.08);
        background-color: #E2D8F8;
    }

    .sec-card:hover .sec-icon {
        animation: tada .9s ease-in-out 1;
    }
}
</style>