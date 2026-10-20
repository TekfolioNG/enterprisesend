#!/usr/bin/env bash
# Starts the local Auth and Firestore emulators (no Google login needed: "demo-" project ID).
cd "$(dirname "$0")/../../.."   # repo root, where firebase.json lives
exec firebase emulators:start --only auth,firestore --project demo-enterprisesend
