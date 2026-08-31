# LearnerLoop

LearnerLoop is a state-aware autonomous operations agent built for the All Things Agentic Hackathon.

It observes live operational signals, compares current and prior state, reasons with Gemini 3.5 Flash through Google's Agent Development Kit (ADK), creates a structured intervention request, and returns that action to an orchestration workflow for persistence and later re-evaluation.

## Hackathon scope

This repository contains the new hackathon agent layer:
- Google ADK agent
- Gemini 3.5 Flash reasoning
- scoped intervention tool
- Cloud Run deployment instructions
- reproducible sample input

Existing product infrastructure and pre-existing automation used as orchestration/data context are not claimed as newly created hackathon work.

## Architecture

`Operational signal -> n8n context -> Cloud Run -> Google ADK -> Gemini 3.5 Flash -> intervention tool -> structured decision -> n8n decision log -> next run`

## Safety

The submitted agent does not directly modify live advertising budgets, bids, campaigns, ad sets, or ads. Higher-risk decisions are emitted as human-approval-required candidates.

## Requirements

- Python 3.11+
- Google Cloud project with billing enabled
- Google Cloud Shell or gcloud CLI
- Cloud Run
- Vertex AI
- Google ADK

## Reproducible testing

### 1. Select project
```bash
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable APIs
```bash
gcloud services enable \
  run.googleapis.com \
  aiplatform.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com
```

### 3. Deploy
```bash
gcloud run deploy learnerloop-agent \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=global
```

### 4. Verify
```bash
curl "$SERVICE_URL/list-apps"
```

### 5. Create session
```bash
curl -X POST \
  "$SERVICE_URL/apps/learnerloop_agent/users/demo_user/sessions/demo_session" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 6. Run
```bash
curl -X POST "$SERVICE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{
    "appName":"learnerloop_agent",
    "userId":"demo_user",
    "sessionId":"demo_session",
    "newMessage":{
      "role":"user",
      "parts":[{
        "text":"{\"current_performance\":{\"spend\":1450,\"purchases\":16,\"verified_roas\":2.19,\"verified_cpa\":90.63},\"previous_performance\":{\"spend\":980,\"purchases\":8,\"verified_roas\":1.48,\"verified_cpa\":122.5},\"previous_decision\":{\"decision\":\"WATCH\"},\"targets\":{\"target_cpa\":100,\"minimum_roas\":1.8}}"
      }]
    }
  }'
```

Expected: one structured intervention such as HOLD, WATCH, INVESTIGATE, SCALE_CANDIDATE, REDUCE_CANDIDATE, or PAUSE_CANDIDATE.

## Model
`gemini-3.5-flash`

## Google agent framework
Google Agent Development Kit (ADK)

## Google Cloud
Cloud Run + Vertex AI
