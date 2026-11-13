<script setup lang="ts">
import type { Component } from 'vue';
import { site } from '~/utils/config';

// Shared layout for the Privacy and Terms pages: a quiet header, a sticky contents list and numbered sections.
// Text in [square brackets] is a placeholder to edit; it is highlighted so none is missed before launch.
type Block = string | { ul: string[] }
defineProps<{
    kicker: string
    title: string
    lead: string
    updated: string
    sections: { id: string; title: string; blocks: Block[] }[]
    highlights?: { title: string; text: string; icon: Component }[]
}>()

const parts = (t: string) => t.split(/(\[[^\]]+\])/g).filter(Boolean)
const isPh = (s: string) => /^\[[^\]]+\]$/.test(s)
</script>

<template>
    <PageHero :kicker="kicker" :title="title" :lead="lead">
        <template v-if="$slots.art" #art>
            <slot name="art" />
        </template>
        <p class="m-0 mt-5 text-[.85rem] font-medium text-[#667085]">
            Last updated:
            <template v-for="(p, i) in parts(updated)" :key="i">
                <mark v-if="isPh(p)" class="rounded bg-[#FFF3D6] px-1 text-[#8A5A00]">{{ p }}</mark><template v-else>{{
                    p }}</template>
            </template>
        </p>
    </PageHero>

    <section class="bg-white py-14 max-tablet:py-10">
        <div class="wrap">
            <ul v-if="highlights?.length"
                class="m-0 mx-auto mb-14 grid max-w-[1040px] list-none gap-5 p-0 tablet:grid-cols-3">
                <li v-for="h in highlights" :key="h.title"
                    class="sec-card group rounded-2xl border border-solid border-cloud bg-white p-6 shadow-[0_1px_2px_rgba(11,11,20,.04),0_12px_28px_-18px_rgba(74,21,164,.25)]">
                    <span
                        class="sec-tile mb-4 grid size-12 place-items-center rounded-2xl bg-[#EEE8FA] text-brand-indigo">
                        <component :is="h.icon" class="sec-icon" :size="24" :stroke-width="1.75" aria-hidden="true" />
                    </span>
                    <h2 class="mb-1.5 font-display text-[1.05rem] leading-snug font-bold text-ink">{{ h.title }}</h2>
                    <p class="m-0 text-[.92rem] leading-[1.6] text-[#2D3142]">{{ h.text }}</p>
                </li>
            </ul>

            <div class="mx-auto grid max-w-[1040px] gap-12 tablet:grid-cols-[210px_minmax(0,1fr)]">
                <nav aria-label="On this page" class="max-tablet:hidden">
                    <ol class="sticky top-24 m-0 list-none space-y-1 p-0 text-[.88rem]">
                        <li v-for="(s, i) in sections" :key="s.id">
                            <a :href="`#${s.id}`"
                                class="block rounded-md px-2.5 py-1.5 leading-snug text-[#667085] no-underline transition-colors duration-200 hover:bg-[#F4F0FC] hover:text-brand-indigo">
                                {{ i + 1 }}. {{ s.title }}</a>
                        </li>
                    </ol>
                </nav>

                <div class="max-w-[68ch]">
                    <div class="border-t border-solid border-cloud">
                        <article v-for="(s, i) in sections" :id="s.id" :key="s.id"
                            class="scroll-mt-24 border-b border-solid border-cloud px-4 py-8 tablet:px-5">
                            <h2 class="mb-3 font-display text-[1.2rem] leading-snug font-bold text-ink">{{ i + 1 }}. {{
                                s.title }}</h2>
                            <template v-for="(b, k) in s.blocks" :key="k">
                                <ul v-if="typeof b !== 'string'"
                                    class="m-0 mb-3 list-disc space-y-1.5 pl-5 text-[.98rem] leading-[1.65] text-[#2D3142] marker:text-brand-indigo">
                                    <li v-for="(li, n) in b.ul" :key="n">
                                        <template v-for="(p, j) in parts(li)" :key="j">
                                            <mark v-if="isPh(p)" class="rounded bg-[#FFF3D6] px-1 text-[#8A5A00]">{{ p
                                            }}</mark><template v-else>{{ p }}</template>
                                        </template>
                                    </li>
                                </ul>
                                <p v-else class="m-0 mb-3 text-[.98rem] leading-[1.7] text-[#2D3142]">
                                    <template v-for="(p, j) in parts(b)" :key="j">
                                        <mark v-if="isPh(p)" class="rounded bg-[#FFF3D6] px-1 text-[#8A5A00]">{{ p
                                        }}</mark><template v-else>{{ p }}</template>
                                    </template>
                                </p>
                            </template>
                        </article>
                    </div>

                    <div class="mt-10 rounded-2xl bg-[#F4F0FC] p-6 text-[.95rem] leading-[1.6] text-[#2D3142]">
                        Questions about this page? Write to
                        <a :href="`mailto:${site.contactEmail}`" class="font-semibold text-brand-indigo">{{
                            site.contactEmail }}</a>.
                    </div>
                </div>
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