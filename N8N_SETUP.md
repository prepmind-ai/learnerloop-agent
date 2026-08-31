# n8n minimum integration

Use the DUPLICATED Intraday ROI flow only.

Change:
`Read Latest Intraday Snapshot -> Prepare Decision Log -> Append Growth Decisions`

to:
`Read Latest Intraday Snapshot -> Prepare Agent Context -> Call LearnerLoop Agent -> Prepare Decision Log -> Append Growth Decisions`

## Prepare Agent Context
Pass one JSON object containing only fields you already have:
- current_performance
- previous_performance
- verified_revenue
- previous_decision
- targets

## ADK session
Create once before the demo:

POST
`https://YOUR-SERVICE.run.app/apps/learnerloop_agent/users/n8n_user/sessions/intraday_demo`

JSON body:
`{}`

## Run agent
POST
`https://YOUR-SERVICE.run.app/run`

JSON body:
```json
{
  "appName": "learnerloop_agent",
  "userId": "n8n_user",
  "sessionId": "intraday_demo",
  "newMessage": {
    "role": "user",
    "parts": [
      {
        "text": "={{ JSON.stringify($json) }}"
      }
    ]
  }
}
```

If needed, use n8n Expression mode and set the text value to:
`{{ JSON.stringify($json) }}`

Then feed the agent result into the existing decision-log branch.

Do not add live Meta budget/edit actions for the hackathon demo.
