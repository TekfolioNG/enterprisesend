# Staging deployment (project enterprisesend-staging, region europe-west1)

Run from the repo root. Staging runs WITHOUT MFA until the MFA screen exists: use test data only.

0. Console > Billing > Budgets: a $10 budget with alerts at 50%, 80%, 100%.
1. `chmod +x infra/*.sh && infra/bootstrap_staging.sh`
2. Console > Identity Platform: enable it, add the Email/Password provider.
   Console > APIs & Services > Credentials: copy the "Browser key" value (restrict it later to your web address).
3. Secrets (optional now, hidden prompt): `infra/set_secret.sh paystack-secret-key` (also termii-api-key, sendgrid-api-key)
4. `infra/deploy_api.sh`  -> prints the API address
5. `API_URL=<api address> FIREBASE_API_KEY=<browser key> infra/deploy_web.sh`  -> prints the web address
6. Point the API at the web address (CORS), and allow it to sign in:
   `gcloud run services update enterprisesend-api --region europe-west1 --update-env-vars WEB_ORIGIN=<web address>`
   Console > Identity Platform > Settings > Authorized domains: add the web address's host name.
7. Create users (no emulator variables in this shell):
   `cd services/api && source .venv/bin/activate`
   `GOOGLE_CLOUD_PROJECT=enterprisesend-staging python scripts/create_user.py you@tekfolio.ng demo-client maker`
   (repeat for a checker and an admin with different emails)
8. Lock Firestore against browsers: `firebase login --no-localhost` then
   `firebase deploy --only firestore:rules --project enterprisesend-staging --config infra/firebase.json`
9. Paystack dashboard (test mode): webhook URL = <api address>/webhooks/paystack


## Two-step sign-in (authenticator app)
1. `infra/enable_totp.sh` (once per project). Identity Platform must be enabled.
2. Re-run `scripts/create_user.py` for each staff user: it now marks the email verified, which MFA requires.
3. Each user signs in, opens Security, and scans the QR code with an authenticator app.
4. When everyone is enrolled, enforce it:
   `REQUIRE_MFA=true infra/deploy_api.sh` then `REQUIRE_MFA=true API_URL=... FIREBASE_API_KEY=... infra/deploy_web.sh`
   Production always enforces it, whatever this variable says.
