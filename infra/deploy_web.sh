#!/usr/bin/env bash
# Builds the web app (static) and deploys it to Cloud Run behind nginx.
#   API_URL=https://enterprisesend-api-xxxx.europe-west1.run.app FIREBASE_API_KEY=... infra/deploy_web.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PROJECT="${PROJECT:-enterprisesend-staging}"
REGION="${REGION:-europe-west1}"
: "${API_URL:?Set API_URL to the address printed by deploy_api.sh}"
: "${FIREBASE_API_KEY:?Set FIREBASE_API_KEY to the browser API key of the project}"

( cd apps/web && \
  NUXT_PUBLIC_API_BASE="$API_URL" \
  NUXT_PUBLIC_FIREBASE_API_KEY="$FIREBASE_API_KEY" \
  NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN="${PROJECT}.firebaseapp.com" \
  NUXT_PUBLIC_FIREBASE_PROJECT_ID="$PROJECT" \
  NUXT_PUBLIC_USE_EMULATOR=false \
  NUXT_PUBLIC_REQUIRE_MFA="${REQUIRE_MFA:-false}" \
  npx nuxt generate )

rm -rf infra/web/public
cp -r apps/web/.output/public infra/web/public
trap 'rm -rf infra/web/public' EXIT

gcloud run deploy enterprisesend-web --project "$PROJECT" --region "$REGION" \
  --source infra/web --allow-unauthenticated \
  --min-instances 0 --max-instances 2 --memory 256Mi

echo
echo "Web address:"
gcloud run services describe enterprisesend-web --project "$PROJECT" --region "$REGION" --format='value(status.url)'
