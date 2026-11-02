<script setup lang="ts">
import { signOut } from 'firebase/auth'
const { $auth } = useNuxtApp()
const user = useState<any>('user')
const claims = useState<any>('claims')
const canSeeActivity = computed(() => ['checker', 'admin'].includes(claims.value.role))
async function logout() {
  await signOut($auth as any)
  await navigateTo('/login')
}
</script>

<template>
  <header class="bar noprint">
    <div class="row">
      <BrandLogo variant="compact" />
      <nav class="row">
        <NuxtLink to="/">Dashboard</NuxtLink>
        <NuxtLink v-if="canSeeActivity" to="/activity">Activity</NuxtLink>
        <NuxtLink to="/security">Security</NuxtLink>
      </nav>
    </div>
    <div class="muted">{{ user?.email }} · {{ claims.role }} · {{ claims.tenant_id }}
      <button class="link" @click="logout">Sign out</button></div>
  </header>
</template>
