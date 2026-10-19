# Contrato — fichas do lote {TITULO} ({LOTE})

<!-- Modelo: templates/CONTRATO-FICHAS.md da skill criar-arte. O Claude copia para a pasta do lote trocando {TITULO},
     {LOTE} e {SKILL} (pasta da skill, com barras "/"), e apaga as seções de bloco que o lote não tem. -->

As fichas e os prompts saem do Claude. A IA de imagem só gera, confere, salva e registra. Este contrato diz **o que** cada
agente escreve; as regras de conteúdo moram na skill e **não** são repetidas aqui — leia-as:

| Assunto | Regra |
|---|---|
| campos comuns, nome, descrição, temperamento | `{SKILL}/regras/fichas-nomes-descricoes.md` |
| técnica, cores, rosto e olhos, escada de poder (T1–T10) | `{SKILL}/regras/estilo.md` |
| fusão, fusão de fusões, evolução, variação | `{SKILL}/regras/fusoes.md` |
| humanoides (quantos, classe, corpo) | `{SKILL}/regras/humanoides.md` |
| tipos válidos e o que cada um significa | `{SKILL}/regras/tipagens.md` |
| o que nunca pode aparecer (primordiais, texto, terror, cópia) | `{SKILL}/regras/restricoes.md` |
| lote por tipagem, tema ou referência | `{SKILL}/regras/lotes-tematicos.md` |

Todos os caminhos abaixo são relativos à pasta do lote (rode os comandos de dentro dela).

## Entrada (só leitura)

- `python "{SKILL}/scripts/ver_celulas.py" . <cartelas>` mostra as suas células (aceita `3,4` ou `3-6`). **Não leia o
  `entrada.json` inteiro.** Cada célula traz `n`, `cartela`, `linha`, `coluna`, `bloco`, `tier`, `tipo1`, `tipo2`,
  `humanoide_previsto` e, conforme o bloco, `leitura`, `evolucao`, `original` + `tipo_sai`/`tipo_entra` ou
  `ingredientes` (com `linhagem`).
- **`leitura`** = direção de conceito escrita pelo Claude. Siga a ideia central; o detalhe é seu.
- `plano.json`: o campo `clima` (se houver) é o tom do lote e vai em todo prompt — a ficha não pode contrariá-lo.
- `referencias/cartela_NNN_pais.png`: prancha 2x2 das cartelas com arte de origem (V: o original; F: os pais, mesmo
  tamanho; X/A: BASE grande à esquerda, SACRIFÍCIO pequeno à direita; N: o antecessor de outra cartela, quando houver).
  **Olhe com Read antes de escrever**; para detalhe, `pais/<slug>.png`.
- Nomes que já existem no jogo: `{SKILL}/dados/nomes_existentes.json`. Se o Claude passou uma lista dos monstros que a
  tipagem/pacote já tem, ela vale como anti-repetição de arquétipo, silhueta e ideia central.

## Saída (EXCLUSIVA do agente)

`fichas_claude/parte_<LETRA>.json`: uma **lista** com uma ficha por célula das suas cartelas, em UTF-8 sem BOM. Não
escreva em mais nenhum arquivo. Os campos fixos (cartela, linha, coluna, bloco, tier, tipos, `ingredientes`, `arquivo`,
`visual`) **não** são seus: o `compor_fichas.py` copia/monta.

## Campos de todos os blocos

| campo | regra curta (detalhe nas regras acima) |
|---|---|
| `n` | o da célula |
| `nome` | nome próprio inventado, sonoro, de preferência uma palavra; único (fora de `nomes_existentes.json` e do lote), sem número, até 60 caracteres. **V não escreve `nome`** (escreve `epiteto`) |
| `humanoide` | true/false; `humanoide_previsto: true` obriga true. Cartela de inéditos: 1 ou 2 humanoides; fusão/variação: sai da base/original |
| `classe` | só se humanoide: livre e variada, sem repetir entre células sem motivo |
| `paleta` | `[cor escura do corpo, cor clara de acento]`, nascidas da mistura dos dois tipos. Ciano só com Elétrico |
| `anatomia` | uma frase do corpo, com a postura, na escala do tier. O tamanho vem da lore, não do tier |
| `rosto` | formato, número, posição e cor dos olhos + expressão. **Nunca dois rostos iguais na mesma cartela** |
| `marcas_poder` | lista de traços concretos de ameaça: T1–2 0–2, T3–4 1–2, T5–6 2–3, T7–8 3–4, T9–10 4–5; **F/X/A: +1 nas duas pontas** |
| `brilho` | a ÚNICA parte que emite luz, com a cor |
| `temperamento` | 2–3 palavras, nas cotas |
| `conceito` | 2 frases: o que a criatura É e FAZ no mundo |
| `marca_da_habilidade` | 1 frase com o poder que ela vai explorar |
| `descricao` | texto de jogo, ~440 caracteres, sem aparência, sem algarismo, sem nome de monstro, sem sistema do jogo |

