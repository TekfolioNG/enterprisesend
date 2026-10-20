<script setup lang="ts">
import { signInWithEmailAndPassword } from 'firebase/auth'
const { $auth } = useNuxtApp()
const email = ref('')
const password = ref('')
const error = ref('')
const busy = ref(false)

async function login() {
  busy.value = true
  error.value = ''
  try {
    await signInWithEmailAndPassword($auth as any, email.value, password.value)
    await navigateTo('/')
  } catch (e: any) {
    error.value = e?.code === 'auth/multi-factor-auth-required'
      ? 'This account needs a second sign-in step (MFA). That screen is built in the next step.'
      : 'Sign-in failed. Check your email and password.'
  } finally { busy.value = false }
}
</script>

<template>
  <main class="center">
    <form class="card narrow" @submit.prevent="login">
      <h1>EnterpriseSend</h1>
      <p class="muted">Sign in to your organisation account</p>
      <label>Email<input v-model="email" type="email" autocomplete="username" required></label>
      <label>Password<input v-model="password" type="password" autocomplete="current-password" required></label>
      <p v-if="error" class="error">{{ error }}</p>
      <button :disabled="busy">{{ busy ? 'Signing in…' : 'Sign in' }}</button>
    </form>
  </main>
</template>
