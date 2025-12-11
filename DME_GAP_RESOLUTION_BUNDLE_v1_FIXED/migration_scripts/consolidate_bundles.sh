#!/bin/bash
set -e

echo "This script is a template to help you move legacy zip bundles into dme-platform/archive/."
echo "Adjust paths as needed for your environment."

DEST="dme-platform/archive"
mkdir -p "$DEST"

for f in DME_*.zip dme_*.zip; do
  if [ -f "$f" ]; then
    echo "Moving $f -> $DEST/"
    mv "$f" "$DEST/"
  fi
done

echo "Done. Please update archive/README.md to document what was moved."
