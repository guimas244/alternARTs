# Contrato — fichas do lote {TITULO} ({LOTE})

<!-- Modelo: templates/CONTRATO-FICHAS.md da skill criar-arte. O assistente copia para a pasta do lote trocando {TITULO},
     {LOTE} e {SKILL} (pasta da skill, com barras "/"), e apaga as seções de bloco que o lote não tem. -->

As fichas e os prompts saem do preparo, antes da geração. Na etapa de geração só se gera, confere, salva e registra.
Este contrato diz **o que** cada parte tem (escrita por um agente, se houver subagentes, ou pelo assistente, uma parte
por vez); as regras de conteúdo moram na skill e **não** são repetidas aqui — leia-as:

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
  `humanoide_previsto`, `fidelidade` e, conforme o bloco, `leitura`, `referencia_conteudo` (releitura/homenagem),
  `usar_imagem` (releitura com imagem), `evolucao`,
  `original` + `tipo_sai`/`tipo_entra` ou `ingredientes` (com `linhagem`).
- **`leitura`** = direção de conceito escrita no plano. Siga a ideia central; o detalhe é seu.
- `plano.json`: o campo `clima` (se houver) é o tom do lote e vai em todo prompt — a ficha não pode contrariá-lo.
- `referencias/cartela_NNN_pais.png`: prancha 2x2 das cartelas com arte de origem (V: o original; F: os pais, mesmo
  tamanho; X/A: BASE grande à esquerda, SACRIFÍCIO pequeno à direita; N: o antecessor externo — monstro que já existe no
  jogo —, quando houver; N/L homenagem, ou releitura com `usar_imagem`: a figura de referência enviada pelo usuário,
  quando houver).
  **Olhe a imagem antes de escrever**; para detalhe, `pais/<slug>.png`.
- Nomes que já existem no jogo: `{SKILL}/dados/nomes_existentes.json`. Se veio uma lista dos monstros que a
  tipagem/pacote já tem, ela vale como anti-repetição de arquétipo, silhueta e ideia central.

## Saída (EXCLUSIVA da parte)

`fichas_claude/parte_<LETRA>.json`: uma **lista** com uma ficha por célula das suas cartelas, em UTF-8 sem BOM
(`fichas_claude/` é o nome fixo da pasta das fichas, que os scripts leem). Não escreva em mais nenhum arquivo. Os campos fixos (cartela, linha, coluna, bloco, tier, tipos, `ingredientes`, `arquivo`,
`visual`) **não** são seus: o `compor_fichas.py` copia/monta.

## Campos de todos os blocos

| campo | regra curta (detalhe nas regras acima) |
|---|---|
| `n` | o da célula |
| `nome` | nome próprio inventado, sonoro, de preferência uma palavra; único (fora de `nomes_existentes.json` e do lote), sem número, até 60 caracteres. **V não escreve `nome`** (escreve `epiteto`) |
| `humanoide` | true/false; `humanoide_previsto: true` obriga true. Cartela de inéditos: 1 ou 2 humanoides (cartela com as 4 previstas humanoides = lote de humanoides: as 4); fusão/variação: sai da base/original |
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
- Célula com `evolucao.anterior` ou `evolucao.externo` (monstro existente, na prancha): o estágio novo muda de forma (corpo, postura, armas) e mantém só as 2 cores, os olhos e
  um traço marcante; a `anatomia` começa com "Evolução do <nome>." / "Evolução da <nome>.". Nome sem prefixo obrigatório
  em comum com o antecessor.
- O tipo 1 dá conceito e anatomia; o tipo 2 dá material, cor e comportamento.

### N/L — releitura (célula com `fidelidade: "releitura"`; padrão para personagens nomeados)

- **Teste do olhar:** à primeira vista é uma criatura do Techterra; só numa segunda olhada a inspiração aparece
  (~25% referência / ~75% Techterra). A referência é semente, não resultado.
