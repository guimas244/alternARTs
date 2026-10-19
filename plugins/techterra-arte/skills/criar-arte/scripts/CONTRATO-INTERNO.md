# Contrato interno dos scripts — monstros e fusões

Todos os scripts: **Python 3 + Pillow**, sem banco, sem rede, sem caminho pessoal. Rodam assim:

```
python "<skill>/scripts/<script>.py" <pasta_do_lote> [opções]
```

`<skill>` = `${CLAUDE_SKILL_DIR}`. Nada é gravado dentro da skill; tudo vai para `<pasta_do_lote>`. Funções comuns em
`comum.py` (importar com `sys.path.insert(0, os.path.dirname(__file__))`). Texto sempre UTF-8 sem BOM.

## Pasta do lote

```
<lote>/
├── plano.json              entrada (escrito pelo Claude a partir do pedido; formato abaixo)
├── artes/                  artes de origem que o USUÁRIO fornece (pais, originais, antecessores), PNG com alfa de preferência
├── entrada.json            gerado por montar_entrada.py (células numeradas)
├── pais/                   recortes limpos das artes de origem (gerado)
├── referencias/            cópia das referências da skill usadas no lote + pranchas cartela_NNN_pais.png + guia (gerado)
│   └── avulsas/            quadrante da prancha por célula (gerado por preparar_fila.py)
├── fichas_claude/          parte_<L>.json escritas pelos agentes + parte_<L>_validacao.json
├── monstros.json           fichas integradas (gerado por preparar_fila.py) — é também o arquivo do cadastrador
├── prompts/                cartela_NNN.txt, avulsa_NNN_LxCy.txt (gerado)
├── fila.json               fila da sessão de imagem (gerado)
├── PROMPT_<LOTE>.md        prompt da sessão de imagem (gerado a partir de templates/PROMPT_LOTE.md)
├── cartelas/               cartela_NNN_vK.png, cartela_NNN_original.png, avulsa_NNN_LxCy_vK.png (sessão de imagem)
├── validacao/              geracoes_*.json, cartelas_*.json, avulsas_*.json, enquadramento/<imagem>.json
├── recortes/               NN_tTT_<slug>.png 512² RGBA (gerado por recortar_cartela.py)
├── cadastro.json           corpo/força (gerado por montar_entrega.py a partir das fichas)
└── ENTREGA.md              resumo (gerado por montar_entrega.py)
```

## `plano.json`

```json
{
  "lote": "fusoes_halloween",
  "titulo": "Fusões de Halloween",
  "clima": "texto opcional do bloco de clima do tema (vai em todo prompt)",
  "cartelas": [
    {"cartela": 1, "tema": "só em bloco L", "celulas": [ <célula>, <célula>, <célula>, <célula> ]}
  ]
}
```

Célula (ordem L1C1, L1C2, L2C1, L2C2; sempre 4 por cartela):

| campo | blocos | regra |
|---|---|---|
| `bloco` | todos | `N` novo · `V` variação · `F` fusão de fusões (pais já fusões, todos do mesmo tamanho, nenhum é base) · `L` prodígio (tema por cartela) · `X` fusão base+sacrifício · `A` ápice (fusão base+sacrifício de míticos) |
| `tier`, `tipo1`, `tipo2` | todos | ids de `comum.TIPOS` |
| `humanoide_previsto` | todos | bool (opcional, padrão false) |
| `leitura` | todos | opcional: direção de conceito escrita pelo Claude (1 linha) |
| `evolui_de` | N | opcional: `[cartela, linha, coluna]` da célula antecessora (mesma cartela ou anterior) |
| `original` | V | `{nome, tier, tipo1, tipo2, descricao, arte, humanoide}` — `arte` relativo ao lote (`artes/x.png`) |
| `tipo_sai`, `tipo_entra` | V | qual tipo do original sai e qual entra |
| `ingredientes` | F, X, A | lista `{papel, nome, tier, tipo1, tipo2, descricao, arte, humanoide, linhagem}`; X/A: exatamente 2, papéis `BASE` e `SACRIFICIO`; F: 2–3, papel `PAI`; `linhagem` = outros nomes da linha evolutiva/avós (para o nome novo não carregar pedaço) |

