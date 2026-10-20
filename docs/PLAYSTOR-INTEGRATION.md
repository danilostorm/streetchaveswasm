# Integração com o PlayStor G4.3

O projeto já está cadastrado no PlayStor original como jogo Windows / PC, ID **680**. A interface principal hospeda o jogo na área do player; a página Pygbag roda em um quadro **de mesma origem**, não em domínio externo. A execução acontece no navegador, com WASM/Python/pygame-ce.

## Arquivos

- `playstor/index.html`, `web.tar.gz`, `favicon.png`, `CREDITS.txt` → `public/pc-web/street-chaves/`
- `playstor/street-chaves-runtime.mjs` → `public/stormgames/street-chaves-runtime.mjs`
- `playstor/cover.jpg` → importar pelo painel administrativo ou renomear segundo o formato UUID exigido pelo PlayStor
- `web/main.py`, recursos e ferramentas → apenas para desenvolvimento; não precisam estar publicamente acessíveis no PlayStor.

A tabela `game_web_launches` da instalação tem:
```text
game_id = 680
runtime = street-chaves-wasm
launch_url = /pc-web/street-chaves/index.html
```

## Vinculação do player

O `core` de Windows é `pc_web`. Nos arquivos `public/stormgames/games-player.js` e `games-bundle.js`, no início de `prepareEmulator`, **antes do caso genérico `pcweb`**, inclua:

```js
if (engine === 'pcweb' && current?.web_runtime === 'street-chaves-wasm') {
  const { createStreetChavesRuntime } = await import('/stormgames/street-chaves-runtime.mjs');
  instance = await createStreetChavesRuntime({
    game: current,
    stage: $('[data-game-stage]', overlay),
    mode
  });
  return;
}
```

O módulo retorna a interface de player que já oferece `start`, `pause`, `resume`, `pressDown`, `pressUp`, `exit` e `getStatus`. Não anuncia funções inexistentes: `saveState` e `saveSRAM` retornam `null`. Oculte os botões de gravação de save-state para este jogo. Em instalação nova, configure também o catálogo Windows como `playable` quando o endereço interno estiver configurado.

## Compilar e atualizar

Rode `bash tools/build.sh` em Linux. O pacote resultante fica em `.build/web/build/web/web.tar.gz`. Para copiar os arquivos de runtime para uma instalação existente:

```bash
bash tools/install-to-playstor.sh /mnt/user/appdata/playstor .build/web/build/web/web.tar.gz
```

O script **não altera o banco nem os fontes genéricos do player**, nem reinicia automaticamente o serviço. Como o Dockerfile atual usa `COPY public ./public`, atualizações estáticas no host só aparecem no contêiner depois de rebuild/recreate do PlayStor.

## Testes e limites

Testes anteriores confirmaram intro, menu, seleção, luta com Chaves e Glória e teclado no Chromium. Gamepad físico, mobile, gravação de saves e desempenho em hardware diverso não foram validados de ponta a ponta. Controle de áudio depende da interação inicial do navegador.

O upstream é o projeto de fã <https://github.com/Adoregabriel2005/StreetChaves-Remaster>. Não há licença original identificada no repositório-fonte para presumir autorização de redistribuição de recursos de terceiros.
