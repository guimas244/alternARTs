# Lote temático — quando o criador dá uma tipagem, um tema ou uma referência

Para que serve: o ponto de partida de um lote muda o desenho do lote. Este arquivo diz como montar o plano em cada caso
antes de escrever qualquer ficha. O plano (quantas, quais tipos, quais tiers, quais linhas) é mostrado ao criador numa
tabela curta e só depois as fichas começam.

## 1. O criador dá uma TIPAGEM ("um lote de Gelo")

Molde do pacote por tipagem: **32 monstros, 8 cartelas de 4**.

- **Tipo 1 = a tipagem pedida** em todos; o tipo 2 varia: **no mínimo 15 tipos 2 diferentes** no lote. O mesmo par de
  tipos só se repete dentro de uma linha evolutiva.
- **Tiers:** 3 monstros por tier do T1 ao T8 e 4 no T9 e no T10. Distribuição nas cartelas (ordem de leitura):

  | Cartela | Tiers |
  |---|---|
  | 01 | 1, 1, 2, 2 |
  | 02 | 3, 3, 4, 4 |
  | 03 | 5, 5, 6, 6 |
  | 04 | 7, 7, 8, 8 |
  | 05 | 9, 9, 10, 10 |
  | 06 | 1, 2, 3, 4 (o terceiro de cada tier) |
  | 07 | 5, 6, 7, 8 (o terceiro de cada tier) |
  | 08 | 9, 9, 10, 10 (terceiro e quarto) |

- **Linhas evolutivas** entre monstros do lote; um estágio nunca fica numa cartela anterior à do antecessor (ou, como
  no molde mais novo, a linha inteira fica dentro da mesma cartela, para nenhuma cartela depender de outra).
- **A tipagem tem que se ver:** o tipo 1 dá o conceito e a anatomia; o tipo 2 dá material, cor e comportamento. A cor
  NÃO é a estereotipada do tipo (Planta não precisa ser verde).
- **Não repetir o que a tipagem já tem:** peça ao usuário a lista de monstros que a tipagem já possui (nome + ideia) e
  não repita arquétipo, silhueta nem ideia central. Sem a lista, use pelo menos `dados/nomes_existentes.json` para nomes.
- 1–2 humanoides por cartela (regras/humanoides.md).

## 2. O criador dá um TEMA ou uma REFERÊNCIA EXTERNA ("filmes de terror", "Halloween", "circo", "mitologia nórdica")

### Nível de fidelidade (campo `fidelidade` do plano)

Antes do plano, decida o quanto a criatura se parece com a referência. São três níveis:

| | `arquetipo` | `releitura` (**padrão com nomes**) | `homenagem` |
|---|---|---|---|
| Quando | tema aberto, **sem nomes**: "circo assombrado", "filmes de terror", "Halloween" | o usuário lista personagens/figuras **NOMEADOS** (com ou sem "humanoides"), ou diz "parecido", "reconhecível", "como referência" | **só** quando o usuário diz "igual", "fiel", "idêntico", "exatamente como" o personagem |
| O que sai | o arquétipo vira **criatura nova** que só lembra o tema | **criatura original inspirada na figura**: 2–3 **âncoras** deixam entender a referência; os **dois tipos reinventam todo o resto** (corpo, material, paleta, detalhes, pose) | **homenagem reconhecível** à primeira vista pelos **traços icônicos** (máscara, figurino, arma, cores, silhueta, postura), no traço do jogo |
| Figurino/máscara da obra | não | só o que for âncora (em geral o rosto/máscara e UMA silhueta ou objeto); nunca o figurino inteiro, a paleta original inteira nem "pessoa fantasiada" | sim, como traço icônico redesenhado |
| Imagem do personagem | não | **não, por padrão**; só se as âncoras não bastarem: `referencia_conteudo.arte` + `"usar_imagem": true` na célula (o prompt manda ler só as âncoras dela) | opcional, `referencia_conteudo.arte` |
| Sempre proibido | nome do personagem/obra/ator no prompt, no nome e na ficha; rosto de ator; logo, marca ou texto | o mesmo | o mesmo |
| Na ficha | `arquetipo` | `arquetipo` + `ancoras` (2–3) + `reinvencao` (1–2 frases), que vão para o `visual` | `arquetipo` + `tracos_iconicos` (3–6), que vão para o `visual` |
| No prompt | — | bloco `REIMAGINED CELLS` + marca `REIMAGINED` na linha | bloco `HOMAGE CELLS` + marca `HOMAGE` na linha |

**O mesmo personagem nos três níveis** — "assassino da máscara de grito", célula Fantasma/Elétrico:

