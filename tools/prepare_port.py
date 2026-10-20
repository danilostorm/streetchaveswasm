"""Prepare a separately staged Street Chaves port for Pygbag, without changing upstream."""
from pathlib import Path
from PIL import Image
import numpy as np
import shutil, json, sys, re

ROOT = Path("/mnt/user/appdata/playstor/data/projects/street-chaves-wasm")
SRC = ROOT / "source"
WEB = ROOT / "web"
WEB.mkdir(exist_ok=True)
FOLDERS = ["Animacoes", "Cenarios", "Efeitos", "Falas", "Musicas", "Rostos", "Sons"]
for folder in FOLDERS:
    shutil.copytree(SRC / folder, WEB / folder, dirs_exist_ok=True)
(WEB / "Lutadores").mkdir(exist_ok=True)

stats = {}
for bmp in sorted((SRC / "Lutadores").glob("*.bmp")):
    rgb = np.asarray(Image.open(bmp).convert("RGB"))
    h, w, _ = rgb.shape
    sep = np.flatnonzero((rgb.max(axis=2) <= 50).mean(axis=0) >= .95).tolist()
    boundaries = sep + ([w] if (not sep or sep[-1] != w-1) else [])
    frames, prev = [], 0
    for x in boundaries:
        fw = x - prev
        if fw > 2:
            visible = ~np.all(rgb[:,prev:x,:] >= 248,axis=2)
            rows = np.flatnonzero(visible.any(axis=1))
            anchor=fw//2
            if len(rows):
                bt, bb = int(rows[0]), int(rows[-1])
                hip_start = bb-max(15, (bb-bt)//3)
                weights=visible[hip_start:bb+1,:].sum(axis=0)
                if weights.sum()>0:
                    anchor=int((np.arange(fw)*weights).sum()/weights.sum())
            frames.append({"rect":[prev,0,fw,h],"anchor":anchor})
        prev=x+1
    rgba=np.empty((h,w,4), dtype=np.uint8)
    rgba[:,:,:3]=rgb
    rgba[:,:,3]=np.where(np.all(rgb>=248,axis=2),0,255).astype(np.uint8)
    dest=WEB/"Lutadores"/(bmp.stem+".png")
    Image.fromarray(rgba,"RGBA").save(dest,optimize=True)
    (WEB/"Lutadores"/(bmp.stem+".json")).write_text(json.dumps(frames,separators=(",",":")),encoding="utf-8")
    stats[bmp.stem]={"frames":len(frames),"bmp_bytes":bmp.stat().st_size,"png_bytes":dest.stat().st_size}
print("Processed fighter sprites:",json.dumps(stats))

src=(SRC/"street_chaves_remaster.py").read_text(encoding="utf-8")
src=src.replace("import numpy as np", "import asyncio\n# NumPy sprite processing is performed offline for the WASM package.")
st=src.index("def load_sprite_strip(filepath):")
en=src.index("\ndef scale_surface(",st)
new_load='''def load_sprite_strip(filepath):
    """Use preprocessed transparent PNG sheets and precise frame anchors in WASM."""
    stem = os.path.splitext(filepath)[0]
    with open(stem + ".json", encoding="utf-8") as f:
        sprites = json.load(f)
    sheet = pygame.image.load(stem + ".png").convert_alpha()
    return ([sheet.subsurface(tuple(item["rect"])).copy() for item in sprites],
            [item["anchor"] for item in sprites])

'''
src=src[:st]+new_load+src[en:]
# In packaged app the sprite sheets are .png; the path passed to loader may be .bmp.
src=src.replace('f"C{i:02d}.bmp"', 'f"C{i:02d}.png"')
src=src.replace('self.handle_pause()\n                    return True', 'self._web_paused = True\n                    return True')
# Remove synchronous fade, which blocks the WASM browser event loop.
src=src.replace('def fade_out(self, duration=20):\n', 'def fade_out(self, duration=20):\n        if sys.platform == "emscripten":\n            return\n')
# Disable screen-mode changes that break a canvas embedded in PlayStor.
src=src.replace('def _apply_display_mode(self):\n', 'def _apply_display_mode(self):\n        if sys.platform == "emscripten":\n            self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))\n            return\n')
# Add nonblocking pause screen and turn main dispatch into async frame scheduler.
st=src.index("    # ==========================================\n    # MAIN LOOP\n",src.index("    def handle_pause(self):"))
src=src[:st]+'''    def handle_pause_web(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_p, pygame.K_ESCAPE):
                self._web_paused = False
            elif event.key in (pygame.K_UP, pygame.K_w):
                self._web_pause_option = (self._web_pause_option-1)%3
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._web_pause_option = (self._web_pause_option+1)%3
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_h):
                option=self._web_pause_option
                self._web_paused=False
                if option==1:
                    self.state="select"
                    self.p1_confirmed=self.p2_confirmed=False
                    self.p1_wins=self.p2_wins=0
                    self.round_num=1
                    pygame.mixer.music.stop()
                elif option==2:
                    self.state="tower" if self.is_tower_mode else "title"
                    if self.is_tower_mode:
                        self.tower_state="display"
                    pygame.mixer.music.stop()
        self.draw_fight()
        overlay=pygame.Surface((SCREEN_W,SCREEN_H),pygame.SRCALPHA)
        overlay.fill((0,0,0,160))
        self.screen.blit(overlay,(0,0))
        self.draw_centered_text("PAUSA",SCREEN_H//2-80,self.font_big,(255,255,0))
        for i,item in enumerate(("CONTINUAR","SELECAO DE LUTADOR","MENU PRINCIPAL")):
            self.draw_centered_text(("> " if i==self._web_pause_option else "  ")+item,SCREEN_H//2-20+i*40,self.font_medium,(255,255,0) if i==self._web_pause_option else (180,180,180))
        return True

    # ==========================================
    # ASYNC MAIN LOOP (required for WASM / Pygbag)
    # ==========================================
    async def run(self):
        self._web_paused=False
        self._web_pause_option=0
        running=True
        while running:
            if self._web_paused:
                running=self.handle_pause_web()
            elif self.state=="intro":
                running=self.handle_intro()
            elif self.state=="title":
                running=self.handle_title()
            elif self.state=="options":
                running=self.handle_options()
            elif self.state=="jukebox":
                running=self.handle_jukebox()
            elif self.state=="select":
                running=self.handle_select()
            elif self.state=="fight":
                running=self.handle_fight()
            elif self.state=="result":
                running=self.handle_result()
            elif self.state=="tower":
                running=self.handle_tower()
            pygame.display.flip()
            self.clock.tick(FPS)
            await asyncio.sleep(0)
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(Game().run())
'''
# Large unsupported EXE resources remain outside this staging folder.
(WEB/"main.py").write_text(src,encoding="utf-8")
(WEB/"README-playstor.txt").write_text("Street Chaves Remaster - experimental WebAssembly adaptation for PlayStor; source: https://github.com/Adoregabriel2005/StreetChaves-Remaster; runtime: pygame-web/pygbag; not yet verified as browser-playable.\n",encoding="utf-8")
import compileall
assert compileall.compile_file(str(WEB/"main.py"),quiet=1)
print("Staged source validated. Game files:",len(list(WEB.rglob("*"))))
