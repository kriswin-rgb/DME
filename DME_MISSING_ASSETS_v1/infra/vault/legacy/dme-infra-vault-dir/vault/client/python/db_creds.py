#!/usr/bin/env python3
"""
Fetch dynamic Postgres credentials from Vault (db role).
"""
import json
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ENV = Path(__file__).resolve().parent.parent / ".env.vault"
CA  = Path(__file__).resolve().parents[2] / "tls" / "ca.crt"

def load_env():
    m = {}
    for line in ENV.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k,v = line.split("=",1)
            m[k.strip()] = v.strip()
    return m

def sess():
    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=Retry(total=3, backoff_factor=0.4, status_forcelist=[429,500,502,503,504])))
    return s

def main():
    e = load_env()
    base = e.get("VAULT_ADDR","https://localhost:8200")
    login = sess().post(f"{base}/v1/auth/approle/login", json={"role_id": e["VAULT_ROLE_ID_DB"], "secret_id": e["VAULT_SECRET_ID_DB"]}, verify=str(CA), timeout=5)
    login.raise_for_status()
    token = login.json()["auth"]["client_token"]

    creds = sess().get(f"{base}/v1/database/creds/app-readonly", headers={"X-Vault-Token": token}, verify=str(CA), timeout=5)
    creds.raise_for_status()
    print(json.dumps(creds.json()["data"], indent=2))

if __name__ == "__main__":
    main()
