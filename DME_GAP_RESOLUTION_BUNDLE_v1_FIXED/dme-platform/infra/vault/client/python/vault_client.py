from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import os

import hvac  # type: ignore


@dataclass
class VaultClient:
    url: str
    token: str

    @classmethod
    def from_env(cls) -> "VaultClient":
        url = os.environ.get("VAULT_ADDR")
        token = os.environ.get("VAULT_TOKEN")
        if not url or not token:
            raise RuntimeError("VAULT_ADDR and VAULT_TOKEN must be set")
        return cls(url=url, token=token)

    def _client(self) -> hvac.Client:
        return hvac.Client(url=self.url, token=self.token)

    def read_kv2(self, path: str) -> Dict[str, Any]:
        client = self._client()
        resp = client.secrets.kv.v2.read_secret_version(path=path)
        return resp["data"]["data"]
