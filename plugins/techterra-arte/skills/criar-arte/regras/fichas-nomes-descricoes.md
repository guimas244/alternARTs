Como escrever a ficha de cada monstro (campos, nome e descrição de jogo), para qualquer lote de monstros ou fusões.

# Fichas, nomes e descrições

A ficha é escrita pelo Claude, nunca pela IA de imagem. Dela saem o texto do prompt (campos visuais) e o texto do jogo
(`nome` e `descricao`). Regras próprias de fusão, evolução e variação estão em [fusoes.md](fusoes.md); de humanoide, em
[humanoides.md](humanoides.md); o que nunca pode aparecer, em [restricoes.md](restricoes.md).

## Antes de escrever

- **Leia e tipe pela arte.** Quando a ficha parte de uma imagem que já existe (original de variação, pais de fusão,
  antecessor de evolução), olhe a imagem e o nome antes de qualquer coisa. Exemplo real: o "bico laranja" era um nariz
  de cenoura — ficha escrita sem olhar sai errada.
- **Tipagem sai da arte**, dentro do repertório do lugar ou do lote.
- **Leia as fichas que já existem** no lote (e nos lotes anteriores que o usuário indicar). Agentes que escrevem em
  paralelo repetem raízes e ideias (já saíram cinco "pipas" e cinco "sinos" numa leva). Por isso: cada um lê as partes
  dos outros desde o início, e um revisor cruzado confere tudo no fim.
- **Escolha o temperamento de cada ficha antes de escrever** (cotas abaixo).

## Campos comuns

| Campo | Regra |
|---|---|
| `nome` | ver "Nomes" abaixo |
| `tipo1`, `tipo2` | sempre dois tipos, diferentes entre si. O tipo 1 dá conceito e anatomia; o tipo 2 muda material, cor e comportamento. Sem segundo sinal na arte → tipo 2 `normal` |
| `humanoide` | true/false. Humanoide = proporção humana (cabeça, tronco, 2 braços, 2 pernas, ereto). Ver [humanoides.md](humanoides.md) |
| `classe` | só se humanoide: classe livre (mago, ferreira, rei caído, carteiro…) |
| `paleta` | `[cor escura do corpo, cor clara de acento]`, nascidas da **mistura dos dois tipos** (planta não precisa ser verde; misturas impensáveis são o objetivo) |
| `anatomia` | uma frase do corpo, na escala do tier (escada de poder abaixo). Inclui a postura ("de pé, ereto", "corpo longo e baixo", "pairando") |
| `rosto` | formato, número, posição e cor dos olhos + expressão ligada ao temperamento |
| `marcas_poder` | lista de traços concretos de ameaça, na quantidade do tier (tabela abaixo) |
| `brilho` | a **única** parte que emite luz, com a cor (olhos OU outra parte; halo curto). Nada mais brilha |
| `temperamento` | 2–3 palavras, seguindo as cotas |
| `conceito` | 2 frases: o que a criatura É e o que FAZ no mundo |
| `marca_da_habilidade` | 1 frase com o poder que a criatura vai explorar |
| `descricao` | texto de jogo — ver "Descrição" abaixo |
| `visual` | descrição física **só para a arte** (postura, silhueta, material, 2 cores, rosto, brilho, marcas de poder). Nunca vai para o jogo |

Tipos válidos (30): agua, alien, desconhecido, deus, docrates, dragao, eletrico, fantasma, fera, fogo, gelo, inseto,
luz, magico, marinho, mistico, normal, nostalgico, pedra, planta, psiquico, subterraneo, tecnologia, tempo, terrestre,
trevas, venenoso, vento, voador, zumbi. (`terra`, `metal` e `neutro` não servem.)

### Paleta, rosto e escada de poder

- Conferências de **paleta** e de **rosto**: [estilo.md](estilo.md) (seções Cores e Rosto e olhos).
- **Escada de poder e quantidade de `marcas_poder` por tier:** [estilo.md](estilo.md) (seção Escada de poder).
  O tier diz a **ameaça**, nunca o tamanho. **Fusão: +1 marca.**
- T1–4 podem ser fofos, tímidos, curiosos; nos T1–6, no máximo 6 com expressão brava por pacote.

## Nomes

- **Inventados, em português, sonoros**, de preferência uma palavra, evocando a ideia ou o domínio da criatura.
- **Sem número** e até 60 caracteres.
- **Únicos**: compare (sem acento, minúsculo) com a lista de nomes que já existem no jogo, em
  `dados/nomes_existentes.json` desta skill, e com todos os nomes do próprio lote.
- **Sem raiz repetida**: não reaproveite raiz de nome de outro pacote ou de outra parte do lote (já saíram fichas
  "gêmeas" com Toxi-, Sutur-, Brasi-, Drac-, -númen…).
- Nada de nome de personagem, filme, jogo ou franquia.

## Descrição (`descricao`)

Texto que o jogador lê. **~440 caracteres, 4 a 6 frases**, com:

