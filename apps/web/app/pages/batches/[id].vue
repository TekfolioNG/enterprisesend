<script setup lang="ts">
const route = useRoute()
const { call } = useApi()
const messages = ref<any[]>([])
const error = ref('')
const naira = (k = 0) => '₦' + (k / 100).toLocaleString('en-NG', { minimumFractionDigits: 2 })
const chan: Record<string, string> = { sms: 'SMS', whatsapp: 'WhatsApp', email: 'Email' }

onMounted(async () => {
  const res = await call(`/v1/batches/${route.params.id}/messages`)
  if (res.ok) messages.value = (await res.json()).messages
  else error.value = 'Could not load this batch.'
})
</script>

<template>
  <main class="page">
    <TopBar />
    <section class="card">
      <h2>Messages in batch <code>{{ String(route.params.id).slice(0, 8) }}</code></h2>
      <p class="muted"><NuxtLink to="/">← Back to dashboard</NuxtLink></p>
      <p v-if="error" class="error">{{ error }}</p>
      <table v-if="messages.length">
        <thead><tr><th>Customer</th><th>Contact</th><th>Bill</th><th>Status</th><th>Delivery</th><th>Receipt</th><th>Message</th></tr></thead>
        <tbody><tr v-for="m in messages" :key="m.row">
          <td>{{ m.recipient_name }}<br><code>{{ m.account_id }}</code></td>
          <td><code>{{ m.phone }}<br>{{ m.email }}</code></td>
          <td>{{ naira(m.amount_kobo) }}</td>
          <td><span class="tag" :class="m.status">{{ m.status.replace('_', ' ') }}</span></td>
          <td><span v-for="a in m.attempts" :key="a.channel + a.at" class="chip" :class="a.result">
            {{ chan[a.channel] }}: {{ a.result }}</span></td>
          <td><span v-for="a in m.receipt_attempts" :key="a.channel" class="chip" :class="a.result">
            {{ chan[a.channel] }}: {{ a.result }}</span><span v-if="!m.receipt_attempts.length" class="muted">—</span></td>
          <td><details v-if="m.preview"><summary>View</summary><div class="linkbox">{{ m.preview }}</div></details></td>
        </tr></tbody>
      </table>
    </section>
  </main>
</template>
