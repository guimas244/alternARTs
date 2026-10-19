# Itens: equipamento de monstro, livro, campeonato e agendas

Regras da arte de item em cartela 5x5: o que o objeto é, como a grade se organiza, o texto fixo do prompt e o nome dos
arquivos.

## 1. Estilo

- **"Miniatura 3D estilizada"**, aprovado pelo dono: objetos de fantasia com cara de pequenas esculturas digitais,
  formas esculpidas e arredondadas, espessura evidente, bordas chanfradas, materiais suaves, metal acetinado, luz macia
  que mostra o volume.
- Referência: `referencias/itens/estilo_03_miniatura_3d.png` (só estilo; os objetos dela nunca são copiados).
- **A tipagem não impõe cor.** A identidade vem de forma, criatura, material, fenômeno e referência (Marinho pode ser
  peixe, oceano, hidra, kraken; Fogo pode ser sol, vulcão). O azul da referência é daquela cartela, não regra do estilo.
  Itens da mesma linha não dividem uma paleta só.
- **Criatividade padrão = a da primeira cartela Marinho** aprovada: muitas referências diferentes (anatomia, fenômeno,
  material, artefato), cada uma virando um equipamento distinto.

## 2. É equipamento DE MONSTRO

Quem veste arma, armadura e orb no jogo é o **monstro**, não o treinador. O dono reprovou porrete e espada com cabo:
*"são equipamentos de monstros — uma garra ao invés de arma, um capacete de monstro, um peitoral de monstro, um orb ou
brasão"*.

| Slot | O que desenhar |
|---|---|
| **Arma** | capa de garra, capa de presa, ferrão, capa de chifre, capa de bico, pinça, ferradura, lâmina de cauda, maça de cauda, lâmina de barbatana, esporão |
| **Armadura** | peitoral de fera (com vãos de pata), barda, casco de costas, manto, focinheira, ombreira, arreio, peitoral de coleira, elmo de monstro (focinho longo, vão de orelha ou chifre; nunca capacete de gente) |
| **Orb** | orbe, medalhão, brasão, sino, lanterna, pingente, amuleto, relicário, pendurado em coleira, chifre, cauda ou peito |

- Toda peça mostra **como prende**: correia, argola, presilha, punho, encaixe.
- A peça aparece **sozinha e oca**: sem criatura viva, cabeça, rosto, olho, membro ou asa. Dente, osso, chifre, couro e
  pena só como material trabalhado.
- **Frase obrigatória no prompt:** `monster equipment, no handle, no hilt, no human glove/torso`.
- **Teste do monstro:** *uma pessoa conseguiria segurar ou vestir isso, do jeito que está desenhado? Se sim, regere.*

## 3. Faixas: progressão sem objeto recolorido

- Faixa 1 a 10 = força, da menor à maior. **Faixa mais alta = objeto mais elaborado, nunca maior.** Todos no mesmo
  tamanho de ícone.
- **Cada célula é um conceito novo.** Proibido o mesmo objeto recolorido ou com enfeite a mais entre faixas, e proibido
  preencher a cartela variando objetos dentro de uma cor só.
- Escada de materiais que funcionou:
  - faixas 1–2: material bruto e humilde (osso, couro cru, madeira, pedra lascada, corda);
  - faixas 3–4: ofício honesto (metal simples, costura firme, rebite);
  - faixas 5–6: trabalho fino (metal polido, uma gema ou um material raro do tipo);
  - faixas 7–8: peça encantada (material vivo ou impossível, luz presa dentro da peça; "vivo" = material que brilha ou
    cresce, nunca bicho, rosto ou olho);
  - faixas 9–10: relíquia (ornamento rico, vários materiais nobres, presença única).
- Em item comum: **sem coroa de louros, sem estrela de patente, sem medalha de patente** (louro e estrela são a marca
  dos itens de campeonato, § 7).

## 4. A grade

- Cartela **1254×1254**, PNG com alfa de verdade, **exatamente 25 objetos** numa grade invisível de 5 colunas × 5
  linhas. Recorte final **320×320** (ver [formatos.md](formatos.md)).
