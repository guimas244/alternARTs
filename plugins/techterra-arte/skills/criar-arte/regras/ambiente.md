Para que serve: como esta skill roda em cada ambiente (ChatGPT, Codex, Claude Code) — onde fica a pasta do lote, como
rodar os scripts, quem gera as imagens e como o pacote chega ao usuário. **Leia no começo de todo lote.**

# Ambiente

`{SKILL}` = a pasta desta skill (onde está o SKILL.md). `<lote>` = a pasta de trabalho do lote (nunca dentro da skill).

O fluxo é o mesmo em todo lugar: **plano → fichas → fila e prompts → geração das imagens → conferência e recorte →
entrega**. O que muda é quem gera as imagens e onde os arquivos ficam.

| | ChatGPT desktop (principal) | ChatGPT web | Codex | Claude Code |
|---|---|---|---|---|
| Gera imagem? | **sim**, na própria conversa | **sim**, na própria conversa | sim (`image_gen`) | **não** |
| Pasta do lote | **pasta local** (o app enxerga o disco) | espaço de arquivos da conversa (ex.: `/mnt/data/<lote>/`) | pasta local | pasta local |
| Scripts | locais | ambiente de código da conversa (Pillow já vem) | locais | locais |
| Artes de origem | arquivo local | o usuário envia por upload | arquivo local | arquivo local |
| Entrega | a pasta | `.zip` para baixar | a pasta | a pasta |
| Subagentes | conforme o ambiente | não | conforme o ambiente | conforme o ambiente |

**Como saber qual ChatGPT é:** se o ambiente de código enxerga o disco do usuário (ex.: `D:\...`, `C:\Users\...`, a
pasta do projeto) e **não** existe `/mnt/data`, é o **ChatGPT desktop**: trabalhe direto na pasta local, como no Codex.
Se existe `/mnt/data` e o disco do usuário não aparece, é o **ChatGPT web**.

## ChatGPT desktop — o caso normal do dono

O app do ChatGPT no computador roda os scripts e lê/grava **direto no disco**. Funciona como o Codex:

- **Pasta do lote:** a pasta local que o usuário indicar (ou o caminho do `PROMPT_<LOTE>.md`). Nada de `/mnt/data`,
  nada de `.zip`, nada de upload: leia e grave direto nela.
- **Geração preparada em outro lugar (ex.: Claude Code):** o usuário cola só
  `criar-arte: leia e execute <caminho absoluto>\PROMPT_<LOTE>.md — TODOS`. O roteiro já diz a pasta do lote, os
  anexos (caminhos relativos a ela), a conferência do enquadramento e onde salvar — não peça mais nada.
- **Scripts:** `python -B "{SKILL}/scripts/<script>.py" <lote>`; `{SKILL}` = a pasta onde o app instalou a skill
  (procure o próprio SKILL.md se não souber).
- **Imagem gerada:** salve no caminho da fila (`cartelas/cartela_NNN_v1.png` e a aprovada como `_original.png`) e rode
  o verificador logo depois.
- **Entrega:** a própria pasta do lote (sem `.zip`).

## ChatGPT web — sem acesso ao disco

**Uma conversa só faz tudo:** plano → fichas → prompts → **gera as cartelas com a ferramenta de imagem da própria
conversa** → confere e recorta com Python → entrega o `.zip`.

- **Pasta do lote:** crie em `/mnt/data/<lote>/` (o espaço de arquivos da conversa). Tudo o que a skill grava vai para
  lá; trate a pasta da skill como só leitura.
- **Achar `{SKILL}`:** a skill fica numa pasta montada pelo ChatGPT. Descubra o caminho com Python antes do primeiro
  script, procurando o próprio SKILL.md (ex.: `glob.glob("/**/criar-arte/SKILL.md", recursive=True)`), e use esse
  caminho absoluto como `{SKILL}` em todos os comandos. *(A confirmar no piloto: onde a skill aparece no ambiente de
  código.)*
- **Scripts:** rode pelo ambiente de código da conversa, com a pasta do lote como argumento — ex.:
  `subprocess.run(["python", "-B", f"{SKILL}/scripts/montar_entrada.py", "/mnt/data/<lote>"])` (ou `!python -B …`).
  O `-B` evita gravar `__pycache__` dentro da skill. Pillow já está disponível; sem internet, não há `pip install`.
- **Artes de origem** (pais de fusão, original, antecessor, artes do jogo para capa, personagem a atualizar): peça ao
  usuário para **enviar por upload** e copie de `/mnt/data/` para `<lote>/artes/` (ou a subpasta que o modo pedir).