- `ancoras`: lista de **1 a 2** traços **de FORMA** — contorno do rosto/máscara, silhueta, gesto/postura ou
  objeto-assinatura — **já traduzidos pelos tipos**: a forma fica, o material e a cor vêm dos tipos. Sem cor e sem
  peça de figurino (o validador avisa). Ex. (assassino da máscara de grito, Fantasma/Elétrico): "contorno de rosto de
  grito alongado, de olhos caídos e boca oval aberta, feito de estática chiando", "silhueta de capuz pontudo feita de
  névoa que se desfia em fios".
- `reinvencao`: 1–2 frases (≥ 20 caracteres) com a **camada Techterra**, citando os **DOIS tipos** pelo nome (o
  validador exige): paleta de **2 cores da mistura dos tipos** (regras/estilo.md "Cores"), o **elemento visível no
  próprio corpo e material** (não só na arma), **UM sistema de brilho** próprio e a pose. Em lote **de humanoides**,
  mantenha cabeça, tronco, 2 braços e 2 pernas, de pé — os tipos mudam material e paleta, não tiram membros. Ex.: "o
  fantasma faz o corpo de névoa índigo carregada, com pernas que se desfazem em fumaça só nos pés; o elétrico corre
  nele em veias de corrente ciano e faz brotar isoladores de vidro dos ombros; só a corrente brilha; pose torta de
  quem desliza".
- `classe`: o **papel da criatura no mundo do jogo** (ex.: "caçador de estática", "bufão de espinhos", "coveiro de
  geada") — conceito próprio, nunca "o assassino do filme". `rosto` no padrão do jogo (regras/estilo.md "Rosto e
  olhos") e `marcas_poder` do tier completam a camada Techterra.
- **Proibido:** as cores originais; o figurino original, nem uma peça dele (macacão, avental, terno, máscara de
  hóquei…); a arma/objeto "como no filme" (objeto-assinatura só como forma refeita no material dos tipos); "pessoa
  fantasiada". O resultado não pode parecer o personagem original — nem virar criatura sem relação com ele.
- `anatomia`, `paleta`, `rosto` e `marcas_poder` seguem a reinvenção (não o figurino original). `tracos_iconicos` é só
  da homenagem.
- O `compor_fichas.py` põe no `visual`, logo depois da `anatomia`: "âncoras de forma (traduzidas pelos tipos; só elas
  lembram a referência): …" e "criatura do Techterra — reinvenção pelos tipos: …". `ver_celulas.py` mostra a figura
  (descrição interna); se a célula tiver `usar_imagem`, a figura está no quadrante da prancha — olhe só para ler a
  forma das âncoras.
- **Nunca** o nome do personagem, da obra ou do ator em campo nenhum: o validador recusa.

### N/L — homenagem reconhecível (célula com `fidelidade: "homenagem"`; só quando pedirem "igual/fiel/idêntico")

- `tracos_iconicos`: lista de **3 a 6** traços visuais concretos que fazem a figura clássica ser reconhecida à primeira
  vista — forma da máscara ou do rosto, figurino, arma/objeto, cores, silhueta, postura, detalhe-assinatura. Ex.:
  "máscara branca alongada de boca aberta num grito", "manto preto de capuz com barra esfarrapada", "faca de caça erguida
  junto ao peito". O `compor_fichas.py` põe esses traços no `visual`, logo depois da `anatomia`.
- `ver_celulas.py` mostra a figura (descrição interna do plano) e, se houver, a referência no quadrante da prancha —
  **olhe a imagem**. Tire dela os traços; não descreva a imagem como cópia.
- **Nunca** o nome do personagem, da obra ou do ator em campo nenhum (nome, arquétipo, traços, anatomia, conceito,
  descrição…): o validador recusa. Rosto de ator, logo, marca e texto também não. A criatura é redesenhada no traço do
  jogo, com nome próprio inventado e descrição de jogo própria; o tipo 1 continua mandando no conceito e o tipo 2 no
  material e na cor, sem apagar os traços icônicos.

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
