#!/usr/bin/env bash
# Install only the Street Chaves runtime/resources into a local PlayStor checkout.
# Do not replace player source files, game database, or unrelated PlayStor games.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd)"
DEST="${1:-/mnt/user/appdata/playstor}"
BUNDLE="${2:-$ROOT/playstor/web.tar.gz}"
test -f "$DEST/compose.yaml"
test -f "$DEST/public/stormgames/games-player.js"
test -f "$BUNDLE"
test -f "$ROOT/playstor/index.html"
test -f "$ROOT/playstor/street-chaves-runtime.mjs"
TARGET="$DEST/public/pc-web/street-chaves"
mkdir -p "$TARGET"
if [ -f "$TARGET/web.tar.gz" ]; then
  cp -p "$TARGET/web.tar.gz" "$DEST/data/street-chaves-previous-web.tar.gz"
fi
install -m 644 "$BUNDLE" "$TARGET/web.tar.gz"
install -m 644 "$ROOT/playstor/index.html" "$TARGET/index.html"
install -m 644 "$ROOT/playstor/favicon.png" "$TARGET/favicon.png"
install -m 644 "$ROOT/playstor/CREDITS.txt" "$TARGET/CREDITS.txt"
install -m 644 "$ROOT/playstor/street-chaves-runtime.mjs" "$DEST/public/stormgames/street-chaves-runtime.mjs"
sha256sum "$TARGET/web.tar.gz"
echo 'Street Chaves files copied. For first-time setup, integrate player source per docs/PLAYSTOR-INTEGRATION.md.'
echo 'To publish new static files in the existing Docker image, rebuild and restart only the PlayStor service:'
echo " cd '$DEST' && docker compose build playstor && docker compose up -d --no-deps --no-build playstor"
