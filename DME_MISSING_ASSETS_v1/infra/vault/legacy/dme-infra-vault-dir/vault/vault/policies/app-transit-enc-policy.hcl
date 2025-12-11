# App: encrypt-only capability on transit key 'dme' (no decrypt)
path "transit/encrypt/dme" {
  capabilities = ["update"]
}
# Optional: allow reading key metadata if needed
path "transit/keys/dme" {
  capabilities = ["read"]
}
