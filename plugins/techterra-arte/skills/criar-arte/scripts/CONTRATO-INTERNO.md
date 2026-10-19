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

`fidelidade` (opcional; o script assume `"arquetipo"` quando falta): `"arquetipo"` = a referência vira criatura nova
(tema aberto, sem nomes) · `"releitura"` = criatura do Techterra com uma semente da figura clássica: só 1–2 âncoras
de forma, traduzidas pelos tipos, e os dois tipos fazem o resto (**o plano usa esta quando o usuário lista personagens nomeados**) · `"homenagem"` =
homenagem reconhecível à figura (só quando o usuário diz "igual", "fiel", "idêntico"); regras/lotes-tematicos.md §Nível
de fidelidade. Copiada para cada célula; a célula pode trazer a sua. Só vale em N/L (em V/F/X/A vira `"arquetipo"`).

Célula (ordem L1C1, L1C2, L2C1, L2C2; sempre 4 por cartela):

| campo | blocos | regra |
|---|---|---|
| `bloco` | todos | `N` novo · `V` variação · `F` fusão de fusões (pais já fusões, todos do mesmo tamanho, nenhum é base) · `L` prodígio (tema por cartela) · `X` fusão base+sacrifício · `A` ápice (fusão base+sacrifício de míticos) |
| `tier`, `tipo1`, `tipo2` | todos | ids de `comum.TIPOS` |
| `humanoide_previsto` | todos | bool (opcional, padrão false). As 4 da cartela `true` = cartela de humanoides (lote "de humanoides"): sem o limite de 1–2 |
| `fidelidade` | N, L | opcional: troca a do lote só nesta célula |
| `referencia_conteudo` | N, L releitura/homenagem | opcional: `{"descricao": "...", "arte": "artes/x.png"}` — `descricao` diz qual é a figura de referência (interno: pode citá-la; nunca vai para ficha nem prompt); `arte` opcional (print/arte enviada pelo usuário), recortada para `pais/referencia_NN.png` e posta grande no quadrante da célula na prancha. **Com `arte`, exclusiva com `antecessor_externo`** (um quadrante por célula). **Na releitura, `arte` só com `usar_imagem: true`** (senão é erro) |
| `usar_imagem` | N, L releitura | opcional, bool: `true` autoriza a `referencia_conteudo.arte` na releitura (por padrão a releitura não anexa imagem do personagem); `true` sem `arte` = erro; fora da releitura, ignorado com aviso |
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
com célula N/L homenagem (ou releitura com `usar_imagem`) de `referencia_conteudo` com arte (estes grandes e centrados
no quadrante da célula;
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
- N/L com `fidelidade: "releitura"`: `ancoras` (lista de 1–2 traços de FORMA — contorno do rosto/máscara, silhueta,
  gesto/postura ou objeto-assinatura — já traduzidos pelos tipos) e `reinvencao` (1–2 frases, ≥ 20 caracteres, citando
  os DOIS tipos: a camada Techterra — paleta de 2 cores dos tipos, elemento no próprio corpo, um brilho, pose); `classe`
  = papel próprio no mundo do jogo. Proibido: cores originais, figurino original ou peça dele, arma/objeto "como no
  filme", "pessoa fantasiada"; sem o nome da figura/obra/ator;
- V: `epiteto`, `mantem`, `muda`;
- F/X/A: `herda` {nome exato de cada pai: o que veio dele}, `ascensao`.

`compor_fichas.py` acrescenta: campos fixos da entrada, `fidelidade`, `nome` (V = original + epíteto), `ingredientes`
(nomes), `arquivo`, `visual` (fórmula por bloco; na homenagem, logo depois da anatomia: "traços icônicos da homenagem
(reconhecível à primeira vista por quem conhece a figura clássica): (1) … (2) …"; na releitura, logo depois da anatomia:
"âncoras de forma (traduzidas pelos tipos; só elas lembram a referência): (1) … (2) …; criatura do Techterra —
reinvenção pelos tipos: …") e roda `valida_fichas.py --arquivo` (que exige `tracos_iconicos` 3–6 na homenagem,
`ancoras` 1–2 e `reinvencao` ≥ 20 caracteres citando os dois tipos na releitura — com aviso se uma âncora citar cor ou
peça de figurino —, e recusa nome de personagem/filme de terror em qualquer campo de texto).

No prompt (`preparar_fila.py`), a linha da célula homenagem leva `HOMAGE` (`HOMAGE WITH REFERENCE` quando a figura está
na prancha) e a cartela ganha o bloco `HOMAGE CELLS`; a linha da célula releitura leva `REIMAGINED` (`REIMAGINED WITH
REFERENCE` com `usar_imagem`) e a cartela ganha o bloco `REIMAGINED CELLS` (criatura do Techterra à primeira vista;
só as 1–2 âncoras de forma, traduzidas, lembram a figura; com imagem, "use the reference figure … ONLY to read the
shape of the anchors; do not copy anything else"). A
avulsa de célula com figura na prancha anexa o quadrante.

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
