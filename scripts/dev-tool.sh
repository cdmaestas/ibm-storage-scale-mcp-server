#!/bin/bash
# Run a project dev tool (ruff, pytest, ...) with whichever environment is
# available, so git hooks work whether or not `uv` is on PATH:
#   1. uv on PATH        -> uv run <tool>
#   2. project venv      -> .venv/bin/<tool>
#   3. plain PATH lookup -> <tool>
# Fails loudly rather than silently skipping if the tool cannot be found.
set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "usage: $0 <tool> [args...]" >&2
    exit 2
fi

tool="$1"
shift

if command -v uv >/dev/null 2>&1; then
    exec uv run "$tool" "$@"
fi

if [ -x ".venv/bin/$tool" ]; then
    exec ".venv/bin/$tool" "$@"
fi

if command -v "$tool" >/dev/null 2>&1; then
    exec "$tool" "$@"
fi

echo "ASSERT: cannot find '$tool'. Install uv, or run: uv sync --all-groups" >&2
exit 1
