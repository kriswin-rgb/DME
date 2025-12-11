/**
 * KV read using AppRole (kv role) with CA pinning via undici Agent.
 */
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { Agent } from "undici";

const envPath = path.resolve(process.cwd(), "client/.env.vault");
const caPath  = path.resolve(process.cwd(), "tls/ca.crt");

const env = Object.fromEntries(
  fs.readFileSync(envPath, "utf8")
    .split("\n")
    .filter(Boolean)
    .filter((l) => !l.trim().startsWith("#"))
    .map((l) => l.split("=", 2).map((s) => s.trim()))
);

const base = env.VAULT_ADDR || "https://localhost:8200";
const roleId = env.VAULT_ROLE_ID_KV;
const secretId = env.VAULT_SECRET_ID_KV;

const ca = fs.readFileSync(caPath, "utf8");
const dispatcher = new Agent({ connect: { ca, timeout: 5000 }, headersTimeout: 5000, bodyTimeout: 5000 });

const loginRes = await fetch(`${base}/v1/auth/approle/login`, {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ role_id: roleId, secret_id: secretId }),
  dispatcher
});
if (!loginRes.ok) { console.error(await loginRes.text()); process.exit(1); }
const token = (await loginRes.json()).auth.client_token;

const kvRes = await fetch(`${base}/v1/kv/data/app/demo`, { headers: { "X-Vault-Token": token }, dispatcher });
if (!kvRes.ok) { console.error(await kvRes.text()); process.exit(1); }
const data = await kvRes.json();
console.log(JSON.stringify(data.data.data, null, 2));
