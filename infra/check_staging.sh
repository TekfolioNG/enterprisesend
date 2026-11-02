#!/usr/bin/env bash
# Quick health check of a deployed environment.
#   API_URL=https://enterprisesend-api-xxxx.europe-west1.run.app WEB_URL=https://staging.enterprisesend.com infra/check_staging.sh
set -uo pipefail
API="${API_URL:?Set API_URL}"; WEB="${WEB_URL:?Set WEB_URL}"
FAILED=0
pass() { echo "PASS  $1"; }
fail() { echo "FAIL  $1"; FAILED=1; }
code() { curl -s -o /dev/null -m 20 -w '%{http_code}' "$@"; }

[ "$(code "$API/health")" = "200" ] && pass "API answers /health" || fail "API /health did not return 200"
[ "$(code "$API/v1/me")" = "401" ] && pass "API refuses requests without a login (401)" || fail "API /v1/me should return 401 without a token"
curl -s -m 20 "$API/v1/me" | grep -q "Missing token" && pass "API message is ours (not a platform error page)" || fail "API reply did not say 'Missing token'"

HDR="$(curl -s -m 20 -D - -o /dev/null -X OPTIONS "$API/v1/me" -H "Origin: $WEB" -H "Access-Control-Request-Method: GET" -H "Access-Control-Request-Headers: authorization")"
echo "$HDR" | tr -d '\r' | grep -qi "^access-control-allow-origin: ${WEB}$" \
  && pass "API allows the web address ($WEB) and only that" || fail "API CORS does not allow $WEB (set WEB_ORIGIN on the API)"

[ "$(code "$WEB/")" = "200" ] && pass "Web app answers at $WEB" || fail "Web app did not return 200 at $WEB"
[ "$(code "$WEB/login")" = "200" ] && pass "Sign-in page path works (single-page routing)" || fail "$WEB/login did not return 200"
WH="$(curl -s -m 20 -D - -o /dev/null "$WEB/" | tr -d '\r')"
echo "$WH" | grep -qi "^x-frame-options: deny" && pass "Web app sends clickjacking protection header" || fail "Web app is missing X-Frame-Options"
curl -s -m 20 "$WEB/" | grep -qi "enterprisesend" && pass "Web page contains the product name" || fail "Web page does not mention EnterpriseSend"
case "$WEB" in https://*) pass "Web address uses HTTPS";; *) fail "Web address is not HTTPS";; esac

[ "$FAILED" = "0" ] && echo "All checks passed." || echo "Some checks failed: see FAIL lines above."
exit "$FAILED"
