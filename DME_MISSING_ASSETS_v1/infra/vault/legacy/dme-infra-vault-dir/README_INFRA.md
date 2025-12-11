# /infra/vault — DME Secrets Stack (Vault + Agent + Transit + Dynamic DB)

Generated: 2025-11-03

Drop this folder at the root of your repo:
  - `infra/vault/docker-compose.yml` spins up: Vault (TLS, Raft, audit), Postgres, Vault Agent
  - `infra/vault/scripts/*` bootstrap, rotate, wrap helpers
  - `infra/vault/vault/config/*` server config
  - `infra/vault/vault/policies/*` least-privilege policies
  - `infra/vault/agent/*` auto-auth + templates (renders `agent/rendered/secrets.env`)

Quick start (local/dev):
  1) `cd infra/vault`
  2) `bash scripts/generate_certs.sh`
  3) `docker compose up -d`
  4) `bash scripts/bootstrap.sh`
  5) Test clients: see `README.md` inside this directory.

Security notes:
  - Self-signed TLS for local use; replace with real CA in prod.
  - Enable mTLS in `vault/config/vault.hcl` for production.
  - Use response wrapping + short TTLs for AppRole Secret IDs.
  - Store any credentials in a vault (Proton Pass/1Password), not in git.
