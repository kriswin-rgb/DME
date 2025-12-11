# DME Vendor, Identity & Automation – DevOps 101 (Extended)

**Version:** 1.1  
**Audience:** DevOps, Tech Lead, Senior Engineers  
**Related docs:**  
- `DME_Vendor_Identity_Automation_Master_Brief_v1.docx`  
- `DME_Combined_Vendor_And_Dev101_Brief_v1_2.docx`  
- `DME_New_Dev_Onboarding_Checklist_v1_0.docx`  
- `DME_DEV_101_and_DEPLOY_GUIDE_v3.docx`  
- `DME Vendor list - Dec.xlsx` / `DME_Master_Vendor_List_Template_v1.xlsx`  

---

## 0. Purpose & Scope

This document is the **authoritative 101 for DevOps** to stand up and operate the DME vendor, identity, email and automation foundation.

It covers, in **step-by-step detail**:

- Creating and managing third‑party vendor accounts
- Enforcing the “**no personal / Gmail**” rule (business emails only)
- Configuring **1Password** vaults, 2FA and naming standards
- Setting up **Cloudflare** DNS and **Proton Mail** email (with multiple role accounts)
- Pointing the **domain to the web server** / app
- Creating and wiring **Slack**, **n8n**, **Telegram**, and AI providers via APIs
- Integrating **1Password into AWS** as the primary secrets source

The goal: **a clean, auditable, fully-automatable baseline** that DevOps can maintain with confidence.

---

## 1. Roles, Ownership & Guardrails

### 1.1 Core roles

- **Founder / Master Control**
  - Final approval on vendors and high‑risk changes.
  - 1Password org owner.
- **Tech Lead**
  - Owns vendor selection for tech/platform stack.
  - Owns this DevOps 101 and its evolution.
- **DevOps**
  - Implements everything in this document.
  - Runs infra, automation, and CI/CD.
- **Engineering**
  - Consumes credentials, APIs and automation exposed by DevOps.
- **Finance**
  - Owns billing details, cost tracking and renewals.
- **Operations**
  - Owns operational vendors (support desk, CRM, etc.).

### 1.2 Guardrail principles

1. **Business emails only** – all vendor accounts use `@dailymacroedge.com` role addresses.
2. **Single source of truth** – Master Vendor Excel + 1Password + this 101.
3. **2FA everywhere** – everything that supports 2FA must have it enabled.
4. **No secrets in git** – all real secrets are in 1Password (or its AWS-facing integration).
5. **Least privilege** – smallest possible scopes for API keys and roles.
6. **DEV≠PROD** – separate credentials, workspaces and (where possible) separate vendors / projects.

---

## 2. Master Vendor List – Excel 101

### 2.1 Where it lives

- Canonical file:  
  - `DME Vendor list - Dec.xlsx` (historical)  
  - or `DME_Master_Vendor_List_Template_v1.xlsx` (new template)

Store in:

- Private “Platform / Vendor” folder in your document store (SharePoint/Drive/etc.).
- Readable by:
  - Founder, Tech Lead, DevOps, Finance.
- Editable by:
  - Tech Lead, DevOps, Finance.

### 2.2 Columns (extended)

Ensure the sheet has **at least** these columns:

- `Vendor Name`
- `Category` (DNS, Email, Hosting, AI Provider, Payments, Automation, Logging, Monitoring, Support, Marketing, Legal, etc.)
- `URL` (login / admin console)
- `Primary Email (login)` (must be `@dailymacroedge.com`)
- `Owner Role` (Tech Lead, DevOps, Finance, Ops, Marketing, etc.)
- `Status` (Proposed, Approved, Active, Deprecated)
- `2FA Enabled (Yes/No)`
- `Environment Scope` (DEV, STAGE, PROD, Multi)
- `Data Classification` (Low, Medium, High)
- `Billing Cycle` (Monthly, Annual, Usage)
- `Monthly Cost (Approx, GBP)`
- `API Available (Yes/No)`
- `API Auth Method` (Key, OAuth, Token, Other)
- `API Docs URL`
- `API Key / Credential Stored In` (1Password vault/item)
- `API Scopes / Permissions` (short but explicit)
- `Webhooks Used (Yes/No)`
- `Webhook Target (n8n URL / Endpoint)`
- `Notes`

