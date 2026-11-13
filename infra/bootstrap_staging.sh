#!/usr/bin/env bash
# One-time setup of the staging project: services, service account, upload bucket.
set -euo pipefail
PROJECT="${PROJECT:-enterprisesend-staging}"
REGION="${REGION:-europe-west1}"
SA_EMAIL="es-api@${PROJECT}.iam.gserviceaccount.com"
BUCKET="${PROJECT}-uploads"

gcloud config set project "$PROJECT"
gcloud services enable run.googleapis.com firestore.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com secretmanager.googleapis.com cloudtasks.googleapis.com \
  cloudscheduler.googleapis.com storage.googleapis.com identitytoolkit.googleapis.com

gcloud iam service-accounts describe "$SA_EMAIL" >/dev/null 2>&1 || \
  gcloud iam service-accounts create es-api --display-name="EnterpriseSend API"

# Least privilege: the API can use Firestore, read secrets and queue tasks.
for role in roles/datastore.user roles/secretmanager.secretAccessor roles/cloudtasks.enqueuer roles/firebaseauth.viewer; do
  gcloud projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:${SA_EMAIL}" \
    --role="$role" --condition=None --quiet >/dev/null
done

# Source deploys build with the default Compute service account, which needs the Cloud Run Builder role.
PROJECT_NUMBER="$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')"
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role=roles/run.builder --condition=None --quiet >/dev/null

# Uploaded billing files are audit evidence: private, and the API may only CREATE objects.
gcloud storage buckets describe "gs://${BUCKET}" >/dev/null 2>&1 || \
  gcloud storage buckets create "gs://${BUCKET}" --location="$REGION" \
    --uniform-bucket-level-access --public-access-prevention
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member="serviceAccount:${SA_EMAIL}" --role=roles/storage.objectCreator >/dev/null

echo "Bootstrap done for $PROJECT in $REGION. Upload bucket: gs://${BUCKET}"
