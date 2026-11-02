<!-- components/herovisuals.vue -->
<template>
  <div class="hero-visual" aria-hidden="true">
    <div class="msg">
      <div class="msg-from">
        <span class="badge-v"></span> Silverwood Estate
        <span class="verified">Verified sender</span>
      </div>
      <p>Dear Adaeze Ishola, your service charge for December, 202X is due. Pay securely with your personal link.
        Reply STOP to opt out.</p>
      <div class="msg-link">Pay securely</div>
    </div>

    <svg class="path" viewBox="0 0 200 60" role="img" aria-label="">
      <g fill="none" stroke="#FFFFFF" stroke-width="6">
        <circle class="n n1" cx="14" cy="30" r="11" />
        <path class="n n1" d="M26 30H41" />
        <circle class="n n2" cx="56" cy="30" r="11" />
        <path class="n n2" d="M68 30H83" />
        <circle class="n n3" cx="98" cy="30" r="11" />
        <path class="n n3" d="M110 30H142" />
      </g>
      <!-- The background circle ring system driven by GSAP parameters -->
      <circle class="disc" cx="170" cy="30" r="30" fill="#FFFFFF" />
      <path class="tick" d="M157 31L166 40L184 20" fill="none" stroke="#4A15A4" stroke-width="7" stroke-linecap="round"
        stroke-linejoin="round" />
    </svg>

    <!-- Changed transaction string to Payment Completed with custom styling overrides applied below -->
    <div class="matched">
      <span class="dot"></span> Payment Completed. Receipt sent.
    </div>
  </div>
</template>

<style scoped>
/* Target styling variables to ensure uniform brand contrast alignment */
.matched {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 700;
  color: #0B7A52;
  /* Verified Green Token Color */
  background-color: #E3F4EC;
  padding: 0.5rem 1rem;
  border-radius: 22px;
  border: 1px solid #BFE6D3;
}

/* Recolor the bubble indicator dot from native navy to match deep brand indigo circle patterns */
.matched .dot {
  width: 8px;
  height: 8px;
  background-color: #4A15A4;
  /* Core Brand Indigo */
  border-radius: 50%;
  display: inline-block;
}
</style>
