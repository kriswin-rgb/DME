#!/bin/bash
set -e

echo "Setting up DME development environment..."

command -v node >/dev/null 2>&1 || { echo "Node.js required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3.11+ required"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "docker-compose required"; exit 1; }

cp .env.example .env

cd apps/web && npm install && cd ../..
cd apps/orchestrator && npm install && cd ../..

cd services/dme_core_v5
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
cd ../..

docker-compose up -d postgres redis || echo "docker-compose up failed; ensure Docker is running"

echo "Dev setup complete. Next steps:"
echo "  - Run ./scripts/run_tests.sh"
echo "  - Start web app with: cd apps/web && npm run dev"
