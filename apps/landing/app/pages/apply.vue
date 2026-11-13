<script setup lang="ts">
import { BadgeCheck, Check, ChevronDown, CircleAlert, ClipboardCheck, CreditCard, GraduationCap } from 'lucide-vue-next'
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

const steps = [
  { icon: ClipboardCheck, title: 'We review your details', text: 'A short review, and we may call you.' },
  { icon: BadgeCheck, title: 'We verify your organisation', text: 'Your registration number and an authorised contact.' },
  { icon: CreditCard, title: 'You confirm your setup', text: 'We send a quote and a payment link. Founding pilots start free.' },
  { icon: GraduationCap, title: 'We set you up', text: 'Your account, sender names and a short training for your team.' }
]

// shared look for the fields; an invalid field swaps its border and ring to red
const field = 'h-12 w-full rounded-xl border border-solid bg-white px-4 text-[.98rem] text-ink outline-none transition duration-200 placeholder:text-[#98A2B3] focus:ring-4'
const ok = 'border-[#CBD0D8] hover:border-brand-indigo/45 focus:border-brand-indigo focus:ring-brand-indigo/15'
const bad = 'border-[#E5484D] focus:border-[#E5484D] focus:ring-[#E5484D]/15'
const cls = (k: string) => [field, errors[k] ? bad : ok]
const label = 'block text-[.85rem] font-semibold text-ink'
</script>

<template>
  <section
    class="apply-band -mt-[72px] pt-[calc(72px+3.5rem)] pb-20 max-tablet:pt-[calc(72px+1.5rem)] max-tablet:pb-14">
    <div class="wrap">
      <div
        class="mx-auto grid max-w-[1040px] items-start gap-12 tablet:grid-cols-[minmax(0,.9fr)_minmax(0,1.1fr)] tablet:gap-14">

        <div>
          <p class="mb-3 font-display text-[.8rem] font-bold tracking-[.12em] text-brand-indigo uppercase">Apply</p>
          <h1 class="ap-title font-display font-bold text-ink">Start Secure Billing</h1>
          <p class="m-0 max-w-[48ch] text-[1.05rem] leading-[1.65] text-[#2D3142]">Tell us about your organisation. We
            verify every organisation before it can send, so your customers can trust every message that carries your
            name.</p>

          <ol class="m-0 mt-9 list-none p-0">
            <li v-for="(s, i) in steps" :key="s.title" class="step group relative flex gap-4 pb-7 last:pb-0">
              <span v-if="i < steps.length - 1" class="absolute top-12 bottom-1 left-[1.4rem] w-px bg-[#DAD3EE]"
                aria-hidden="true"></span>
              <span
                class="step-tile relative grid size-11 shrink-0 place-items-center rounded-2xl bg-[#EEE8FA] text-brand-indigo">
                <component :is="s.icon" class="step-icon" :size="22" :stroke-width="1.75" aria-hidden="true" />
              </span>
              <div class="pt-0.5">
                <h2 class="mb-1 font-display text-[1.02rem] leading-snug font-bold text-ink">{{ s.title }}</h2>
                <p class="m-0 text-[.93rem] leading-[1.55] text-[#2D3142]">{{ s.text }}</p>
              </div>
            </li>
          </ol>
        </div>

        <form novalidate
          class="grid gap-5 rounded-3xl border border-solid border-cloud bg-white p-6 shadow-[0_1px_2px_rgba(11,11,20,.04),0_24px_48px_-24px_rgba(74,21,164,.35)] tablet:p-8"
          @submit.prevent="submit">
          <div>
            <h2 class="mb-1 font-display text-[1.25rem] font-bold text-ink">Your organisation</h2>
            <p class="m-0 text-[.9rem] text-[#667085]">All fields are required unless marked optional.</p>
          </div>

          <label :class="label">Organisation name
            <input v-model="f.org" type="text" autocomplete="organization" :aria-invalid="!!errors.org"
              :class="[...cls('org'), 'mt-1.5']">
            <span v-if="errors.org" class="mt-1.5 flex items-center gap-1.5 text-[.82rem] font-medium text-[#B42318]"
              role="alert">
              <CircleAlert :size="15" :stroke-width="2.2" />{{ errors.org }}
            </span>
          </label>

          <label :class="label">CAC registration number
            <input v-model="f.rc" type="text" placeholder="RC 1234567" :aria-invalid="!!errors.rc"
              :class="[...cls('rc'), 'mt-1.5']">
            <span v-if="errors.rc" class="mt-1.5 flex items-center gap-1.5 text-[.82rem] font-medium text-[#B42318]"
              role="alert">
              <CircleAlert :size="15" :stroke-width="2.2" />{{ errors.rc }}
            </span>
          </label>

          <div class="grid gap-5 tablet:grid-cols-2">
            <label :class="label">Your name
              <input v-model="f.name" type="text" autocomplete="name" :aria-invalid="!!errors.name"
                :class="[...cls('name'), 'mt-1.5']">
              <span v-if="errors.name" class="mt-1.5 flex items-center gap-1.5 text-[.82rem] font-medium text-[#B42318]"
                role="alert">
                <CircleAlert :size="15" :stroke-width="2.2" />{{ errors.name }}
              </span>
            </label>
            <label :class="label">Phone
              <input v-model="f.phone" type="tel" autocomplete="tel" :aria-invalid="!!errors.phone"
                :class="[...cls('phone'), 'mt-1.5']">
              <span v-if="errors.phone"
                class="mt-1.5 flex items-center gap-1.5 text-[.82rem] font-medium text-[#B42318]" role="alert">
                <CircleAlert :size="15" :stroke-width="2.2" />{{ errors.phone }}
              </span>
            </label>
          </div>

          <label :class="label">Work email
            <input v-model="f.email" type="email" autocomplete="email" :aria-invalid="!!errors.email"
              :class="[...cls('email'), 'mt-1.5']">
            <span v-if="errors.email" class="mt-1.5 flex items-center gap-1.5 text-[.82rem] font-medium text-[#B42318]"
              role="alert">
              <CircleAlert :size="15" :stroke-width="2.2" />{{ errors.email }}
            </span>
          </label>

          <div class="grid gap-5 tablet:grid-cols-2">
            <label :class="label">What will you send?
              <span class="relative mt-1.5 block">
                <select v-model="f.use" :class="[field, ok, 'appearance-none pr-10']">
                  <option>Bills and fees</option>
                  <option>Notices and invitations</option>
                  <option>Both</option>
                </select>
                <ChevronDown class="pointer-events-none absolute top-1/2 right-3.5 -translate-y-1/2 text-[#667085]"
                  :size="18" :stroke-width="2" aria-hidden="true" />
              </span>
            </label>
            <label :class="label">People you message each month
              <span class="relative mt-1.5 block">
                <select v-model="f.volume" :class="[field, ok, 'appearance-none pr-10']">
                  <option>Under 500</option>
                  <option>500 to 1,500</option>
                  <option>1,500 to 10,000</option>
                  <option>Over 10,000</option>
                </select>
                <ChevronDown class="pointer-events-none absolute top-1/2 right-3.5 -translate-y-1/2 text-[#667085]"
                  :size="18" :stroke-width="2" aria-hidden="true" />
              </span>
            </label>
          </div>

          <label :class="label">Anything else we should know? <span class="font-normal text-[#667085]">(optional)</span>
            <textarea v-model="f.notes" rows="4"
              class="mt-1.5 w-full resize-y rounded-xl border border-solid border-[#CBD0D8] bg-white px-4 py-3 text-[.98rem] text-ink outline-none transition duration-200 hover:border-brand-indigo/45 focus:border-brand-indigo focus:ring-4 focus:ring-brand-indigo/15"></textarea>
          </label>

          <button class="btn btn-lg w-full" type="submit">Send my details</button>

          <p v-if="opened"
            class="m-0 flex items-start gap-2.5 rounded-xl bg-[#E3F4EC] p-4 text-[.9rem] leading-[1.55] text-[#0B7A52]"
            role="status">
            <Check class="mt-0.5 shrink-0" :size="18" :stroke-width="2.6" aria-hidden="true" />
            <span>Your email app should open with your application ready to send. If it did not, write to {{
              site.contactEmail }}.</span>
          </p>
        </form>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* base.css styles every h1 and sits outside Tailwind's layers, so the title size is set here to win over it */
