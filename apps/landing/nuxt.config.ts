import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  devtools: { enabled: false },
  vite: { plugins: [tailwindcss()] },
  css: [
    '~/assets/css/tailwind.css',
    '@fontsource-variable/space-grotesk/index.css',
    '@fontsource-variable/inter/index.css',
    '~/assets/css/base.css'
  ],
  nitro: { prerender: { routes: ['/', '/apply', '/privacy', '/terms'] } },
  runtimeConfig: {
    public: {
      // Where the Sign in button goes. Override with NUXT_PUBLIC_APP_URL (production: https://app.enterprisesend.com).
      appUrl: 'https://staging.enterprisesend.com',
      // Set NUXT_PUBLIC_INDEXABLE=true only for the production site. Anything else tells search engines not to list it.
      indexable: 'false'
    }
  },
  app: {
    head: {
      htmlAttrs: { lang: 'en' },
      // Marks the page as 'will animate' before first paint, unless the visitor prefers reduced motion.
      // If the animation code has not started within 5 seconds, the class is removed so nothing stays hidden.
      script: [{ innerHTML: "(function(){var d=document.documentElement;if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;d.classList.add('anim');setTimeout(function(){if(!window.__heroStarted)d.classList.remove('anim')},5000)})()", tagPosition: 'head' }],
      noscript: [{ innerHTML: '<style>.anim .reveal,.anim .kicker-reveal,.anim .beat-inner,.anim .scene-hide,.anim .ov{opacity:1!important;visibility:visible!important}</style>' }],
      title: 'EnterpriseSend: verified billing, fast payments, no arguments',
      meta: [
        { name: 'description', content: 'Upload your billing file to reach every customer across SMS, WhatsApp, and email with a personalized, secure payment link, and match every incoming payment to its bill.' },
        { property: 'og:title', content: 'EnterpriseSend: verified billing and messaging' },
        { property: 'og:description', content: 'Bills and notices your customers will trust, from verified organisations only.' },
        { property: 'og:type', content: 'website' },
        { name: 'theme-color', content: '#310CA7' }
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon-dark.svg', media: '(prefers-color-scheme: dark)' },
        { rel: 'icon', href: '/favicon.ico', sizes: '48x48' },
        { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' }
      ]
    }
  }
})
