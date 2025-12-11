import process from 'node:process';

export class VaultClient {
  constructor(url, token) {
    if (!url || !token) {
      throw new Error('VAULT_ADDR and VAULT_TOKEN must be set');
    }
    this.url = url;
    this.token = token;
  }

  static fromEnv() {
    return new VaultClient(process.env.VAULT_ADDR, process.env.VAULT_TOKEN);
  }

  async readKv2(path) {
    // Minimal example using fetch; replace with full-featured client if desired.
    const resp = await fetch(`${this.url}/v1/${path}`, {
      headers: { 'X-Vault-Token': this.token }
    });
    if (!resp.ok) {
      throw new Error(`Vault read failed: ${resp.status}`);
    }
    const data = await resp.json();
    return data.data.data;
  }
}
