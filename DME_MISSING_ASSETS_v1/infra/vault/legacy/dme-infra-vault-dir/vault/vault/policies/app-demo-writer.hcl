# Operator: rotate only the demo KV secret
path "kv/data/app/demo" {
  capabilities = ["create", "update", "read"]
}
