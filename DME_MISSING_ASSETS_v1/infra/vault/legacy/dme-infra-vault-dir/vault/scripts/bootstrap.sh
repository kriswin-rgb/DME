#!/usr/bin/env bash
set -euo pipefail

VAULT_CONTAINER="dme-vault"
VAULT_ADDR_IN_CONTAINER="https://127.0.0.1:8200"
VAULT_ADDR_HOST="https://localhost:8200"
VAULT_CACERT="/tls/ca.crt"
POSTGRES_DSN="postgresql://postgres:postgrespass@dme-postgres:5432/postgres?sslmode=disable"

# Optional CIDR binding for approle tokens/secret_ids (e.g., 127.0.0.1/32 for local)
BOUND_CIDR="${BOUND_CIDR:-}"

vin() {
  docker exec -e VAULT_ADDR="${VAULT_ADDR_IN_CONTAINER}" -e VAULT_CACERT="${VAULT_CACERT}" "$VAULT_CONTAINER" vault "$@"
}

echo "==> Checking Vault status..."
if docker exec "$VAULT_CONTAINER" sh -lc 'VAULT_ADDR=https://127.0.0.1:8200 VAULT_CACERT=/tls/ca.crt vault status | grep -q "Initialized *true"'; then
  echo "Vault already initialized. Exiting to avoid re-init."
  exit 0
fi

echo "==> Initializing Vault..."
INIT_JSON=$(docker exec "$VAULT_CONTAINER" vault operator init -key-shares=1 -key-threshold=1 -format=json)

# Parse JSON safely using Python (no jq requirement)
UNSEAL_KEY=$(python3 - <<'PY'
import json,os
j=json.loads(os.environ["INIT_JSON"])
print(j["unseal_keys_b64"][0])
PY
)
ROOT_TOKEN=$(python3 - <<'PY'
import json,os
j=json.loads(os.environ["INIT_JSON"])
print(j["root_token"])
PY
)

echo "==> Unsealing..."
docker exec "$VAULT_CONTAINER" vault operator unseal "$UNSEAL_KEY"

echo "==> Login with bootstrap token..."
vin login "${ROOT_TOKEN}" >/dev/null

echo "==> Enable audit (file)..."
vin audit enable file file_path=/vault/logs/audit.log || true

echo "==> Enable KV v2 at 'kv/' and write demo secret..."
vin secrets enable -path=kv kv-v2 || true
vin kv put kv/app/demo api_key="demo-ABC123" note="example secret value"

echo "==> Enable Transit and create key 'dme' (encrypt only via policy)..."
vin secrets enable transit || true
vin write -f transit/keys/dme deletion_allowed=false exportable=false >/dev/null

echo "==> Enable Database engine and configure Postgres (local)"
vin secrets enable database || true
vin write database/config/dme-postgres   plugin_name=postgresql-database-plugin   allowed_roles=app-readonly   connection_url="${POSTGRES_DSN}"   username="postgres"   password="postgrespass" >/dev/null

vin write database/roles/app-readonly   db_name=dme-postgres   creation_statements="CREATE ROLE "{{name}}" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT CONNECT ON DATABASE postgres TO "{{name}}"; GRANT USAGE ON SCHEMA public TO "{{name}}"; GRANT SELECT ON ALL TABLES IN SCHEMA public TO "{{name}}"; ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "{{name}}";"   default_ttl="1h"   max_ttl="24h" >/dev/null

echo "==> Write policies..."
vin policy write app-kv /vault/policies/app-kv-policy.hcl
vin policy write app-transit-enc /vault/policies/app-transit-enc-policy.hcl
vin policy write app-db-read /vault/policies/app-db-read-policy.hcl
vin policy write app-demo-writer /vault/policies/app-demo-writer.hcl

echo "==> Enable AppRole and create roles..."
vin auth enable approle || true

BOUND_OPTS=""
if [ -n "$BOUND_CIDR" ]; then
  BOUND_OPTS="token_bound_cidrs=${BOUND_CIDR} secret_id_bound_cidrs=${BOUND_CIDR}"
fi

# KV role
vin write auth/approle/role/app-kv token_policies="app-kv" token_ttl="1h" token_max_ttl="4h" secret_id_num_uses=10 secret_id_ttl=30m ${BOUND_OPTS} >/dev/null
ROLE_ID_KV=$(vin read -field=role_id auth/approle/role/app-kv/role-id)
SECRET_ID_KV=$(vin write -field=secret_id -f auth/approle/role/app-kv/secret-id)

# Transit encrypt role
vin write auth/approle/role/app-transit-enc token_policies="app-transit-enc" token_ttl="30m" token_max_ttl="2h" secret_id_num_uses=5 secret_id_ttl=15m ${BOUND_OPTS} >/dev/null
ROLE_ID_TR=$(vin read -field=role_id auth/approle/role/app-transit-enc/role-id)
SECRET_ID_TR=$(vin write -field=secret_id -f auth/approle/role/app-transit-enc/secret-id)

# DB creds role
vin write auth/approle/role/app-db-read token_policies="app-db-read" token_ttl="30m" token_max_ttl="2h" secret_id_num_uses=5 secret_id_ttl=15m ${BOUND_OPTS} >/dev/null
ROLE_ID_DB=$(vin read -field=role_id auth/approle/role/app-db-read/role-id)
SECRET_ID_DB=$(vin write -field=secret_id -f auth/approle/role/app-db-read/secret-id)

# Write client env files (do not echo secrets to console)
mkdir -p client
cat > client/.env.vault <<EOF
VAULT_ADDR=${VAULT_ADDR_HOST}
VAULT_CACERT=../tls/ca.crt

# KV
VAULT_ROLE_ID_KV=${ROLE_ID_KV}
VAULT_SECRET_ID_KV=${SECRET_ID_KV}

# Transit (encrypt-only)
VAULT_ROLE_ID_TR=${ROLE_ID_TR}
VAULT_SECRET_ID_TR=${SECRET_ID_TR}

# Database (dynamic creds)
VAULT_ROLE_ID_DB=${ROLE_ID_DB}
VAULT_SECRET_ID_DB=${SECRET_ID_DB}
EOF

# Files for vault-agent auto_auth
echo -n "${ROLE_ID_KV}"  > client/.env.vault.role_kv
echo -n "${SECRET_ID_KV}" > client/.env.vault.secret_kv

echo "Client env written to client/.env.vault (and role/secret files for agent)."

echo "==> Revoking bootstrap/root token..."
vin token revoke -self || true

echo "Bootstrap complete."
