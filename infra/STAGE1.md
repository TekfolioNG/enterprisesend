# Stage 1: put the app on its real address and finish the staging check

Addresses
- Staging app:    https://staging.enterprisesend.com   (project enterprisesend-staging)
- Production:     https://app.enterprisesend.com        (project enterprisesend, later)
- Marketing site: https://enterprisesend.com            (Stage 2)
tekfolio.ng (registered at TrueHost, Workspace email) is deliberately NOT used here, so its DNS and email are untouched.
Do not use TrueHost's "Cloudflare DNS Push" for now: it changes nameservers and can break MX records.

## A. Check the base domain is verified for the gcloud account
`gcloud domains list-user-verified` must list enterprisesend.com.
If not: Google Search Console > Add property > Domain > enterprisesend.com, signed in as kelvinkeshi@tekfolio.ng.
Add the TXT record in Cloudflare (DNS only), press Verify, and check the list again.

## B. Map the domain
`infra/map_domain.sh staging.enterprisesend.com enterprisesend-web`
Add the printed record in Cloudflare (normally CNAME `staging` -> `ghs.googlehosted.com`), proxy OFF (grey cloud).
Wait for the certificate (minutes to a few hours):
`gcloud beta run domain-mappings describe --domain staging.enterprisesend.com --region europe-west1 --project enterprisesend-staging`

## C. Tell the pieces about the new address
1. `gcloud run services update enterprisesend-api --project enterprisesend-staging --region europe-west1 --update-env-vars WEB_ORIGIN=https://staging.enterprisesend.com`
2. Identity Platform > Settings > Authorized domains: add `staging.enterprisesend.com`.
3. Browser API key (Credentials): restrict to websites `https://staging.enterprisesend.com/*`, and to the Identity Toolkit and Token Service APIs.

## D. Check it
`API_URL=<api address> WEB_URL=https://staging.enterprisesend.com infra/check_staging.sh`

## E. Two-step sign-in on the real site
`infra/enable_totp.sh`, then create users with `scripts/create_user.py` (marks emails verified).
Sign in at https://staging.enterprisesend.com, open Security, scan the QR code, enter the code.
Sign out and in again: the code step must appear.
When every staff member is enrolled: `REQUIRE_MFA=true infra/deploy_api.sh` and
`REQUIRE_MFA=true API_URL=... FIREBASE_API_KEY=... infra/deploy_web.sh`.

## F. Template download
Click Download template on the real site. If it fails:
`gcloud run services logs read enterprisesend-api --project enterprisesend-staging --region europe-west1 --limit 30`
and send the lines around any Traceback.

Note: Cloud Run domain mapping is a Preview feature. Fine for staging. For production, plan a global load balancer
(with Cloud Armor) once the first client pays.
