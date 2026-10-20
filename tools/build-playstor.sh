#!/usr/bin/env bash
# Rebuilds the Street Chaves WebAssembly assets and updates only its existing
# game archive in the PlayStor app. The main PlayStor server is not restarted.
set -euo pipefail

PROJECT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PLAYSTOR="$(cd "$PROJECT/../../.." && pwd)"
DEPLOY="$PLAYSTOR/public/pc-web/street-chaves"
PY="$PROJECT/.venv/bin/python"
PIP="$PROJECT/.venv/bin/pip"

test -d "$PROJECT/source/.git"
test -f "$DEPLOY/index.html"
test -f "$PLAYSTOR/public/stormgames/street-chaves-runtime.mjs"

if [ ! -x "$PY" ]; then
  python3 -m venv "$PROJECT/.venv"
fi
"$PIP" install --disable-pip-version-check 'pygbag==0.9.3' 'pygame-ce>=2.5' 'Pillow>=10' 'numpy>=1.24' 'imageio-ffmpeg>=0.6'

"$PY" "$PROJECT/prepare_port.py"
"$PY" "$PROJECT/convert_media.py"
"$PY" "$PROJECT/fix_surfarray.py"

# Pygbag's regular optimizer can generate stale *-pygbag.py files.
find "$PROJECT/web" -name 'main-pygbag.py' -type f -delete
rm -rf -- "$PROJECT/web/build/web"
mkdir -p "$PROJECT/web/build/web"

"$PY" -m pygbag --no_opt --build --title 'Street Chaves Remaster - PlayStor' "$PROJECT/web"

"$PY" - "$PROJECT/web/build/web/web.tar.gz" <<'PY'
import sys, tarfile
from pathlib import Path
p=Path(sys.argv[1])
with tarfile.open(p,'r:gz') as tar:
    mains=[x for x in tar if x.name == 'assets/main.py']
    assert len(mains)==1, f'expected one main.py; found {len(mains)}'
    code=tar.extractfile(mains[0]).read()
    assert b'pygame.surfarray' not in code, 'NumPy-dependent code still present'
assert p.stat().st_size>1_000_000, 'missing game assets'
print('Verified WASM game archive:',p.stat().st_size,'bytes')
PY

# Keep the last known-good deployed build in this private project folder.
if [ -f "$DEPLOY/web.tar.gz" ]; then
  cp -p "$DEPLOY/web.tar.gz" "$PROJECT/previous-deployed-web.tar.gz"
fi
install -m 644 "$PROJECT/web/build/web/web.tar.gz" "$DEPLOY/web.tar.gz"
sha256sum "$PROJECT/web/build/web/web.tar.gz" "$DEPLOY/web.tar.gz"
echo 'Street Chaves WASM updated inside PlayStor.'
echo 'Docker rebuild is not required for static assets; refresh the browser after cache expiration.'