.ap-title {
  font-size: clamp(1.9rem, 3.6vw, 2.7rem);
  line-height: 1.08;
  letter-spacing: -0.02em;
  margin: 0 0 1rem;
}

.apply-band {
  background:
    radial-gradient(55% 60% at 8% 0%, #EEE8FA 0%, rgba(238, 232, 250, 0) 70%),
    radial-gradient(45% 50% at 100% 100%, #F3EFFB 0%, rgba(243, 239, 251, 0) 70%),
    #F9FBFF;
}

/* hover: the step icon tile grows and the icon plays a short "tada" once; off for reduced motion */
.step-tile {
  transition: transform .35s cubic-bezier(.22, 1, .36, 1), background-color .35s;
}

@keyframes tada {
  0% {
    transform: scale(1) rotate(0)
  }

  10%,
  20% {
    transform: scale(.92) rotate(-4deg)
  }

  30%,
  50%,
  70% {
    transform: scale(1.12) rotate(4deg)
  }

  40%,
  60% {
    transform: scale(1.12) rotate(-4deg)
  }

  100% {
    transform: scale(1) rotate(0)
  }
}

@media (hover: hover) and (prefers-reduced-motion: no-preference) {
  .step:hover .step-tile {
    transform: scale(1.08);
    background-color: #E2D8F8;
  }

  .step:hover .step-icon {
    animation: tada .9s ease-in-out 1;
  }
}
</style>