### 2.3 Categories and examples

Seed categories and typical vendors:

- **DNS & Email Routing** – Cloudflare
- **Email Provider** – Proton Mail
- **Hosting / Compute** – AWS, Hetzner, DigitalOcean
- **Automation** – n8n
- **ChatOps** – Slack
- **Secrets** – 1Password
- **AI Providers** – OpenAI, Anthropic, others
- **Payments** – Stripe, Paddle, NOWPayments, etc.
- **Monitoring & Logging** – Sentry, New Relic, Grafana Cloud, etc.
- **Support & CRM** – Zendesk, HubSpot, etc.

### 2.4 Process for new vendors

1. **Propose**
   - Dev/Egineer/Founder adds row:
     - `Status = Proposed`
     - Category, URL, Owner Role filled.
   - Optional: add estimated cost, reason in `Notes`.

2. **Approve**
   - Tech Lead (with Founder/Finance as needed) updates row:
     - `Status = Approved` or `Rejected`.
   - If Approved, continue to Section 5 vendor setup process.

3. **Activate**
   - Once account is created:
     - `Status = Active`
     - `Primary Email` set.
     - `2FA Enabled` set to `Yes`.
     - `API Available` and API columns populated.

4. **Deprecate**
   - When a vendor is retired:
     - `Status = Deprecated`
     - `Notes` updated with retirement date & replacement.

---

## 3. 1Password – Vaults, Groups & Standards

### 3.1 Vault design

Create these vaults:

- `DME-Global`
  - Cross‑cutting org accounts (Cloudflare, 1Password admin, Proton domain admin, Slack workspace owner).
- `DME-Engineering-Dev`
- `DME-Engineering-Prod`
- `DME-Finance`
- `DME-Marketing`
- `DME-Operations`

### 3.2 Group design

Groups (as in the master briefs):

- `DME-Founders`
- `DME-Tech-Lead`
- `DME-DevOps`
- `DME-Engineering`
- `DME-Finance`
- `DME-Marketing`
- `DME-Ops`

ACLs (high‑level):

- `DME-Global` – Founders, Tech Lead, limited DevOps.
- `DME-Engineering-Dev` – Tech Lead, DevOps, Engineering.
- `DME-Engineering-Prod` – Tech Lead, DevOps.
- `DME-Finance` – Founders, Finance.
- `DME-Marketing` – Founders, Marketing.
- `DME-Operations` – Founders, Ops.

### 3.3 Item naming and metadata

For each vendor, create items like:

- `CLOUDFLARE - PROD - ADMIN`
- `CLOUDFLARE - DEV - ADMIN`
- `PROTONMAIL - PROD - ADMIN`
- `SLACK - BOT - PROD`
- `N8N - ADMIN - DEV`
- `OPENAI - API - DEV`
- `OPENAI - API - PROD`
- `TELEGRAM - BOT - ALERTS - PROD`

Inside each:

- **Username** = role‑based email (e.g. `tech@dailymacroedge.com`)
- **Password** = long, unique passphrase
- **Custom fields**:
  - `API_KEY_<ENV>` (e.g. `API_KEY_PROD`)
  - `CLIENT_ID`, `CLIENT_SECRET` (for OAuth)
  - `WEBHOOK_SECRET`, `SIGNING_SECRET` where relevant
- **Tags**:
  - `vendor-cloudflare`, `env-prod`, `owner-tech-lead`
  - `vendor-openai`, `env-dev`, `api`, etc.

### 3.4 2FA & backup codes

For every vendor that supports 2FA:

1. Enable TOTP or hardware 2FA.
2. Scan QR using primary admin device.
3. Save **backup codes** in the 1Password item:
   - Field name: `2FA_BACKUP_CODES` (or attach file).
4. Confirm at least **two** people (Founder + Tech Lead / DevOps) can recover access (via appropriate vault sharing).

---

## 4. Business Email Standard – No Gmail

### 4.1 Role mailbox plan

Use **Proton Mail** to host:

