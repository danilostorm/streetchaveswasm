# Street Chaves Remaster — WebAssembly / PlayStor

Port do fan game Street Chaves Remaster (Python/Pygame) para WebAssembly, preparado para o player integrado do PlayStor.

**Versão de referência:** 19 de outubro de 2026. Confirmados no Chromium: inicialização, intro, menu, seleção de personagem e tela de luta com comandos de teclado. O pacote usa Pygbag 0.9.3, CPython WebAssembly e pygame-ce. O PlayStor registra esse jogo como Windows / PC (ID 680) com runtime `street-chaves-wasm`.

## Arquivos

- `src/main.py`: código-fonte do jogo portado, editável.
- `src/upstream-original.py`: código principal original para comparação.
- `assets/original-source-assets.zip`: código e recursos originais sem os executáveis EXE nem diretório .git.
- `assets/web-converted-assets.zip`: recursos convertidos para PNG, OGG e JSON usados pelo navegador.
- `dist-web.tar.gz`: pacote Pygbag validado, pronto para uso.
- `playstor/`: index HTML, módulo JavaScript de integração, capa e créditos.
- `tools/`: scripts e testes do port.
- `docs/`: informações de integração e layout no AEROCOOL.

A reconstrução é documentada em `docs/PLAYSTOR-INTEGRATION.md`; para implantação imediata o pacote compilado pode ser usado com `playstor/index.html`.

**Observação:** teclado foi testado, mas o gamepad físico e a gravação de estados ainda não foram validados. O port não oferece save states nativos.

## Origem e direitos

Remaster original: https://github.com/Adoregabriel2005/StreetChaves-Remaster. Street Chaves original por Cybergamba. Trata-se de projeto de fã, com personagens e recursos que podem ter direitos de terceiros. A disponibilização do código aqui não concede uma licença sobre esses materiais; verifique os direitos antes de redistribuir.