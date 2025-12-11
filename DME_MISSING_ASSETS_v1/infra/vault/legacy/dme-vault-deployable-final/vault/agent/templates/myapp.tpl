# Rendered by Vault Agent
{{ with secret "secret/data/myapp/config" -}}
username={{ .Data.data.username }}
password={{ .Data.data.password }}
{{- end }}
