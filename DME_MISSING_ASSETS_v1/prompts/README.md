# DME Agent Prompts v2.0

This bundle contains **production-grade system prompts** and a shared JSON schema
for the DME AI workforce. It is designed to plug into your existing orchestrator
so that each agent (role) stays within its strict remit while producing
machine-validated `DecisionResponseV2` payloads.

## Contents

- `schema/decision-response-v2.json`  
  The canonical response envelope used by every agent. All agent outputs MUST
  conform to this schema.

- `agents/*.md`  
  One system prompt per role, including:
  - Identity and mandate
  - Hard boundaries (MUST / MUST NOT)
  - Escalation rules
  - Input assumptions
  - Output contract (DecisionResponseV2)
  - Allowed `action` values and payload guidelines

Roles included:

- Ingestor – Data & Feature Pipeline Agent
- Strategist – Strategy R&D & Validation Agent
- RiskMonitor – Shadow Trading & Promotion Agent
- Finisher – Signal Delivery & Performance Agent
- ChannelManager – Telegram Operations Agent
- ServerModerator – Discord Operations Agent
- Campaigner – Social Media & Growth Agent
- Producer – Video & Content Factory Agent
- Analyst – Macro & Core Research Agent
- Editor – Editorial & SEO Agent
- Webmaster – Frontend & Experience Agent
- Developer – Core Codebase & Release Agent
- Watcher – Infrastructure & SRE Agent
- Auditor – Payments & Access Control Agent
- Shield – Security, Fraud & Abuse Agent
- Converter – Marketing & Funnel Agent
- Comptroller – Data & Governance Agent
- Communicator – Customer Service & Messaging Agent

## How to Use

1. **Pick a role** and load the corresponding `agents/<role>_system_prompt.md`
   content as the `system` message when creating that agent in OpenAI / Claude / Gemini.

2. Ensure the agent is called with:
   - A `task` description relevant to its remit.
   - Any required context objects (metrics, logs, configs, previous decisions).

3. Enforce that the agent **only ever returns** a single JSON object that matches
   the `DecisionResponseV2` schema, with:
   - `role` set to the correct role name (e.g. `Ingestor`).
   - `action` set to one of the allowed actions listed in that role’s prompt.
   - A structured `payload` and `metadata` block as described.

4. Your orchestrator / n8n workflows can then:
   - Validate the JSON against `schema/decision-response-v2.json`.
   - Inspect `role`, `action`, and `metadata.confidence_score`.
   - Route decisions to the appropriate downstream services (signals, content, GitHub, etc.).
   - Log and trace everything using `metadata.correlation_id`.

By keeping all roles aligned on the same envelope and prompt structure,
you get **consistent, auditable, and safely-bounded** behaviour across
your entire DME AI workforce.
