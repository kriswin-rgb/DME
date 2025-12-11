# DME AI Workforce – Jobs & Task Catalogue

This file lists the practical jobs each agent is responsible for. Use this as the
"what must happen every day" checklist when you design workflows in n8n and when
you wire tools into each AI agent.

---

## 1. Ingestor – Data & Feature Pipeline Agent

- Maintain asset/timeframe universe (FX, crypto, indices, gold).
- Subscribe to all configured data feeds (ticks, OHLCV, orderbook, funding, macro).
- Validate each tick for schema, timestamp freshness, and value sanity.
- Normalise raw ticks into canonical format and write to Timescale/TSDB.
- Maintain rolling feature windows for 1H, 4H, 1D and longer horizons.
- Detect anomalies (gaps, spikes, stale feeds) and generate anomaly reports.
- Fail over to backup feeds when primary sources degrade.
- Emit "feature set ready" events for each new bar per asset/timeframe.
- Keep an audit trail of data issues and remediation steps.

## 2. Strategist – Strategy R&D & Validation Agent

- Intake new hypotheses from humans or higher‑level agents.
- Define parameter search spaces and backtest configurations.
- Run backtests (grid/ Bayesian) and generate full artefact packages.
- Perform train/test split and out‑of‑sample validation.
- Run the 7‑point robustness suite (overfitting, regimes, drawdown, costs, etc.).
- Classify strategies as PROMISING / NEUTRAL / REJECTED.
- Produce R&D summaries and recommended next actions.
- Maintain experiment registry and ensure full reproducibility.
- Hand off validated candidates to RiskMonitor for shadow trading.

## 3. RiskMonitor – Shadow Trading & Promotion Agent

- Run shadow trading for candidate strategies on live data (no client impact).
- Compare shadow vs production performance and risk.
- Enforce promotion/demotion rules (min sample, stability, risk budgets).
- Propose lifecycle moves: Keep in R&D, Promote to Shadow, Promote to Prod, Park, Kill.
- Apply live risk filters on production signals (exposure, leverage, correlations).
- Flag and log any breaches of risk limits.
- Recommend parameter adjustments or de‑leveraging when conditions change.

## 4. Finisher – Signal Delivery & Performance Agent

- Construct canonical signal objects (asset, direction, size, confidence, expiry).
- Write signals to DB and streaming layers (Redis/Kafka/etc.).
- Fan‑out signals to all active channels (web, API, Telegram, Discord, email).
- Enforce access and geofencing: who is allowed to see which signals.
- Retry and log any failed deliveries.
- Aggregate daily and weekly performance metrics per strategy/asset/timeframe.
- Generate transparency feed for dashboards and public reporting.

## 5. ChannelManager – Telegram Operations Agent

- Post formatted signals to the correct Telegram channels.
- Onboard new users (welcome messages, quickstart guides, pinned posts).
- Answer basic FAQs via bot/KB integration.
- Detect spam/scams and auto‑moderate simple cases.
- Escalate complex issues to Communicator and Shield.
- Summarise daily activity, top questions, and churn signals.

## 6. ServerModerator – Discord Operations Agent

- Keep Discord server structure and roles up to date (Trial, Pro, Admin).
- Post signals in signal channels, tagging the right roles.
- Run moderation rules (NSFW, scams, abusive behaviour).
- Produce structured moderation logs with evidence for appeals.
- Surface community feedback, feature requests, and power users.

## 7. Campaigner – Social Media & Growth Agent

- Maintain 2–4 week rolling content calendar for X, LinkedIn, TikTok, etc.
- Turn wins, research, and macro stories into platform‑specific posts.
- Ensure all links are UTM‑tagged and consistent with your analytics plan.
- Schedule posts at optimal times for each audience.
- Monitor engagement and test hooks, creatives, and CTAs.
- Propose small experiments and report their results.

## 8. Producer – Video & Content Factory Agent

