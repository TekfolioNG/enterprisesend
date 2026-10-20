export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  ssr: false, // single-page app: simple to host and nothing sensitive renders on a server
  devtools: { enabled: false },
  css: ['~/assets/main.css'],
  runtimeConfig: {
    public: {
      // Defaults point at the local emulators. Override with NUXT_PUBLIC_* in staging/production.
      apiBase: 'http://localhost:8080',
      firebaseApiKey: 'fake',
      firebaseAuthDomain: 'localhost',
      firebaseProjectId: 'demo-enterprisesend',
      useEmulator: 'true',
      authEmulatorUrl: 'http://localhost:9099'
    }
  }
})
