#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Prefer docker compose, fall back to docker-compose
if command -v docker-compose >/dev/null 2>&1; then
  DC="docker-compose"
else
  DC="docker compose"
fi

VAULT_CONT="dme-vault"

echo "==> Starting Vault container..."
$DC up -d vault

echo "==> Waiting for Vault HTTP endpoint..."
ok=0
for i in {1..40}; do
  if docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault status >/dev/null 2>&1'; then
    ok=1; break
  fi
  sleep 2
done
if [ "$ok" -ne 1 ]; then
  echo "ERROR: Vault did not become reachable in time." >&2
  exit 1
fi

echo "==> Checking initialization state..."
if docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault status | grep -q "Initialized *true"'; then
  echo "Already initialized; skipping init/unseal."
else
  echo "==> Initializing Vault (1 key share, threshold 1)..."
  INIT_JSON=$(docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault operator init -key-shares=1 -key-threshold=1 -format=json')
  mkdir -p keys
  printf '%s' "$INIT_JSON" > keys/init-keys.json

  UNSEAL_KEY=$(printf '%s' "$INIT_JSON" | python3 -c 'import sys,json; j=json.load(sys.stdin); print(j["unseal_keys_b64"][0])' 2>/dev/null || true)
  ROOT_TOKEN=$(printf '%s' "$INIT_JSON" | python3 -c 'import sys,json; j=json.load(sys.stdin); print(j["root_token"])' 2>/dev/null || true)

  if [ -z "${UNSEAL_KEY:-}" ] || [ -z "${ROOT_TOKEN:-}" ]; then
    # Fallback to non-JSON parsing if python3 not available on host
    UNSEAL_KEY=$(grep -o '"unseal_keys_b64":\[\s*"[^"]\+"' keys/init-keys.json | sed -E 's/.*"unseal_keys_b64":\[\s*"([^"]+)".*/\1/')
    ROOT_TOKEN=$(grep -o '"root_token":\s*"[^"]+"' keys/init-keys.json | sed -E 's/.*"root_token":\s*"([^"]+)".*/\1/')
  fi

  printf '%s' "$UNSEAL_KEY" > keys/unseal_key.txt
  printf '%s' "$ROOT_TOKEN" > keys/root_token.txt
  chmod 600 keys/unseal_key.txt keys/root_token.txt keys/init-keys.json

  echo "==> Unsealing Vault..."
  docker exec "$VAULT_CONT" sh -lc "VAULT_ADDR=http://127.0.0.1:8200 vault operator unseal $(cat keys/unseal_key.txt)"

  echo "==> Logging in with root token..."
  docker exec "$VAULT_CONT" sh -lc "VAULT_ADDR=http://127.0.0.1:8200 vault login $(cat keys/root_token.txt) >/dev/null"
fi

echo "==> Enabling KV v2 at secret/ (idempotent)..."
docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault secrets enable -path=secret -version=2 kv || true'

echo "==> Writing sample secret at secret/myapp/config ..."
docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault kv put secret/myapp/config username="vault-user" password="vault-pass"'

echo "==> Creating policy from policies/myapp-policy.hcl ..."
docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault policy write myapp-policy /vault/policies/myapp-policy.hcl'

echo "==> Enabling AppRole auth..."
docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault auth enable approle || true'

echo "==> Creating AppRole (myapp-role) with myapp-policy..."
docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault write auth/approle/role/myapp-role token_policies="myapp-policy" token_ttl=1h token_max_ttl=4h >/dev/null'

ROLE_ID=$(docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault read -field=role_id auth/approle/role/myapp-role/role-id')
SECRET_ID=$(docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault write -field=secret_id -f auth/approle/role/myapp-role/secret-id')

printf '%s' "$ROLE_ID"  > agent/role_id
printf '%s' "$SECRET_ID" > agent/secret_id
chmod 600 agent/role_id agent/secret_id

echo "==> Creating a short-lived test token with myapp-policy..."
TEST_TOKEN=$(docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 vault token create -policy=myapp-policy -ttl=1h -format=json' | python3 -c 'import sys,json; print(json.load(sys.stdin)["auth"]["client_token"])')
printf '%s' "$TEST_TOKEN" > keys/myapp_token.txt
chmod 600 keys/myapp_token.txt

cat <<EOF

Bootstrap complete.

Vault UI: http://localhost:18200

Files:
- keys/unseal_key.txt
- keys/root_token.txt
- keys/myapp_token.txt
- agent/role_id
- agent/secret_id
EOF
