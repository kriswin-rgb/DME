#!/bin/sh
set -e

echo "⏳ Waiting for PostgreSQL to be ready..."
until nc -z db 5432; do
  echo "🕒 Still waiting for PostgreSQL..."
  sleep 2
done

echo "✅ Database is ready! Running Drizzle migrations..."
npx drizzle-kit migrate || echo "⚠️ Migration step skipped or failed, continuing..."

echo "🚀 Starting Next.js app..."

# Force binding to all interfaces
export PORT=3000
export HOSTNAME=0.0.0.0

if [ -f "server.js" ]; then
  node server.js
else
  echo "⚠️ server.js not found, falling back to npm start"
  npm run start
fi