<script setup lang="ts">
import { ArrowLeft, CircleAlert } from 'lucide-vue-next'
const route = useRoute()
const { call } = useApi()
const messages = ref<any[]>([])
const error = ref('')
const loading = ref(true)
const naira = (k = 0) => '₦' + (k / 100).toLocaleString('en-NG', { minimumFractionDigits: 2 })
const chan: Record<string, string> = { sms: 'SMS', whatsapp: 'WhatsApp', email: 'Email' }
const label = (s: string) => s.replace('_', ' ')

onMounted(async () => {
  try {
    const res = await call(`/v1/batches/${route.params.id}/messages`)
    if (res.ok) messages.value = (await res.json()).messages
    else error.value = 'Could not load this batch.'
  } catch { error.value = 'Could not reach the server.' }
  finally { loading.value = false }
})
</script>

<template>
  <main class="page">
    <TopBar />
    <NuxtLink to="/" class="viewlink noprint"
      style="display:inline-flex;align-items:center;gap:.35rem;margin-bottom:.75rem">
      <ArrowLeft :size="16" :stroke-width="2" />Back to dashboard
    </NuxtLink>
    <div class="page-head">
      <h1>Batch messages</h1>
      <p class="muted">Batch <code>{{ String(route.params.id).slice(0, 8) }}</code> · {{ messages.length }} message{{
        messages.length === 1 ? '' : 's' }}</p>
    </div>

    <p v-if="error" class="notice bad" role="alert">
      <CircleAlert :size="18" :stroke-width="2" />{{ error }}
    </p>

    <section class="card">
      <p v-if="loading" class="busy">
        <MarkLoader /><span class="muted">Loading…</span>
      </p>
      <p v-else-if="!messages.length && !error" class="muted" style="margin:0">No messages in this batch.</p>
      <table v-else-if="messages.length">
        <thead>
          <tr>
            <th>Customer</th>
            <th>Contact</th>
            <th>Bill</th>
            <th>Status</th>
            <th>Delivery</th>
            <th>Receipt</th>
            <th>Message</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in messages" :key="m.row">
            <td><b style="font-weight:600">{{ m.recipient_name }}</b><br><code>{{ m.account_id }}</code></td>
            <td><code>{{ m.phone }}<br>{{ m.email }}</code></td>
            <td>{{ naira(m.amount_kobo) }}</td>
            <td><span class="tag" :class="m.status">{{ label(m.status) }}</span></td>
            <td><span v-for="a in m.attempts" :key="a.channel + a.at" class="chip" :class="a.result">{{ chan[a.channel]
            }}: {{ a.result }}</span></td>
            <td><span v-for="a in m.receipt_attempts" :key="a.channel" class="chip" :class="a.result">{{ chan[a.channel]
            }}: {{ a.result }}</span><span v-if="!m.receipt_attempts.length" class="muted">—</span></td>
            <td>
              <details v-if="m.preview">
                <summary>View</summary>
                <div class="linkbox">{{ m.preview }}</div>
              </details>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>