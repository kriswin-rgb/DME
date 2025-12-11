import os

import pytest

from services.entitlement_sds_service.src.db_connector import load_db_config, _fetch_secret_from_vault


def test_load_db_config_env_fallback(monkeypatch):
    monkeypatch.delenv("ENTITLEMENT_DB_VAULT_PATH", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/dme")
    cfg = load_db_config()
    assert cfg.dsn.startswith("postgresql://")


def test_fetch_secret_from_vault_missing_env(monkeypatch):
    monkeypatch.delenv("VAULT_ADDR", raising=False)
    monkeypatch.delenv("VAULT_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        _fetch_secret_from_vault("secret/data/dme", "DATABASE_URL", None)
