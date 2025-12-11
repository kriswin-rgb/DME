# DEV profile — enable TLS for prod (see comments below).
ui = true
disable_mlock = true

storage "raft" {
  path    = "/vault/data"
  node_id = "vault-node-1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
  # --- PROD EXAMPLE ---
  # tls_disable     = 0
  # tls_cert_file   = "/vault/config/tls/server.crt"
  # tls_key_file    = "/vault/config/tls/server.key"
  # tls_min_version = "tls12"
}

api_addr     = "http://localhost:8200"
cluster_addr = "http://dme-vault:8201"

audit "file" {
  path = "/vault/logs/audit.log"
}