- **Coleção por tipagem:** cada tipagem tem **2 páginas de 25** = 50 itens, cinco por faixa.
  - Página 1 = faixas 1–5; página 2 = faixas 6–10.
  - Nessa coleção, **cada linha é uma faixa** (os cinco itens daquela faixa) e a página inteira é da mesma tipagem.
- **Pacote misto (várias tipagens por cartela):** **linha = tipagem, coluna = faixa** (5 tipagens por cartela; uma
  cartela com as faixas 1–5 e a seguinte com as 6–10).
- O diagrama `guia_grade_5x5.png` é **neutro** (só posição): serve para os dois arranjos. Este arquivo é a referência
  única da organização da grade.
- O prompt **diz qual dos dois** numa linha `LAYOUT OF THIS SHEET` e lista as células na ordem exata
  (`Row r, column c (...)`). **A ordem é o que dá nome a cada recorte**: célula fora de ordem = arquivo com nome errado.

### Enquadramento: o diagrama manda

- O gerador **não obedece porcentagem** de ocupação (pedir 72%, 75% ou 90% dá 91–99%). O controle que funciona é o
  **diagrama da grade anexado** (`referencias/guias/guia_grade_5x5.png`): quadrado cinza = onde o objeto fica e o
  máximo que pode ocupar; linha rosa = vão proibido. Ele nunca é desenhado.
- Objeto comprido: compacto e na diagonal. Pares e peças pequenas encostam no objeto principal, como um conjunto.
- **Vãos limpos:** nada de partícula, faísca, fumaça, fragmento, aura externa, nuvem de brilho, chão, sombra, cenário,
  textura de fundo ou grade visível. Brilho, chama, gelo, água, raio e névoa ficam **dentro** do objeto ou colados na
  superfície.
- Objeto um pouco grande que não encosta no vizinho **está aprovado**: o recortador separa por objeto e recentraliza.
  "Reprovação por margem" não é critério.

### Sem nome em português na célula

- A linha de cada célula descreve o objeto em inglês (material, forma, cor, encaixe). **O nome do item em português não
  entra no prompt**: o gerador escreve o nome na imagem.
- Os nomes ficam numa **tabela de conferência fora do prompt** (linha × coluna → nome), para quem confere.

## 5. O texto fixo do prompt (equipamento de monstro)

Anexos, nesta ordem: 1) `referencias/itens/estilo_03_miniatura_3d.png`; 2) `referencias/guias/guia_grade_5x5.png`.
Troque só o que está entre `{}`.

