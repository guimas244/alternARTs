# Contrato interno dos scripts — monstros e fusões

Todos os scripts: **Python 3 + Pillow**, sem banco, sem rede, sem caminho pessoal. Rodam assim:

```
python "<skill>/scripts/<script>.py" <pasta_do_lote> [opções]
```

`<skill>` = a pasta desta skill (onde está o SKILL.md). Nada é gravado dentro da skill; tudo vai para `<pasta_do_lote>`. Funções comuns em
`comum.py` (importar com `sys.path.insert(0, os.path.dirname(__file__))`). Texto sempre UTF-8 sem BOM.

## Pasta do lote

```
<lote>/
├── plano.json              entrada (escrito pelo assistente a partir do pedido; formato abaixo)
├── artes/                  artes de origem que o USUÁRIO fornece (pais, originais, antecessores), PNG com alfa de preferência
├── entrada.json            gerado por montar_entrada.py (células numeradas)
├── pais/                   recortes limpos das artes de origem (gerado)
├── referencias/            cópia das referências da skill usadas no lote + pranchas cartela_NNN_pais.png + guia (gerado)
│   └── avulsas/            quadrante da prancha por célula (gerado por preparar_fila.py)
├── fichas_claude/          parte_<L>.json escritas por parte (agente ou sequência) + parte_<L>_validacao.json
│                           (nome fixo da pasta das fichas: é contrato dos scripts, não indica ambiente)
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
  "fidelidade": "arquetipo",
  "cartelas": [
    {"cartela": 1, "tema": "só em bloco L", "celulas": [ <célula>, <célula>, <célula>, <célula> ]}
  ]
}
```

`fidelidade` (opcional, padrão `"arquetipo"`): `"arquetipo"` = a referência vira criatura nova (tema aberto) ·
`"homenagem"` = homenagem reconhecível a uma figura clássica (personagens nomeados; regras/lotes-tematicos.md §Nível de
fidelidade). Copiada para cada célula; a célula pode trazer a sua. Só vale em N/L (em V/F/X/A vira `"arquetipo"`).

Célula (ordem L1C1, L1C2, L2C1, L2C2; sempre 4 por cartela):

| campo | blocos | regra |
|---|---|---|
| `bloco` | todos | `N` novo · `V` variação · `F` fusão de fusões (pais já fusões, todos do mesmo tamanho, nenhum é base) · `L` prodígio (tema por cartela) · `X` fusão base+sacrifício · `A` ápice (fusão base+sacrifício de míticos) |
| `tier`, `tipo1`, `tipo2` | todos | ids de `comum.TIPOS` |
| `humanoide_previsto` | todos | bool (opcional, padrão false). As 4 da cartela `true` = cartela de humanoides (lote "de humanoides"): sem o limite de 1–2 |
| `fidelidade` | N, L | opcional: troca a do lote só nesta célula |
| `referencia_conteudo` | N, L homenagem | opcional: `{"descricao": "...", "arte": "artes/x.png"}` — `descricao` diz qual é a figura homenageada (interno: pode citá-la; nunca vai para ficha nem prompt); `arte` opcional (print/arte enviada pelo usuário), recortada para `pais/referencia_NN.png` e posta grande no quadrante da célula na prancha. **Com `arte`, exclusiva com `antecessor_externo`** (um quadrante por célula) |
| `leitura` | todos | opcional: direção de conceito escrita pelo assistente (1 linha) |
| `evolui_de` | N | opcional: `[cartela, linha, coluna]` da célula antecessora (mesma cartela ou anterior) |
| `antecessor_externo` | N | opcional, **exclusivo com `evolui_de`**: monstro que JÁ EXISTE no jogo (fora do lote) do qual esta célula evolui — `{nome, tier, tipo1, tipo2, descricao, arte, humanoide}`, `arte` relativo ao lote (`artes/x.png`, enviada pelo usuário). Tier da célula ≥ tier dele (igual = aviso; menor = erro); humanoide liga `humanoide_previsto` |
| `evolucao_modo`, `level_requerido` | N | opcionais, com `evolui_de` ou `antecessor_externo`: vão para `evolucao` no `monstros.json` (padrão `"a_definir"`; level inteiro ≥ 1) |
| `original` | V | `{nome, tier, tipo1, tipo2, descricao, arte, humanoide}` — `arte` relativo ao lote (`artes/x.png`) |
| `tipo_sai`, `tipo_entra` | V | qual tipo do original sai e qual entra |
| `ingredientes` | F, X, A | lista `{papel, nome, tier, tipo1, tipo2, descricao, arte, humanoide, linhagem}`; X/A: exatamente 2, papéis `BASE` e `SACRIFICIO`; F: 2–3, papel `PAI`; `linhagem` = outros nomes da linha evolutiva/avós (para o nome novo não carregar pedaço) |

