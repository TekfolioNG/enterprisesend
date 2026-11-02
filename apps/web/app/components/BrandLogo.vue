<script setup lang="ts">
import { brand } from '~/utils/brand'
const props = defineProps<{ variant?: 'compact' | 'full' }>()
const light = computed(() => (props.variant === 'full' ? brand.logo.primary : brand.logo.oneLine))
const dark = computed(() => (props.variant === 'full' ? brand.logo.primaryDark : brand.logo.oneLineDark))
</script>

<template>
  <picture>
    <source :srcset="dark" media="(prefers-color-scheme: dark)">
    <img :src="light" :alt="`${brand.productName} logo`" :class="variant === 'full' ? 'logo-full' : 'logo-compact'">
  </picture>
</template>
