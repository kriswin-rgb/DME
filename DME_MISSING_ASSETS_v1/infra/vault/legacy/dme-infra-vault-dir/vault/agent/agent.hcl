pid_file = "/agent/pidfile"

auto_auth {
  method "approle" {
    mount_path = "auth/approle"
    config = {
      role_id_file_path   = "/client/.env.vault.role_kv"
      secret_id_file_path = "/client/.env.vault.secret_kv"
    }
  }

  sink "file" {
    config = {
      path = "/agent/token"
    }
  }
}

template {
  source      = "/agent/templates/kv_demo.tpl"
  destination = "/agent/rendered/secrets.env"
}
