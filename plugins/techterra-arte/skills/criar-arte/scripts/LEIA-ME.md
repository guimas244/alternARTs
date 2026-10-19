# scripts/

Ferramentas da skill (Python 3 + Pillow; sem banco, sem rede). Antes: `python -c "import PIL"` (falta → `pip install
pillow`; no ChatGPT, Pillow já vem). `{SKILL}` = a pasta desta skill (onde está o SKILL.md); `<lote>` = a pasta de
trabalho do lote (no ChatGPT, `/mnt/data/<lote>`). Como rodar em cada ambiente: [../regras/ambiente.md](../regras/ambiente.md).
`fichas_claude/` (nos comandos abaixo) é o nome fixo da pasta das fichas dentro do lote: os scripts leem dali.

**Regra:** todo script recebe a pasta do lote (ou uma imagem dela) por argumento e grava só ali — **nunca dentro da
skill** (nem `__pycache__`). Rodar sem argumentos (ou com `--help`, no `recortar_grade.py`) mostra o uso. O detalhe de
cada um está na docstring do próprio arquivo.

## Monstros e fusões ([../modos/monstros.md](../modos/monstros.md), [../modos/fusoes.md](../modos/fusoes.md))

| Script | O que faz | Comando |
|---|---|---|
| `montar_entrada.py` | valida `plano.json`; gera `entrada.json`, `pais/`, pranchas `referencias/cartela_NNN_pais.png` e copia as referências | `python "{SKILL}/scripts/montar_entrada.py" <lote>` |
| `ver_celulas.py` | mostra, compacto, as células de algumas cartelas para o agente de fichas (não grava) | `python "{SKILL}/scripts/ver_celulas.py" <lote> 1,2` (ou `3-5`, `todas`) |
| `compor_fichas.py` | completa uma parte de fichas (campos fixos, nome, `visual`) e valida | `python "{SKILL}/scripts/compor_fichas.py" <lote> fichas_claude/parte_A.json` |
| `valida_fichas.py` | valida uma parte (`--arquivo`) ou todas (revisão cruzada) | `python "{SKILL}/scripts/valida_fichas.py" <lote> [--arquivo fichas_claude/parte_A.json]` |
| `preparar_fila.py` | integra as partes em `monstros.json`, escreve prompts, `fila.json` e `PROMPT_<LOTE>.md` (sem `--gravar` = ensaio) | `python "{SKILL}/scripts/preparar_fila.py" <lote> [--gravar] [--partes A,B] [--conserto 3,5]` |
| `checa_enquadramento.py` | confere o enquadramento de uma cartela 2x2 ou de uma avulsa (usado pela sessão de imagem) | `python "{SKILL}/scripts/checa_enquadramento.py" <lote>/cartelas/cartela_001_original.png [--avulsa] [--lote <lote>]` |
| `recortar_cartela.py` | recorta as cartelas em tiles 512² RGBA, aplica as avulsas e monta `recortes/_visao_geral.png` | `python "{SKILL}/scripts/recortar_cartela.py" <lote> [--cartelas 1,3]` |
| `montar_entrega.py` | valida o lote e escreve `cadastro.json` + `ENTREGA.md` | `python "{SKILL}/scripts/montar_entrega.py" <lote>` |

## Personagens / NPC ([../modos/personagens.md](../modos/personagens.md))

| Script | O que faz | Comando |
|---|---|---|
| `npc_montar_prompts.py` | valida `tema.json`/`roster.json`/`visual/parte_*.json`; com `--gravar` grava prompts, referências, `fila.json` e `PROMPT_IMAGEM_<LOTE>.md`; `--contrato` grava o contrato dos agentes | `python "{SKILL}/scripts/npc_montar_prompts.py" <lote> [--gravar \| --parte visual/parte_A.json \| --contrato]` |
| `npc_recortar.py` | recorta as páginas (3 colunas) em rosto 512² + corpo 512×1024 e atualiza `fichas.json` | `python "{SKILL}/scripts/npc_recortar.py" <lote> [--paginas 1,3]` |

## Itens e ícones ([../modos/itens.md](../modos/itens.md), [../modos/icones.md](../modos/icones.md))

| Script | O que faz | Comando |
|---|---|---|
| `itens_montar_prompts.py` | valida `itens.json`; com `--gravar` grava prompts das páginas 5x5, referências, `fila.json` e `PROMPT_ITENS_<LOTE>.md` | `python "{SKILL}/scripts/itens_montar_prompts.py" <lote> [--gravar [--forcar]]` |
| `recortar_grade.py` | recortador único de grade: páginas de itens (lote), ícones 4x4 (`--mascara-circular`), avulsa 1x1 | `python "{SKILL}/scripts/recortar_grade.py" <lote\|imagem> [--grade 5x5] [--lado 320] [--margem 16] [--mascara-circular] [--reduzir] [--saida pasta] [--nomes lista.json] [--pagina N] [--simular] [--substituir]` |

## Cenários, mapas e capas ([../modos/cenarios.md](../modos/cenarios.md), [../modos/mapas.md](../modos/mapas.md), [../modos/capas.md](../modos/capas.md))

| Script | O que faz | Comando |
|---|---|---|
| `fundos_normalizar.py` | leva cada bruto ao tamanho do destino, mede e registra em `entregas.json` (fundo de Local/lados fora da medida reprova, salvo `--aceitar`) | `python "{SKILL}/scripts/fundos_normalizar.py" <lote> --destino local\|lados\|portao\|submapa\|mundi\|narraris_mapa\|wallpaper\|moldura [--entrada brutos] [--saida finais] [--aceitar]` |
| `capas_converter.py` | corta a cartela 2x2 de capas em 4 capas 510×680 WebP e confere o miolo | `python "{SKILL}/scripts/capas_converter.py" <lote>\|<cartela.png> [--saida finais]` |

## Apoio

- `comum.py` — funções e constantes comuns (tipagens, medidas da cartela, leitura/gravação de JSON, pasta do lote).
  Não roda sozinho.
- [`CONTRATO-INTERNO.md`](CONTRATO-INTERNO.md) — formato dos arquivos do lote de monstros/fusões (`plano.json`,
  `entrada.json`, fichas, `monstros.json`, `fila.json`, registro de avulsas).
- `test_recortar_grade.py` — testes do `recortar_grade.py` e do `itens_montar_prompts.py` com imagens sintéticas em
  pasta temporária: `python "{SKILL}/scripts/test_recortar_grade.py"`.
