<script setup lang="ts">
const { call } = useApi()
const claims = useState<any>('claims')
const entries = ref<any[]>([])
const result = ref<any>(null)
const error = ref('')
const busy = ref(false)

const labels: Record<string, string> = {
  batch_uploaded: 'Batch uploaded', batch_approved: 'Batch approved', batch_send_run: 'Sending run',
  self_approval_blocked: 'Self-approval blocked', payment_matched: 'Payment matched',
  payment_mismatch: 'Payment amount mismatch', wallet_topped_up: 'Wallet topped up',
  opt_out_recorded: 'Opt-out recorded'
}
const label = (a: string) => labels[a] || a
const short = (h: string) => h.slice(0, 10) + '…'
const detail = (d: any) => Object.entries(d || {}).map(([k, v]) => `${k}: ${v}`).join(' · ')

async function load() {
  const res = await call('/v1/audit?limit=200')
  if (res.ok) entries.value = (await res.json()).entries
  else error.value = 'You do not have access to the activity log.'
}
async function verify() {
  busy.value = true
  const res = await call('/v1/audit/verify')
  if (res.ok) result.value = await res.json()
  busy.value = false
}
const print = () => window.print()
onMounted(load)
</script>

<template>
  <main class="page">
    <TopBar />
    <section class="card">
      <div class="row" style="justify-content: space-between">
        <h2>Activity log for {{ claims.tenant_id }}</h2>
        <div class="row noprint">
          <button :disabled="busy" @click="verify">Verify log integrity</button>
          <button class="secondary" @click="print">Print / save as PDF</button>
        </div>
      </div>
      <p class="muted">Every action is recorded in order, and each record is sealed to the one before it, so any later change or deletion shows up when the log is verified.</p>
      <p v-if="result && result.intact" class="ok">Intact: {{ result.entries }} entries checked. Latest seal {{ short(result.last_hash || '') }}</p>
      <p v-if="result && !result.intact" class="error">
        Problem found: {{ result.broken_at_seq ? `entry #${result.broken_at_seq} does not match its seal` : 'the log end does not match the record of its length (entries may have been removed)' }}.
      </p>
      <p v-if="error" class="error">{{ error }}</p>
      <table>
        <thead><tr><th>#</th><th>When</th><th>Who</th><th>What</th><th>Details</th><th>Seal</th></tr></thead>
        <tbody><tr v-for="e in entries" :key="e.seq">
          <td>{{ e.seq }}</td>
          <td>{{ new Date(e.at).toLocaleString() }}</td>
          <td><code>{{ e.actor.slice(0, 12) }}</code></td>
          <td>{{ label(e.action) }}</td>
          <td class="muted">{{ detail(e.detail) }}</td>
          <td><code>{{ short(e.hash) }}</code></td>
        </tr></tbody>
      </table>
    </section>
  </main>
</template>
