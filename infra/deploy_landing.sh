#!/usr/bin/env bash
# Builds the public marketing site (static) and deploys it to Cloud Run behind nginx.
#   infra/deploy_site.sh                       # staging preview, not indexed by search engines
#   INDEXABLE=true APP_URL=https://app.enterprisesend.com PROJECT=enterprisesend infra/deploy_site.sh   # production
set -euo pipefail
cd "$(dirname "$0")/.."
PROJECT="${PROJECT:-enterprisesend-staging}"
REGION="${REGION:-europe-west1}"
APP_URL="${APP_URL:-https://staging.enterprisesend.com}"
INDEXABLE="${INDEXABLE:-false}"

( cd apps/landing && npm install --no-audit --no-fund --legacy-peer-deps >/dev/null && \
  NUXT_PUBLIC_APP_URL="$APP_URL" NUXT_PUBLIC_INDEXABLE="$INDEXABLE" npx nuxt generate )

rm -rf infra/landing/public
cp -r apps/landing/.output/public infra/landing/public
trap 'rm -rf infra/landing/public' EXIT

gcloud run deploy enterprisesend-site --project "$PROJECT" --region "$REGION" \
  --source infra/landing --allow-unauthenticated \
  --min-instances 0 --max-instances 2 --memory 256Mi

echo
echo "Site address:"
gcloud run services describe enterprisesend-site --project "$PROJECT" --region "$REGION" --format='value(status.url)'