- `founder@dailymacroedge.com`
- `tech@dailymacroedge.com`
- `devops@dailymacroedge.com` (optional)
- `finance@dailymacroedge.com`
- `ops@dailymacroedge.com`
- `support@dailymacroedge.com`
- `sales@dailymacroedge.com`
- `alerts@dailymacroedge.com`
- `billing@dailymacroedge.com`

Each mailbox:

- Has 2FA turned on (see Proton section).
- Is stored in 1Password as a credential:
  - `PROTONMAIL - MAILBOX - TECH`
  - `PROTONMAIL - MAILBOX - FINANCE`, etc.

### 4.2 Migrating away from personal emails

For each vendor:

1. Identify if the login is currently a Gmail/personal address.
2. If yes:
   - Change login email to the correct role address (via account settings).
   - If vendor requires support involvement, open a ticket from the new role email.
3. Update:
   - 1Password item (username).
   - Master Vendor List `Primary Email`.

---

## 5. Cloudflare & Proton Mail – Domain & Email 101

### 5.1 Domain pointing (web server)

In Cloudflare for `dailymacroedge.com`:

1. Create/confirm:

   - `A @` → IP of the web server, or
   - `CNAME @` → host given by your provider (e.g. `app.hostingprovider.com`).
   - `CNAME www` → `@` (or direct to provider).

2. Ensure **proxy** (orange cloud) is on for the web service if you want Cloudflare WAF/CDN.

3. Confirm your website responds on HTTPS:
   - TLS cert either via Cloudflare or your server.

### 5.2 Proton domain hookup

In Proton admin:

1. Add `dailymacroedge.com` as a custom domain.
2. Proton will provide:
   - DNS TXT for verification.
   - MX records.
   - DKIM CNAMEs.
   - Optional SPF/DMARC examples.

3. In Cloudflare, create:
   - TXT `_protonmail.domainkey` (or similar) for verification.
   - MX records exactly as Proton lists.
   - DKIM CNAMEs.
   - SPF TXT: e.g. `v=spf1 include:_spf.protonmail.ch -all`
   - DMARC TXT:
     - Example: `v=DMARC1; p=quarantine; rua=mailto:alerts@dailymacroedge.com`

4. Wait for Proton to verify DNS.

### 5.3 Mailbox provisioning

In Proton:

1. Create each role mailbox from 4.1.
2. For each:
   - Set a strong password (store in 1Password).
   - Enable **2FA (TOTP)**.
   - Store backup codes in the same 1Password item.

3. Test:
   - Send emails to/from each mailbox.
   - Verify deliverability and spam scores (using testing tools when needed).

---

## 6. Standard Vendor Setup & API Integration Process

Follow this for **each vendor** once Approved.

### 6.1 Account creation

1. Log in to `founder@` or `tech@` Proton mailbox.
2. Register at vendor URL using the appropriate role email.
3. Set a strong password, store in 1Password in the correct vault.
4. Enable 2FA and store backup codes.

### 6.2 API keys & OAuth

1. Locate API / developer console.
2. Create **separate keys** per environment where supported:
   - `DME-DEV`, `DME-STAGE`, `DME-PROD` or equivalent.
3. Choose auth:
   - **API key / bearer token** – store as `API_KEY_DEV`, `API_KEY_PROD` fields.
   - **OAuth** – store `CLIENT_ID`, `CLIENT_SECRET`, redirect URIs in 1Password.

4. Set **scopes** to least privilege:
   - E.g. Slack: `chat:write`, limited channels.
   - Cloudflare: only DNS and Email routing, not full account admin for routine tasks.

5. Update Master Vendor List with:
   - `API Available`, `API Auth Method`, `API Docs URL`.
   - `API Key / Credential Stored In` (vault + item).

### 6.3 n8n credentials

In **n8n DEV**:

1. Create credentials for each vendor:
   - `Slack Bot - Dev`
   - `Telegram Alerts Bot - Dev`
   - `Cloudflare API - Dev`
   - `OpenAI - Dev`, etc.
2. Copy values from 1Password (NOT from personal notes).
3. Test with simple workflows (ping endpoints, list resources).