```text
Use case: stylized-concept.
Create a NEW parent sprite sheet for the fantasy game Techterra: MONSTER EQUIPMENT {coleção}, sheet {n} of {total} ({tipagens}; tiers {a}–{b}).
The FIRST supplied image is a STYLE REFERENCE ONLY. Match its sculpted stylized 3D miniatures, substantial beveled forms, richly dimensional satin materials and soft studio light. Use the objects listed below, not the objects of the reference.
The SECOND supplied image is a LAYOUT DIAGRAM ONLY: each of its 25 grey squares shows where one item sits and the largest area it may fill; the pink lines are forbidden gutters that nothing may touch. Never draw the diagram itself, its grey squares or its pink lines.
Canvas: square 1254 x 1254 pixels, true transparent background with genuine alpha; never paint a checkerboard pattern. EXACTLY 25 complete isolated items arranged in an INVISIBLE grid of 5 columns by 5 rows. Follow the precise row/column order.
LAYOUT OF THIS SHEET: {each ROW is one elemental type (row 1 = …; row 5 = …). Each COLUMN is one tier, from tier a on the left to tier b on the right. | the whole sheet is type …; each ROW is one tier, from tier a at the top to tier b at the bottom.}
Long objects are drawn compact and on a diagonal. Never clip a tip or intrude into a neighboring cell. All 25 items are drawn at the SAME icon size.
The gutters must be entirely clear: no loose particles, sparks, smoke, flying fragments, exterior aura, glow cloud, floor, ground shadow, scenery, background texture or visible grid. Glow, flame, ice, water, lightning and mist stay INSIDE the object or fused to its surface. All small details attach to their main object. Pairs overlap or touch as one compact asset.
Each cell is ONE piece of MONSTER EQUIPMENT: gear worn by a creature on its own body, never a human weapon or human armor. Weapons are pieces such as claw caps, fang caps, stingers, horn caps, beak caps, pincers, hoof shoes, tail blades, tail maces, fin blades or spurs. Armor is a piece such as a beast chest plate, barding, back shell, mantle, muzzle guard, shoulder guard, harness, collar chest piece or monster helm; a monster helm has a long snout guard and ear or horn openings, never a human helmet. Orbs are pieces such as orbs, medallions, crests, bells, lanterns, pendants, amulets or reliquaries that hang from a collar, horn, tail or chest. Every piece shows how it attaches (strap, ring, clasp, cuff, socket). Monster equipment, no handle, no hilt, no human glove/torso: absolutely no crossguard, staff, five-fingered glove or human-shaped torso armor. Show the equipment alone and hollow: no living creature, no head, no face, no eyes, no limbs, no wings; teeth, bone, horn, hide and feathers appear only as worked material. Test: if a person could hold or wear it as drawn, it is wrong.
TIER PROGRESSION: {a escada do § 3 para as faixas desta cartela}. A higher tier is a MORE ELABORATE object, never a bigger one.
VARIETY: the elemental type shows through concept and material, never through one mandatory color; items of the same row must not share a single palette. Follow the materials and colors written for each item. Every item has a distinct silhouette; never recolors of the same object. No laurel wreaths, no rank stars, no medals of rank.
NO TEXT UNDER ANY CIRCUMSTANCES: no letters, numbers, labels, runes, pseudo-writing, logos, signatures, watermarks or inscriptions. Dials have no numerals; covers, plaques, labels and screens stay blank or show only abstract shapes.

Row 1, column 1 ({Tipo}, tier {n}, {weapon|armor|orb}): {o objeto em inglês: material, forma, cores, como prende}.
…
Row 5, column 5 (…): ….
Return only the transparent 25-item parent sheet.
```

## 6. Executar, salvar e recortar

- **Uma geração por cartela.** Refazer só por erro real (quantidade errada, fundo opaco ou xadrez pintado, texto,
  objeto de gente, diagrama desenhado), **do zero**, ajustando o texto. **Nunca editar a imagem.** No máximo 3 imagens
  por cartela; se uma ou duas células ainda falharem, registre quais e siga (viram imagem avulsa depois).
  *(Inferência: mesmo orçamento dos monstros — confirmar com o dono.)*
- Conferir no olho: 25 objetos em 5x5; ordem igual à lista; nenhum texto; fundo sem xadrez; diagrama não desenhado;
  nenhuma peça com cabo, formato de gente ou criatura dentro; faixa alta mais elaborada, não maior.
- **Nomes dos arquivos** (regra geral em [fluxo-sessoes.md](fluxo-sessoes.md)):
  - cartela original, sem edição: `pagina_01_original.png`, `pagina_02_original.png`; o prompt exato ao lado em
    `pagina_NN.prompt.txt`; cada tentativa em `pagina_NN_vK.png` + `.prompt.txt`;
  - recorte de cada item, na pasta da tipagem: **`faixa_NN_<descricao>.png`**, faixa com dois dígitos e descrição curta
    com `_` (ex.: `marinho/faixa_06_astrolabio_de_conchas.png`).
- Por tipagem, guardar também a descrição mínima de cada item e um índice com faixa, página, posição, arquivo e estado
  de aprovação. Nome e classificação ficam nos documentos, nunca na arte.
- **Recorte** (`scripts/recortar_grade.py`): separa os objetos **antes** de enquadrar (senão a janela pega pedaço do vizinho), centraliza em
  **320×320 RGBA sem redimensionar**, margem de referência 16 px (mínimo 8); objeto maior que 304 px em qualquer lado é
  rejeitado. Os pixels mantidos não mudam. A cartela original nunca é editada.
- Quem aprova a arte é o dono. Nunca marque uma cartela como aprovada por ele sem que isso aconteça.

## 7. Casos especiais

### Livro de Habilidade: "Tomo Fechado"

A arte do Livro de Habilidade é uma só e serve a todas as tipagens: o jogo pinta a cor e põe o ícone do elemento por
cima.

- Desenho escolhido: **Tomo Fechado** — livro grosso e fechado, encadernado em couro marrom gasto, cantoneiras de latão
  e um fecho de latão, com o medalhão no centro da capa.
