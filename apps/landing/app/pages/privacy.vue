<script setup lang="ts">
import { Ban, BellOff, UserCog } from 'lucide-vue-next'
import { site } from '~/utils/config'
useHead({ title: 'Privacy: EnterpriseSend' })

const highlights = [
  { title: 'Never sold', text: 'We do not sell personal data, and we never use your customers\u2019 data for advertising.', icon: Ban },
  { title: 'You stay in control', text: 'For the files you upload, you decide the purpose. We process them only on your instructions.', icon: UserCog },
  { title: 'Opt-outs honoured', text: 'Every message carries a way to opt out, and we stop messaging that contact.', icon: BellOff }
]
// Edit the text here. Anything in [square brackets] is a placeholder and shows highlighted on the page.
// Have a Nigerian data-protection lawyer review this before launch.
const sections = [
  {
    id: 'who', title: 'Who we are',
    blocks: [
      'EnterpriseSend is operated by [Legal entity operating EnterpriseSend], a company registered in Nigeria ([CAC registration number]), with its office at [Registered address]. In this policy, "we" and "us" mean that company.',
      'EnterpriseSend lets organizations send verified bills and receipts to their customers and match the payments they receive.'
    ]
  },
  {
    id: 'roles', title: 'Our role and yours',
    blocks: [
      'For the account details of the people who use EnterpriseSend, and for how we run and secure the service, we are the data controller.',
      'For the billing files you upload, including your customers’ names, phone numbers, email addresses, amounts and account references, you are the data controller and we are your data processor. We handle that data only on your instructions, under our data processing agreement, which is available on request.'
    ]
  },
  {
    id: 'collect', title: 'What we collect',
    blocks: [
      {
        ul: [
          'Account data: your name, work email, phone number, role and sign-in details.',
          'Verification data: your organization’s name, CAC registration number and authorized contact.',
          'Billing data you upload: recipient names, contact details, amounts, descriptions and due dates.',
          'Payment data: payment references, amounts and status, received from our payment partner. We do not store card numbers.',
          'Delivery and activity data: which messages were sent, their status, and a record of actions taken in your account.',
          'Technical data: device and browser information, IP address and error logs.'
        ]
      }
    ]
  },
  {
    id: 'use', title: 'How we use it',
    blocks: [
      {
        ul: [
          'To provide the service: checking files, sending messages, creating payment links, matching payments and issuing receipts.',
          'To verify organizations and prevent fraud and misuse.',
          'To keep the service secure, reliable and auditable.',
          'To contact you about your account, billing and service changes.',
          'To meet legal obligations.'
        ]
      },
      'We do not sell personal data, and we do not use your customers’ data for advertising.'
    ]
  },
  {
    id: 'basis', title: 'Lawful basis',
    blocks: [
      'We rely on performance of our contract with you, our legitimate interests in running and securing the service, compliance with legal obligations and, where required, consent. You are responsible for having a lawful basis, such as an existing billing relationship or consent, to contact the people in the files you upload.'
    ]
  },
  {
    id: 'share', title: 'Who we share it with',
    blocks: [
      'We share data only with service providers that help us deliver EnterpriseSend, under written terms that protect it:',
      {
        ul: [
          'Google Cloud, for hosting and storage. Data is stored in Belgium.',
          'Our payment partner, for payment processing.',
          'Messaging providers, for SMS and WhatsApp delivery.',
          'An email delivery provider, for email.',
          '[Other providers, for example analytics or support tools].'
        ]
      },
      'We may also disclose data when the law requires it or to protect the rights and safety of our users and the public.'
    ]
  },
  {
    id: 'transfers', title: 'Where data goes',
    blocks: [
      'Our primary data is stored in the European Union. Some providers process data in other countries. Where data leaves Nigeria, we use safeguards that meet the Nigeria Data Protection Act, such as contractual protections. [Confirm provider locations and safeguards.]'
    ]
  },
  {
    id: 'retention', title: 'How long we keep it',
    blocks: [
      'We keep account data while your account is open and for [retention period] afterwards. Billing files and message records are kept for [retention period] so you can reconcile and audit, then deleted or anonymized. Activity logs are kept for [retention period] because their value depends on being complete. Some records may be kept longer where the law requires.'
    ]
  },
  {
    id: 'security', title: 'How we protect it',
    blocks: [
      'We separate each organization’s data, require two-step sign-in, encrypt data in transit and at rest, and record actions in a tamper-evident log. See our Security page for details. No system is perfectly secure, and we will notify you and the regulator where the law requires after a breach.'
    ]
  },
  {
    id: 'rights', title: 'Your rights',
    blocks: [
      'Under the Nigeria Data Protection Act, you can ask to access, correct, delete or restrict the use of your personal data, object to its processing, and receive a copy in a portable format. You can withdraw consent at any time.',
      'If you received a message through EnterpriseSend and want to exercise these rights over data in a billing file, contact the organization that sent it. We will help them respond. To exercise rights over your own account data, write to us.'
    ]
  },
  {
    id: 'optout', title: 'Message opt-outs',
    blocks: [
      'Every message carries a way to opt out. Reply STOP and we stop messaging that contact on behalf of every organization using EnterpriseSend.'
    ]
  },
  {
    id: 'cookies', title: 'Cookies',
    blocks: [
      'We use only the cookies and similar storage needed to sign you in and keep the service secure. [Update this section if you add analytics.]'
    ]
  },
  {
    id: 'children', title: 'Children',
    blocks: [
      'EnterpriseSend is for organizations and is not directed at children. Billing files may include the names of parents or guardians; they should not include children’s personal data beyond what a bill requires.'
    ]
  },
  {
    id: 'changes', title: 'Changes to this policy',
    blocks: [
      'We will post updates on this page and, for material changes, tell account holders by email before they take effect.'
    ]
  },
  {
    id: 'contact', title: 'Contact and complaints',
    blocks: [
      `Write to us at ${site.contactEmail}. Our data protection contact is [Name or title]. You also have the right to complain to the Nigeria Data Protection Commission.`
    ]
  }
]
</script>

<template>
  <LegalDoc kicker="Legal" title="Privacy policy"
    lead="How EnterpriseSend collects, uses and protects personal data, for the people who use it and the customers they bill."
    updated="[Effective date]" :sections="sections" :highlights="highlights">
    <template #art>
      <PrivacyArt />
    </template>
  </LegalDoc>
</template>