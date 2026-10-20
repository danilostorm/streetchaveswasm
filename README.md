# Street Chaves Remaster — WebAssembly / PlayStor

Port do jogo de fãs [Street Chaves Remaster](https://github.com/Adoregabriel2005/StreetChaves-Remaster) de **Python/Pygame para WebAssembly**, integrado ao player do **PlayStor**.

Este repositório é uma cópia de preservação do projeto criado no AEROCOOL, para que seja possível desenvolver, corrigir e recompilar no futuro sem depender de uma pasta temporária do servidor.

## Estado verificado — 19/10/2026

- Executa Python 3.12/Pygame-CE no navegador via **Pygbag 0.9.3 / WebAssembly**.
- Chromium: intro, menu, escolha de personagem, início de luta e comandos de teclado testados.
- **15 lutadores, 12 cenários, 686 frames** preparados como PNG e JSON; áudio convertido para OGG.
- Runtime do navegador sem dependência do NumPy/`pygame.surfarray`.
- Publicado no PlayStor, **Windows / PC**, **jogo ID 680**, runtime `street-chaves-wasm`.
- O player PlayStor mantém menus, tela cheia e histórico de tempo; o engine Pygbag roda em um quadro local de mesma origem (não em domínio externo).
- Gamepad físico, versão móvel e save states **não estão homologados**. Este port não oferece save states.

## Estrutura do repositório

| Pasta/arquivo | Conteúdo |
| --- | --- |
| [`web/`](web/) | **Port completo editável:** `main.py`, sprites, cenários, áudios e metadados já convertidos |
| [`upstream/`](upstream/) | Fontes Python e recursos originais usados na adaptação, sem arquivos EXE ou histórico `.git` |
| [`playstor/`](playstor/) | `web.tar.gz` compilado e validado (aprox. 8,4 MB), wrapper HTML, integração do player, favicon, capa e créditos |
| [`tools/build.sh`](tools/build.sh) | Reconstruir o WebAssembly a partir dos arquivos desta cópia |
| [`tools/install-to-playstor.sh`](tools/install-to-playstor.sh) | Copiar apenas os componentes próprios do Street Chaves para uma instalação PlayStor |
| [`tools/`](tools/) | Scripts originais de preparação e conversão dos recursos |
| [`tests/`](tests/) | Scripts de smoke tests usados durante a adaptação |
| [`docs/PLAYSTOR-INTEGRATION.md`](docs/PLAYSTOR-INTEGRATION.md) | Reinstalação e integração com o player nativo |
| [`docs/README-AEROCOOL.md`](docs/README-AEROCOOL.md) | Layout da instalação original |

## Reconstrução

Em Linux com Python 3.11+ e `venv` disponíveis:

```bash
git clone https://github.com/danilostorm/streetchaveswasm.git
cd streetchaveswasm
bash tools/build.sh
```

O arquivo final será `.build/web/build/web/web.tar.gz`. O script verifica que existe exatamente um `main.py` e que a antiga dependência NumPy não voltou. Não modifica a instalação em produção.

Para voltar à versão comprovadamente testada, utilize o pacote pronto `playstor/web.tar.gz`. SHA-256 da cópia de referência:

```text
e1df64d4d26aef06de45dd1e20e63fbc0963a32ce76de4266802686002e34f06
```

Para reinstalar, consulte [as instruções de integração](docs/PLAYSTOR-INTEGRATION.md). Evite sobrescrever arquivos genéricos do PlayStor ou seu banco SQLite; eles pertencem ao projeto principal.

## Direitos e créditos

Street Chaves original é creditado à **Cybergamba**; o remaster de fã é creditado a **Adoregabriel2005**. Os personagens e arquivos gráficos/sonoros podem ser de terceiros. Este repositório **não concede licença de redistribuição nem uso comercial** sobre tais materiais. Nenhum arquivo de licença do upstream foi identificado durante a preparação. Confirme as permissões correspondentes antes de qualquer redistribuição.

Os executáveis Windows originais foram excluídos por não serem necessários para o port WebAssembly.
