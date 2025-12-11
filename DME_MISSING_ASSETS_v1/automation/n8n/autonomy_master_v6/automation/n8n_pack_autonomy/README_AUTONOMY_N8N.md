# DME Autonomy n8n Pack

This folder contains three ready-to-import n8n workflows that integrate with the
DME Orchestrator (apps/orchestrator) and your existing DME APIs.

Workflows:

- `signals_rnd_review.json`
- `content_planning.json`
- `incident_review.json`

Import each JSON into n8n via **Settings → Import Workflow**.

Before running:

1. Set environment variable `ORCH_SHARED_SECRET` on the n8n host to match the
   value used by the orchestrator service.
2. Create a Slack credential in n8n named **"DME Slack"** that points at your
   workspace/bot.
3. Replace `YOUR_DME_DOMAIN` and `YOUR_DOMAIN` in the HTTP Request node URLs
   with your real API and orchestrator hostnames.
