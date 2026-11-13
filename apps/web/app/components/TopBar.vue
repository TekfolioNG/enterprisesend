<script setup lang="ts">
import { signOut } from 'firebase/auth'
import { LayoutDashboard, LogOut, ScrollText, ShieldCheck } from 'lucide-vue-next'
const { $auth } = useNuxtApp()
const user = useState<any>('user')
const claims = useState<any>('claims')
const canSeeActivity = computed(() => ['checker', 'admin'].includes(claims.value?.role))
// Roles stay maker / checker / admin in code; on screen they are Preparer / Approver / Admin.
const roleLabel = computed(() => ({ maker: 'Preparer', checker: 'Approver', admin: 'Admin' } as Record<string, string>)[claims.value?.role] ?? claims.value?.role)
const initial = computed(() => (user.value?.email ?? '?').charAt(0).toUpperCase())
async function logout() {
  await signOut($auth as any)
  await navigateTo('/login')
}
</script>

<template>
  <header class="bar noprint">
    <div class="row" style="gap:1.25rem">
      <NuxtLink to="/" aria-label="EnterpriseSend home" style="padding:0;margin:0">
        <BrandLogo variant="compact" />
      </NuxtLink>
      <nav class="row" style="gap:.15rem" aria-label="Main">
        <NuxtLink to="/" style="display:inline-flex;align-items:center;gap:.4rem">
          <LayoutDashboard :size="16" :stroke-width="1.9" />Dashboard
        </NuxtLink>
        <NuxtLink v-if="canSeeActivity" to="/activity" style="display:inline-flex;align-items:center;gap:.4rem">
          <ScrollText :size="16" :stroke-width="1.9" />Activity
        </NuxtLink>
        <NuxtLink to="/security" style="display:inline-flex;align-items:center;gap:.4rem">
          <ShieldCheck :size="16" :stroke-width="1.9" />Security
        </NuxtLink>
      </nav>
    </div>
    <div class="row" style="gap:.75rem">
      <span aria-hidden="true"
        style="width:34px;height:34px;border-radius:50%;background:var(--brand-soft);color:var(--brand);display:grid;place-items:center;font-weight:700;font-size:.9rem">{{
          initial }}</span>
      <div style="line-height:1.25">
        <div style="font-size:.88rem;font-weight:600">{{ user?.email }}</div>
        <div class="muted" style="font-size:.78rem">{{ roleLabel }} · {{ claims?.tenant_id }}</div>
      </div>
      <button class="secondary small" style="display:inline-flex;align-items:center;gap:.4rem" @click="logout">
        <LogOut :size="15" :stroke-width="1.9" />Sign out
      </button>
    </div>
  </header>
</template>