- **Referências da skill:** anexe à geração as imagens de `{SKILL}/referencias/` que o modo e a fila indicam, na ordem.
  Se a ferramenta de imagem não conseguir usar um arquivo da pasta da skill, mostre ao usuário a **lista** (nome do
  arquivo e ordem) e peça para ele anexar essas imagens na conversa — elas estão no `.zip` da skill, em `referencias/`.
  *(A confirmar no piloto: se a ferramenta de imagem enxerga arquivos da skill e de `/mnt/data`.)*
- **Imagem gerada:** salve no lote com o nome que a fila manda (`cartelas/cartela_NNN_v1.png` etc.) e só então rode o
  verificador/recortador. Se o ambiente de código **não enxergar** a imagem que a conversa acabou de gerar, peça ao
  usuário para baixar a cartela e reenviá-la por upload; aí copie para o caminho da fila. *(A confirmar no piloto:
  imagem gerada visível no Python; tamanho e transparência reais que a ferramenta entrega — os scripts medem pela
  proporção, mas o fundo precisa vir transparente de verdade.)*
- **Sem subagentes:** escreva as fichas **uma cartela (ou parte) por vez, em sequência**, fechando cada parte com o
  validador, e rode a revisão cruzada no fim com todas as partes. Na geração, faça as faixas em sequência.
- **O `PROMPT_<LOTE>.md`** (ou `PROMPT_IMAGEM_*`/`PROMPT_ITENS_*`) vira o **roteiro que a própria conversa segue** na
  etapa de geração (modo TODOS, faixas em sequência). Ao entrar nessa etapa, as fichas e os prompts estão fechados: a
  conversa passa a só gerar, conferir, salvar e registrar. Se a conversa ficar longa demais, o mesmo arquivo pode ser
  levado para uma **conversa nova** (o usuário envia o `.zip` do lote e a frase do modo).
- **Entrega:** gere o pacote com Python — `shutil.make_archive("/mnt/data/<lote>", "zip", "/mnt/data/<lote>")` — e
  entregue o link do `/mnt/data/<lote>.zip` para o usuário baixar. O conteúdo segue [entrega.md](entrega.md).
- **Tamanho da skill:** as referências somam alguns MB. *(A confirmar no piloto: o limite de tamanho de upload de
  skill no ChatGPT.)*

## Codex

- Pasta do lote local (o diretório da sessão ou o que o usuário indicar); scripts locais (`python -B "{SKILL}/scripts/…"`).
- `image_gen` disponível: o `PROMPT_<LOTE>.md` pode ser seguido **na mesma sessão** (depois da fila cheia) ou em outra
  sessão aberta dentro de `<lote>`.
- Entrega: a própria pasta do lote.

## Claude Code

- Prepara tudo: plano, fichas, fila, prompts, recorte e entrega, com pasta e scripts locais.
- **Não gera imagem.** A geração vai para o ChatGPT ou o Codex com o `PROMPT_<LOTE>.md`: entregue ao usuário a frase do
  modo (ex.: `criar-arte: leia e execute <lote>/PROMPT_<LOTE>.md — TODOS`), sem instruções extras. No ChatGPT desktop
  e no Codex não há `.zip`: a sessão trabalha direto na pasta do lote. Só para o ChatGPT web vai o `.zip` do lote. Os
  caminhos absolutos do `PROMPT_<LOTE>.md` são os da máquina local; lá, o lote extraído em `/mnt/data/<lote>` faz o
  papel da pasta do lote (a fila usa caminhos relativos, e o próprio roteiro avisa disso). Depois que as cartelas
  voltarem para `<lote>/cartelas/`, siga com a conferência, o recorte e a entrega.
- Subagentes, se houver: fichas por parte em paralelo, com revisão cruzada no fim
  ([fluxo-sessoes.md](fluxo-sessoes.md#orquestração-com-vários-agentes)).

## A confirmar no primeiro piloto no ChatGPT

1. Onde a skill aparece no ambiente de código (caminho de `{SKILL}`) e se os scripts rodam de lá.
2. Se a ferramenta de imagem consegue anexar arquivos da pasta da skill (`{SKILL}/referencias/`) e de `/mnt/data`;
   senão, o usuário anexa à mão.
3. Se a imagem gerada fica visível para o Python (para salvar, medir e recortar); senão, baixar e reenviar.
4. Tamanho e fundo transparente reais da imagem gerada (o prompt pede 1254² com alfa; outro tamanho passa se a
   proporção for a do formato, fundo opaco reprova).
5. Limite de tamanho de upload da skill (as referências pesam alguns MB).
6. Limite de anexos por geração (a regra assume no máximo 5).