In **n8n PROD**:

1. Repeat using **PROD** keys and a separate credentials name:
   - `Slack Bot - Prod`, etc.
2. Ensure Prod credentials exist only in Prod n8n.

---

## 7. Slack Mission Control – Detailed Setup

### 7.1 Workspace structure

- Create channels:
  - `#general`, `#engineering`, `#ops`, `#vendors`,
  - `#dme-decision-gate`, `#dme-alerts`, `#ai-agents`.
- Only core team in `#dme-decision-gate` (approvers).

### 7.2 Slack app configuration

In `api.slack.com/apps`:

1. Create app: `DME Mission Control`.
2. Add Slash Commands:
   - `/status` – sends health / status requests.
   - `/decision` – triggers Decision Gate.
   - `/global-stop` – toggles STOP workflow.
3. Set **Request URL** to Slack gateway:
   - `https://gateway.dailymacroedge.com/slack/commands`.

4. Events:
   - Enable `Event Subscriptions`.
   - Set Request URL:
     - `https://gateway.dailymacroedge.com/slack/events`.
   - Subscribe to:
     - `message.channels`, `app_mention`, etc. (minimal necessary set).

5. Interactivity:
   - Enable interactive components.
   - Request URL:
     - `https://gateway.dailymacroedge.com/slack/interactivity`.

6. OAuth & Permissions:
   - Add bot scopes:
     - `chat:write`, `chat:write.public`
     - `commands`
     - `channels:history` (only if needed)
     - `users:read` (if needed for names)
   - Install app to workspace.

7. Capture credentials:
   - Bot token (`xoxb-...`).
   - Signing secret.
   - Store in 1Password items:
     - `SLACK - BOT - DEV`, `SLACK - BOT - PROD`.

8. In the Slack gateway `.env` (DEV only, not committed):
   - `SLACK_SIGNING_SECRET` from 1Password.
   - `SLACK_BOT_TOKEN` from 1Password.
   - `N8N_BASE_URL` for that environment.

---

## 8. Telegram & Bots – 101

### 8.1 Create the bot

1. In Telegram, chat with `@BotFather`.
2. Run `/newbot`, follow prompts:
   - Name: `DME Alerts Bot`.
   - Get bot token.
3. Store token in 1Password:
   - Item: `TELEGRAM - BOT - ALERTS - PROD`.

### 8.2 Create groups

1. Create group: `DME Alerts`.
2. Add:
   - DME Alerts Bot.
   - Founder, Tech Lead, DevOps, Ops leads.
3. Optionally:
   - Create `DME Dev Alerts` for dev‑only noise.

### 8.3 Hook into n8n

In n8n:

1. Create **Telegram** credentials:
   - Use the bot token from 1Password.
2. Build workflow:
   - Trigger: HTTP/Webhook or internal events.
   - Action: Telegram node → `Send Message` to group ID.
3. Where to send alerts:
   - n8n global error handler (failed workflows).
   - Sentinel / high‑severity risk alerts.
   - Infrastructure incidents (if integrating with Prometheus/Grafana/Alertmanager).

### 8.4 Optional: Telegram → n8n

For 2‑way automation:

1. Use Telegram Trigger node (if supported) or a custom bot that forwards messages to n8n via webhook.
2. Use n8n to parse commands (e.g. `/status`, `/ack`) from Telegram.
3. Carefully restrict which actions are allowed from Telegram to avoid bypassing Slack governance.

---

## 9. Automation Wiring – n8n Patterns

### 9.1 Baseline workflows

Recommended minimal set:

1. **HEALTHCHECK_SLACK**
   - Cron: every 15 minutes.
   - Slack: post a simple success message or maintain a heartbeat in a status channel.

2. **VENDOR_2FA_COMPLIANCE_CHECK**
   - Input:
     - Fetch vendor list (via storage, WebDAV, S3, or manual upload).
   - Logic:
     - Identify `Status = Active` where `2FA Enabled != Yes`.
   - Output:
     - Slack alert to `#dme-alerts` with a summary table.
   - Optional:
     - Create tasks in ClickUp/Monday for remediation.

