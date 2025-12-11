#!/usr/bin/env bash
set -euo pipefail
TLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../tls" && pwd)"
cd "$TLS_DIR"

# Self-signed CA + server cert (localhost + dme-vault)
if [ ! -f ca.key ]; then openssl genrsa -out ca.key 4096; fi
if [ ! -f ca.crt ]; then
  openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt -subj "/C=US/ST=CA/L=SF/O=DME/OU=Security/CN=DME Local CA"
fi

openssl genrsa -out server.key 4096

cat > server.csr.cnf <<'EOF'
[ req ]
prompt = no
distinguished_name = dn
req_extensions = req_ext
[ dn ]
C=US
ST=CA
L=SF
O=DME
OU=Security
CN=localhost
[ req_ext ]
subjectAltName = @alt_names
[ alt_names ]
DNS.1 = localhost
DNS.2 = dme-vault
IP.1  = 127.0.0.1
EOF

openssl req -new -key server.key -out server.csr -config server.csr.cnf

cat > server.ext <<'EOF'
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = localhost
DNS.2 = dme-vault
IP.1 = 127.0.0.1
EOF

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 825 -sha256 -extfile server.ext

echo "TLS artifacts generated in $TLS_DIR"
