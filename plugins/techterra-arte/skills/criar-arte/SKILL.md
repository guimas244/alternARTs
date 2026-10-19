---
name: criar-arte
description: Cria arte do jogo Techterra no padrão do jogo. Monta lotes de monstros, fusões, personagens/NPCs (rosto e corpo), itens, cenários, mapas, capas e ícones. Escreve fichas e prompts, monta a fila para a IA de imagem e confere e recorta as cartelas. Use quando pedirem arte, cartela, lote ou pacote de monstros, fusão, NPC, item, fundo, mapa, capa ou ícone do Techterra.
---

# criar-arte — fábrica de arte do Techterra

Você planeja e prepara a arte. **A IA de imagem só gera.** Fichas, nomes, descrições, o texto final de cada prompt e a
fila saem desta skill; a sessão de imagem só anexa, cola, gera, confere, salva onde foi mandado e registra.

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

Sempre leia também [regras/formatos.md](regras/formatos.md) (tamanho de cada tipo),
[referencias/REFERENCIAS.md](referencias/REFERENCIAS.md) (o que anexar, em que ordem) e
[regras/entrega.md](regras/entrega.md) (todo lote termina com **recortes + fichas com descrição de jogo**, no formato que
o cadastrador do jogo lê).

## 2. Regras que valem para todo modo

- **Pasta de trabalho:** tudo o que você gera (fichas, prompts, fila, cartelas, recortes) vai para a pasta de trabalho do
  usuário — o diretório da sessão ou o caminho que ele indicar. **Nunca grave dentro desta skill**: a pasta do plugin é
  trocada a cada atualização.
- **Referências:** estão em `${CLAUDE_SKILL_DIR}/referencias/`. Anexe pelo caminho absoluto dessa pasta. O que for gerado
  **não vira referência** sem o dono do repositório mandar.
- **Fila cheia antes de gerar:** a sessão de imagem só começa quando todos os prompts do lote estão escritos e validados.
- **Uma geração por cartela/página**, sem refazer por detalhe; quem julga a qualidade é o dono, depois. Refazer só por erro
  real, definido por modo em [regras/fluxo-sessoes.md](regras/fluxo-sessoes.md).
- **ONDE SALVAR:** todo prompt de sessão de imagem diz a pasta absoluta de saída, a regra de nome e os registros
  esperados — conforme [regras/fluxo-sessoes.md](regras/fluxo-sessoes.md).
- **Nenhum texto na arte** e demais proibições: [regras/restricoes.md](regras/restricoes.md).
- **Sem banco e sem produção:** esta skill termina nas cartelas recortadas e nas fichas. Cadastro no jogo é outro processo.

## 3. Ferramentas

Scripts em `${CLAUDE_SKILL_DIR}/scripts/` (Python 3 + Pillow). Antes de usar, confira `python -c "import PIL"`; se
faltar, oriente `pip install pillow`. Os scripts recebem a pasta de trabalho por argumento.

Lista dos scripts, por modo, com o comando de cada um: [scripts/LEIA-ME.md](scripts/LEIA-ME.md).

> Estado (19/10/2026): todos os modos têm fluxo completo e scripts. Ainda é **manual** (feito pelo Claude, sem script):
> - recorte do mundi em volta do ponto da Região (sub-mapa), com editor de imagem;
> - `ENTREGA.md` de itens, NPC, cenários, mapas, capas e ícones (só monstros/fusões têm `montar_entrega.py`);
> - recorte da avulsa de item: `recortar_grade.py <avulsa.png> --grade 1x1 --nomes <lista>` chamado à mão;
> - `trocas.json` do modo TROCAS (monstros), escrito pelo Claude;
> - cotas de temperamento por lote: sem checagem automática, confira ao revisar as fichas.
>
> Artes de origem (pais de fusão, original, antecessor, artes do jogo para capa, personagem a atualizar) e listas de
> nomes de NPC **o usuário fornece**: a skill não tem banco nem acervo.