- `arquetipo`: criatura nova que só lembra o medo de ser perseguido de noite (ex.: um espectro de corredor que some
  quando a luz acende) — sem máscara de grito, sem manto; quem conhece o filme não liga uma coisa à outra.
- `releitura`: espectro do tipo fantasma/elétrico com **o rosto de grito alongado feito de estática** e **a silhueta de
  manto com capuz** (as duas âncoras); o resto é reinventado — corpo de névoa translúcida, fios de alta tensão no lugar
  das costuras, paleta azul-petróleo e ciano, pose torta de quem desliza. Quem conhece a figura entende a inspiração;
  ninguém diria que é o personagem.

**Lote "de humanoides" em releitura:** a reinvenção muda **material, paleta, superfície, detalhes e pose**, mas mantém o
corpo humanoide — cabeça, tronco, dois braços e **duas pernas**, de pé (regras/humanoides.md). Nada de "sem pernas",
"cauda no lugar das pernas" ou corpo de bicho: o tipo fantasma deixa o corpo translúcido ou de névoa, não tira as
pernas. Fora de lote de humanoides, a anatomia pode mudar à vontade.
- `homenagem`: a figura reconhecível no traço do jogo — máscara branca de grito, manto preto de capuz esfarrapado,
  faca erguida, a postura de quem espreita.

Na dúvida, use `releitura` e diga em uma linha no próprio plano que dá para subir para homenagem ou descer para
arquétipo. *Por quê: em arquétipo, uma lista de personagens nomeados saiu "incompreensível" (nada lembrava a
referência); em homenagem com a imagem do personagem anexada, saiu "idêntico". O dono quer "como referência: dá pra
entender, mas não incompreensível nem idêntico".*

### 2.0 Pedido curto com uma lista ("Quero lotes criando: 1. Ghostface — Pânico; 2. Chucky — …")

Uma lista de personagens, filmes, obras ou figuras, com ou sem a palavra "monstro", é um **lote temático de MONSTROS
por referência**. Não devolva um questionário: responda já com o **plano pronto** e só peça aprovação. Primeiro escolha a
**fidelidade** (tabela acima): personagens nomeados = **`releitura`** (padrão, com ou sem "humanoides"); só
"igual/fiel/idêntico" = `homenagem`; tema aberto sem nomes = `arquetipo`.

