"""Template script to assist with migrating .env secrets into Vault.

This does NOT talk to a real Vault instance by default. Replace the stubbed
`push_to_vault` function with your actual Vault API calls.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict


def load_env_file(path: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()
    return data


def push_to_vault(service: str, key: str, value: str) -> None:
    # TODO: Replace this with hvac client calls.
    print(f"[DRY-RUN] Would write secret for {service}/{key} to Vault")


def migrate(path: str, service: str) -> None:
    env = load_env_file(path)
    for k, v in env.items():
        push_to_vault(service, k, v)


if __name__ == "__main__":
    env_path = os.environ.get("ENV_FILE", ".env")
    service_name = os.environ.get("SERVICE_NAME", "dme-platform")
    migrate(env_path, service_name)
