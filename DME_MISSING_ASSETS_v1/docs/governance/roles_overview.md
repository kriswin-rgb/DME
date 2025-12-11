# DME AI Workforce – Roles Overview

This file describes every autonomous AI role in the DME system, how they fit together,
and the high‑level responsibility boundaries for each.

## Legend

- **Agent ID** – short, stable identifier used in orchestration/routing.
- **Domain** – which part of the business this agent belongs to.
- **Primary Outputs** – what artefacts/messages this agent is expected to produce.
- **Downstream** – who consumes those outputs next.
- **Orchestrator Tag** – handy label to use in `role` / `agent_name` fields.

---

## 1. Signals & Trading Intelligence

### 1.1 Ingestor – Data & Feature Pipeline Agent
- **Agent ID:** `ingestor_001`
- **Domain:** Signals / Data
- **Mission:** Keep all market & macro data clean, fresh, and usable for every strategy.
- **Primary Outputs:**
  - Normalised feature sets per asset/timeframe (`ready_feature_set`)
  - Anomaly reports (`anomaly_report`)
  - Data quality alerts (`data_quality_alert`)
- **Downstream:** Strategist, RiskMonitor, Watcher, Comptroller
- **Orchestrator Tag:** `Ingestor`

### 1.2 Strategist – Strategy R&D & Validation Agent
- **Agent ID:** `strategist_001`
- **Domain:** Signals / Research
- **Mission:** Turn hypotheses into fully‑validated strategies with reproducible research artefacts.
- **Primary Outputs:**
  - Backtest configs + experiment registrations
  - Validation reports & strategy classifications (`classification`)
  - R&D summaries for management
- **Downstream:** RiskMonitor, Analyst, Converter
- **Orchestrator Tag:** `Strategist`

### 1.3 RiskMonitor – Shadow Trading & Promotion Agent
- **Agent ID:** `risk_monitor_001`
- **Domain:** Signals / Risk
- **Mission:** Gatekeep what reaches clients; run shadow trading, enforce risk, and manage strategy lifecycle.
- **Primary Outputs:**
  - Shadow trading logs & comparisons
  - Promotion / demotion proposals
  - Live risk filter decisions on signals
- **Downstream:** Finisher, Watcher, Comptroller
- **Orchestrator Tag:** `RiskMonitor`

### 1.4 Finisher – Signal Delivery & Performance Agent
- **Agent ID:** `finisher_001`
- **Domain:** Signals / Client Delivery
- **Mission:** Turn canonical signal objects into clean, compliant, low‑latency client‑facing messages.
- **Primary Outputs:**
  - Canonical signal records (DB + streams)
  - Fan‑out messages to web, Telegram, Discord, email
  - Daily/weekly performance summaries
- **Downstream:** ChannelManager, ServerModerator, Campaigner, Producer, Comptroller
- **Orchestrator Tag:** `Finisher`

---

## 2. Communication & Social Operations

### 2.1 ChannelManager – Telegram Operations Agent
- **Agent ID:** `channel_manager_001`
- **Domain:** Comms / Telegram
- **Mission:** Own all Telegram channels: signal posting, onboarding, moderation, and first‑line support triage.
- **Primary Outputs:**
  - Formatted Telegram posts for each signal
  - Onboarding flows and help responses
  - Moderation + abuse reports
- **Downstream:** Communicator, Shield, Auditor
- **Orchestrator Tag:** `ChannelManager`

### 2.2 ServerModerator – Discord Operations Agent
- **Agent ID:** `server_moderator_001`
- **Domain:** Comms / Discord
- **Mission:** Mirror Telegram operations on Discord with strong role/channel hygiene and safety.
- **Primary Outputs:**
  - Discord signal posts & @mentions
  - Moderation actions + audit log entries
  - Escalations for scams/abuse
- **Downstream:** Communicator, Shield, Auditor
- **Orchestrator Tag:** `ServerModerator`

### 2.3 Campaigner – Social Media & Growth Agent
- **Agent ID:** `campaigner_001`
- **Domain:** Growth / Social
- **Mission:** Execute the rolling content calendar across X, LinkedIn, TikTok and similar platforms.
- **Primary Outputs:**
  - Platform‑specific post payloads and schedules
  - Engagement summaries and experiment results
  - Suggestions for new growth angles
- **Downstream:** Converter, Producer, Editor
- **Orchestrator Tag:** `Campaigner`

### 2.4 Producer – Video & Content Factory Agent
- **Agent ID:** `producer_001`
- **Domain:** Content / Video
- **Mission:** Own end‑to‑end video production from data‑driven planning through scripting to publishing feedback loops.
- **Primary Outputs:**
  - Content slates (long‑form + shorts)
  - Scripts, thumbnail briefs, metadata packs
  - Post‑mortem performance reviews
- **Downstream:** Campaigner, Converter, Webmaster
- **Orchestrator Tag:** `Producer`

---

## 3. Research & Editorial

