# Vault Integration Guide

- Python services should use `infra.vault.client.python.vault_client.VaultClient`
  and helper loaders to fetch secrets.
- Node.js apps should use `infra/vault/client/nodejs/vault_client.js`.

For local development, apps may fall back to `.env` environment variables.
