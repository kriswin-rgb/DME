ui = true
disable_mlock = true

storage "raft" {
  path = "/vault/data"
  node_id = "vault-node-1"
}

listener "tcp" {
  address                           = "0.0.0.0:8200"
  tls_cert_file                     = "/tls/server.crt"
  tls_key_file                      = "/tls/server.key"
  tls_disable_client_certs          = "true"
  tls_min_version                   = "tls12"
  tls_prefer_server_cipher_suites   = "true"
}

api_addr     = "https://localhost:8200"
cluster_addr = "https://dme-vault:8201"

audit "file" {
  path = "/vault/logs/audit.log"
}

telemetry {
  prometheus_retention_time = "24h"
  disable_hostname = true
}
