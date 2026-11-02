<script setup lang="ts">
const appUrl = useRuntimeConfig().public.appUrl
</script>

<template>
  <footer class="footer">
    <div class="wrap footer-row">
      <img src="/brand/logo-one-line-dark.svg" alt="EnterpriseSend, by Tekfolio" class="logo">
      <nav aria-label="Footer" class="footer-nav">
        <NuxtLink to="/apply">Start Secure Billing</NuxtLink>
        <a :href="`${appUrl}/login`">Sign in</a>
        <NuxtLink to="/privacy">Privacy</NuxtLink>
        <NuxtLink to="/terms">Terms</NuxtLink>
      </nav>
    </div>
    <div class="wrap footer-note">EnterpriseSend is a product of Tekfolio.</div>
  </footer>
</template>