- Analyse YouTube and short‑form metrics (CTR, retention, watch time).
- Propose daily/weekly slates of long‑form videos and shorts.
- Draft scripts: hook, narrative, close, and disclaimers.
- Specify or generate thumbnails, B‑roll, captions, and metadata.
- Monitor 24–48h performance and recommend title/thumbnail tweaks.
- Feed best‑performing topics back to Strategist, Analyst, and Campaigner.

## 9. Analyst – Macro & Core Research Agent

- Track macro calendars, major events, and regime shifts.
- Maintain an internal macro dashboard for the team.
- Produce concise macro briefs linking market moves to your strategies.
- Suggest new factor ideas and stress‑test scenarios.
- Provide background notes for content pieces and educational explainers.

## 10. Editor – Editorial & SEO Agent

- Turn ideas and performance reports into fully structured articles.
- Apply SEO best practices: headings, keywords, schema, internal links.
- Maintain editorial tone: clear, non‑hyped, risk‑aware.
- Publish to CMS and route derivatives to email/social/Telegram.
- Maintain and update evergreen content as markets and products evolve.

## 11. Webmaster – Frontend & Experience Agent

- Keep all core flows healthy (landing → checkout → dashboard).
- Monitor UX metrics (bounce, scroll depth, conversion rate).
- Identify and log frontend bugs and jank.
- Suggest and configure safe A/B tests (copy/layout/CTAs).
- Ensure technical SEO hygiene (sitemaps, canonicals, structured data).
- Verify that tracking and webhooks fire correctly into analytics and n8n.

## 12. Developer – Core Codebase & Release Agent

- Maintain repo structure, documentation, and coding standards.
- Keep CI/CD pipelines green and fast.
- Track and group technical debt into GitHub issues/epics.
- Coordinate and document releases and rollbacks.
- Review automated PRs (e.g., from Copilot) before human approval.

## 13. Watcher – Infrastructure & SRE Agent

- Monitor infra metrics (CPU, memory, latency, errors, queue depth).
- Manage SLOs/SLA dashboards and error budgets.
- Coordinate incidents, timelines, and remediation tasks.
- Verify backups and test restores regularly.
- Propose reliability improvements (circuit breakers, caching, autoscaling).

## 14. Auditor – Payments & Access Control Agent

- Reconcile daily payment events with internal records.
- Maintain subscription states and entitlements across web, Telegram, Discord.
- Trigger dunning flows and follow‑up comms for failed payments.
- Produce revenue, churn, and cohort summaries.
- Flag anomalies like double charges or missing entitlements.

## 15. Shield – Security, Fraud & Abuse Agent

- Monitor logs and events for suspicious auth and payment patterns.
- Keep an eye on community channels for impersonation and scams.
- Prioritise and route potential security incidents to Watcher + humans.
- Propose WAF rules and auth policy updates.
- Maintain a risk log with mitigations and residual risk notes.

## 16. Converter – Marketing & Funnel Agent

- Design the funnel from lead magnet to core offers.
- Maintain and optimise email sequences (welcome, onboarding, win‑back).
- Monitor funnel KPIs (opt‑ins, activation, upgrades, churn).
- Own the SEO cluster map and track search rankings.
- Suggest funnel experiments and measure their impact.

## 17. Comptroller – Data & Governance Agent

- Maintain KPI definitions and canonical dashboards.
- Check for missing, inconsistent, or conflicting data.
- Track changes to policies, ToS, privacy, and disclaimers.
- Manage internal access control and review who can touch what.
- Keep audit trails for high‑risk actions (deployments, config changes).

## 18. Communicator – Customer Service & Messaging Agent

- Aggregate tickets and questions from email, forms, Telegram, Discord.
- Categorise requests and draft responses using the KB and policies.
- Escalate complex or high‑risk cases to humans.
- Prepare and coordinate proactive comms during market stress or incidents.
- Summarise sentiment and recurring problems for product and strategy.

---

Use this catalogue when:
- Defining tasks and tools for each LLM agent.
- Designing n8n workflows that map events → agent calls → downstream actions.
- Writing guardrails and escalation rules per role.
