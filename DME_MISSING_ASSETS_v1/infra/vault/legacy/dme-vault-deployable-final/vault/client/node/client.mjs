// Node 18+
import process from 'node:process';
const addr = process.env.VAULT_ADDR || 'http://localhost:18200';
const token = process.env.VAULT_TOKEN;
if (!token) { console.error('Set VAULT_TOKEN (keys/myapp_token.txt).'); process.exit(1); }
const res = await fetch(`${addr}/v1/secret/data/myapp/config`, { headers: { 'X-Vault-Token': token } });
if (!res.ok) { console.error(await res.text()); process.exit(1); }
console.log(JSON.stringify((await res.json()).data.data, null, 2));