### 3.1 Analyst – Macro & Core Research Agent
- **Agent ID:** `analyst_001`
- **Domain:** Research / Macro
- **Mission:** Track the macro regime and produce narratives and factor ideas that feed both strategies and content.
- **Primary Outputs:**
  - Macro briefs & regime summaries
  - Factor research notes for Strategist
  - Topic ideas for Editor & Producer
- **Downstream:** Strategist, Editor, Producer, Converter
- **Orchestrator Tag:** `Analyst`

### 3.2 Editor – Editorial & SEO Agent
- **Agent ID:** `editor_001`
- **Domain:** Content / SEO
- **Mission:** Turn ideas and performance stories into clean, compliant, SEO‑optimised articles and derivatives.
- **Primary Outputs:**
  - Article drafts + final copy
  - SEO briefs, internal linking plans, schema snippets
  - Repurposed snippets for email/social/Telegram
- **Downstream:** Webmaster, Campaigner, Communicator
- **Orchestrator Tag:** `Editor`

---

## 4. Technology & Platform

### 4.1 Webmaster – Frontend & Experience Agent
- **Agent ID:** `webmaster_001`
- **Domain:** Web / UX
- **Mission:** Keep the site fast, reliable, and high‑converting while respecting technical SEO and analytics integrity.
- **Primary Outputs:**
  - UX improvement suggestions and A/B test plans
  - Frontend bug reports and GitHub issues
  - Technical SEO hygiene reports
- **Downstream:** Developer, Converter, Watcher
- **Orchestrator Tag:** `Webmaster`

### 4.2 Developer – Core Codebase & Release Agent
- **Agent ID:** `developer_001`
- **Domain:** Engineering / Delivery
- **Mission:** Maintain repo hygiene, CI/CD, release process, and technical debt roadmap.
- **Primary Outputs:**
  - Structured GitHub issues and PR plans
  - Release notes and changelog entries
  - Refactor and tech‑debt work items
- **Downstream:** Human devs, Copilot, Watcher
- **Orchestrator Tag:** `Developer`

### 4.3 Watcher – Infrastructure & SRE Agent
- **Agent ID:** `watcher_001`
- **Domain:** Infra / SRE
- **Mission:** Monitor systems 24/7, coordinate incidents, and own backups & DR posture.
- **Primary Outputs:**
  - Incident summaries and remediation tasks
  - SLO/SLA reports
  - Backup/restore verification reports
- **Downstream:** Developer, Shield, Comptroller, Communicator
- **Orchestrator Tag:** `Watcher`

---

## 5. Business, Compliance & Customer

### 5.1 Auditor – Payments & Access Control Agent
- **Agent ID:** `auditor_001`
- **Domain:** Billing / Access
- **Mission:** Ensure billing events and access permissions remain perfectly aligned.
- **Primary Outputs:**
  - Reconciliation reports
  - Entitlement updates & anomalies
  - Revenue/churn summaries
- **Downstream:** Comptroller, Communicator, ChannelManager, ServerModerator
- **Orchestrator Tag:** `Auditor`

### 5.2 Shield – Security, Fraud & Abuse Agent
- **Agent ID:** `shield_001`
- **Domain:** Security / Fraud
- **Mission:** Detect and respond to abuse, fraud, and security issues across apps and communities.
- **Primary Outputs:**
  - Security alerts and runbook suggestions
  - Fraud risk flags and account actions
  - Community abuse/impersonation reports
- **Downstream:** Watcher, Auditor, Communicator
- **Orchestrator Tag:** `Shield`

### 5.3 Converter – Marketing & Funnel Agent
- **Agent ID:** `converter_001`
- **Domain:** Marketing / Funnel
- **Mission:** Design, measure, and optimise the customer journey from lead to loyal subscriber.
- **Primary Outputs:**
  - Funnel maps and experiment designs
  - Email sequence briefs and copy suggestions
  - SEO cluster and ranking reports
- **Downstream:** Editor, Campaigner, Webmaster, Comptroller
- **Orchestrator Tag:** `Converter`

### 5.4 Comptroller – Data & Governance Agent
- **Agent ID:** `comptroller_001`
- **Domain:** Data / Governance
- **Mission:** Own KPIs, data quality, policy docs, and access governance across DME.
- **Primary Outputs:**
  - KPI dashboards and anomaly flags
  - Policy & disclaimer update suggestions
  - Access/governance change proposals
- **Downstream:** Watcher, Auditor, Developer, Communicator
- **Orchestrator Tag:** `Comptroller`

### 5.5 Communicator – Customer Service & Messaging Agent
- **Agent ID:** `communicator_001`
- **Domain:** Support / Comms
- **Mission:** Provide consistent, calm, compliant communication with customers and prospects.
- **Primary Outputs:**
  - Triage classifications and ticket summaries
  - Reply drafts for support, Telegram, Discord, email
  - Proactive messaging packages during incidents or volatility
- **Downstream:** Human support, ChannelManager, ServerModerator, Watcher
- **Orchestrator Tag:** `Communicator`

---

Use this overview together with the detailed prompts in `agents/` and the job catalogue
in `jobs/jobs_catalogue.md` when wiring agents into the orchestrator or assigning
OpenAI/Claude/Gemini instances to each role.
