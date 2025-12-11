from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import os

import hvac  # type: ignore
import psycopg2  # type: ignore


@dataclass
class DBConfig:
    dsn: str


def _fetch_secret_from_vault(path: str, key: str, client: Optional[hvac.Client] = None) -> str:
    addr = os.environ.get("VAULT_ADDR")
    token = os.environ.get("VAULT_TOKEN")
    if not addr or not token:
        raise RuntimeError("VAULT_ADDR and VAULT_TOKEN must be set to use Vault-based secrets")
    client = client or hvac.Client(url=addr, token=token)
    response = client.secrets.kv.v2.read_secret_version(path=path)
    value = response["data"]["data"].get(key)
    if not value:
        raise KeyError(f"Key {key!r} not found in Vault path {path!r}")
    return value


def load_db_config() -> DBConfig:
    vault_path = os.environ.get("ENTITLEMENT_DB_VAULT_PATH")
    if vault_path:
        dsn = _fetch_secret_from_vault(vault_path, "DATABASE_URL")
    else:
        dsn = os.environ.get("DATABASE_URL")
        if not dsn:
            raise RuntimeError("DATABASE_URL is not set and ENTITLEMENT_DB_VAULT_PATH is not configured.")
    return DBConfig(dsn=dsn)


def get_connection() -> psycopg2.extensions.connection:
    cfg = load_db_config()
    return psycopg2.connect(cfg.dsn)
