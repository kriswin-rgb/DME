#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
VAULT_CONT="dme-vault"
docker exec "$VAULT_CONT" sh -lc 'VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=$(cat /vault/keys/myapp_token.txt) vault kv get secret/myapp/config'
