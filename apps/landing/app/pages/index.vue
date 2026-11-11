<script setup lang="ts">
useHead({ title: 'EnterpriseSend: verified billing, fast payments, no arguments' })

onMounted(() => {
  const spine = document.querySelector('.spine') as HTMLElement | null
  if (!spine) return
  const nodes = Array.from(spine.querySelectorAll<HTMLElement>('.node'))
  const segs = Array.from(spine.querySelectorAll<HTMLElement>('.seg'))
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  let queued = false
  const update = () => {
    queued = false
    const line = window.innerHeight * 0.62
    segs.forEach((s) => {
      const r = s.getBoundingClientRect()
      const p = reduce ? 1 : Math.max(0, Math.min(1, (line - r.top) / r.height))
      s.style.setProperty('--p', String(p))
    })
    nodes.forEach((n) => {
      const r = n.getBoundingClientRect()
      n.classList.toggle('lit', reduce || r.top + r.height / 2 < line)
    })
  }
  const onScroll = () => { if (!queued) { queued = true; requestAnimationFrame(update) } }
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onScroll)
  update()
  onBeforeUnmount(() => { window.removeEventListener('scroll', onScroll); window.removeEventListener('resize', onScroll) })
})
</script>

<template>
  <div>
    <HeroSection />
    <Problem />
    <Howitworks />
    <Steps />





    <section class="who-for">
      <div class="wrap">
        <h2>Built for organisations that bill or notify many people</h2>
        <dl class="rows">
          <div>
            <dt>Estates and property managers</dt>
            <dd>Service charges, levies and power tokens, with reminders.</dd>
          </div>
          <div>
            <dt>Schools</dt>
            <dd>Term fees, deadlines and receipts for parents.</dd>
          </div>
          <div>
            <dt>Clinics and professional practices</dt>
            <dd>Invoices, follow-up payments and appointment notices.</dd>
          </div>
          <div>
            <dt>Associations and event organisers</dt>
            <dd>Dues, meeting notices and invitations to a verified list.</dd>
          </div>
          <div>
            <dt>Utilities and fintechs</dt>
            <dd>High-volume bills and receipts with a full audit trail.</dd>
          </div>
        </dl>
      </div>
    </section>



    <section id="faq" class="faq">
      <div class="wrap narrow">
        <h2>Questions</h2>
        <details>
          <summary>Do we need our own SMS or WhatsApp account?</summary>
          <p>No. We send through approved providers on your behalf, and set up your sender names as part of onboarding.
          </p>
        </details>
        <details>
          <summary>Who can use EnterpriseSend?</summary>
          <p>Registered organisations that pass our verification. This keeps the network trustworthy for everyone who
            receives a message.</p>
        </details>
        <details>
          <summary>What can we send?</summary>
          <p>Bills, receipts, reminders, notices and invitations to people you have a relationship with. Unsolicited
            promotion and misleading messages are not allowed.</p>
        </details>
        <details>
          <summary>How long does it take to start?</summary>
          <p>That depends on sender-name and WhatsApp approvals, which are outside our control. We give you a date after
            your application is reviewed.</p>
        </details>
        <details>
          <summary>Can people opt out?</summary>
          <p>Yes. Every message includes an opt-out, and we stop messaging anyone who asks.</p>
        </details>
        <details>
          <summary>How is personal data handled?</summary>
          <p>We process your customers' data only on your instructions, under a data processing agreement we sign with
            you. Each client's data is kept separate.</p>
        </details>
        <details>
          <summary>What happens if a message fails?</summary>
          <p>You see which channel failed for which customer, and your wallet is not charged for messages that fail.</p>
        </details>
      </div>
    </section>

    <section class="closing">
      <div class="wrap closing-row">
        <svg class="closing-mark" viewBox="0 0 200 60" aria-hidden="true">
          <g fill="none" stroke="#B48CFF" stroke-width="6">
            <circle cx="14" cy="30" r="11" />
            <path d="M26 30H41" />
            <circle cx="56" cy="30" r="11" />
            <path d="M68 30H83" />
            <circle cx="98" cy="30" r="11" />
            <path d="M110 30H142" />
          </g>
          <circle cx="170" cy="30" r="30" fill="#B48CFF" />
          <path d="M157 31L166 40L184 20" fill="none" stroke="#0B0B14" stroke-width="7" stroke-linecap="round"
            stroke-linejoin="round" />
        </svg>
        <div>
          <h2>Ready to send with confidence?</h2>
          <p>Tell us about your organisation. We review every application ourselves.</p>
          <NuxtLink to="/apply" class="btn btn-light btn-lg">Start Secure Billing</NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>