## `entrada.json` (lista de células, gerada)

Cada célula = a do plano + `n` (1..4×cartelas, ordem de leitura), `cartela`, `linha`, `coluna`, `slot` (`X001_1`),
`arquivo` = `"{n:02d}_t{tier:02d}_{slug_do_nome}.png"` (o `{slug_do_nome}` literal até o nome existir),
`evolucao` (N: `{"anterior": n|null, "seguinte": n|null}`), e nos ingredientes/original `recorte` = `pais/<slug>.png`.

## Fichas (`fichas_claude/parte_<L>.json`, lista)

Campos que o AGENTE escreve (o resto o `compor_fichas.py` copia da entrada):

- todos: `n`, `nome` (V: não escreve; escreve `epiteto`), `humanoide`, `classe` (se humanoide), `paleta` [escura, clara],
  `anatomia`, `rosto`, `marcas_poder` (lista), `brilho`, `temperamento`, `conceito`, `marca_da_habilidade`, `descricao`;
- N/L: `arquetipo`; L: `tema` (igual nas 4 da cartela);
- V: `epiteto`, `mantem`, `muda`;
- F/X/A: `herda` {nome exato de cada pai: o que veio dele}, `ascensao`.

`compor_fichas.py` acrescenta: campos fixos da entrada, `nome` (V = original + epíteto), `ingredientes` (nomes),
`arquivo`, `visual` (fórmula por bloco) e roda `valida_fichas.py --arquivo`.

Faixa de `marcas_poder` por tier: T1–2 0–2, T3–4 1–2, T5–6 2–3, T7–8 3–4, T9–10 4–5; F/X/A: +1 nas duas pontas.

## `monstros.json` (integrado; formato do cadastrador)

`{"lote", "status", "monstros": [ficha completa, ordenada por n]}`. Cada ficha tem, além dos campos acima, os campos que o
cadastrador lê: `nome`, `tipo1`, `tipo2`, `tier`, `descricao`, `arquivo`, `humanoide`, `evolucao` no formato
`{"de": "<nome do antecessor>", "modo": "a_definir"}` quando há antecessor (o criador decide modo/level; o plano pode
trazer `evolucao_modo`/`level_requerido` na célula), `ingredientes` `[{"papel","nome"}]` em F/X/A, `variacao_de` em V.

## `fila.json` (lista, uma por cartela)

```json
{"cartela": 1, "leva": "crossover", "estado": "pronta", "prompt": "prompts/cartela_001.txt",
 "anexos": ["referencias/referencia-estilo.png", "referencias/referencia-variedade.png",
            "referencias/cartela_001_pais.png", "referencias/guia_enquadramento_2x2.png", "referencias/referencia-humanoides.png"],
 "salvar": "cartelas/cartela_001_original.png", "monstros": ["A","B","C","D"],
 "avulsas": [{"linha":1,"coluna":1,"nome":"A","prompt":"prompts/avulsa_001_L1C1.txt",
              "anexos":["...","referencias/avulsas/cartela_001_L1C1_pais.png","cartelas/cartela_001_original.png"],
              "salvar":"cartelas/avulsa_001_L1C1_v1.png"}]}
```

Caminhos **relativos à pasta do lote** (a sessão de imagem roda dentro dela). No máximo 5 anexos.

## Registro de avulsas (sessão de imagem)

`validacao/avulsas*.json`: lista `{"cartela", "linha", "coluna", "nome", "arquivo": "cartelas/avulsa_NNN_LxCy_vK.png"}`.
O recortador aplica a avulsa mais recente de cada célula **depois** de recortar a cartela.
