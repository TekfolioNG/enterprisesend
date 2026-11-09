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

    <section class="problem">
      <div class="wrap">
        <h2 class="sr-only">The problem</h2>
        <p class="big">Bills go out, and nobody can say who received them.</p>
        <p class="big">Payments arrive as bank transfers, and someone matches them by hand.</p>
        <p class="big">Customers ignore messages from senders they do not recognise.</p>
        <p class="after">EnterpriseSend handles all three in one flow, from upload to receipt.</p>
      </div>
    </section>

    <section id="how" class="how">
      <div class="wrap">
        <h2>From billing file to receipt in four steps</h2>
        <div class="spine">
          <article class="stage">
            <div class="node"><span></span></div><div class="seg"></div>
            <div class="stage-body">
              <div class="stage-text">
                <h3>Upload your billing file</h3>
                <p>Download our template, fill it in and upload it. Mistakes such as a wrong phone number are caught and shown row by row, before anything is sent.</p>
              </div>
              <div class="mock" aria-hidden="true">
                <div class="mock-row mock-head"><span>Customer</span><span>Phone</span><span>Amount</span></div>
                <div class="mock-row"><span>Ada Obi</span><span>234801 234 5678</span><span>₦50,000</span></div>
                <div class="mock-row bad"><span>Tunde Bello</span><span>0801 23</span><span>₦50,000</span></div>
                <div class="mock-flag">Row 3: phone number must start with 234 and have 13 digits.</div>
              </div>
            </div>
          </article>

          <article class="stage">
            <div class="node"><span></span></div><div class="seg"></div>
            <div class="stage-body">
              <div class="stage-text">
                <h3>A second person approves</h3>
                <p>The person who uploads a batch cannot approve it. A manager checks the total and a sample message, then approves. Nothing is sent before that.</p>
              </div>
              <div class="mock" aria-hidden="true">
                <div class="who"><b>Prepared by</b><span>Ada, billing officer</span></div>
                <div class="who"><b>Approved by</b><span>Tunde, finance manager</span></div>
                <div class="chip ok">Approved. Ready to send.</div>
              </div>
            </div>
          </article>

          <article class="stage">
            <div class="node"><span></span></div><div class="seg"></div>
            <div class="stage-body">
              <div class="stage-text">
                <h3>Messages go out on every channel</h3>
                <p>Each customer gets the bill by SMS, WhatsApp and email, with a personal payment link. Opt-outs are respected, and you see the result per customer.</p>
              </div>
              <div class="mock" aria-hidden="true">
                <div class="chan"><span>SMS</span><em>Sent</em></div>
                <div class="chan"><span>WhatsApp</span><em>Sent</em></div>
                <div class="chan"><span>Email</span><em>Sent</em></div>
                <div class="mock-note">Messages that fail are not charged to your wallet.</div>
              </div>
            </div>
          </article>

          <article class="stage final">
            <div class="node disc"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12.5l4 4 8-9" /></svg></div>
            <div class="stage-body">
              <div class="stage-text">
                <h3>Payment is matched and receipted</h3>
                <p>When a customer pays, the payment is matched to the right bill and a receipt is sent. Every upload, approval, send and payment is written to an activity log that shows any later change.</p>
              </div>
              <div class="mock" aria-hidden="true">
                <div class="receipt"><b>₦50,000</b><span>Ada Obi, Q4 service charge</span></div>
                <div class="chip ok">Matched to the bill</div>
                <div class="mock-note">Receipt sent by email and WhatsApp. Recorded in the activity log.</div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="difference">
      <div class="wrap">
        <h2>What is different from a bulk SMS tool</h2>
        <div class="table-wrap">
          <table>
            <thead><tr><th scope="col"></th><th scope="col">Typical bulk SMS tools</th><th scope="col">EnterpriseSend</th></tr></thead>
            <tbody>
              <tr><th scope="row">Who can send</th><td>Anyone with a card</td><td>Organisations we have verified</td></tr>
              <tr><th scope="row">Before sending</th><td>You hope the file is right</td><td>The file is checked, then a second person approves</td></tr>
              <tr><th scope="row">Getting paid</th><td>A phone number or account to transfer to</td><td>A personal payment link per customer, matched automatically</td></tr>
              <tr><th scope="row">The record</th><td>A delivery report</td><td>An activity log of uploads, approvals, sends and payments</td></tr>
              <tr><th scope="row">Channels</th><td>SMS</td><td>SMS, WhatsApp and email</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="who-for">
      <div class="wrap">
        <h2>Built for organisations that bill or notify many people</h2>
        <dl class="rows">
          <div><dt>Estates and property managers</dt><dd>Service charges, levies and power tokens, with reminders.</dd></div>
          <div><dt>Schools</dt><dd>Term fees, deadlines and receipts for parents.</dd></div>
          <div><dt>Clinics and professional practices</dt><dd>Invoices, follow-up payments and appointment notices.</dd></div>
          <div><dt>Associations and event organisers</dt><dd>Dues, meeting notices and invitations to a verified list.</dd></div>
          <div><dt>Utilities and fintechs</dt><dd>High-volume bills and receipts with a full audit trail.</dd></div>
        </dl>
      </div>
    </section>

    <section id="security" class="security">
      <div class="wrap">
        <h2>Trust is the product</h2>
        <p class="lead">Customers act on a message only when they believe it. We protect that belief at the source.</p>
        <dl class="rows rows-wide">
          <div><dt>Verified before access</dt><dd>We check each organisation's registration before it can send. Fraudsters cannot sign up with a card.</dd></div>
          <div><dt>Two-step sign-in</dt><dd>Staff sign in with a password and a code from an authenticator app.</dd></div>
          <div><dt>Your data stays apart</dt><dd>Each client's records are kept separate from every other client's, and tested that way.</dd></div>
          <div><dt>A record that shows tampering</dt><dd>Each entry in the activity log is chained to the one before, so a later change is detectable.</dd></div>
          <div><dt>Opt-out in every message</dt><dd>People can stop messages at any time, and we honour it.</dd></div>
          <div><dt>Built on Google Cloud</dt><dd>Hosted on Google Cloud infrastructure, with secrets kept out of code.</dd></div>
        </dl>
      </div>
    </section>

    <section id="pricing" class="pricing">
      <div class="wrap">
        <h2>How you pay</h2>
        <dl class="rows">
          <div><dt>Setup and verification</dt><dd>A one-time fee covers checking your organisation, setting up your account and sender names, and training your team.</dd></div>
          <div><dt>Messaging wallet</dt><dd>Top up in advance and pay only for the messages you send.</dd></div>
          <div><dt>Collections</dt><dd>A small commission on payments collected through your payment links.</dd></div>
        </dl>
        <p class="after">We quote after a short call, based on your size and how often you bill.</p>
        <NuxtLink to="/apply" class="btn">Talk to us</NuxtLink>
      </div>
    </section>

    <section id="faq" class="faq">
      <div class="wrap narrow">
        <h2>Questions</h2>
        <details><summary>Do we need our own SMS or WhatsApp account?</summary><p>No. We send through approved providers on your behalf, and set up your sender names as part of onboarding.</p></details>
        <details><summary>Who can use EnterpriseSend?</summary><p>Registered organisations that pass our verification. This keeps the network trustworthy for everyone who receives a message.</p></details>
        <details><summary>What can we send?</summary><p>Bills, receipts, reminders, notices and invitations to people you have a relationship with. Unsolicited promotion and misleading messages are not allowed.</p></details>
        <details><summary>How long does it take to start?</summary><p>That depends on sender-name and WhatsApp approvals, which are outside our control. We give you a date after your application is reviewed.</p></details>
        <details><summary>Can people opt out?</summary><p>Yes. Every message includes an opt-out, and we stop messaging anyone who asks.</p></details>
        <details><summary>How is personal data handled?</summary><p>We process your customers' data only on your instructions, under a data processing agreement we sign with you. Each client's data is kept separate.</p></details>
        <details><summary>What happens if a message fails?</summary><p>You see which channel failed for which customer, and your wallet is not charged for messages that fail.</p></details>
      </div>
    </section>

    <section class="closing">
      <div class="wrap closing-row">
        <svg class="closing-mark" viewBox="0 0 200 60" aria-hidden="true">
          <g fill="none" stroke="#B48CFF" stroke-width="6"><circle cx="14" cy="30" r="11"/><path d="M26 30H41"/><circle cx="56" cy="30" r="11"/><path d="M68 30H83"/><circle cx="98" cy="30" r="11"/><path d="M110 30H142"/></g>
          <circle cx="170" cy="30" r="30" fill="#B48CFF"/><path d="M157 31L166 40L184 20" fill="none" stroke="#0B0B14" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
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
