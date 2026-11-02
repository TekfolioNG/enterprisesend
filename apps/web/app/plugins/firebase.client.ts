import { initializeApp } from 'firebase/app'
import { getAuth, connectAuthEmulator, onAuthStateChanged } from 'firebase/auth'

export default defineNuxtPlugin(() => {
  const c = useRuntimeConfig().public
  const app = initializeApp({
    apiKey: c.firebaseApiKey,
    authDomain: c.firebaseAuthDomain,
    projectId: c.firebaseProjectId
  })
  const auth = getAuth(app)
  if (c.useEmulator === 'true') connectAuthEmulator(auth, c.authEmulatorUrl, { disableWarnings: true })

  const user = useState<any>('user', () => null)
  const claims = useState<any>('claims', () => ({}))

  // Resolves once Firebase has told us whether someone is signed in. It must ALWAYS resolve:
  // if the session cannot be refreshed (offline, expired, emulator not running) we treat the
  // person as signed out, so they land on the sign-in page instead of a blank screen.
  const authReady = new Promise<void>((resolve) => {
    onAuthStateChanged(auth, async (u) => {
      try {
        if (u) {
          const t = await u.getIdTokenResult(true)
          user.value = { email: u.email, uid: u.uid }
          claims.value = { tenant_id: t.claims.tenant_id, role: t.claims.role }
        } else {
          user.value = null
          claims.value = {}
        }
      } catch {
        user.value = null
        claims.value = {}
      } finally {
        resolve()
      }
    })
  })
  return { provide: { auth, authReady } }
})