3. **ALERT_ROUTER**
   - All workflows call this on error.
   - Standard format:
     - Workflow name, error message, environment, severity, link to execution.

4. **TELEGRAM_ALERTS_HIGH_SEVERITY**
   - On `severity = high|critical` from ALERT_ROUTER, send Telegram message.

### 9.2 Integration patterns

- **Vendor webhooks → n8n**
  - E.g., Stripe events, Cloudflare alerts.
  - Configure vendor webhooks to point at `https://n8n-<env>.dme.../webhook/<name>`.
  - n8n validates signatures where possible, fans out to Slack/Telegram/email.

- **n8n → vendor APIs**
  - Use dedicated **credentials** per environment.
  - For each flow, add:
    - Try/catch or error branch.
    - Alert on failures.

---

## 10. 1Password → AWS – Integration 101

### 10.1 Target pattern

Goal: **No long‑lived secrets in code or infra definitions.**  
Applications in AWS read credentials from **1Password** via:

- 1Password Connect server  
- Or a short bridge to AWS Secrets Manager (if needed).

### 10.2 1Password Connect (recommended)

1. Deploy 1Password Connect server in AWS:
   - Run as ECS service, EKS deployment, or EC2 Docker container.
   - Locked down to **internal network** only (private subnet, security group).

2. Create an integration token in 1Password:
   - Restrict to the minimal set of vaults (e.g. `DME-Engineering-Prod`).

3. Configure apps to use Connect:
   - Use official 1Password SDK or HTTP API.
   - At app startup, fetch named secrets:
     - e.g. `CLOUDFLARE - PROD - ADMIN`, field `API_KEY_PROD`.

4. Bind secrets into app:
   - Map retrieved values into environment variables or in‑memory config.
   - Do not write them to disk logs or error messages.

### 10.3 Optional: syncing into AWS Secrets Manager

If you must use AWS Secrets Manager (e.g. for native integrations):

1. Write a scheduled job (Lambda/ECS) that:
   - Reads keys from 1Password.
   - Writes them into Secrets Manager (`PutSecretValue`).
   - Optionally tags them with source metadata.

2. Treat **1Password as canonical**:
   - Never update secrets directly in AWS SM.
   - If a secret changes, update 1Password first and rerun sync job.

3. Use IAM roles:
   - Apps only get `secretsmanager:GetSecretValue` for specific ARNs.

### 10.4 IAM and network security

- Use **IAM roles** for EC2/ECS/EKS tasks:
  - No access keys in code.
- Restrict access:
  - Connect server only accessible from app subnets.
  - Outbound connections from Connect limited to 1Password endpoints.
- Monitor access:
  - CloudTrail for AWS SM.
  - 1Password access logs.

---

## 11. Final DevOps Checklists

### 11.1 Vendor & Identity

- [ ] Master Vendor List populated for all Active vendors.
- [ ] All logins use `@dailymacroedge.com` role addresses.
- [ ] All Active vendors have 2FA enabled.
- [ ] All credentials and API keys stored in 1Password with correct naming.
- [ ] No secrets stored directly in git, Slack, or flat docs.

### 11.2 Email & DNS

- [ ] `dailymacroedge.com` DNS in Cloudflare with correct A/CNAME records to the web server.
- [ ] Proton domain verified and MX/SPF/DKIM/DMARC set and passing.
- [ ] All role mailboxes created; test emails sent/received.

### 11.3 Automation & Alerts

- [ ] Slack Mission Control app installed; slash commands wired.
- [ ] n8n DEV and PROD running; credentials configured.
- [ ] Baseline healthcheck and alert routing workflows in place and tested.
- [ ] Telegram Alerts Bot live, integrated with n8n for high‑severity alerts.

### 11.4 AWS Secrets Integration

- [ ] 1Password Connect (or equivalent) running in AWS.
- [ ] Apps use Connect/AWS SM bridge for secrets, not hardcoded values.
- [ ] IAM roles locked to least privilege for secrets access.

If all of the above are satisfied, the DME vendor, identity, email and automation foundation is considered **ready for production use** and can support further autonomous and AI‑driven workflows safely.
