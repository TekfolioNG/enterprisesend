<script setup lang="ts">
import { signOut } from 'firebase/auth'
const { $auth } = useNuxtApp()
const { call } = useApi()
const user = useState<any>('user')
const claims = useState<any>('claims')

const batches = ref<any[]>([])
const problems = ref<any[]>([])
const message = ref('')
const messageIsError = ref(false)
const busy = ref(false)

const canUpload = computed(() => ['maker', 'admin'].includes(claims.value.role))
const canApprove = computed(() => ['checker', 'admin'].includes(claims.value.role))
const naira = (kobo: number) => '₦' + (kobo / 100).toLocaleString('en-NG', { minimumFractionDigits: 2 })

function say(text: string, isError = false) { message.value = text; messageIsError.value = isError }

async function load() {
  const res = await call('/v1/batches')
  if (res.ok) batches.value = (await res.json()).batches
}

async function downloadTemplate() {
  const res = await call('/v1/template.xlsx')
  if (!res.ok) return say('Could not download the template', true)
  const url = URL.createObjectURL(await res.blob())
  const a = document.createElement('a')
  a.href = url; a.download = 'enterprisesend-template.xlsx'; a.click()
  URL.revokeObjectURL(url)
}

async function upload(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  busy.value = true; problems.value = []; say('')
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await call('/v1/batches', { method: 'POST', body: form })
    const data = await res.json()
    if (res.status === 201) {
      const flags = data.ai_flags?.length ? ` The AI check flagged ${data.ai_flags.length} row(s) for review.` : ''
      say(`Checked ${data.rows} rows. Waiting for a manager's approval.${flags}`)
      await load()
    } else {
      problems.value = data.errors || []
      say(data.error || 'Upload failed', true)
    }
  } catch { say('Could not reach the server', true) }
  finally { busy.value = false; input.value = '' }
}

async function approve(id: string) {
  const res = await call(`/v1/batches/${id}/approve`, { method: 'POST' })
  const data = await res.json()
  say(res.ok ? 'Batch approved.' : data.error, !res.ok)
  await load()
}

async function logout() {
  await signOut($auth as any)
  await navigateTo('/login')
}
onMounted(load)
</script>

<template>
  <main class="page">
    <header class="bar">
      <h1>EnterpriseSend</h1>
      <div class="muted">{{ user?.email }} · {{ claims.role }} · {{ claims.tenant_id }}
        <button class="link" @click="logout">Sign out</button></div>
    </header>

    <section v-if="canUpload" class="card">
      <h2>1. Upload a billing file</h2>
      <p class="muted">Use the template so columns and formats match.
        <button class="link" @click="downloadTemplate">Download template</button></p>
      <input type="file" accept=".csv,.xlsx" :disabled="busy" @change="upload">
    </section>

    <p v-if="message" :class="messageIsError ? 'error' : 'ok'">{{ message }}</p>

    <section v-if="problems.length" class="card">
      <h2>Fix these problems, then upload again</h2>
      <table>
        <thead><tr><th>Row</th><th>Column</th><th>Problem</th></tr></thead>
        <tbody><tr v-for="(p, i) in problems" :key="i">
          <td>{{ p.row }}</td><td>{{ p.column }}</td><td>{{ p.message }}</td>
        </tr></tbody>
      </table>
    </section>

    <section class="card">
      <h2>Batches</h2>
      <p v-if="!batches.length" class="muted">No batches yet.</p>
      <table v-else>
        <thead><tr><th>Created</th><th>Rows</th><th>Total</th><th>Status</th><th>AI flags</th><th></th></tr></thead>
        <tbody><tr v-for="b in batches" :key="b.id">
          <td>{{ new Date(b.created_at).toLocaleString() }}</td>
          <td>{{ b.row_count }}</td>
          <td>{{ naira(b.total_kobo) }}</td>
          <td><span class="tag" :class="b.status">{{ b.status }}</span></td>
          <td>{{ b.ai?.enabled ? b.ai.flags.length : 'off' }}</td>
          <td><button v-if="canApprove && b.status === 'checked'" @click="approve(b.id)">Approve</button></td>
        </tr></tbody>
      </table>
    </section>
  </main>
</template>
