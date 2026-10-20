from pathlib import Path
from PIL import Image
from subprocess import run, DEVNULL
import imageio_ffmpeg
W=Path('/mnt/user/appdata/playstor/data/projects/street-chaves-wasm/web')
ff=imageio_ffmpeg.get_ffmpeg_exe()
audio_images={}
for folder in ['Animacoes','Cenarios','Efeitos','Rostos']:
    n=0
    for src in (W/folder).glob('*.bmp'):
        dest=src.with_suffix('.png')
        if not dest.exists():
            with Image.open(src) as img: img.save(dest, optimize=True)
        assert dest.stat().st_size>100,(src,dest)
        src.unlink();n+=1
    audio_images[folder]=n
for folder in ['Falas','Sons','Musicas']:
    n=0
    for src in (W/folder).glob('*.wav'):
        dest=src.with_suffix('.ogg')
        if not dest.exists() or dest.stat().st_size<100:
            p=run([ff,'-nostdin','-hide_banner','-loglevel','error','-y','-i',str(src),'-c:a','libvorbis','-qscale:a','3',str(dest)],stdout=DEVNULL,stderr=-1,text=True)
            if p.returncode: raise RuntimeError(f'{src}: {p.stderr[:400]}')
        src.unlink();n+=1
    audio_images[folder]=n
p=W/'main.py';s=p.read_text(encoding='utf-8')
s=s.replace('.bmp', '.png').replace('.wav','.ogg')
p.write_text(s,encoding='utf-8')
print('Media converted:',audio_images)
print('All game media size (MB):',round(sum(f.stat().st_size for f in W.rglob('*') if f.is_file() and 'build' not in f.parts)/1048576,2))