1. **tamanho concreto, por comparação** ("alto como um poste", "cabe numa cumbuca", "comprido como um ônibus");
2. **temperamento**;
3. **do que gosta**;
4. **do que não gosta**;
5. **o que faz nas folgas**.

### Sem físico

Nunca aparência: cor, material, pele, olhos, forma, roupa, armadura. *Por quê: a arte já mostra o físico; o texto dá
caráter.* O físico vai no `visual`.

### Tamanho vem da lore

- O tamanho é decidido pela história da criatura, **nunca pelo tier**: um T1 pode ser enorme, um T10 do tamanho de uma
  fada. Deus ou ser mítico pode ter tamanho humano.
- Distribua no pacote: pessoa ou menor / médio / grande / colossal. **Colossal é raro (até ~15%).** Sem cota de tamanho
  por tier.
- Nunca "maior que o pai" (nem que o antecessor).
- O porte tem que ficar claro na frase: quem cadastra classifica o tamanho por essa comparação.

### Proibido no texto

- **Algarismos** (escreva por extenso).
- As palavras **tier, nível, patamar, fusão, sacrifício, mítico, variação, variante** e **Pritz** (a moeda é Cripto;
  ver [restricoes.md](restricoes.md)).
- **Sistemas do jogo** (Jornada, expedição, raid, missão, rituais, passe, ranking, loja, moeda…). A criatura vive o
  mundo, não o sistema.
- **Superlativo de recorde** ("a maior estrutura viva do mundo", "o mais antigo de todos"). *Por quê: crava um fato que
  o próximo lote contradiz.*
- **Nome de monstro**: nem o próprio, nem pais, original ou antecessor, **nem palavra comum que também é nome de
  monstro** (Pedra, Final, Destino, Presente, Chamado, Moita, Ruínas, Casa, Cama…). A lista completa está em
  `dados/nomes_existentes.json`: antes de fechar, procure cada palavra com inicial maiúscula e cada substantivo comum
  suspeito nela, e troque o que bater.
- Nome de obra, personagem ou ator.

### Forma e abertura

- **Não abrir com "Mede".** Varie a abertura: temperamento, hábito, uma cena, o nome (no máximo 1/4 do pacote abre com
  o próprio nome). O tamanho pode vir em qualquer frase.
- Gostos, desgostos e folgas **concretos e da criatura** (comida, clima, som, lugar, mania), não lição de moral.
- Clichês proibidos: "É X e protege…", "Detesta poder usado para…", "Nas folgas, acompanha a recuperação…", "Nas
  folgas, visita lugares onde…", "Nas folgas, procura sinais de…", "Gosta de regiões onde…", "Gosta de encontros em
  que…", "é paciente e espera", "é conquistador e enfrenta rivais".

### Sem molde

- Duas descrições quaisquer do lote (e das anteriores que você tiver) com semelhança **difflib < 0,5** (texto sem acento
  e minúsculo).
- Um mesmo trecho de **5 palavras** em **mais de 8** descrições = molde → reescreva.
- **A frase de tamanho vira molde** entre partes paralelas ("tem a altura de um…") — revise isso no fim, de propósito.
- Gosto ou hábito parecido em 2 criaturas é aceito; o mesmo texto ou o mesmo esqueleto de frase, não.

## Temperamento — cotas

Por pacote de 32 (proporcional em pacote menor), um por criatura, escolhido antes de escrever:

| Grupo | Exemplos | Quantidade |
|---|---|---|
| Solitários, reclusos, territoriais | eremita, ranzinza, desconfiado, some quando visto | **≥ 8** |
| Predadores, hostis, cruéis, rancorosos | caçador frio, sádico, vingativo, guloso, provocador | **≥ 6** |
| Indiferentes, excêntricos, obsessivos, preguiçosos | colecionador, maníaco por ordem, dorminhoco, vaidoso | **≥ 6** |
| Curiosos, brincalhões, tímidos, medrosos | xereta, pregador de peças, assustadiço | ≥ 4 |
| Sociáveis, protetores, gregários | cuida de filhotes, vive em bando, guarda um lugar | **≤ 6** |

- Vocabulário de convívio (comunidade, aldeia, vizinhos, visitantes, viajantes, abrigo, proteger, ajudar, confiança…)
  **só** nos sociáveis. *Por quê: antes da regra, quase um terço das descrições tinha "comunidade" e "proteger".*
- Tier alto não é automaticamente "divindade protetora": pode ser tirano, indiferente, faminto, vaidoso, entediado.
- Na linha evolutiva, o temperamento amadurece ou se deforma, mas continua reconhecível.

## Conferência final da parte

- Contagens (por tier, por cartela), nomes únicos, tipos válidos, cotas de paleta, rosto e marcas.
- Descrições: tamanho, sem físico, sem palavra proibida, sem nome de monstro, abertura, semelhança, trechos repetidos,
  cotas de temperamento.
- Só libere a fila de imagens depois da revisão cruzada das fichas.
