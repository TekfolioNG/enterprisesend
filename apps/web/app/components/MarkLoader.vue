<script setup lang="ts">
import { brand } from '~/utils/brand'
</script>

<template>
  <picture aria-hidden="true">
    <source :srcset="brand.logo.loaderDark" media="(prefers-color-scheme: dark)">
    <img :src="brand.logo.loader" alt="" class="mark-loader">
  </picture>
</template>
