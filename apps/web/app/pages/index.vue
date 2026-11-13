<script setup lang="ts">
import { Check, CircleAlert, CircleCheck, Hourglass, Send, TriangleAlert, UploadCloud, Wallet } from 'lucide-vue-next'
const { call } = useApi()
const user = useState<any>('user')
const claims = useState<any>('claims')

const batches = ref<any[]>([])
const dash = ref<any>(null)
const problems = ref<any[]>([])
const message = ref('')
const messageIsError = ref(false)
const busy = ref(false)
const over = ref(false)
const topupAmount = ref(5000)
const topupLink = ref('')

// Roles in the code stay maker / checker / admin. On screen they read as: prepares, approves, both.
const canUpload = computed(() => ['maker', 'admin'].includes(claims.value.role))
const canApprove = computed(() => ['checker', 'admin'].includes(claims.value.role))
const canSend = canApprove
const canTopup = computed(() => claims.value.role === 'admin')
const naira = (kobo = 0) => '₦' + (kobo / 100).toLocaleString('en-NG', { minimumFractionDigits: 2 })

const statusLabel: Record<string, string> = {
  checked: 'Awaiting approval', approved: 'Approved', sending: 'Sending', needs_funding: 'Needs funding', completed: 'Completed'
}
const label = (s: string) => statusLabel[s] ?? s.replace('_', ' ')
const isMine = (b: any) => b.uploaded_by && b.uploaded_by === user.value?.uid

function say(text: string, isError = false) { message.value = text; messageIsError.value = isError }

async function load() {
  const [b, d] = await Promise.all([call('/v1/batches'), call('/v1/dashboard')])
  if (b.ok) batches.value = (await b.json()).batches
  if (d.ok) dash.value = await d.json()
}

async function downloadTemplate() {
  try {
    const res = await call('/v1/template.xlsx')
    if (!res.ok) return say(`Could not download the template (the server answered ${res.status}).`, true)
    const url = URL.createObjectURL(await res.blob())
    const a = document.createElement('a')
    a.href = url; a.download = 'enterprisesend-template.xlsx'
    document.body.appendChild(a); a.click(); a.remove()
    URL.revokeObjectURL(url)
  } catch {
    say('Could not download the template: the browser could not reach the server.', true)
  }
}

async function uploadFile(file: File) {
  busy.value = true; problems.value = []; say('')
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await call('/v1/batches', { method: 'POST', body: form })
    const data = await res.json()
    if (res.status === 201) {
      say(`Checked ${data.rows} rows. A second person needs to approve this batch before it can be sent.`)
    } else {
      problems.value = data.errors || []
      say(data.error || 'Upload failed', true)
    }
  } catch { say('Could not reach the server', true) }
  finally { busy.value = false; await load() }
}
const onPick = (e: Event) => {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) uploadFile(file).finally(() => { input.value = '' })
}
const onDrop = (e: DragEvent) => {
  over.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file && canUpload.value && !busy.value) uploadFile(file)
}

async function approve(id: string) {
  const res = await call(`/v1/batches/${id}/approve`, { method: 'POST' })
  const data = await res.json()
  say(res.ok ? 'Batch approved. You can now send it.' : data.error, !res.ok)
  await load()
}

async function send(id: string) {
  busy.value = true
  try {
    const res = await call(`/v1/batches/${id}/send`, { method: 'POST' })
    const d = await res.json()
    if (res.ok) {
      say(`Sent ${d.sent}, failed ${d.failed}, not funded ${d.unfunded}, scheduled for later ${d.scheduled}.` +
        (d.status === 'needs_funding' ? ' Top up the wallet, then send again.' : ''), d.failed > 0)
    } else say(d.error, true)
  } finally { busy.value = false; await load() }
}

async function topup() {
  topupLink.value = ''
  const res = await call('/v1/wallet/topup', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount_naira: Number(topupAmount.value) })
  })
  const d = await res.json()
  if (res.ok) topupLink.value = d.payment_url
  else say(d.error, true)
}
onMounted(load)
</script>

