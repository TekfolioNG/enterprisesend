<script setup lang="ts">
useHead({ title: 'EnterpriseSend: verified billing, fast payments, no arguments' })

onMounted(() => {
  const spine = document.querySelector('.spine') as HTMLElement | null
  if (!spine) return
  const nodes = Array.from(spine.querySelectorAll<HTMLElement>('.node'))
  const segs = Array.from(spine.querySelectorAll<HTMLElement>('.seg'))
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  let queued = false
  const update = () => {
    queued = false
    const line = window.innerHeight * 0.62
    segs.forEach((s) => {
      const r = s.getBoundingClientRect()
      const p = reduce ? 1 : Math.max(0, Math.min(1, (line - r.top) / r.height))
      s.style.setProperty('--p', String(p))
    })
    nodes.forEach((n) => {
      const r = n.getBoundingClientRect()
      n.classList.toggle('lit', reduce || r.top + r.height / 2 < line)
    })
  }
  const onScroll = () => { if (!queued) { queued = true; requestAnimationFrame(update) } }
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onScroll)
  update()
  onBeforeUnmount(() => { window.removeEventListener('scroll', onScroll); window.removeEventListener('resize', onScroll) })
})
</script>

<template>
  <div>
    <HeroSection />
    <Problem />
    <Howitworks />
    <Steps />
    <Whofor />
    <Faq />
    <Closing />

  </div>
</template>
