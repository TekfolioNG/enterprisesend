<script setup lang="ts">
import { site } from '~/utils/config'
useHead({ title: 'Start Secure Billing: EnterpriseSend' })

const f = reactive({ org: '', rc: '', name: '', email: '', phone: '', use: 'Bills and fees', volume: 'Under 500', notes: '' })
const errors = reactive<Record<string, string>>({})
const opened = ref(false)

function validate() {
  Object.keys(errors).forEach((k) => delete errors[k])
  if (!f.org.trim()) errors.org = 'Enter your organisation name.'
  if (!f.rc.trim()) errors.rc = 'Enter your CAC registration number.'
  if (!f.name.trim()) errors.name = 'Enter your name.'
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email)) errors.email = 'Enter a work email address.'
  if (f.phone.replace(/\D/g, '').length < 10) errors.phone = 'Enter a phone number we can call.'
  return Object.keys(errors).length === 0
}

function submit() {
  if (!validate()) return
  const body = [
    `Organisation: ${f.org}`, `CAC registration: ${f.rc}`, `Contact: ${f.name}`, `Email: ${f.email}`, `Phone: ${f.phone}`,
    `What we will send: ${f.use}`, `People we message each month: ${f.volume}`, '', f.notes
  ].join('\n')
  window.location.href = `mailto:${site.contactEmail}?subject=${encodeURIComponent('Start Secure Billing: ' + f.org)}&body=${encodeURIComponent(body)}`
  opened.value = true
}
</script>

<template>
  <section class="apply">
    <div class="wrap apply-grid">
      <div>
        <h1>Start Secure Billing</h1>
        <p class="lead">Tell us about your organisation. We verify every organisation before it can send, so your customers can trust every message that carries your name.</p>
        <ol class="next">
          <li><b>We review your details.</b> We may call you.</li>
          <li><b>We verify your organisation.</b> Registration number and an authorised contact.</li>
          <li><b>You pay the setup fee.</b> A payment link is sent to you.</li>
          <li><b>We set you up.</b> Your account, sender names and a short training for your team.</li>
        </ol>
      </div>

      <form class="form" novalidate @submit.prevent="submit">
        <label>Organisation name<input v-model="f.org" type="text" autocomplete="organization" :aria-invalid="!!errors.org"><small v-if="errors.org">{{ errors.org }}</small></label>
        <label>CAC registration number<input v-model="f.rc" type="text" placeholder="RC 1234567" :aria-invalid="!!errors.rc"><small v-if="errors.rc">{{ errors.rc }}</small></label>
        <div class="two">
          <label>Your name<input v-model="f.name" type="text" autocomplete="name" :aria-invalid="!!errors.name"><small v-if="errors.name">{{ errors.name }}</small></label>
          <label>Phone<input v-model="f.phone" type="tel" autocomplete="tel" :aria-invalid="!!errors.phone"><small v-if="errors.phone">{{ errors.phone }}</small></label>
        </div>
        <label>Work email<input v-model="f.email" type="email" autocomplete="email" :aria-invalid="!!errors.email"><small v-if="errors.email">{{ errors.email }}</small></label>
        <div class="two">
          <label>What will you send?
            <select v-model="f.use"><option>Bills and fees</option><option>Notices and invitations</option><option>Both</option></select>
          </label>
          <label>People you message each month
            <select v-model="f.volume"><option>Under 500</option><option>500 to 1,500</option><option>1,500 to 10,000</option><option>Over 10,000</option></select>
          </label>
        </div>
        <label>Anything else we should know?<textarea v-model="f.notes" rows="4"></textarea></label>
        <button class="btn btn-lg" type="submit">Send my details</button>
        <p v-if="opened" class="sent">Your email app should open with your application ready to send. If it did not, write to {{ site.contactEmail }}.</p>
      </form>
    </div>
  </section>
</template>
