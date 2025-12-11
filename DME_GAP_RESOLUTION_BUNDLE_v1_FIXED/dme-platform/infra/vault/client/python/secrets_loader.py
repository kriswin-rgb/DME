from __future__ import annotations

from typing import Dict

from .vault_client import VaultClient


def load_service_secrets(path: str) -> Dict[str, str]:
    client = VaultClient.from_env()
    return client.read_kv2(path)