- **Medalhão redondo vazio**, de frente e desobstruído, liso, de latão ou pergaminho, com cerca de 1/4 da largura do
  objeto e nada desenhado dentro (é ali que o jogo sobrepõe o ícone).
- **Paleta neutra:** marrons quentes, creme de pergaminho, latão envelhecido, um pouco de ferro escuro, pedra clara ou
  cristal fumê claro. **Nenhuma cor de elemento dominante** (nada de vermelho-fogo, azul-gelo, verde-veneno,
  amarelo-elétrico), porque o jogo tinge depois.
- Cabe no círculo inscrito da célula (o jogo recorta a arte em círculo) e se lê como "conhecimento a aprender" mesmo a
  48 px.
- Um brilho leve pode ficar **sobre** a borda das páginas ou o lacre, nunca em volta do objeto. Páginas em branco ou só
  com linhas ornamentais abstratas: nada de escrita, runa ou pseudoescrita.
- Sem pessoa, mão, criatura ou mesa: o objeto sozinho, como item de catálogo.

### Itens de campeonato: Roseta plissada

- A **Roseta plissada** é a moldura que o **jogo** desenha em volta do card do item exclusivo de campeonato: dois anéis
  concêntricos de metal e, por dentro, no canto de cima à esquerda, uma roseta de pregas com miolo de estrela cuja fita
  tem 1, 2 ou 3 pontas conforme o circuito. **Ela não vai na arte**: não desenhe moldura, roseta nem fita no objeto.
- O que vai na arte é a identidade da coleção, em todo item:
  - um pequeno **motivo de louro** (coroa, faixa de folhas ou rebites de folha);
  - o **metal do circuito**: **Local = bronze polido com 1 cravo de estrela**; **Regional = prata acetinada com 2**;
    **Mundial = ouro rico com gemas e 3**. O cravo é uma estrelinha simples de cinco pontas, nunca selo de nota;
  - bronze visivelmente mais humilde que prata, e prata que ouro. Fora o metal, as cores seguem o conceito de cada item.
- Os equipamentos de monstro de campeonato seguem todas as regras do § 2.

### Agendas: estilo gadget

A Agenda é o aparelho pessoal do treinador (não é equipamento de monstro; o § 2 não se aplica).

- **Orientação ao Claude (não vai para o prompt):** o estilo lembra os aparelhos de treinador de animes de monstrinhos
  — **o prompt nunca nomeia a franquia nem produto dela**; descreva só a forma abaixo.
- **Só o estilo, nunca o tema:** desenho de brinquedo
  robusto, cascas arredondadas de pílula e cápsula, carcaça em duas cores fortes e saturadas, plástico injetado brilhante
  com poucos acabamentos de metal, botões redondos grandes, direcional, tampa articulada, antena curta, encaixes de chip
  visíveis, tela com moldura grossa; render 3D limpo, luz de estúdio suave, sombreado quase cel, legível em miniatura.
- **Proibido o tema:** nada de esfera vermelha e branca, nenhuma réplica de aparelho de franquia, nenhuma criatura,
  nenhum rosto ou olho no aparelho, nenhum logo ou símbolo. São aparelhos originais do mundo.
- Tela só com formas abstratas coloridas (blocos, pontos, barras, mancha de mapa), nunca interface escrita.
- A quantidade de **encaixes de chip visíveis** bate com o valor do item. Cada item com silhueta, proporção e cores
  próprias (nunca 25 recolorações de um celular).
- Progressão por elaboração: faixa 1 caderno e engenhoca mecânica; 2 portáteis robustos; 3 dobráveis e vestíveis;
  4 celulares de tela inteira; 5 aparelhos inteligentes especializados (pulso, scanner, controle); 6 tablets e aparelhos
  avançados; 7 ligados a outro equipamento, com pequenas projeções; 8 holográficos; 9 núcleos de alta tecnologia
  encantados; 10 os portáteis mais avançados do mundo, com hologramas ricos — sempre de mão ou de mesa, nunca prédio.
- São 2 cartelas (faixas 1–5 e 6–10); a cartela 2 usa a cartela 1 recém-gerada como referência de estilo.
