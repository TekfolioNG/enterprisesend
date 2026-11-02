<script setup lang="ts">
import { multiFactor, TotpMultiFactorGenerator } from 'firebase/auth'
import QRCode from 'qrcode'
import { brand } from '~/utils/brand'

const { $auth } = useNuxtApp()
const user = useState<any>('user')
const required = useRuntimeConfig().public.requireMfa === 'true'

const factors = ref<any[]>([])
const qr = ref('')
const secretKey = ref('')
const code = ref('')
const message = ref('')
const isError = ref(false)
const busy = ref(false)
let secret: any = null

const current = () => ($auth as any).currentUser
function refresh() { factors.value = current() ? multiFactor(current()).enrolledFactors.map((f: any) => ({ name: f.displayName, at: f.enrollmentTime })) : [] }
function say(text: string, err = false) { message.value = text; isError.value = err }

function explain(e: any): string {
  switch (e?.code) {
    case 'auth/requires-recent-login': return 'For security, sign out and sign in again, then retry.'
    case 'auth/unverified-email': return 'Your email address must be verified before two-step sign-in can be set up. Ask your administrator.'
    case 'auth/invalid-verification-code': return 'That code was not accepted. Wait for a new code and try again.'
    case 'auth/operation-not-allowed': return 'Two-step sign-in is not switched on for this project yet.'
    default: return 'Could not complete this step. On the local test system this is expected, because it does not support authenticator apps.'
  }
}

async function start() {
  busy.value = true; say('')
  try {
    const session = await multiFactor(current()).getSession()
    secret = await TotpMultiFactorGenerator.generateSecret(session)
    qr.value = await QRCode.toDataURL(secret.generateQrCodeUrl(current().email, brand.productName), { margin: 1, width: 220 })
    secretKey.value = secret.secretKey
  } catch (e: any) { say(explain(e), true) } finally { busy.value = false }
}

async function finish() {
  busy.value = true; say('')
  try {
    const assertion = TotpMultiFactorGenerator.assertionForEnrollment(secret, code.value.trim())
    await multiFactor(current()).enroll(assertion, 'Authenticator app')
    qr.value = ''; secretKey.value = ''; code.value = ''; secret = null
    refresh(); say('Two-step sign-in is on. You will be asked for a code each time you sign in.')
    if (required) await navigateTo('/')
  } catch (e: any) { say(explain(e), true) } finally { busy.value = false }
}
onMounted(refresh)
</script>

<template>
  <main class="page">
    <TopBar />
    <section class="card">
      <h2>Two-step sign-in</h2>
      <p class="muted">Protect {{ user?.email }} with a 6-digit code from an authenticator app (Google Authenticator, Microsoft Authenticator, 1Password and similar).</p>
      <p v-if="required && !factors.length" class="error">Your organisation requires two-step sign-in. Set it up to continue.</p>

      <div v-if="factors.length">
        <p class="ok">On: {{ factors.map(f => f.name).join(', ') }}</p>
      </div>

      <div v-else-if="!qr">
        <button :disabled="busy" @click="start">Set up authenticator app</button>
      </div>

      <div v-else class="narrow" style="display:grid; gap:.75rem">
        <p>1. Scan this code with your authenticator app.</p>
        <img :src="qr" alt="QR code for your authenticator app" class="qr">
        <p class="muted">Cannot scan? Enter this key by hand: <code>{{ secretKey }}</code></p>
        <p>2. Enter the 6-digit code it shows.</p>
        <form style="display:grid; gap:.75rem" @submit.prevent="finish">
          <input v-model="code" type="text" class="codebox" inputmode="numeric" autocomplete="one-time-code" maxlength="6" required>
          <button :disabled="busy || code.length < 6">Turn on two-step sign-in</button>
        </form>
      </div>

      <p v-if="message" :class="isError ? 'error' : 'ok'">{{ message }}</p>
    </section>
  </main>
</template>
