#!/usr/bin/env bash
# Builds and deploys the API to Cloud Run (staging).
set -euo pipefail
cd "$(dirname "$0")/.."
PROJECT="${PROJECT:-enterprisesend-staging}"
REGION="${REGION:-europe-west1}"
SA_EMAIL="es-api@${PROJECT}.iam.gserviceaccount.com"
BUCKET="${PROJECT}-uploads"
WEB_ORIGIN="${WEB_ORIGIN:-https://staging.enterprisesend.com}"

# The container build only sees services/api, so ship the shared settings file inside it.
cp settings/app.json services/api/app_settings.json
trap 'rm -f services/api/app_settings.json' EXIT

ENVVARS="ENVIRONMENT=staging,GOOGLE_CLOUD_PROJECT=${PROJECT},UPLOAD_BUCKET=${BUCKET},WEB_ORIGIN=${WEB_ORIGIN},APP_SETTINGS_FILE=/app/app_settings.json,REQUIRE_MFA=${REQUIRE_MFA:-false}"
[ -n "${TERMII_SENDER_ID:-}" ] && ENVVARS="${ENVVARS},TERMII_SENDER_ID=${TERMII_SENDER_ID}"

SECRETS=""
for pair in TERMII_API_KEY:termii-api-key SENDGRID_API_KEY:sendgrid-api-key PAYSTACK_SECRET_KEY:paystack-secret-key; do
  var="${pair%%:*}"; name="${pair##*:}"
  if gcloud secrets describe "$name" --project "$PROJECT" >/dev/null 2>&1; then
    SECRETS="${SECRETS:+$SECRETS,}${var}=${name}:latest"
  else
    echo "Note: secret '$name' not set yet, so ${var} will be empty."
  fi
done

gcloud run deploy enterprisesend-api --project "$PROJECT" --region "$REGION" \
  --source services/api --service-account "$SA_EMAIL" --allow-unauthenticated \
  --min-instances 0 --max-instances 2 --memory 512Mi \
  --set-env-vars "$ENVVARS" ${SECRETS:+--set-secrets "$SECRETS"}

echo
echo "API address:"
gcloud run services describe enterprisesend-api --project "$PROJECT" --region "$REGION" --format='value(status.url)'
