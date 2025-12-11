#!/usr/bin/env python3
import os, json, requests, sys
addr = os.getenv("VAULT_ADDR", "http://localhost:18200")
token = os.getenv("VAULT_TOKEN")
if not token:
    print("Set VAULT_TOKEN (keys/myapp_token.txt).", file=sys.stderr); sys.exit(1)
r = requests.get(f"{addr}/v1/secret/data/myapp/config", headers={"X-Vault-Token": token})
r.raise_for_status()
print(json.dumps(r.json()["data"]["data"], indent=2))
