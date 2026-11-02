<script setup lang="ts">
import { signInWithEmailAndPassword, getMultiFactorResolver, TotpMultiFactorGenerator } from 'firebase/auth'
const { $auth } = useNuxtApp()
const email = ref('')
const password = ref('')
const code = ref('')
const error = ref('')
const busy = ref(false)
const step = ref<'password' | 'code'>('password')
let resolver: any = null

async function login() {
  busy.value = true
  error.value = ''
  try {
    await signInWithEmailAndPassword($auth as any, email.value, password.value)
    await navigateTo('/')
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
    await navigateTo('/')
  } catch {
    error.value = 'That code was not accepted. Wait for a new code and try again.'
    code.value = ''
  } finally { busy.value = false }
}

function startOver() { step.value = 'password'; password.value = ''; code.value = ''; error.value = ''; resolver = null }
</script>

<template>
  <main class="center">
    <form v-if="step === 'password'" class="card narrow" @submit.prevent="login">
      <div class="login-brand">
        <BrandLogo variant="full" />
        <h1 class="sr-only">EnterpriseSend sign in</h1>
      </div>
      <p class="muted">Sign in to your organisation account</p>
      <label>Email<input v-model="email" type="email" autocomplete="username" required></label>
      <label>Password<input v-model="password" type="password" autocomplete="current-password" required></label>
      <p v-if="error" class="error">{{ error }}</p>
      <button :disabled="busy">{{ busy ? 'Signing in…' : 'Sign in' }}</button>
    </form>

    <form v-else class="card narrow" @submit.prevent="verify">
      <div class="login-brand"><BrandLogo variant="full" /></div>
      <h1 class="sr-only">Two-step sign-in</h1>
      <p class="muted">Enter the 6-digit code from your authenticator app.</p>
      <input v-model="code" type="text" class="codebox" inputmode="numeric" autocomplete="one-time-code" maxlength="6" required>
      <p v-if="error" class="error">{{ error }}</p>
      <button :disabled="busy || code.length < 6">{{ busy ? 'Checking…' : 'Verify and sign in' }}</button>
      <button type="button" class="link" @click="startOver">Use a different account</button>
    </form>
  </main>
</template>
