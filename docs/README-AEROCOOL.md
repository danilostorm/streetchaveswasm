# Street Chaves Remaster — PlayStor / Windows PC

O port WebAssembly de Street Chaves Remaster foi centralizado no PlayStor. O jogo está cadastrado na plataforma **Windows / PC**, ID **680**, e utiliza o **player G4.3 do PlayStor**.

## Arquivos ativos de produção

- Página interna e assets Pygbag: `/mnt/user/appdata/playstor/public/pc-web/street-chaves/`
- Arquivo carregado pelo navegador: `public/pc-web/street-chaves/web.tar.gz`
- Módulo de integração: `public/stormgames/street-chaves-runtime.mjs`
- Entradas do player: `public/stormgames/games-player.js` e `games-bundle.js`
- Registro na base SQLite: `data/playstor.sqlite` (game ID 680, runtime `street-chaves-wasm`, página `/pc-web/street-chaves/index.html`)
- Capa: `data/covers/`, pelo campo `games.cover_path`

Nenhum container Docker próprio do Street Chaves é necessário. O PlayStor é quem hospeda tudo.

## Arquivos de desenvolvimento privados

Este diretório (`data/projects/street-chaves-wasm/`) está fora da raiz pública e excluído do contexto do Docker pelo `.dockerignore` de PlayStor (regra `data`).

- `source/`: repositório original, recursos e histórico Git do remaster.
- `web/`: fontes do port Python/Pygame e assets convertidos; `web/build/web/` guarda saída de compilação para auditoria.
- `prepare_port.py`, `convert_media.py`, `fix_surfarray.py`: adaptação, conversão de recursos e remoção da dependência NumPy em tempo de execução.
- `install_playstor_native.py` e outros scripts: registros do processo inicial de integração e testes.
- `build-playstor.sh`: receita de reconstrução que prepara dependências em `.venv` e publica **somente** o novo `web.tar.gz`, preservando o player e o restante do PlayStor.

Para recompilar manualmente, executar no AEROCOOL:

```bash
bash /mnt/user/appdata/playstor/data/projects/street-chaves-wasm/build-playstor.sh
```

Esse script faz backup do arquivo WASM implantado anteriormente como `previous-deployed-web.tar.gz`. Não reinicia o container.

Ambientes locais `venv/` e navegadores Playwright de teste em `browsers/` foram removidos para evitar ocupar centenas de MB. São ferramentas regeneráveis, não fazem parte do jogo.

## Créditos

Port baseado em [StreetChaves-Remaster](https://github.com/Adoregabriel2005/StreetChaves-Remaster), projeto de fã. Street Chaves original por Cybergamba; personagens e recursos permanecem sob os direitos dos seus respectivos titulares. A presença deste arquivo não implica autorização de redistribuição dos recursos de terceiros.
