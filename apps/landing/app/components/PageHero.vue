<script setup lang="ts">
// Shared header band for the Security, Pricing, Privacy and Terms pages.
// Optional #art slot: sits to the right on desktop and above the text on mobile.
defineProps<{ kicker: string; title: string; lead?: string }>()
</script>

<template>
    <section
        class="page-hero -mt-[72px] pt-[calc(72px+3.5rem)] pb-14 max-tablet:pt-[calc(72px+1.5rem)] max-tablet:pb-10">
        <div class="wrap">
            <div class="mx-auto grid max-w-[1040px] items-center gap-10"
                :class="$slots.art ? 'tablet:grid-cols-[minmax(0,1fr)_minmax(0,.95fr)] tablet:gap-12' : ''">
                <div>
                    <p class="mb-3 font-display text-[.8rem] font-bold tracking-[.12em] text-brand-indigo uppercase">{{
                        kicker }}</p>
                    <h1 class="ph-title max-w-[22ch] font-display font-bold text-ink">{{ title }}</h1>
                    <p v-if="lead" class="m-0 max-w-[60ch] text-[1.05rem] leading-[1.65] text-[#2D3142]">{{ lead }}</p>
                    <slot />
                </div>
                <div v-if="$slots.art" class="max-tablet:order-first">
                    <slot name="art" />
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
/* base.css styles every h1 and sits outside Tailwind's layers, so the title size is set here to win over it */
.ph-title {
    font-size: clamp(1.9rem, 3.4vw, 2.6rem);
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin: 0 0 1rem;
}

.page-hero {
    background:
        radial-gradient(55% 90% at 90% 0%, #EEE8FA 0%, rgba(238, 232, 250, 0) 70%),
        #F9FBFF;
    border-bottom: 1px solid #E5E8ED;
}
</style>