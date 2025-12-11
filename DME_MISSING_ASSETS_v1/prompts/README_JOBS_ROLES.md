# DME AI Workforce – Roles, Jobs & Prompts Pack

This bundle combines **three layers**:

1. **Roles overview** – who each agent is and how they fit together  
   - `roles/roles_overview.md`

2. **Jobs & tasks catalogue** – what must be done, by whom, every day  
   - `jobs/jobs_catalogue.md`

3. **System prompts & schema** – what you hand to OpenAI / Claude / Gemini  
   - `agents/*.md` (one per agent, from the prompts pack)  
   - `schema/decision-response-v2.json`

## How this fits into the DME stack

- The **orchestrator** (DME Brain) routes tasks to the right agent based on `role` / `agent_id`.
- Each agent uses its **system prompt** (from `agents/*.md`) plus tools (HTTP, DB, queues) to
  perform the jobs listed in `jobs/jobs_catalogue.md`.
- All agents emit structured JSON matching `schema/decision-response-v2.json` so n8n and your
  services can validate and route outputs safely.

## How to use this pack

1. **Design:**  
   - Start from `roles/roles_overview.md` to understand the full “org chart”.  
   - Use `jobs/jobs_catalogue.md` when designing n8n workflows and metrics.

2. **Implementation:**  
   - For each runtime agent (OpenAI / Claude / Gemini), choose the right `agents/*.md` prompt.  
   - Combine the system prompt with a small, specific user/task payload.  
   - Enforce the JSON schema in `schema/decision-response-v2.json` in your orchestrator.

3. **Operations:**  
   - When you want to change who does what, update `jobs/jobs_catalogue.md` first, then
     adjust the relevant agent prompts and tools.

This zip is the **single source of truth** for:
- DME AI job roles
- Which jobs belong to which role
- The prompts that tell each AI what to do and how to behave
