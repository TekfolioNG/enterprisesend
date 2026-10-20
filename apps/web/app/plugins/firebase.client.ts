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

  // resolves once Firebase has told us whether someone is signed in
  const authReady = new Promise<void>((resolve) => {
    onAuthStateChanged(auth, async (u) => {
      user.value = u ? { email: u.email, uid: u.uid } : null
      if (u) {
        const t = await u.getIdTokenResult(true)
        claims.value = { tenant_id: t.claims.tenant_id, role: t.claims.role }
      } else {
        claims.value = {}
      }
      resolve()
    })
  })
  return { provide: { auth, authReady } }
})
