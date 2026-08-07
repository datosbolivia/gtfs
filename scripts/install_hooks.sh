#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)

chmod +x "$ROOT_DIR/.githooks/"* 2>/dev/null || true

git config core.hooksPath "$ROOT_DIR/.githooks"
echo "✅ Git hooks configured to use '$ROOT_DIR/.githooks'!"
