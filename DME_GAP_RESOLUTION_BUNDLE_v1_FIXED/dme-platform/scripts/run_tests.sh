#!/bin/bash
set -e

echo "Running backend tests..."
pytest services/dme_core_v5/tests

echo "Running integration tests..."
pytest tests/integration

echo "Running frontend tests..."
cd apps/web
npm test -- --coverage
