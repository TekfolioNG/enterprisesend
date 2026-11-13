<script setup lang="ts">
import { CircleAlert, Printer, ScrollText, ShieldAlert, ShieldCheck } from 'lucide-vue-next'
const { call } = useApi()
const claims = useState<any>('claims')
const entries = ref<any[]>([])
const result = ref<any>(null)
const error = ref('')
const busy = ref(false)
const loading = ref(true)

const labels: Record<string, string> = {
  batch_uploaded: 'Batch uploaded', batch_approved: 'Batch approved', batch_send_run: 'Sending run',
  self_approval_blocked: 'Self-approval blocked', payment_matched: 'Payment matched',
  payment_mismatch: 'Payment amount mismatch', wallet_topped_up: 'Wallet topped up',
  opt_out_recorded: 'Opt-out recorded'
}
const label = (a: string) => labels[a] || a
const short = (h = '') => h.slice(0, 10) + '…'
const detail = (d: any) => Object.entries(d || {}).map(([k, v]) => `${k}: ${v}`).join(' · ')

async function load() {
  try {
    const res = await call('/v1/audit?limit=200')
    if (res.ok) entries.value = (await res.json()).entries
    else error.value = 'You do not have access to the activity log.'
  } catch { error.value = 'Could not reach the server.' }
  finally { loading.value = false }
}
async function verify() {
  busy.value = true
  try {
    const res = await call('/v1/audit/verify')
    if (res.ok) result.value = await res.json()
    else error.value = 'Could not verify the log right now.'
  } catch { error.value = 'Could not reach the server.' }
  finally { busy.value = false }
}
const print = () => window.print()
onMounted(load)
</script>

<template>
  <main class="page">
    <TopBar />
    <div class="page-head"
      style="display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;flex-wrap:wrap">
      <div>
        <h1>Activity log</h1>
        <p class="muted">{{ claims?.tenant_id }} · every action, in order</p>
      </div>
      <div class="row noprint">
        <button :disabled="busy" style="display:inline-flex;align-items:center;gap:.4rem" @click="verify">
          <ShieldCheck :size="16" :stroke-width="1.9" />{{ busy ? 'Verifying…' : 'Verify log integrity' }}
        </button>
        <button class="secondary" style="display:inline-flex;align-items:center;gap:.4rem" @click="print">
          <Printer :size="16" :stroke-width="1.9" />Print / save as PDF
        </button>
      </div>
    </div>

    <p class="muted" style="margin:0 0 1rem;max-width:62ch">Each record is sealed to the one before it, so any later
      change or deletion shows up when the log is verified.</p>

    <p v-if="result && result.intact" class="notice" role="status">
      <ShieldCheck :size="18" :stroke-width="2" />Intact: {{ result.entries }} entries checked. Latest seal {{
        short(result.last_hash) }}
    </p>
    <p v-if="result && !result.intact" class="notice bad" role="alert">
      <ShieldAlert :size="18" :stroke-width="2" />
      Problem found: {{ result.broken_at_seq ? `entry #${result.broken_at_seq} does not match its seal`
        : 'the log end does not match the record of its length(entries may have been removed) ' }}.
    </p>
    <p v-if="error" class="notice bad" role="alert">
      <CircleAlert :size="18" :stroke-width="2" />{{ error }}
    </p>

    <section class="card">
      <p v-if="loading" class="busy">
        <MarkLoader /><span class="muted">Loading…</span>
      </p>
      <p v-else-if="!entries.length && !error" class="muted" style="margin:0">
        <ScrollText :size="16" style="vertical-align:-3px" /> No activity recorded yet.
      </p>
      <table v-else-if="entries.length">
        <thead>
          <tr>
            <th>#</th>
            <th>When</th>
            <th>Who</th>
            <th>What</th>
            <th>Details</th>
            <th>Seal</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in entries" :key="e.seq">
            <td>{{ e.seq }}</td>
            <td>{{ new Date(e.at).toLocaleString() }}</td>
            <td><code>{{ e.actor.slice(0, 12) }}</code></td>
            <td><b style="font-weight:600">{{ label(e.action) }}</b></td>
            <td class="muted">{{ detail(e.detail) }}</td>
            <td><code>{{ short(e.hash) }}</code></td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>