# Personagens e NPCs: o método Lote 09

Regras da imagem de pessoa (rosto + corpo inteiro): preâmbulo, texto de cada pessoa, nomes, conferência e refação.

O dono aprovou este método em 09/10/2026, depois de ver o lote "Nórdicos e Eslavos": *"gostei muito dos resultados,
eles ficaram bonitos"*. Todo lote novo de NPC parte daqui.

## 1. O que nunca usar

- O prompt antigo de personagem (o que pedia "pele real, poros, assimetria natural, sem filtro de beleza, **sem rosto de
  modelo**", "2 marcas únicas" e "equipamento de campo prático") **não serve para lote**. Ele deixa as pessoas feias: o
  gerador foge do rosto bonito de propósito, as marcas viram cicatriz no rosto e toda roupa vira jaqueta técnica com
  calça cargo.
- Ele só sobrevive num caso: **atualizar um personagem que já existe** (§ 11), porque ali a arte atual manda.
- Também está superado o "nada sensual" dos lotes antigos de gente bonita. Vale o que está abaixo.

## 2. A página

- Quadrada, **1254×1254**, PNG com alfa de verdade (fundo transparente, sem chão, sem sombra, sem xadrez pintado).
- **3 colunas iguais**, uma pessoa por coluna: **2 mulheres + 1 homem**, cada um de um subtipo, com cabelo e paleta
  diferentes.
- Em cada coluna: **busto no terço de cima** (cabeça e ombros, de frente, olhando para a câmera) e **a mesma pessoa de
  corpo inteiro nos dois terços de baixo**, em pé, de frente (leve 3/4 permitido), os dois pés visíveis.
- Mesma pessoa em cima e embaixo: mesmo rosto, cabelo, maquiagem, marcas e roupa.
- Recorte depois: rosto **512×512** + corpo **512×1024** (ver [formatos.md](formatos.md)).

### Geometria

O preâmbulo aprovado (§ 3) **cita coordenadas em pixel**, ao contrário da cartela de monstros. Mantenha como está: foi
assim que funcionou. O que ele fixa, e por quê:

| Regra | Por quê |
|---|---|
| olhos do busto a ~42% do terço de cima; corte reto na base do busto | rostos alinhados entre colunas e lotes |
| busto termina em y=380; faixa **y=381–420 vazia na folha inteira** | o recorte separa rosto e corpo por essa linha vazia |
| cabelo do corpo começa em y≥440; cabelo do busto abaixo de y=15 | nada corta no topo de cada parte |
| nada cruza x=418 nem x=836 | as colunas se separam sem pedaço do vizinho |
| corpo: cabeça a ~5% e pés a ~95% da área de baixo | os dois pés aparecem; escala igual em todas |
| vestido longo e casaco param acima do sapato | o sapato fica visível |

## 3. O preâmbulo (em inglês, igual em toda página)

Cada página enviada = **preâmbulo** + linha em branco + **bloco da página** (as 3 pessoas, em português). O preâmbulo
vai sem mudar uma vírgula, exceto nos dois trechos de tema (§ 4).

Os blocos e o que cada um exige:

| Bloco | Exige |
|---|---|
| **BEAUTY** | todo mundo com beleza de top model de capa de revista; o traço do tema; cada pessoa um subtipo diferente; pele lisa com textura fina (nunca plástico); cabelo de salão; maquiagem bem-feita; lista do que é proibido no rosto |
| **WOMEN** | mulheres femininas, meigas e sensuais com elegância: rosto delicado, boca cheia, cílios longos, olhar expressivo que prende, postura graciosa, cintura marcada, roupa feminina. Nunca "machona" (cara dura, corpo ou pose masculinos, terno quadrado). Homens bonitos, masculinos, olhar caloroso |
| **EYES** | a cor da íris exata, viva, visível no busto, inclusive cores de fantasia; **só pigmento, sem brilho**; heterocromia só quando pedida, do lado pedido |
| **FASHION** | moda de editorial, sensual de campanha de luxo (ombro, braço, perna na fenda, decote elegante). Proibido: nudez, lingerie, transparência, pose vulgar. Sem armadura nem arma salvo quando pedido |
| **LAYOUT** | a geometria do § 2 |
| **WORLD RULES** | pessoa sem magia; sem cibernética; como é a prision; **só a prision brilha**; LADO = lado anatômico da própria pessoa |

```text
Create ONE square PNG character sheet for TechTerra: exactly THREE different adult humans in three equal columns. Reference 1 is ONLY a layout/technique reference, do not copy its people. Reference 2 defines the small capture devices called prisions. References 3 and 4 define the TARGET LEVEL OF BEAUTY AND FINISH ONLY: do not copy their faces, hair or clothes.

BEAUTY (the main goal of this sheet): every person is strikingly beautiful or handsome, like a top fashion model on a magazine editorial cover. [TEMA-TRAÇO: All three have clearly NORDIC or SLAVIC features (Scandinavian, Finnish, Icelandic, Baltic, Russian, Ukrainian, Polish, Czech, Balkan looks): high sculpted cheekbones, defined jawline, straight refined nose, almond or slightly deep-set eyes, strong elegant brows, fair to light skin with cool, rosy or golden undertones.] Each of the three is a DIFFERENT sub-type with a different face shape, hair color and style, never the same face repeated. Harmonious, symmetrical, photogenic faces; flawless even skin with only a fine natural texture (never plastic, never airbrushed wax); salon-quality glossy hair; well-done makeup matching the described style; healthy bright smile when smiling; elegant confident posture. Forbidden on faces: scars, broken or crooked noses, crooked or missing teeth, eye bags, deep wrinkles, blemishes, acne, windburn or sunburn, red cold noses, dirty or greasy hair, awkward grimaces, unflattering angles, tired, cold or sick look. Bodies are fit and well proportioned. Charisma: each expression must feel alive and inviting, as described.

WOMEN (very important): every woman is clearly FEMININE, sweet and sensual in an elegant, tasteful way. Soft delicate facial features, full soft lips, long lashes, big expressive eyes with a warm, deep, captivating gaze that connects with the viewer; gentle, tender or playful expression, never stern, hard, tough or tomboyish. Graceful feminine body language (relaxed shoulders, soft hands, slight hip or head tilt), feminine silhouette with a defined waist, long flowing or beautifully styled hair, soft glamorous makeup. Their clothes are feminine and flattering: fitted waists, dresses, skirts, soft knits, off-shoulder or elegant necklines as described. Never give a woman a masculine face, masculine build, mannish stance or boxy menswear unless described. Men are handsome and masculine with a warm, charming look.

EYES: render each iris EXACTLY in the color described, vivid and saturated, clearly visible from the bust view (ice blue, silver, violet, amber and other fantasy colors are natural iris colors in this world). It is ONLY iris pigment: no glow, no light emission, no glowing pupils, no special effects. Heterochromia only when described, on the described side.

FASHION: [TEMA-MODA: contemporary northern high fashion exactly as described: Scandinavian minimalism, modern Slavic folk embroidery, winter tailoring, knitwear, shearling, wool and leather, with real fabrics, tailoring and accessories, ready for a fashion editorial. Not historical costume, not Viking cosplay, not peasant clothing.] Adults may show shoulders, arms, legs through a skirt slit or an elegant fashion neckline when described; sensual but classy, like a luxury fashion campaign; never nudity, lingerie, see-through fabric or vulgar poses. No armor, no horned helmets and no weapons unless described.

Photoreal fashion studio photography, 85mm lens, no illustration, no painting, no 3D or CGI look. Soft beauty key light 45 degrees from left, gentle fill, cool rim light. Truly transparent alpha background: no floor, snow, scenery, ground shadow, checkerboard, gradient, text, letters, numerals, logos, borders or dividers. No monsters, animals or creatures.

LAYOUT: each column = one person. Top third: front-facing head-and-shoulders bust looking at camera, eyes around 42% of this third, straight horizontal crop at the bottom of the bust. Bottom two thirds: the SAME person with identical face, hair, makeup, marks and clothing, standing full length, front-facing (slight 3/4 allowed), head near 5% and both feet fully visible near 95% of this area. Bust artwork ends at y=380; rows y=381 to y=420 completely transparent across the ENTIRE sheet; full-body hair starts at y=440 or lower; bust hair starts below y=15. No element may cross x=418 or x=836 on the 1254 px canvas; keep clear transparent margins between columns. Nothing cut off: hair, hands, coat tails, shoes. Long dresses and coats stop above the shoes so both shoes stay visible.

WORLD RULES: humans have NO magic. No auras, runes, glowing tattoos, glowing eyes, glowing jewelry or spell effects; no mage robes. No cybernetics. Prisions are palm-sized translucent faceted crystal capture capsules inside ornate brass or steel cages with tiny gems, with a luminous vortex around a dark core inside; each person carries them exactly as described. ONLY the prisions glow. LEFT/RIGHT always means the person's own anatomical side; every small style mark (beauty spot, piercing, earring, ring, fine tattoo, colored streak) stays on the described side in both views and never glows.

Output one 1254 x 1254 PNG with real RGBA alpha.
```

Os colchetes `[TEMA-…: …]` marcam o que troca; **apague os colchetes e o rótulo** ao montar a página. O texto dentro
deles é o exemplo aprovado (tema nórdico e eslavo).

## 4. O que troca por tema

Para outro povo ou outra região, troque **só** dois trechos:

1. **BEAUTY — a frase do traço** (`TEMA-TRAÇO`): os povos de referência e os traços do rosto e da pele daquele tema.
2. **FASHION — a lista de estilos** (`TEMA-MODA`): a moda daquele tema, sempre contemporânea e de editorial, com o
   que ela **não** deve virar (ex.: "não fantasia histórica, não roupa de camponês").

Todo o resto (WOMEN, EYES, o resto de BEAUTY e FASHION, LAYOUT, WORLD RULES) fica igual. Se o tema não tiver neve,
pode tirar "snow" da lista de proibidos do fundo; o resto da frase fica.

Lore e texto nunca citam país da Terra: o traço vem do mundo do jogo (ex.: Nação do Gelo, Serra Branca, Torres de
Gelo). O nome do povo da Terra só aparece no `subtipo` da pessoa, como referência de traço.

## 5. Anexos (ordem fixa, toda geração)

| # | Arquivo (em `referencias/personagens/`) | É no prompt | Para quê |
|---|---|---|---|
| 1 | `estilo_pagina_1.png` | Reference 1 | layout e técnica (nunca as pessoas dela) |
| 2 | `prisions.png` | Reference 2 | como é a prision |
| 3 | `beleza_marta.png` | Reference 3 | **nível** de beleza e acabamento, não o rosto |
| 4 | `beleza_elira.png` | Reference 4 | idem |

O limite da ferramenta é 5 anexos: com os 4 fixos, sobra 1 vaga (o tile do rosto numa refação, § 11).

## 6. O texto de cada pessoa

Uma linha só, em português, de **750 a 980 caracteres**:

```text
cria a|o <Nome>, <idade> anos, <papel>. Beleza de top model <subtipo>, <2 adjetivos do temperamento>: pele <pele>,
cabelo <cor> <corte>, olhos <cor> <forma> e vivos (só a cor da íris, sem brilho) <maquiagem dos olhos>, <2–3 traços
do rosto>; <marca de estilo 1 com LADO>, <marca de estilo 2 com LADO>. <corpo e postura>. <roupa: 3–5 peças com tecido,
corte e cor>; <N por extenso> prisions <cor> <onde ficam>. Expressão <concreta, ligada ao temperamento>.
```

- **Homem:** "Beleza de modelo masculino <subtipo>", com a barba escrita (feita, por fazer bem desenhada, curta…).
- **A frase `vivos (só a cor da íris, sem brilho)` é obrigatória e literal.** A cor do olho e a do cabelo são escritas
  igual ao que foi sorteado.
- **Prisions literais:** `<duas|três|quatro> prisions <cor>` + onde ficam (cinto, corrente, colar, bandoleira,
  bolsinha, laço…). Varie o lugar.
- **LADO sempre em MAIÚSCULAS** (ESQUERDO/ESQUERDA/DIREITO/DIREITA) nas duas marcas de estilo: pinta de beleza, brinco,
  ear cuff, piercing pequeno, anel, pulseira, presilha, tatuagem fina, mecha. As marcas são de **estilo**, nunca defeito
  no rosto (sem cicatriz).
- **A peça-chave é a roupa principal e tem de aparecer.** A paleta dá as duas cores dominantes. O "estilo de roupa" é
  só o tempero dos acessórios; se brigar com a peça-chave, a peça-chave ganha.
- Um detalhe ligado ao papel (fita métrica, leque, caderno **sem nada escrito**, luvas de patinação na mão) é bem-vindo,
  sem virar fantasia.
- **Nada de "Tier N" nem outro número além da idade:** o gerador escreve número na imagem.

### Mulheres (o ponto mais importante)

- Abre com "meiga e sensual" (ou equivalente do temperamento sorteado).
- Rosto: traços delicados, olhos grandes ou amendoados, cílios longos, boca cheia, maquiagem suave ou glamourosa.
- Corpo e postura: graciosa, cintura marcada, cabeça levemente inclinada, mão delicada, quadril levemente projetado.
- Roupa: vestido, saia, tricô de ombro caído, corselete, fenda, decote elegante, meia-calça, bota de cano alto, salto.
  **Nada de** terno quadrado, jaqueta técnica, calça cargo, coturno. Calça e jardineira saem da lista de peças
  femininas.
- Expressão: doce, quente, sonhadora, brincalhona, sedutora serena. Nunca dura, séria, fechada ou desafiadora.

### Palavras proibidas no texto

- Cicatriz, olheira, ruga, "cansado", "desgrenhado".
- "brilhante", "luminoso", "neon", "reluzente", "refletivo" (puxam brilho; use "de salão", "acetinado", "sedoso",
  "fosco").
- Arma, armadura, cibernética, magia, aura, runa (salvo o papel pedir arma, § 7).
- Pele de animal (use shearling, lã, pelúcia sintética); monstro ou bicho.
- País da Terra fora do `subtipo`; nomes de lugares, sistemas ou eventos do jogo; texto escrito em objeto.
- Fantasia histórica do tema (ex.: viking) ou roupa de camponês.

## 7. Regras do mundo

- **A magia é das criaturas.** Humanos não conseguem manter magia: comandam monstros que usam magia. Na pessoa: nada de
  aura, runa, tatuagem que brilha, olho brilhando, joia brilhando, efeito de feitiço, roupa de mago. Olho de cor
  diferente é só pigmento.
- **Só a prision brilha.** Prision = cápsula do tamanho da palma, cristal facetado translúcido numa gaiola ornamentada
  de latão ou aço com pequenas gemas, com um vórtice luminoso em volta de um núcleo escuro (ver `prisions.png`). Todo
  NPC é treinador e carrega prisions.
- **Cibernética é rara.** Padrão: nenhuma (o preâmbulo diz "No cybernetics"). Só quando o pedido mandar, e no máximo
  ~1 por lote.
- **Sem monstro, bicho ou criatura na imagem.** O monstro do NPC aparece em outra arte.
- Sempre humanoide; quase sempre humano comum. Não humano só quando o pedido mandar.
- Arma só para soldado, bandido ou mercenário (e então escrita na linha). A maioria não tem arma.
- Todos com expressão concreta. Nenhum texto, letra, número ou logo na página.

## 8. Adultos e limites

- **Lote de beleza (este método) = só adultos.** Sensual de campanha de luxo; **proibido** nudez, lingerie,
  transparência, pose vulgar.
- **Lotes de faixa baixa (mirins, T1–2): 95% crianças de 10 a 13 anos** — são lotes fora do método de beleza.
- Fora dos lotes de beleza, quando o pedido tiver **menor de 18 anos**: roupa completa e discreta, pose natural, nada sensual. Nunca misture criança numa página com o preâmbulo de
  beleza: use o texto da pessoa sem BEAUTY/WOMEN de top model.
- Idade é o único número que entra no texto.

## 9. Olhos e moda

### Tabela de olhos de fantasia (só cor da íris, nunca brilho)

| Grupo | % | Cores |
|---|---|---|
| **Fantasia quente** | 22 | vermelho-rubi, vermelho-vinho, laranja-âmbar, laranja-cobre, dourado-mel intenso |
| **Fantasia fria** | 25 | violeta, lilás, turquesa, azul-safira profundo, azul-gelo quase branco, prata |
| **Verdes vivos** | 13 | verde-esmeralda, verde-jade, verde-limão claro, verde-oliva dourado |
| **Rosa e raros** | 5 | rosa-quartzo, magenta escuro, cinza-tempestade |
| **Heterocromia** | 5 | dois olhos de cores diferentes (lado definido) |
| **Naturais bonitos** | 30 | castanho-mel, avelã, verde, azul, cinza, castanho-escuro "de veludo" |

- Padrão: **70% fantasia, 30% natural**. O lote pode mudar a proporção (o "Nórdicos e Eslavos" usou 50/50).
- Não repita cor de olho na mesma página.
- Cabelo de fantasia (rosa, prata, azul tingido): ~12%, **como tintura de moda**, nunca como magia.

### Os 20 estilos de moda (cada um ≤ 6% do lote)

1. bartender de luxo
2. alfaiataria romântica
3. couro de estrada
4. tecno-streetwear de grife
5. alfaiataria futurista (terno de ombro marcado, capa curta)
6. gala de corte moderno
7. boho de viajante
8. náutico chique
9. desert-chic (linho, ouro, lenço)
10. gótico elegante
11. sportswear premium (de campeonato)
12. avant-garde de passarela (golas esculturais, assimetria)
13. cottagecore refinado
14. minimalismo de luxo (gola alta preta, nada mais)
15. corte das nações (Fogo vermelho-ouro, Gelo prata-azul…)
16. utilitário-glam de oficina (macacão cortado, cinto de ferramentas bonito)
17. alta-costura de festival
18. art déco urbano
19. preppy de ateliê
20. retro-futurismo de salão

- Na mesma página, **3 estilos diferentes**.
- Num lote temático, a lista vira a moda do tema. Exemplo aprovado (norte frio), femininos: folk eslavo moderno
  bordado, minimalismo escandinavo, tricô de luxo, veludo de salão de inverno, romântico de renda e fita, gala da corte
  do gelo, boho de feira de inverno, náutico do mar gelado, après-ski chique, couro macio com saia, alfaiataria feminina
  acinturada, vestido-casaco de lã, cottagecore do norte, glamour de cassino, bailarina fora do palco, festival de
  inverno, ateliê de artista, camurça e franja, cetim e caxemira, floral de lenço eslavo. Masculinos: alfaiataria de
  inverno, tricô de pescador de grife, couro e lã, folk eslavo moderno masculino, minimalismo escandinavo masculino,
  náutico do mar gelado, après-ski elegante, oficina chique, casaco militar de gala sem insígnias, boho de viajante do
  norte, smoking de cassino, esportivo de campeonato premium.

## 10. Variedade e conferência

### Papel × roupa

- **Sorteie a peça-chave dentro do papel.** Sorteio solto junta papel e roupa que brigam (pescador de smoking).
- Papel durão (capitã de quebra-gelo, guarda-costas, mecânica) puxa jaqueta e cara fechada. Dê às mulheres papéis que
  combinem com o tom, ou transforme o papel (dona do barco de passeio, não capitã de quebra-gelo).

### Molde repetido

- Na mesma página: silhueta, comprimento de roupa e penteado diferentes; nenhuma página monocromática (três roupas
  grafite, chumbo e preto = molde).
- No lote: a mesma marca de estilo no máximo 4 vezes a cada 36 pessoas; duas expressões nunca começam com as mesmas
  três palavras; varie calçado, acessório e lugar da prision; não copie frases do piloto.
- **Lote por tipagem ou faixa:** o objeto-assinatura de uma tipagem **não pode repetir** nas pessoas dessa tipagem. Num
  lote de 75, 24 das 30 tipagens saíram com o mesmo objeto nas 5 pessoas (cantil para Água, relógio de bolso para
  Tempo, óculos de aviador para Voador) e o dono leu como fôrma. Fixe os acenos um a um, por pessoa, e proíba repetir.
- Não copie peças marcantes de personagens já existentes (o apito e o boné de um, os fones de outro).
- Cuidado com o molde de etnia: pele clara + loira + olho azul-acinzentado repetido em várias pessoas de lotes que não
  são nórdicos.
- Revisor cruzado no fim, lendo todas as linhas juntas, antes de liberar a geração.

### Nomes (escritos à mão)

- **Nome de NPC é escrito à mão e conferido um a um.** Num lote de 90, 87 nomes saíram de gerador combinatório
  (Loriro, Lorira, Kaliro, Kalena…) e tiveram de ser trocados todos.
- **Pool separado por etnia/subtipo**: o nome casa com o subtipo da pessoa (nada de nome lituano numa pessoa "búlgara").
  Se um script sortear, sorteia de uma lista curada à mão, e a lista inteira é lida antes de seguir.
- Únicos dentro do lote e contra a lista de nomes de NPC existentes. Essa lista **não vem com a skill** (`dados/` só
  tem nomes de monstro): peça ao usuário; sem ela, avise que a checagem ficou só dentro do lote.
- Sem diacrítico estrangeiro que o jogador não digita nem lê: Tram Anh Doan (não Trâm Anh Đoàn), Vukasin Tamindzic
  (não Vukašin Tamindžić).
- Sem dois nomes quase iguais no mesmo lote (Tilila × Tiril), sem nome que soe como palavra comum (Popoca, "pipoca"),
  sem várias pessoas com a mesma inicial rara.

### Conferência de cada página (quem gera confere; o preparo confere de novo antes de recortar)

1. **Beleza:** as três pessoas são bonitas de verdade, no nível das referências 3 e 4. Abaixo disso: anote para o dono (não gera refação).
2. **Traço:** as três têm o traço do tema, cada uma de um subtipo (não a mesma loira três vezes).
3. **Mulheres meigas e sensuais:** rosto delicado, olhar que prende, postura e roupa femininas. "Machona" = anotar para o dono (não gera refação).
4. Olhos na cor pedida, visíveis no busto e sem brilho.
5. Fundo transparente de verdade; vão entre busto e corpo; nada cruza a coluna; os dois pés aparecem.
6. Mesma pessoa em cima e embaixo, mesma roupa, maquiagem e marcas, cada marca do lado certo.
7. Roupa de moda como descrita, sem virar fantasia histórica nem roupa de camponês.
8. Só as prisions brilham. Nenhum texto, número, logo, monstro ou bicho.
9. Sensual sem ser vulgar: sem nudez, lingerie, transparência ou pose vulgar.

**Uma geração por página.** Refaz **1 vez**, só por erro grave: não saíram 3 pessoas, fundo todo opaco, nudez. Quem
julga a beleza é o dono, depois.

### Fluxo do lote

1. **Piloto de 4 páginas** (uma por sessão de imagem): o dono julga o traço antes de escalar.
2. **Roster**: sexo, idade, subtipo, pele, cabelo, olho, corpo, temperamento, papel, peça-chave, paleta e prisions,
   sem repetir na página.
3. Textos escritos por partes, cada parte dona de um arquivo, seguindo o § 6 — por agentes em paralelo, se o
   ambiente tiver subagentes; senão, uma parte por vez, em sequência; revisor cruzado no fim.
4. Validar todas as linhas (tamanho, frase literal dos olhos, LADO, prisions, palavras proibidas) e montar
   `prompts/pagina_NNN.txt`. **A fila tem de estar cheia antes de mandar colar.**
5. Sessões de imagem com páginas de 4 em 4, uma geração por página, direto até a última.

## 11. Refação fiel e personagem já existente

### Refação fiel (mesma pessoa, de novo)

A IA não guarda identidade. O que segura o rosto:

1. **DNA do rosto em inglês**, escrito uma vez e **copiado sem mudar** em toda geração daquela pessoa: formato do rosto,
   pele, olhos (cor e forma), sobrancelhas, nariz, boca, cabelo, barba, idade aparente.
2. **Âncoras:** pelo menos 2 marcas visíveis com LADO, que a IA repete bem. Neste método são as 2 marcas de estilo
   (pinta, piercing, ear cuff, mecha, tatuagem fina), nunca cicatriz.
3. **Tile do rosto aprovado anexado** (5º anexo) com a instrução `Column N: same person as reference image 5`.
4. **Na mesma grade de 3 colunas**, juntando até 3 refações; se houver só uma, as outras colunas pegam os próximos
   pendentes do lote. Escala e luz continuam iguais.
5. **Traje separado do rosto:** troca de roupa ou de fase sem mexer no DNA.

O resultado esperado é "claramente a mesma pessoa", não um clone perfeito.

### Atualizar personagem de jogador (ou NPC que já tem arte)

Aqui **a arte atual é a referência**, não o preâmbulo de beleza: não "embeleze" a pessoa. Este é o único uso do modo
antigo, e ele vai escrito assim:

- Anexos: `rosto.png` e `corpo.png` **atuais** da pessoa, mais `estilo_pagina_1.png` (layout) e `prisions.png`.
- Pedido em uma frase: o que muda ("envelhece para 30 anos", "cabelo curto", "troca a roupa para uniforme de soldado",
  "usa esta foto como novo rosto").
- **Mude só o que foi pedido.** Rosto, cor dos olhos, pele, cabelo, marcas, tatuagens, roupa e físico continuam iguais
  às imagens anexadas.
- **Envelhecer ou rejuvenescer** = a mesma pessoa com outra idade: mantém formato do rosto, olhos, nariz, boca, marcas e
  tatuagens; muda só os sinais da idade (pele, rugas, grisalho, postura, corpo).
- **"Físico extremamente avançado"** (quando a ficha da pessoa disser): corpo de atleta de elite no limite humano,
  musculatura densa e definida, estrutura larga, visível mesmo com roupa, natural, sem exagero de fisiculturista.
  Menor de idade: a mesma ideia de atleta jovem de elite.
- Mesma página de 3 colunas e mesma geometria; com 1 ou 2 pessoas, as outras colunas ficam totalmente transparentes.
- Mesmas regras do mundo (§ 7). Menor de 18: roupa completa e discreta.
- Conferir: é a mesma pessoa das imagens anexadas; fundo transparente; pés visíveis; nada brilha além das prisions.
