#!/bin/bash
# DutyBreak — Cloud Run Deployment Script
# Run from project root: bash deploy.sh

PROJECT_ID="contextos-493904"
REGION="us-central1"
SERVICE_NAME="dutybreak"
IMAGE="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "=== DutyBreak Cloud Run Deploy ==="
echo "Project: $PROJECT_ID"
echo "Region: $REGION"

# Build and push
echo ""
echo "Building container..."
gcloud builds submit --tag $IMAGE --project $PROJECT_ID

# Deploy
echo ""
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_API_KEY=${GEMINI_API_KEY},VERTEX_MODEL=gemini-3.5-flash,APP_ENV=production" \
  --memory 512Mi \
  --cpu 1 \
  --timeout 120 \
  --project $PROJECT_ID

echo ""
echo "=== Deploy complete ==="
gcloud run services describe $SERVICE_NAME --region $REGION --project $PROJECT_ID --format="value(status.url)"