## Por bloco

### N — novos

- `arquetipo`: 2–5 palavras; nenhum igual ou parecido aos do lote nem aos da lista de anti-repetição.
- Célula com `evolucao.anterior`: o estágio novo muda de forma (corpo, postura, armas) e mantém só as 2 cores, os olhos e
  um traço marcante; a `anatomia` começa com "Evolução do <nome>." / "Evolução da <nome>.". Nome sem prefixo obrigatório
  em comum com o antecessor.
- O tipo 1 dá conceito e anatomia; o tipo 2 dá material, cor e comportamento.

### V — variação

- `epiteto`: 1–3 palavras em português que evocam o tipo novo e digam algo do original ("de Maré Baixa", "Sem Sombra");
  o nome final é `<original> <epiteto>`. Varie; nunca palavra que é nome de monstro.
- `mantem` (~70%: silhueta, anatomia, rosto/olhos, pose, ideia) e `muda` (~30%: material, superfície, paleta, detalhes).
- Mesmo porte, idade e tier; `rosto` com o mesmo layout de olhos, cor nova. Original humanoide continua humanoide.
- Original em outro traço: diga na `anatomia` "no traço de ilustração das outras criaturas"; letreiro/moldura no recorte:
  diga o que NÃO entra.

### F — fusão de fusões

- `herda`: `{nome EXATO de cada pai: 1–2 elementos dele}`, com **todos** os pais. Criatura totalmente nova, que não
  lembra nenhum pai sozinho.
- `ascensao`: 1–2 frases do degrau acima de todos os pais.
- Nome sem 4+ letras seguidas em comum com nenhum pai nem com a `linhagem` deles.

### L — prodígio

- `tema`: um por cartela, o mesmo texto curto (2–6 palavras) nas 4 fichas; `arquetipo` como no N.
- As 4 criaturas do tema são de espécies, silhuetas e materiais bem diferentes; ousadia é o objetivo.

### X — fusão base + sacrifício (crossover)

- `herda`: `{nome EXATO da BASE: o que fica (silhueta, cabeça, rosto/olhos, traço marcante), nome EXATO do SACRIFÍCIO: o
  que vem (material de partes do corpo, cor de acento, 1–2 traços, o domínio como aura/arma/emanação)}`.
- `ascensao`: 1–2 frases; bem mais forte que os dois pais, nunca "a base com enfeite", metade-metade ou os dois lado a
  lado. Tier baixo continua jovem.
- `paleta`: corpo da base, acento do sacrifício. Base humanoide → fusão humanoide.
- `marca_da_habilidade`: um poder que nenhum pai tinha sozinho. Nome sem 4+ letras de nenhum pai nem da linhagem.

### A — ápice (base + sacrifício de míticos)

- Igual ao X, no topo: todo sinal mítico da base fica e o domínio do sacrifício entra por cima.
- Mesmos pais nos dois sentidos (A+B e B+A): **dois seres completamente diferentes**, cada um mandado pela sua base.

## Fechar a parte

```
python "{SKILL}/scripts/compor_fichas.py" . fichas_claude/parte_<LETRA>.json
```

O script copia os campos fixos, monta `nome` (V), `ingredientes`, `arquivo` e `visual`, regrava a sua parte e valida
(grava `fichas_claude/parte_<LETRA>_validacao.json`). Corrija até dar **OK** — releia o arquivo antes de cada correção,
porque ele regrava — e rode de novo no fim, porque outras partes podem ter criado o mesmo nome. Só parte validada sem
erros entra na fila (`preparar_fila.py`).
