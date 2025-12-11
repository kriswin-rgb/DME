# Rendered by Vault Agent
# Exposes one env var with the KV demo secret value
{{ with secret "kv/data/app/demo" -}}
APP_DEMO_API_KEY="{{ .Data.data.api_key }}"
{{- end }}
