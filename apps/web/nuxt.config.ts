import { brand } from './app/utils/brand'

export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  ssr: false, // single-page app: simple to host and nothing sensitive renders on a server
  devtools: { enabled: false },
  css: ['~/assets/main.css'],
  app: {
    head: {
      title: brand.productName,
      titleTemplate: (t?: string) => (t && t !== brand.productName ? `${t} · ${brand.productName}` : brand.productName),
      meta: [{ name: 'theme-color', content: '#310CA7' }],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon-dark.svg', media: '(prefers-color-scheme: dark)' },
        { rel: 'icon', href: '/favicon.ico', sizes: '48x48' },
        { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' }
      ]
    }
  },
  runtimeConfig: {
    public: {
      // Defaults point at the local emulators. Override with NUXT_PUBLIC_* in staging/production.
      apiBase: 'http://localhost:8080',
      firebaseApiKey: 'fake',
      firebaseAuthDomain: 'localhost',
      firebaseProjectId: 'demo-enterprisesend',
      useEmulator: 'true',
      authEmulatorUrl: 'http://localhost:9099',
      // 'true' sends staff without two-step sign-in to /security. Set with NUXT_PUBLIC_REQUIRE_MFA.
      requireMfa: 'false'
    }
  }
})
