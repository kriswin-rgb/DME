# DME Missing Assets Bundle (v1)

This bundle collects all artefacts that were **not yet integrated** into the canonical
`dme-platform/` monorepo but are still valuable for automation, infra, analytics,
and AI agent behaviour.

## Structure

- `automation/n8n/autonomy_master_v6/`
  - n8n workflow JSONs and supporting files from `autonomy_master_v6.zip`
  - Includes:
    - `automation/n8n_pack_v4_4/n8n/workflows/*.json`
    - `automation/n8n_pack_autonomy/*.json`
    - Autonomy n8n README / env templates

- `automation/n8n/dme_autonomous_platform_v12/`
  - Core SDS / backtest / risk alert workflows from the v12 bundle:
    - `WF_SDS_SIGNAL_FANOUT_AND_INGEST_V1.json`
    - `WF_STRATEGY_BACKTEST_AND_METRICS_V1.json`
    - `WF_EXEC_RISK_ALERTS_V1.json`

- `infra/vault/legacy/dme-vault-deployable-final/`
  - Vault docker-compose + scripts + base policies from `dme-vault-deployable-final (5).zip`

- `infra/vault/legacy/dme-infra-vault-dir/`
  - Extended Vault infra-as-code (policies, scripts, sample clients) from `dme-infra-vault-dir (3).zip`

- `services/dme_core_v5/advanced_analytics_v12/`
  - Advanced analytics / marketing modules from v12:
    - `portfolio_analytics.py`
    - `utm_etl.py`
    - `seo_rank_tracker.py`
  - These are not wired into the new core service yet; treat them as a reference/backlog.

- `prompts/agents/`
  - All agent system prompt markdown files from `DME_AGENT_ROLES_JOBS_v1.zip`
  - Examples:
    - `strategist_system_prompt.md`
    - `risk_monitor_system_prompt.md`
    - `producer_system_prompt.md`
    - etc.

- `docs/governance/`
  - `roles_overview.md` – high-level role definitions
  - `jobs_catalogue.md` – job catalogue for agents / human roles

- `schema/decision-response-v2.json`
  - JSON schema describing the AI agent decision/response envelope.

- `legacy/webhooks/autonomy_master_v6/apps/web/src/app/api/webhook/payment/route.ts`
  - Historical full implementation of the payment webhook from Autonomy Master v6.
  - Use this as a reference when finalising DB transaction logic in the new monorepo.

## How to Use

- **Repo Integration**:
  - Copy the relevant subdirectories into your main `dme-platform/` repo, for example:
    - `automation/n8n/*` -> `dme-platform/automation/n8n/`
    - `infra/vault/legacy/*` -> `dme-platform/infra/vault/legacy/`
    - `services/dme_core_v5/advanced_analytics_v12/*` -> `dme-platform/services/dme_core_v5/advanced_analytics_v12/`
    - `prompts/*` & `docs/governance/*` -> appropriate locations in `dme-platform/`

- **n8n Workflows**:
  - Import the JSON files into your n8n instance (UI → Import).
  - Optionally keep them version-controlled under `automation/n8n/` in the main repo.

- **Vault Infra**:
  - Use the `infra/vault/legacy/*` files as a starting point for your Vault deployment.
  - Align with the new Vault client patterns already present in `dme-platform/infra/vault/client/`.

- **Analytics Modules**:
  - When ready, adapt and integrate the v12 analytics modules into the new `services/dme_core_v5` layout.
  - Add tests and wire into CI before promoting to production.

- **Agent Prompts**:
  - Link the prompt files here to the entries in `config/prompt_registry.yml` in your main repo.
  - This keeps prompt text and registry metadata in sync.