## `entrada.json` (lista de células, gerada)

Cada célula = a do plano + `n` (1..4×cartelas, ordem de leitura), `cartela`, `linha`, `coluna`, `slot` (`X001_1`),
`arquivo` = `"{n:02d}_t{tier:02d}_{slug_do_nome}.png"` (o `{slug_do_nome}` literal até o nome existir),
`evolucao` (N: `{"anterior": n|null, "seguinte": n|null}`; com antecessor externo, `{"anterior": null, "seguinte": …,
"externo": {nome, tier, tipo1, tipo2, descricao, recorte, humanoide}}` — o `antecessor_externo` do plano sai da célula),
`fidelidade` (sempre), e nos ingredientes/original/antecessor externo `recorte` = `pais/<slug>.png`; na
`referencia_conteudo` com arte, `recorte` = `pais/referencia_NN.png`.

Prancha `referencias/cartela_NNN_pais.png`: toda cartela com V/F/X/A **ou** com célula N de antecessor externo **ou**
com célula N/L homenagem de `referencia_conteudo` com arte (estes grandes e centrados no quadrante da célula;
quadrantes sem origem ficam vazios). Antecessor interno nunca vai na prancha: mesma cartela = está na própria folha;
cartela anterior = a cartela gerada vai anexada.

Na N com antecessor (interno ou externo), a `anatomia` começa com "Evolução do <nome>." / "Evolução da <nome>." e o
`nome` novo é diferente do antecessor (erro no `valida_fichas.py`).

## Fichas (`fichas_claude/parte_<L>.json`, lista)

Campos que o AGENTE escreve (o resto o `compor_fichas.py` copia da entrada):

- todos: `n`, `nome` (V: não escreve; escreve `epiteto`), `humanoide`, `classe` (se humanoide), `paleta` [escura, clara],
  `anatomia`, `rosto`, `marcas_poder` (lista), `brilho`, `temperamento`, `conceito`, `marca_da_habilidade`, `descricao`;
- N/L: `arquetipo`; L: `tema` (igual nas 4 da cartela);
- N/L com `fidelidade: "homenagem"`: `tracos_iconicos` (lista de 3–6 traços visuais concretos: forma da máscara,
  figurino, arma/objeto, cores, silhueta, postura, detalhe-assinatura), sem o nome da figura/obra/ator;
- V: `epiteto`, `mantem`, `muda`;
- F/X/A: `herda` {nome exato de cada pai: o que veio dele}, `ascensao`.

`compor_fichas.py` acrescenta: campos fixos da entrada, `fidelidade`, `nome` (V = original + epíteto), `ingredientes`
(nomes), `arquivo`, `visual` (fórmula por bloco; na homenagem, logo depois da anatomia: "traços icônicos da homenagem
(reconhecível à primeira vista por quem conhece a figura clássica): (1) … (2) …") e roda `valida_fichas.py --arquivo`
(que exige `tracos_iconicos` na homenagem e recusa nome de personagem/filme de terror em qualquer campo de texto).

No prompt (`preparar_fila.py`), a linha da célula homenagem leva `HOMAGE` (`HOMAGE WITH REFERENCE` quando a figura está
na prancha) e a cartela ganha o bloco `HOMAGE CELLS`; a avulsa dessa célula anexa o quadrante da prancha.

Faixa de `marcas_poder` por tier: T1–2 0–2, T3–4 1–2, T5–6 2–3, T7–8 3–4, T9–10 4–5; F/X/A: +1 nas duas pontas.

## `monstros.json` (integrado; formato do cadastrador)

`{"lote", "status", "monstros": [ficha completa, ordenada por n]}`. Cada ficha tem, além dos campos acima, os campos que o
cadastrador lê: `nome`, `tipo1`, `tipo2`, `tier`, `descricao`, `arquivo`, `humanoide`, `evolucao` no formato
`{"de": "<nome do antecessor>", "modo": "a_definir"}` quando há antecessor, interno ou externo (o criador decide
modo/level; o plano pode trazer `evolucao_modo`/`level_requerido` na célula, e aí sai
`{"de", "modo": <evolucao_modo>, "level_requerido"}`), `ingredientes` `[{"papel","nome"}]` em F/X/A, `variacao_de` em V.

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
