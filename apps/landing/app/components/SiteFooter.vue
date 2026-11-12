<script setup lang="ts">
// Footer (ink): one calm band under the closing call to action. A slightly deeper ink than the section above, with a hairline
// between them, so the page ends instead of running on. Logo and one line on the left, three short link groups on the right,
// then a thin legal row. Tekfolio appears once, small and grey, bottom right ("Designed & developed by"), linking to tekfolio.ng.

const appUrl = useRuntimeConfig().public.appUrl
const year = new Date().getFullYear()

const groups = computed(() => [
  {
    title: 'Product',
    links: [
      { label: 'How it works', to: '/#how' },
      { label: 'Security', to: '/#security' },
      { label: 'Pricing', to: '/#pricing' },
      { label: 'FAQ', to: '/#faq' }
    ]
  },
  {
    title: 'Company',
    links: [
      { label: 'About', to: '/about' },
      { label: 'Team', to: '/team' }
    ]
  },
  {
    title: 'Account',
    links: [
      { label: 'Start Secure Billing', to: '/apply' },
      { label: 'Sign in', href: `${appUrl}/login` }
    ]
  }
])

const link = 'text-[.95rem] text-[#9AA3B5] no-underline transition-colors duration-200 hover:text-white focus-visible:text-white'
</script>

<template>
  <footer class="relative bg-[#0B0B14]">
    <!-- a lavender hairline that fades out at both ends, so the join with the section above reads as a deliberate edge -->
    <div aria-hidden="true"
      class="absolute inset-x-0 top-0 h-px bg-[linear-gradient(to_right,transparent,rgba(180,140,255,.45),transparent)]">
    </div>
    <div class="wrap">
      <div
        class="grid gap-12 py-14 max-tablet:gap-10 max-tablet:py-12 tablet:grid-cols-[minmax(0,1.15fr)_minmax(0,1.85fr)] tablet:gap-16">

        <div>
          <NuxtLink to="/" aria-label="EnterpriseSend home" class="inline-block">
            <img src="/brand/logo-one-line-dark.svg" alt="EnterpriseSend" class="block h-8 w-auto">
          </NuxtLink>
          <p class="mt-5 mb-0 max-w-[30ch] text-[.95rem] leading-[1.6] text-[#9AA3B5]">
            Verified messages, bills and payments.
          </p>
        </div>

        <nav aria-label="Footer" class="grid grid-cols-2 gap-x-8 gap-y-10 tablet:grid-cols-3">
          <div v-for="g in groups" :key="g.title">
            <p class="mb-4 text-[.75rem] font-bold tracking-[.12em] text-[#EEF0F8] uppercase">{{ g.title }}
            </p>
            <ul class="m-0 grid list-none gap-3 p-0">
              <li v-for="l in g.links" :key="l.label">
                <a v-if="l.href" :href="l.href" :class="link">{{ l.label }}</a>
                <NuxtLink v-else :to="l.to" :class="link">{{ l.label }}</NuxtLink>
              </li>
            </ul>
          </div>
        </nav>
      </div>

      <div
        class="flex flex-wrap items-center justify-between gap-x-6 gap-y-3 border-t border-solid border-white/10 py-6 text-[.82rem] text-[#7C8497] max-tablet:flex-col max-tablet:items-start">
        <p class="m-0 flex flex-wrap items-center gap-x-5 gap-y-2">
          <span>© {{ year }} EnterpriseSend</span>
          <NuxtLink to="/privacy" class="text-[#7C8497] no-underline transition-colors duration-200 hover:text-white">
            Privacy
          </NuxtLink>
          <NuxtLink to="/terms" class="text-[#7C8497] no-underline transition-colors duration-200 hover:text-white">
            Terms
          </NuxtLink>
        </p>
        <p class="m-0 text-[.78rem]">
          Designed &amp; developed by
          <a href="https://tekfolio.ng" target="_blank" rel="noopener"
            class="text-[#7C8497] no-underline transition-colors duration-200 hover:text-white">Tekfolio</a>
        </p>
      </div>
    </div>
  </footer>
</template>