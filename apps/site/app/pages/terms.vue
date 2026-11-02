<script setup lang="ts">
import { site } from '~/utils/site'
useHead({ title: 'Terms: EnterpriseSend' })
</script>

<template>
  <section class="legal">
    <div class="wrap narrow">
      <h1>Terms</h1>
      <p class="lead">Our terms of service is being finalised and will be published here before we onboard clients.</p>
      <p>If you have questions in the meantime, write to <a :href="`mailto:${site.contactEmail}`">{{ site.contactEmail }}</a>.</p>
    </div>
  </section>
</template>
