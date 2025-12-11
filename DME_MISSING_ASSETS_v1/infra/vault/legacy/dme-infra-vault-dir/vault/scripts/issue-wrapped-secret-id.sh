#!/usr/bin/env bash
set -euo pipefail
# Issue a wrapped SECRET_ID for AppRole to avoid transmitting raw secret_id directly.
# Usage: VAULT_TOKEN=<operator-token> ROLE_NAME=app-kv WRAP_TTL=5m ./scripts/issue-wrapped-secret-id.sh

ROLE_NAME="${ROLE_NAME:-app-kv}"
WRAP_TTL="${WRAP_TTL:-5m}"
VAULT_ADDR="${VAULT_ADDR:-https://localhost:8200}"
VAULT_CACERT="${VAULT_CACERT:-./tls/ca.crt}"

# Create a wrapped response
WRAPPED=$(vault write -ca-cert="$VAULT_CACERT" -address="$VAULT_ADDR" -wrap-ttl="$WRAP_TTL" -f auth/approle/role/${ROLE_NAME}/secret-id -format=json)
WRAP_TOKEN=$(echo "$WRAPPED" | python3 -c 'import sys,json;print(json.load(sys.stdin)["wrap_info"]["token"])')

echo "Give this single-use wrap token to the client to unwrap within ${WRAP_TTL}:"
echo "$WRAP_TOKEN"
