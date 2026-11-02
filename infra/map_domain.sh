#!/usr/bin/env bash
# Maps a custom domain to a Cloud Run service (Cloud Run domain mapping, Preview, available in europe-west1).
#   infra/map_domain.sh staging.enterprisesend.com enterprisesend-web
# The base domain (tekfolio.ng) must be verified for your Google account first (see infra/STAGE1.md).
set -euo pipefail
DOMAIN="${1:?usage: infra/map_domain.sh DOMAIN SERVICE}"
SERVICE="${2:?usage: infra/map_domain.sh DOMAIN SERVICE}"
PROJECT="${PROJECT:-enterprisesend-staging}"
REGION="${REGION:-europe-west1}"
BASE="$(echo "$DOMAIN" | awk -F. '{print $(NF-1)"."$NF}')"   # fine for enterprisesend.com and tekfolio.ng

if ! gcloud domains list-user-verified 2>/dev/null | grep -qi "$BASE"; then
  echo "The base domain $BASE is not verified for your Google account yet."
  echo "Verify it in Google Search Console (DNS TXT record at whoever hosts the DNS), then run this again."
  exit 1
fi

gcloud beta run domain-mappings create --service "$SERVICE" --domain "$DOMAIN" \
  --region "$REGION" --project "$PROJECT"

echo
echo "Add the DNS record(s) below in Cloudflare, with the proxy OFF (grey cloud, 'DNS only'):"
gcloud beta run domain-mappings describe --domain "$DOMAIN" --region "$REGION" --project "$PROJECT" \
  --format="yaml(status.resourceRecords,status.conditions)"
echo
echo "The HTTPS certificate is issued after the record resolves, which can take from minutes to a few hours."
echo "Check progress with: gcloud beta run domain-mappings describe --domain $DOMAIN --region $REGION --project $PROJECT"
