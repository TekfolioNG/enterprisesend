<script setup lang="ts">
const indexable = useRuntimeConfig().public.indexable === 'true'
useHead({ meta: indexable ? [] : [{ name: 'robots', content: 'noindex, nofollow' }] })
</script>

<template>
  <a class="skip" href="#main">Skip to content</a>
  <SiteHeader />
  <main id="main"><NuxtPage /></main>
  <SiteFooter />
</template>
