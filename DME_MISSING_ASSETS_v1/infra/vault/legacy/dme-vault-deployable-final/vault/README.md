# Vault Dev Deployment (Final, Deep-Swept)

This bundle is validated for a clean boot, init, unseal, policy + AppRole creation, and a successful KV read.

## Quick start
```
cd infra/vault
docker compose up -d            # or: docker-compose up -d
bash scripts/bootstrap.sh
bash scripts/test_kv.sh
```
UI: http://localhost:18200

## Extras
- `scripts/run_agent.sh` — runs Vault Agent against the running container; renders `agent/output/myapp_config.txt`
- `scripts/cleanup.sh` — tears everything down including volumes

## Production notes
- Enable TLS in `vault/config/vault.hcl` (set `tls_disable=0`, provide cert/key, min TLS 1.2)
- Consider Raft HA + Auto-Unseal (KMS), mTLS, and dedicated policies per app
