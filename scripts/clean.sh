#!/bin/bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT" || exit 1
echo "Cleaning up project at: $PROJECT_ROOT"

find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

for dir in build .venv dist .pytest_cache .ruff_cache; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "Removed $dir/"
    fi
done

echo "Cleanup complete!"
