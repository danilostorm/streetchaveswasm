from pathlib import Path
from PIL import Image
import numpy as np
W=Path('/mnt/user/appdata/playstor/data/projects/street-chaves-wasm/web')
p=W/'main.py';s=p.read_text(encoding='utf-8')
start=s.index('def make_transparent(img):')
end=s.index('\n\n# ============================================================',start)
s=s[:start]+'''def make_transparent(img):
    """Transparency is prepared in RGBA at build time; no NumPy required."""
    return img.convert_alpha()
'''+s[end:]
s=s.replace('img = pygame.image.load(path).convert()', 'img = pygame.image.load(path).convert_alpha()')
assert 'pygame.surfarray' not in s
p.write_text(s,encoding='utf-8')
from collections import Counter
count=Counter()
for folder in ['Animacoes','Efeitos','Rostos']:
  for png in (W/folder).glob('*.png'):
    with Image.open(png) as im:
      ar=np.asarray(im.convert('RGB'))
      h,w,_=ar.shape
      out=np.empty((h,w,4),dtype=np.uint8)
      out[:,:,:3]=ar
      out[:,:,3]=np.where(np.all(ar>=248,axis=2),0,255).astype(np.uint8)
      Image.fromarray(out,'RGBA').save(png,optimize=True)
    count[folder]+=1
print('RGBA transparent prepared:',count)
import py_compile
py_compile.compile(str(p),doraise=True)
print('Source passes syntax; runtime no longer uses pygame.surfarray')
