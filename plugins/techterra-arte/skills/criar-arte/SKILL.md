---
name: criar-arte
description: Cria arte do jogo Techterra no padrão do jogo. Monta lotes de monstros, fusões, personagens/NPCs (rosto e corpo), itens, cenários, mapas, capas e ícones. Escreve fichas e prompts, monta a fila, gera as cartelas com a ferramenta de imagem (quando o ambiente tem uma), confere e recorta com Python e entrega o pacote. Use quando pedirem arte, cartela, lote ou pacote de monstros, fusão, NPC, item, fundo, mapa, capa ou ícone do Techterra.
---

# criar-arte — fábrica de arte do Techterra

> **Alvo principal: ChatGPT** — uma conversa só planeja, escreve as fichas e os prompts, **gera as imagens** com a
> ferramenta de imagem da própria conversa, confere, recorta e entrega o `.zip`. A skill também roda no Codex (gera
> com `image_gen`) e no Claude Code (prepara tudo, mas a geração vai para o ChatGPT/Codex).
> **Leia primeiro [regras/ambiente.md](regras/ambiente.md)** — pasta do lote, scripts e geração em cada ambiente.

`{SKILL}` = a pasta desta skill (onde está o SKILL.md). Nos comandos, troque pelo caminho absoluto dela.

Você planeja e prepara a arte e, no ChatGPT/Codex, também gera. Fichas, nomes, descrições, o texto final de cada prompt
e a fila saem **antes** da geração; na etapa de geração só se anexa, cola, gera, confere, salva onde foi mandado e
registra — nada de reescrever ficha ou prompt.

## 1. Descubra o modo e leia o arquivo dele

| Pedido | Leia |
|---|---|
| monstros novos, evolução, variação, humanoide, revitalização; prodígio (sem regra própria ainda: perguntar ao usuário) | [modos/monstros.md](modos/monstros.md) |
| fusão (base + sacrifício, fusão de fusões, Derivada, opções/visões); fusão mítica (sem regra própria ainda: perguntar ao usuário) | [modos/fusoes.md](modos/fusoes.md) |
| personagem ou NPC (rosto + corpo), atualizar personagem de jogador | [modos/personagens.md](modos/personagens.md) |
| item, equipamento de monstro, livro, essência, pedra ritual; joia e item de passe (sem regra própria ainda: perguntar ao usuário) | [modos/itens.md](modos/itens.md) |
| fundo de batalha / cenário de Local, portão; capa de Jornada (sem regra própria ainda: perguntar ao usuário) | [modos/cenarios.md](modos/cenarios.md) |
| sub-mapa de Região, mapa-múndi, mapa dos lados | [modos/mapas.md](modos/mapas.md) |
| capa de evento/expedição/raid, wallpaper de passe, moldura de invasão | [modos/capas.md](modos/capas.md) |
| ícone de mapa, ícone de tipo; selo (sem regra própria ainda: perguntar ao usuário) | [modos/icones.md](modos/icones.md) |

Se o criador deu uma **tipagem** ("um lote de Gelo"), um **tema/referência** ("filmes de terror", "Halloween") ou uma
**imagem de referência**, leia antes [regras/lotes-tematicos.md](regras/lotes-tematicos.md): o plano do lote sai de lá.

Sempre leia também [regras/ambiente.md](regras/ambiente.md) (onde e como rodar), [regras/formatos.md](regras/formatos.md) (tamanho de cada tipo),
[referencias/REFERENCIAS.md](referencias/REFERENCIAS.md) (o que anexar, em que ordem) e
[regras/entrega.md](regras/entrega.md) (todo lote termina com **recortes + fichas com descrição de jogo**, no formato que
o cadastrador do jogo lê).

## 2. Regras que valem para todo modo

- **Pasta de trabalho:** tudo o que você gera (fichas, prompts, fila, cartelas, recortes) vai para a pasta do lote:
  - **ChatGPT:** `/mnt/data/<lote>/` (espaço de arquivos da conversa); no fim, entregue o lote como `.zip`
    (`shutil.make_archive`);
  - **Codex / Claude Code:** o diretório da sessão ou o caminho que o usuário indicar.

  **Nunca grave dentro desta skill**: a pasta da skill é trocada a cada atualização (e no ChatGPT pode ser só leitura).
- **Referências:** estão em `{SKILL}/referencias/`. Anexe pelo caminho absoluto dessa pasta; se a ferramenta de imagem
  não alcançar a pasta da skill, peça ao usuário para anexar as imagens listadas ([regras/ambiente.md](regras/ambiente.md)).
  O que for gerado **não vira referência** sem o dono do repositório mandar.
- **Fila cheia antes de gerar:** a etapa de geração só começa quando todos os prompts do lote estão escritos e validados.
- **Uma geração por cartela/página**, sem refazer por detalhe; quem julga a qualidade é o dono, depois. Refazer só por erro
  real, definido por modo em [regras/fluxo-sessoes.md](regras/fluxo-sessoes.md).
- **ONDE SALVAR:** todo prompt de sessão de imagem diz a pasta absoluta de saída, a regra de nome e os registros
  esperados — conforme [regras/fluxo-sessoes.md](regras/fluxo-sessoes.md).
- **Nenhum texto na arte** e demais proibições: [regras/restricoes.md](regras/restricoes.md).
- **Sem banco e sem produção:** esta skill termina nas cartelas recortadas e nas fichas. Cadastro no jogo é outro processo.

## 3. Ferramentas

Scripts em `{SKILL}/scripts/` (Python 3 + Pillow). Os scripts recebem a pasta do lote por argumento; rode com
`python -B` (não grava `__pycache__` na skill).

- **ChatGPT:** rode pelo ambiente de código da conversa (Pillow já vem; ex.: `subprocess.run(["python", "-B",
  f"{SKILL}/scripts/<script>.py", "/mnt/data/<lote>"])`). A geração usa a ferramenta de imagem da conversa.
- **Codex:** scripts locais; geração com `image_gen`.
- **Claude Code:** scripts locais; **não gera imagem** — a geração vai para o ChatGPT/Codex com o `PROMPT_<LOTE>.md`.
- Fora do ChatGPT, confira antes `python -c "import PIL"`; se faltar, oriente `pip install pillow`.

Lista dos scripts, por modo, com o comando de cada um: [scripts/LEIA-ME.md](scripts/LEIA-ME.md).

> Estado (19/10/2026): todos os modos têm fluxo completo e scripts. Ainda é **manual** (feito pelo assistente, sem script):
> - recorte do mundi em volta do ponto da Região (sub-mapa), com editor de imagem;
> - `ENTREGA.md` de itens, NPC, cenários, mapas, capas e ícones (só monstros/fusões têm `montar_entrega.py`);
> - recorte da avulsa de item: `recortar_grade.py <avulsa.png> --grade 1x1 --nomes <lista>` chamado à mão;
> - `trocas.json` do modo TROCAS (monstros), escrito pelo assistente;
> - cotas de temperamento por lote: sem checagem automática, confira ao revisar as fichas.
>
> Artes de origem (pais de fusão, original, antecessor, artes do jogo para capa, personagem a atualizar) e listas de
> nomes de NPC **o usuário fornece** (no ChatGPT, por upload na conversa): a skill não tem banco nem acervo.
