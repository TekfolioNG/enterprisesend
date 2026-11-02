#!/usr/bin/env bash
# Switches on authenticator-app (TOTP) two-step sign-in for the project. Run once per project.
# Needs Identity Platform enabled. Uses the Identity Toolkit admin API, as Google's TOTP guide describes.
set -euo pipefail
PROJECT="${PROJECT:-enterprisesend-staging}"
curl -sS -X PATCH "https://identitytoolkit.googleapis.com/admin/v2/projects/${PROJECT}/config?updateMask=mfa" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "X-Goog-User-Project: ${PROJECT}" \
  -H "Content-Type: application/json" \
  -d '{"mfa":{"providerConfigs":[{"state":"ENABLED","totpProviderConfig":{"adjacentIntervals":1}}]}}'
echo
echo "If the reply above lists an mfa block with state ENABLED, TOTP is on."
