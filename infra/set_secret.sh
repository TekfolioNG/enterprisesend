#!/usr/bin/env bash
# Stores one secret in Secret Manager. The value is typed hidden: it never touches your shell history.
#   infra/set_secret.sh termii-api-key | sendgrid-api-key | paystack-secret-key
set -euo pipefail
NAME="${1:?usage: infra/set_secret.sh SECRET_NAME}"
PROJECT="${PROJECT:-enterprisesend-staging}"
REGION="${REGION:-europe-west1}"
read -r -s -p "Value for ${NAME} (hidden): " VALUE; echo
[ -n "$VALUE" ] || { echo "Empty value, nothing stored."; exit 1; }
gcloud secrets describe "$NAME" --project "$PROJECT" >/dev/null 2>&1 || \
  gcloud secrets create "$NAME" --project "$PROJECT" --replication-policy=user-managed --locations="$REGION"
printf '%s' "$VALUE" | gcloud secrets versions add "$NAME" --project "$PROJECT" --data-file=-
echo "Stored a new version of ${NAME}."
