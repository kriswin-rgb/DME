# DME Secrets Management PoC v3 — Vault + AppRole + Agent + Transit + Dynamic DB

**Date:** 2025-11-03

Third pass with deeper hardening and broader coverage:
- **Vault Agent auto-auth** (AppRole) renders a **template file** for apps that prefer *not* to call Vault directly.
- **Transit** engine for **encryption-as-a-service** (encrypt-only policy).
- **Database** engine issuing **dynamic Postgres credentials** (TTL-bound, auto-revoked).
- **Multiple AppRoles** (kv / transit-enc / db) to enforce **least privilege** per use case.
- **Wrapped secret_id issuance** helper (no raw secret_id transport).
- Maintains: TLS, Raft, audit, healthchecks, idempotent bootstrap, CIDR binding.

---

## Quickstart

```bash
# 1) TLS
bash scripts/generate_certs.sh

# 2) Up services
docker compose up -d

# 3) Bootstrap Vault (init, unseal, kv/transit/db, policies, approles, agent files)
bash scripts/bootstrap.sh

# 4) Test KV (Python)
python3 -m venv .venv && source .venv/bin/activate
pip install -r client/python/requirements.txt
python client/python/get_kv.py

# 5) Test Transit (encrypt-only)
python client/python/transit_encrypt.py

# 6) Test dynamic DB creds
python client/python/db_creds.py

# 7) Try Vault Agent rendered file
# After a few seconds, check:
cat agent/rendered/secrets.env
```

---

## Security Enhancements in v3

- **Agent auto-auth** removes Vault client logic from apps. Agent acquires token using **AppRole** and renders templates securely.
- **Encrypt-only policy** prevents data exfiltration: clients can encrypt but **cannot decrypt** with the same role.
- **Dynamic DB creds** eliminate long-lived DB passwords; creds expire automatically, drastically reducing blast radius.
- **Wrapped secret_id** issuance (`scripts/issue-wrapped-secret-id.sh`) prevents direct sharing of secret IDs.
- **No echoing secrets** in bootstrap; all role/secret IDs are saved to `client/.env.vault` and role/secret files for agent only.

---

## Policies & AppRoles

- `app-kv-policy.hcl` → **read-only** `kv/data/app/demo` → role **app-kv**
- `app-transit-enc-policy.hcl` → **update** `transit/encrypt/dme` (encrypt-only) → role **app-transit-enc**
- `app-db-read-policy.hcl` → **read** `database/creds/app-readonly` → role **app-db-read**
- `app-demo-writer.hcl` → rotate KV demo secret only

Each role has **short TTLs**, limited `secret_id` uses, and optional `BOUND_CIDR` restrictions.

---

## Vault Agent

- Config at `agent/agent.hcl` uses **AppRole** for **app-kv** to render `agent/rendered/secrets.env` from template.
- Template at `agent/templates/kv_demo.tpl` pulls `kv/data/app/demo` and writes `APP_DEMO_API_KEY=...`
- Application containers can consume `secrets.env` without talking to Vault.

---

## Production Hardening Reminders

- Use **real CA certificates**; enable **mTLS** (`tls_client_ca_file`) for clients/services.
- Use **Auto-Unseal** (KMS) and never store unseal keys manually.
- Place Vault on private networks; front with Zero Trust; restrict ingress.
- Split policies **per service**; deny by default; smallest possible paths.
- Enable **wrap/unwrap** and OIDC logins for operators; use just-in-time short-lived tokens.
- Store audit logs in **immutable** storage; practice **DR restores** regularly.

---

## Helper: Wrapped Secret ID Issuance

```bash
# Create a single-use wrap token for a secret_id (requires operator token with approle access)
VAULT_TOKEN=<op-token> ROLE_NAME=app-kv WRAP_TTL=5m bash scripts/issue-wrapped-secret-id.sh
# Give the printed wrap token to the client to unwrap once.
```

---

## File Map

- `docker-compose.yml` — Vault + Postgres + Vault Agent
- `vault/config/vault.hcl` — Raft, TLS, audit
- Policies: `app-kv-policy.hcl`, `app-transit-enc-policy.hcl`, `app-db-read-policy.hcl`, `app-demo-writer.hcl`
- Agent: `agent/agent.hcl`, `agent/templates/kv_demo.tpl`, `agent/rendered/secrets.env` (generated)
- Scripts: `generate_certs.sh`, `bootstrap.sh`, `issue-wrapped-secret-id.sh`
- Clients (Python): `get_kv.py`, `transit_encrypt.py`, `db_creds.py`
- Client (Node): `getSecret.mjs`
