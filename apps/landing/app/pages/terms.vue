<script setup lang="ts">
import { BadgeCheck, UserCheck, WalletCards } from 'lucide-vue-next'
import { site } from '~/utils/config'
useHead({ title: 'Terms: EnterpriseSend' })

const highlights = [
  { title: 'Verified organizations', text: 'We verify every organization before it can send to real recipients.', icon: BadgeCheck },
  { title: 'Prepaid and transparent', text: 'Messages are paid from a wallet you fund, and the cost is shown before you send.', icon: WalletCards },
  { title: 'Approval by default', text: 'A second person approves each batch, unless you choose otherwise.', icon: UserCheck }
]
// Edit the text here. Anything in [square brackets] is a placeholder and shows highlighted on the page.
// Have a Nigerian commercial lawyer review this before launch, especially fees, liability and governing law.
const sections = [
  {
    id: 'agreement', title: 'Agreement',
    blocks: [
      'These terms are a contract between [Legal entity operating EnterpriseSend] ("EnterpriseSend", "we") and the organization that opens an account ("you"). By creating an account or using the service, you agree to them and to our Privacy policy. If you accept for an organization, you confirm you have authority to bind it.'
    ]
  },
  {
    id: 'service', title: 'The service',
    blocks: [
      'EnterpriseSend lets verified organizations upload billing files, check them, preview and approve messages, send them by SMS, WhatsApp and email with payment links, match incoming payments to bills and issue receipts. We may improve or change features over time.'
    ]
  },
  {
    id: 'eligibility', title: 'Eligibility and verification',
    blocks: [
      'The service is for organizations registered in Nigeria. Before you can send to real recipients, we verify your organization, including your CAC registration, an authorized contact and your sender name. You must give us accurate information and keep it current. We may decline or withdraw verification at our discretion where the law or risk requires.'
    ]
  },
  {
    id: 'accounts', title: 'Accounts and security',
    blocks: [
      'You are responsible for the people you give access to and for activity in your account. Keep sign-in details and two-step verification devices secure and tell us promptly about suspected misuse.',
      'Batches are approved by a second person by default. If you choose to let a person approve their own batches, you accept responsibility for that choice, and we record it in your activity log.'
    ]
  },
  {
    id: 'content', title: 'Your data and recipients',
    blocks: [
      'You own the billing data you upload and give us permission to process it to provide the service. You confirm that you have a lawful basis to contact each recipient, that the information is accurate, and that you will honour opt-outs. We process recipient data as your processor, as described in our Privacy policy.'
    ]
  },
  {
    id: 'use', title: 'Acceptable use',
    blocks: [
      'You must not use EnterpriseSend to:',
      {
        ul: [
          'send spam, deceptive, harassing or unlawful messages;',
          'impersonate another person or organization, or use a sender name you are not entitled to use;',
          'bill for goods or services that do not exist, or collect money fraudulently;',
          'upload data you have no right to use;',
          'probe, disrupt or bypass the security of the service.'
        ]
      },
      'We may suspend sending or an account immediately where we reasonably believe these rules are broken.'
    ]
  },
  {
    id: 'fees', title: 'Fees and wallet',
    blocks: [
      'Fees are described on our Pricing page and in your order. Messages are paid from a prepaid wallet at the provider’s cost plus [markup]. A collection commission of [commission rate], capped at [cap] per payment, applies to payments made through your links, unless your agreement says otherwise. Setup and verification fees are [setup fee terms].',
      'Wallet balances are used only for messaging. [State refund and expiry terms for unused balances.] A failed message is refunded to your wallet. Fees exclude taxes, which are added where they apply.'
    ]
  },
  {
    id: 'payments', title: 'Payments',
    blocks: [
      'Payments from your customers are processed by our payment partner, Paystack, under its own terms. [Describe settlement: how and when collected funds reach your account, and any fees deducted.] We match payments using the reference on each payment link and do not guarantee that a customer will pay.'
    ]
  },
  {
    id: 'delivery', title: 'Message delivery',
    blocks: [
      'We send messages through third-party providers and carriers. A status of "sent" means a provider accepted the message. Delivery depends on networks, devices and recipient settings, so we cannot guarantee that any message will be delivered or read. Where delivery receipts are available, we show them.'
    ]
  },
  {
    id: 'availability', title: 'Availability',
    blocks: [
      'We work to keep the service available and will give notice of planned maintenance where we can. We do not promise uninterrupted service. [Add a service level only if you intend to offer one.]'
    ]
  },
  {
    id: 'ip', title: 'Our property',
    blocks: [
      'EnterpriseSend, its software, design and branding belong to us or our licensors. We give you a limited, non-exclusive right to use the service for your own organization while these terms apply. You may not copy, resell or reverse-engineer it.'
    ]
  },
  {
    id: 'liability', title: 'Liability',
    blocks: [
      'The service is provided "as is" to the extent the law permits. We are not liable for indirect or consequential losses, lost profit or lost revenue. Our total liability for any claim is limited to the fees you paid us in the [12] months before the claim. Nothing in these terms limits liability that cannot be limited by law. [Lawyer to confirm.]'
    ]
  },
  {
    id: 'indemnity', title: 'Your responsibility',
    blocks: [
      'You will cover losses we suffer from claims arising from your breach of these terms, the content of your messages, or your failure to have a lawful basis to contact recipients.'
    ]
  },
  {
    id: 'termination', title: 'Ending the agreement',
    blocks: [
      'You may close your account at any time. We may suspend or end your access for breach, legal or security reasons, or non-payment. On closure we handle your data as set out in our Privacy policy, and sections that by their nature continue will continue.'
    ]
  },
  {
    id: 'law', title: 'Governing law',
    blocks: [
      'These terms are governed by the laws of the Federal Republic of Nigeria. The courts of [Lagos State, or arbitration seat] have jurisdiction.'
    ]
  },
  {
    id: 'changes', title: 'Changes',
    blocks: [
      'We may update these terms. We will give account holders reasonable notice of material changes by email or in the product. Continuing to use the service after the change takes effect means you accept it.'
    ]
  },
  {
    id: 'contact', title: 'Contact',
    blocks: [
      `Write to us at ${site.contactEmail}, or at [Registered address].`
    ]
  }
]
</script>

<template>
  <LegalDoc kicker="Legal" title="Terms of service"
    lead="The agreement between EnterpriseSend and the organizations that use it to bill and collect."
    updated="[Effective date]" :sections="sections" :highlights="highlights">
    <template #art>
      <TermsArt />
    </template>
  </LegalDoc>
</template>