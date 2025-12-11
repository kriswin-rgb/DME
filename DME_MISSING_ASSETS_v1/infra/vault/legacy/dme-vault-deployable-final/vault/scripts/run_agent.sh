#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

docker run --rm --name dme-vault-agent --network container:dme-vault   -v "$(pwd)/agent:/vault/agent"   hashicorp/vault:1.16 agent -config=/vault/agent/agent-config.hcl