<template>
  <main class="page">
    <TopBar />

    <div class="page-head">
      <h1>Dashboard</h1>
      <p class="muted">Upload a billing file, get it approved by a second person, then send.</p>
    </div>

    <section v-if="dash" class="stats">
      <div class="stat"><span class="ic">
          <Wallet :size="18" :stroke-width="1.9" />
        </span><span class="muted">Wallet</span><b>{{ naira(dash.wallet_kobo) }}</b></div>
      <div class="stat"><span class="ic">
          <Send :size="18" :stroke-width="1.9" />
        </span><span class="muted">Bills sent</span><b>{{ dash.sent_count }}</b></div>
      <div class="stat"><span class="ic good">
          <CircleCheck :size="18" :stroke-width="1.9" />
        </span><span class="muted">Paid</span><b>{{ dash.paid_count }} · {{ naira(dash.paid_kobo) }}</b></div>
      <div class="stat"><span class="ic warn">
          <Hourglass :size="18" :stroke-width="1.9" />
        </span><span class="muted">Outstanding</span><b>{{ naira(dash.outstanding_kobo) }}</b></div>
      <div class="stat"><span class="ic bad">
          <TriangleAlert :size="18" :stroke-width="1.9" />
        </span><span class="muted">Failed / mismatched</span><b>{{ dash.failed_count }} / {{ dash.mismatch_count }}</b>
      </div>
    </section>

    <div v-if="canUpload || canTopup" class="grid-2">
      <section v-if="canUpload" class="card">
        <h2>Upload a billing file</h2>
        <p class="muted" style="margin:0 0 .9rem">Use the template so columns and formats match.
          <button class="link" @click="downloadTemplate">Download template</button>
        </p>
        <label class="dropzone" :class="{ over, off: busy }" @dragover.prevent="over = true" @dragleave="over = false"
          @drop.prevent="onDrop">
          <span class="ic">
            <UploadCloud :size="22" :stroke-width="1.75" aria-hidden="true" />
          </span>
          <b style="font-size:.95rem">Choose a file or drop it here</b>
          <span class="muted">.csv or .xlsx. Every row is checked before anything can be sent.</span>
          <input type="file" accept=".csv,.xlsx" :disabled="busy" @change="onPick">
        </label>
      </section>

      <section v-if="canTopup" class="card">
        <h2>Top up the messaging wallet</h2>
        <p class="muted" style="margin:0 0 .9rem">Messages are paid from this prepaid wallet.</p>
        <div class="row">
          <input v-model="topupAmount" type="number" min="100" step="100" aria-label="Amount in naira"> <span
            class="muted">₦</span>
          <button @click="topup">Get payment link</button>
        </div>
        <p v-if="topupLink" class="linkbox">Pay here: <a :href="topupLink" target="_blank" rel="noopener">{{ topupLink
        }}</a></p>
      </section>
    </div>

    <div v-if="busy" class="busy">
      <MarkLoader /><span class="muted">Working…</span>
    </div>
    <p v-if="message" class="notice" :class="{ bad: messageIsError }" :role="messageIsError ? 'alert' : 'status'">
      <CircleAlert v-if="messageIsError" :size="18" :stroke-width="2" />
      <Check v-else :size="18" :stroke-width="2.4" />{{ message }}
    </p>

    <section v-if="problems.length" class="card problem">
      <h2>Fix these problems, then upload again</h2>
      <table>
        <thead>
          <tr>
            <th>Row</th>
            <th>Column</th>
            <th>Problem</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(p, i) in problems" :key="i">
            <td>{{ p.row }}</td>
            <td>{{ p.column }}</td>
            <td>{{ p.message }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="card">
      <h2>Batches</h2>
      <p v-if="!batches.length" class="muted" style="margin:.25rem 0 0">No batches yet. Upload your first billing file
        to begin.</p>
      <table v-else>
        <thead>
          <tr>
            <th>ID</th>
            <th>Created</th>
            <th>Rows</th>
            <th>Total</th>
            <th>Status</th>
            <th>Sent</th>
            <th>Paid</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in batches" :key="b.id">
            <td><code :title="b.id">{{ b.id.slice(0, 8) }}</code></td>
            <td>{{ new Date(b.created_at).toLocaleString() }}</td>
            <td>{{ b.row_count }}</td>
            <td>{{ naira(b.total_kobo) }}</td>
            <td><span class="tag" :class="b.status">{{ label(b.status) }}</span>
              <div v-if="b.next_send_at && b.status === 'sending'" class="muted">
                waits until {{ new Date(b.next_send_at).toLocaleString() }}</div>
            </td>
            <td>{{ b.sent_count || 0 }}</td>
            <td>{{ b.paid_count || 0 }}</td>
            <td>
              <NuxtLink :to="`/batches/${b.id}`" class="viewlink">View messages</NuxtLink>
              <button v-if="canApprove && b.status === 'checked' && !isMine(b)" class="small"
                @click="approve(b.id)">Approve</button>
              <span v-else-if="b.status === 'checked' && isMine(b)" class="muted">Waiting for a second person</span>
              <button v-if="canSend && ['approved', 'sending', 'needs_funding'].includes(b.status)" class="small"
                :disabled="busy" @click="send(b.id)">{{ b.status === 'sending' ? 'Send due messages' : 'Send'
                }}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>