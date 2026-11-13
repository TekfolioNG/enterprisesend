<script setup lang="ts">
import { BadgeCheck, BellOff, CloudCog, FileLock2, Fingerprint, ReceiptText, UserCheck, Vault } from 'lucide-vue-next';
import { site } from '~/utils/config';
useHead({ title: 'Security: EnterpriseSend' })

// Edit the wording here. Lines marked CONFIRM describe controls that must be live before launch.
const items = [
    {
        title: 'Isolated by design',
        text: 'Every organization works in its own protected space. Users, files, bills and payments are never visible to another client.',
        icon: Vault
    },
    {
        title: 'Strong sign-in',
        text: 'Two-step verification protects every account, and each person sees only what their role requires.',
        icon: Fingerprint
    },
    {
        title: 'Two-person approval',
        text: 'A second person from your organization approves each batch before a single message leaves. Small teams can approve their own batches, and every self-approval is recorded.',
        icon: UserCheck
    },
    {
        // CONFIRM: file sealing is not built yet.
        title: 'Tamper-evident records',
        text: 'Uploads, approvals, sends and payments are written to an activity log chained with cryptographic hashes, so any change is detected. Approved billing files are sealed the same way.',
        icon: FileLock2
    },
    {
        // CONFIRM: sender-name registration and CAC verification are not built yet.
        title: 'Verified senders',
        text: 'Only organizations that pass our verification, including CAC registration and an authorized contact, can send. Registered sender names show customers exactly who a bill is from.',
        icon: BadgeCheck
    },
    {
        title: 'Payments that reconcile',
        text: 'Each payment is matched to its bill by a unique reference, and a repeated payment notification is never counted twice. Card and bank details are handled by our payment partner, never stored by us.',
        icon: ReceiptText
    },
    {
        // CONFIRM: STOP handling is not built yet.
        title: 'Opt-outs respected',
        text: 'Recipients can reply STOP on any channel. Opted-out contacts are suppressed from every future send.',
        icon: BellOff
    },
    {
        // CONFIRM: penetration test, DPA and NDPC registration are not done yet.
        title: 'Infrastructure and compliance',
        text: 'Hosted on Google Cloud in Belgium, with encryption in transit and at rest and secrets held in a managed vault. Independent penetration tests run before launch and every year after. We design for the Nigeria Data Protection Act, and a data processing agreement is available to every client.',
        icon: CloudCog
    }
]
</script>

<template>
    <PageHero kicker="Security" title="Built so every bill can be trusted"
        lead="Billing data is personal data. EnterpriseSend is designed so that no bill is sent without review, no payment is counted twice, and every action leaves a record.">
        <template #art>
            <SecurityArt />
        </template>
    </PageHero>

    <section class="bg-white py-14 max-tablet:py-10">
        <div class="wrap">
            <ul class="m-0 mx-auto grid max-w-[1040px] list-none gap-5 p-0 tablet:grid-cols-2">
                <li v-for="it in items" :key="it.title"
                    class="sec-card rounded-2xl border border-solid border-cloud bg-white p-6 shadow-[0_1px_2px_rgba(11,11,20,.04),0_12px_28px_-18px_rgba(74,21,164,.25)]">
                    <span
                        class="sec-tile mb-5 grid size-14 place-items-center rounded-2xl bg-[#EEE8FA] text-brand-indigo">
                        <component :is="it.icon" class="sec-icon" :size="28" :stroke-width="1.7" aria-hidden="true" />
                    </span>
                    <h2 class="mb-2 font-display text-[1.1rem] leading-snug font-bold text-ink">{{ it.title }}</h2>
                    <p class="m-0 text-[.95rem] leading-[1.65] text-[#2D3142]">{{ it.text }}</p>
                </li>
            </ul>

            <div
                class="mx-auto mt-8 flex max-w-[1040px] flex-wrap items-center justify-between gap-4 rounded-2xl bg-[#F4F0FC] p-6 tablet:p-8">
                <p class="m-0 max-w-[52ch] text-[.98rem] leading-[1.6] text-[#2D3142]">
                    Running a security review or due-diligence request? We will answer it in writing.</p>
                <a :href="`mailto:${site.contactEmail}`"
                    class="inline-flex min-h-11 items-center rounded-lg bg-brand-indigo px-5 text-[.95rem] font-semibold text-white no-underline transition duration-300 hover:-translate-y-0.5">
                    Contact security</a>
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