**Se o pedido diz "humanoides"** (ex.: *"Quero lotes criando humanoides: 1. Ghostface — do filme Pânico, tipo
fantasma; 2. Chucky — Brinquedo Assassino, docrates; …"*):

- cada item vira **1 humanoide** na **forma real** — sem estágio de objeto/bichinho, sem linha de 3 estágios;
- evolução só se pedirem, e aí os **3 estágios são humanoides**: jovem → adulto → ultimate;
- o tipo que o usuário deu para cada item vira o **`tipo1`**; o `tipo2` o plano propõe (sem repetir par);
- as células levam `humanoide_previsto: true` — cartela com as 4 humanoides é cartela "de humanoides" (o limite de 1–2
  por cartela vale só para lote misto, regras/humanoides.md);
- total múltiplo de 4 (4 itens = 1 cartela); sobrando vaga, proponha completar com mais personagens do mesmo tema;
- toda célula leva `referencia_conteudo: {"descricao": "<quem é a figura>"}` (interno: é o único lugar onde o nome pode
  aparecer).

**Imagem do personagem:**

- `releitura`: **não peça imagem**. No máximo, uma linha no plano: *"anexe a imagem de um personagem só se as âncoras
  não bastarem"*. Se ele anexar, a imagem vai para `<lote>/artes/` e a célula ganha `referencia_conteudo.arte` **e**
  `"usar_imagem": true` (sem `usar_imagem`, o `montar_entrada.py` recusa a arte); o prompt manda usar a figura só para
  ler as âncoras e não copiar mais nada.
- `homenagem`: peça 1 imagem de cada personagem (print ou arte), opcional mas é o que mais aproxima o resultado:
  `referencia_conteudo: {"descricao": "...", "arte": "artes/x.png"}`.

**Aviso de direito autoral** (mostre ao usuário, curto) — obrigatório em `homenagem`: *personagens reconhecíveis são
propriedade de terceiros — usá-los no jogo tem risco de direito autoral, e o gerador de imagem pode recusar; a decisão
de usar é do dono do jogo.* Em `releitura`, uma linha basta: *a releitura reduz o risco, mas não o zera.*

O plano tem, numa resposta só:

1. **Tabela**, uma linha por item da lista: nº · arquétipo (sem nome do personagem nem da obra; ex.:
   "boneco possuído", "assassino da máscara de fantasma ao telefone", "açougueiro mascarado da motosserra",
   "mascarado silencioso da noite das bruxas", "menina possuída", "mestre dos jogos de armadilha", "criatura alada que
   volta de tempos em tempos para caçar", "espírito de abóbora em pijama", "fantasma trapaceiro de terno listrado") ·
   em `releitura`, duas colunas: **"Âncoras (o que fica)"** (2–3 traços, em poucas palavras) e **"Reinvenção (o que
   muda)"** (como os dois tipos refazem corpo, material, paleta e pose); em `homenagem`, os traços icônicos previstos
   (3–6, em poucas palavras); em `arquetipo` sem "humanoides", o
   estágio 1 (objeto/bichinho simples), o 2 (forma real) e o 3 (ultimate) em poucas palavras · tier (ou escada de
   tier) · tipos. A tabela do chat pode mostrar o nome que o usuário escreveu, para ele se localizar; o `plano.json`
   (fora de `referencia_conteudo.descricao`), as fichas e os prompts, nunca.
2. **Estrutura padrão sem "humanoides":** cada item vira **1 linha evolutiva de 3 estágios**; total = 3 × itens,
   completado com míticos T10 até fechar múltiplo de 4 (12 itens → 36 monstros = 9 cartelas, sem mítico; 10 itens →
   30 + 2 míticos = 8 cartelas). Escadas de tier diferentes entre as linhas (da mais fraca T1→T3→T6 à mais forte
   T3→T7→T10). Tipagens: tipo 1 fixo na linha, o estágio final troca o tipo 2; espalhe para cobrir o máximo das 30 sem
   repetir par. **Com "humanoides":** a estrutura de cima (1 humanoide por item).
3. **Repetidos:** confira cada referência em `dados/arquetipos_existentes.json` (o que já virou monstro no jogo). Para
   cada repetido, marque na tabela e proponha: trocar por outra referência do mesmo tema **ou** fazer uma versão
   claramente diferente (outro arquétipo da mesma obra, outro ângulo).
4. O **aviso de direito autoral** (acima); em `homenagem`, o **pedido das imagens**; em `releitura`, só a linha "anexe
   só se as âncoras não bastarem".
5. **Perguntas curtas no fim** (o resto vai no padrão): em `releitura`, **o equilíbrio âncoras × reinvenção está bom**
   (algum item precisa de mais âncora para ser entendido, ou de menos para não ficar igual)? estrutura ok (3 estágios /
   2 estágios / só formas reais; com "humanoides": 1 por item ou com evolução)? o que fazer com os repetidos? quer
   míticos de raid ou fusões depois?

Com o "ok" do criador, siga o passo a passo abaixo a partir do item 3 (tipagens já estão no plano); em `releitura` e
`homenagem`, os itens 1–2 não se aplicam (a estrutura já está no plano).

No modo `arquetipo`, o tema vira **arquétipos**, nunca personagens. Passo a passo:

1. **Liste os arquétipos** do tema (ex.: terror → palhaço do bueiro, predador nascido de ovo, matador mascarado do lago,
   grande tubarão, assombração dos sonhos, múmia, fantasma da tela, conde vampiro, lobisomem, gigante costurado,
   cavaleiro sem cabeça, sacerdote da caixa-enigma). Mostre a lista ao criador antes de seguir.
2. **Escolha a estrutura** do lote e mostre ao criador. O molde aprovado do Halloween:
   - **10 linhas evolutivas de 3 estágios = 30 monstros + 2 míticos T10 = 32** (8 cartelas);
   - estágio 1 = algo **simples e quase inofensivo** (um objeto ou bichinho: o balão, o travesseiro, a fita, o ovo);
     estágio 2 = a **forma real** (o monstro reconhecível); estágio 3 = a **forma ultimate**;
   - as linhas têm **escadas de tier diferentes** (da mais fraca, T1→T3→T6, à mais forte, T3→T7→T10) — vale o tier de
     cada criatura, não o estágio;
   - evolução com **corpo novo** a cada estágio (mesmas 2 cores, mesmos olhos, mesmo traço marcante; nunca "o mesmo
     desenho maior").
3. **Distribua as tipagens.** No Halloween, cada linha usou 3 tipagens: o tipo 1 fixo na linha toda, e o estágio final
   troca o tipo 2 — assim as **30 tipagens aparecem uma vez cada**. Use esse molde quando o criador quiser o lote
   cobrindo todas as tipagens; senão, combine com ele.
4. **Escreva o bloco de clima do tema** que vai em todo prompt do lote (como o "HALLOWEEN PACK"): o que o tema é, o tom,
   o que é proibido. Ex. de terror: *assustador e divertido como noite de Halloween; o medo vem da silhueta, da expressão
   e do clima; sem sangue, sem ferida aberta, sem parte decepada; nunca reproduzir personagem, ator, figurino ou logo de
   filme — siga só a descrição de cada criatura.* Em `releitura`, o clima proíbe o figurino inteiro do personagem e
   "pessoa fantasiada" (as âncoras vêm na linha de cada criatura), além de rosto de ator, logo, nome e texto. Em
   `homenagem`, o clima **não** proíbe figurino/máscara (são os traços icônicos); proíbe rosto de ator, logo, nome e
   texto. Sempre "sem sangue".
5. **Originalidade:** o nome do filme/obra/personagem **nunca** aparece no prompt, no nome nem na descrição — nem em
   `releitura`/`homenagem` (o validador recusa em qualquer campo de texto da ficha). Pode ficar só num campo interno
   `inspiracao` da ficha (ou, em releitura/homenagem, em `referencia_conteudo.descricao` do plano), para o criador saber
   de onde veio. A descrição evoca o arquétipo sem citar (ex.: "o ciclo que volta a cada vinte e sete anos", não o nome
   do palhaço). Exceções: tipagem Nostálgico, onde a referência reconhecível é a definição do tipo, e os modos
   `releitura` e `homenagem` (regras/restricoes.md).
6. **Obtenção e evolução no jogo** (chance, level, evento, quantos por jogador) são decisão do criador: pergunte e
   registre no `monstros.json` como ele disse (regras/entrega.md). No Halloween: estágio 1→2 por chance, 2→3 por level.

## 3. O criador pede FUSÕES de um pacote temático ("fusões com os de Halloween")

Molde aprovado (fusões de Halloween, 19/10/2026):

- **Os dois pais saem do pacote temático.** O espaço novo é o **crossover**: arquétipo × arquétipo (filme × filme),
  sempre do **mesmo estágio** (simples × simples, forma real × forma real, ultimate × ultimate).
- **Anéis:** com N linhas, cada estágio é um anel de N fusões — cada linha entra **1× como base e 1× como sacrifício**
  por estágio, e nenhuma dupla de arquétipos se repete entre os estágios. Com 10 linhas: 3 anéis = 30 fusões.
- **Ápice** com os míticos do pacote. Dois míticos → as duas direções (A base + B sacrifício, e B base + A sacrifício):
  dois seres completamente diferentes, cada um mandado pela sua base.
- **Tipos:** tipo 1 da base, tipo 2 do sacrifício; nenhum par de tipos repete dentro do lote nem com fusões que o
  pacote já tenha (peça a lista ao usuário).
- Escolha os pares pelos **crossovers que fazem sentido** (o vampiro e o lobisomem, o mascarado e o dos sonhos, o gigante
  costurado reanimado por raio…) e escreva para cada par uma **leitura** de 1 linha antes das fichas.
- Base humanoide → fusão humanoide; 1–2 humanoides por cartela (arrume a ordem das cartelas para caber).
- Total múltiplo de 4 (cartelas cheias): se sobrar vaga, complete com um ápice ou uma fusão a mais combinada com o criador.
- Demais regras: regras/fusoes.md.

## 4. O criador anexa uma IMAGEM de referência

- Pergunte para quê: **estilo** (traço, luz, acabamento), **conteúdo** (a criatura/objeto a seguir) ou **encaixe**
  (onde fica a arte e onde fica vazio). Isso muda o texto do anexo no prompt.
- Imagem de **personagem** num lote `homenagem` é referência de conteúdo daquela célula: `referencia_conteudo.arte`
  (vai para o quadrante da célula na prancha; seção "Nível de fidelidade"). Em `releitura`, só com `"usar_imagem": true`
  na célula, e o prompt manda tirar dela apenas as âncoras.
- Ela entra como **anexo do lote** (na pasta de trabalho), dentro do limite de 5 anexos por geração.
- Só vira referência da skill (`referencias/`) se o dono do repositório escolher.
- Nunca copiar a imagem como figura: o prompt diz o que tirar dela ("só o traço", "só a silhueta", "só o encaixe").

## 5. Sempre

- Plano aprovado antes das fichas; fichas validadas antes da fila; fila cheia antes da sessão de imagem
  (regras/fluxo-sessoes.md).
- O lote termina no pacote de entrega com recortes e descrições (regras/entrega.md).
