<script setup lang="ts">
const appUrl = useRuntimeConfig().public.appUrl
const route = useRoute()
const open = ref(false)
const scrolled = ref(false)
const menuBtn = ref<HTMLButtonElement | null>(null)

const onScroll = () => { scrolled.value = window.scrollY > 8 }
const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape' && open.value) close() }
function close() { open.value = false; menuBtn.value?.focus() }

watch(open, (v) => {
  document.documentElement.style.overflow = v ? 'hidden' : ''
  if (v) nextTick(() => (document.querySelector('.sheet nav a') as HTMLElement | null)?.focus())
})
watch(() => route.fullPath, () => { open.value = false })
onMounted(() => { onScroll(); window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('keydown', onKey) })
onBeforeUnmount(() => { window.removeEventListener('scroll', onScroll); window.removeEventListener('keydown', onKey); document.documentElement.style.overflow = '' })
</script>

<template>
  <header :class="['header', { scrolled }]">
    <div class="wrap header-row">
      <NuxtLink to="/" class="logo-link" aria-label="EnterpriseSend home">
        <img src="/brand/logo-one-line.svg" alt="EnterpriseSend" class="logo">
      </NuxtLink>
      <nav class="nav" aria-label="Main">
        <NuxtLink to="/#how">How it works</NuxtLink>
        <NuxtLink to="/#security">Security</NuxtLink>
        <NuxtLink to="/#pricing">Pricing</NuxtLink>
      </nav>
      <div class="header-actions">
        <a :href="`${appUrl}/login`" class="btn-text">Sign in</a>
        <NuxtLink to="/apply" class="btn">Start Secure Billing</NuxtLink>
        <button ref="menuBtn" class="menu-btn" type="button" :aria-expanded="open" aria-controls="menu-sheet" aria-label="Menu" @click="open = !open"><span></span></button>
      </div>
    </div>

    <div id="menu-sheet" :class="['sheet', { open }]" :aria-hidden="!open" role="dialog" aria-label="Menu">
      <div class="sheet-top">
        <img src="/brand/logo-one-line.svg" alt="EnterpriseSend" class="logo">
        <button class="menu-btn" style="display:inline-flex" type="button" aria-label="Close menu" @click="close"><span style="background:transparent"></span></button>
      </div>
      <nav aria-label="Menu">
        <NuxtLink to="/#how" @click="open = false">How it works</NuxtLink>
        <NuxtLink to="/#security" @click="open = false">Security</NuxtLink>
        <NuxtLink to="/#pricing" @click="open = false">Pricing</NuxtLink>
      </nav>
      <div class="sheet-cta">
        <NuxtLink to="/apply" class="btn btn-lg" @click="open = false">Start Secure Billing</NuxtLink>
        <a :href="`${appUrl}/login`" class="btn-text">Sign in</a>
      </div>
    </div>
  </header>
</template>
