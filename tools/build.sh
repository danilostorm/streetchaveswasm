#!/usr/bin/env bash
# Rebuild Street Chaves WASM. Writes under .build, never modifies live PlayStor.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd)"
WORK="$ROOT/.build/web"
test -f "$ROOT/web/main.py"
test -f "$ROOT/playstor/index.html"
command -v python3 >/dev/null

if [ ! -x "$ROOT/.venv/bin/python" ]; then
  python3 -m venv "$ROOT/.venv"
fi
"$ROOT/.venv/bin/python" -m pip install --disable-pip-version-check 'pygbag==0.9.3'
mkdir -p "$ROOT/.build"
rm -rf -- "$WORK"
mkdir -p "$WORK/build/web"
"$ROOT/.venv/bin/python" - "$ROOT" "$WORK" <<'PY'
from pathlib import Path
import shutil,sys
root=Path(sys.argv[1])
dest=Path(sys.argv[2])
shutil.copytree(root/'web',dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc','build','main-pygbag.py'))
assert (dest/'main.py').exists()
PY
"$ROOT/.venv/bin/python" -m pygbag --no_opt --build --title 'Street Chaves Remaster - PlayStor' "$WORK"
"$ROOT/.venv/bin/python" - "$WORK/build/web/web.tar.gz" <<'PY'
import sys,tarfile
from pathlib import Path
archive=Path(sys.argv[1])
with tarfile.open(archive,'r:gz') as tf:
    mains=[m for m in tf if m.name=='assets/main.py']
    assert len(mains)==1, 'expected exactly one main.py'
    script=tf.extractfile(mains[0]).read()
    assert b'pygame.surfarray' not in script, 'NumPy runtime dependency detected'
assert archive.stat().st_size>5_000_000,'missing game resources'
print('Compiled and verified:',archive,archive.stat().st_size,'bytes')
PY
echo "Build complete. To deploy, copy: $WORK/build/web/web.tar.gz"
