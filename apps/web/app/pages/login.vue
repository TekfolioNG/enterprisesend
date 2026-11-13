<script setup lang="ts">
import { getMultiFactorResolver, signInWithEmailAndPassword, TotpMultiFactorGenerator } from 'firebase/auth'
import { CircleAlert, Eye, EyeOff, KeyRound, Lock, Mail } from 'lucide-vue-next'
const { $auth } = useNuxtApp()
const user = useState<any>('user')
const claims = useState<any>('claims')
const email = ref('')
const password = ref('')
const code = ref('')
const error = ref('')
const busy = ref(false)
const showPassword = ref(false)
const step = ref<'password' | 'code'>('password')
let resolver: any = null

async function login() {
  busy.value = true
  error.value = ''
  try {
    await signInWithEmailAndPassword($auth as any, email.value, password.value)
    await finishSignIn()
  } catch (e: any) {
    if (e?.code === 'auth/multi-factor-auth-required') {
      resolver = getMultiFactorResolver($auth as any, e)
      step.value = 'code'
    } else {
      error.value = 'Sign-in failed. Check your email and password.'
    }
  } finally { busy.value = false }
}

async function verify() {
  busy.value = true
  error.value = ''
  try {
    const hint = resolver.hints.find((h: any) => h.factorId === TotpMultiFactorGenerator.FACTOR_ID)
    if (!hint) { error.value = 'No authenticator app is set up for this account. Ask your administrator.'; return }
    const assertion = TotpMultiFactorGenerator.assertionForSignIn(hint.uid, code.value.trim())
    await resolver.resolveSignIn(assertion)
    await finishSignIn()
  } catch {
    error.value = 'That code was not accepted. Wait for a new code and try again.'
    code.value = ''
  } finally { busy.value = false }
}

// The route guard reads this state. Fill it before navigating, or the guard sends the person
// back to /login and the button seems to need a second click.
async function finishSignIn() {
  const u = ($auth as any).currentUser
  const t = await u.getIdTokenResult(true)
  user.value = { email: u.email, uid: u.uid }
  claims.value = { tenant_id: t.claims.tenant_id, role: t.claims.role }
  await navigateTo('/')
}

function startOver() { step.value = 'password'; password.value = ''; code.value = ''; error.value = ''; resolver = null }
</script>

<template>
  <main class="center auth-bg">
    <form v-if="step === 'password'" class="card narrow auth-card" @submit.prevent="login">
      <div class="login-brand">
        <BrandLogo variant="full" />
        <h1 class="sr-only">EnterpriseSend sign in</h1>
      </div>
      <p class="muted auth-title" style="margin:0">Sign in to your organisation account</p>
      <label>Email
        <span class="field">
          <Mail class="lead" :size="18" :stroke-width="1.9" aria-hidden="true" />
          <input v-model="email" type="email" autocomplete="username" required>
        </span>
      </label>
      <label>Password
        <span class="field">
          <Lock class="lead" :size="18" :stroke-width="1.9" aria-hidden="true" />
          <input v-model="password" :type="showPassword ? 'text' : 'password'" autocomplete="current-password" required>
          <button type="button" class="trail" :aria-label="showPassword ? 'Hide password' : 'Show password'"
            @click="showPassword = !showPassword">
            <EyeOff v-if="showPassword" :size="18" :stroke-width="1.9" />
            <Eye v-else :size="18" :stroke-width="1.9" />
          </button>
        </span>
      </label>
      <p v-if="error" class="notice bad" role="alert" style="margin:0">
        <CircleAlert :size="18" :stroke-width="2" />{{ error }}
      </p>
      <button class="wide" :disabled="busy">{{ busy ? 'Signing in…' : 'Sign in' }}</button>
    </form>

    <form v-else class="card narrow auth-card" @submit.prevent="verify">
      <div class="login-brand">
        <BrandLogo variant="full" />
      </div>
      <span class="auth-ic">
        <KeyRound :size="24" :stroke-width="1.75" aria-hidden="true" />
      </span>
      <div class="auth-title">
        <h1 style="font-size:1.35rem">Two-step sign-in</h1>
        <p class="muted">Enter the 6-digit code from your authenticator app.</p>
      </div>
      <input v-model="code" type="text" class="codebox" inputmode="numeric" autocomplete="one-time-code" maxlength="6"
        aria-label="6-digit code" required>
      <p v-if="error" class="notice bad" role="alert" style="margin:0">
        <CircleAlert :size="18" :stroke-width="2" />{{ error }}
      </p>
      <button class="wide" :disabled="busy || code.length < 6">{{ busy ? 'Checking…' : 'Verify and sign in' }}</button>
      <button type="button" class="link" @click="startOver">Use a different account</button>
    </form>
  </main>
</template>