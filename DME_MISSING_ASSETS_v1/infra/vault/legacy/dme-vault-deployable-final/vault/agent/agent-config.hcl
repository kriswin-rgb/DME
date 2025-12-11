pid_file = "/vault/agent/pidfile"

vault {
  address = "http://dme-vault:8200"
  retry { num_retries = 5 }
}

auto_auth {
  method "approle" {
    mount_path = "auth/approle"
    config = {
      role_id_file_path   = "/vault/agent/role_id"
      secret_id_file_path = "/vault/agent/secret_id"
    }
  }
  sink "file" { config = { path = "/vault/agent/output/agent-token.txt" } }
}

template {
  source      = "/vault/agent/templates/myapp.tpl"
  destination = "/vault/agent/output/myapp_config.txt"
}
