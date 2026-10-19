# Cenários, mapas, capas e ícones de mapa

Regras de composição de tudo o que é paisagem ou cena: fundo de batalha, sub-mapa, mapa-múndi, portão da Jornada,
capa, moldura de invasão e ícone de mapa. Tamanhos finais em [formatos.md](formatos.md); anexos em
[REFERENCIAS.md](../referencias/REFERENCIAS.md).

## Regras comuns

- **Nunca editar imagem gerada** (nada de inpaint, image-to-image, "corrija isto"). Saiu errada: gere de novo do zero,
  com o texto ajustado. **Uma geração por imagem**; refazer do zero só por erro real (medida reprovada, vista de cima,
  texto, criatura na cena, encaixe/posição fora do lugar), no máximo 3 imagens; depois, anote como pendente e siga
  (regra geral em [fluxo-sessoes.md](fluxo-sessoes.md)). As medidas citadas abaixo são conferidas por script
  (`scripts/fundos_normalizar.py` e `scripts/capas_converter.py`); o que a medida não vê, confira no olho.
- **Nada escrito:** sem texto, letra, número, placa legível, lombada com título, runa legível, ícone, seta, bússola,
  moldura, borda, vinheta ou marca d'água (salvo onde a regra abaixo pede moldura de propósito, como no mundi). O que
  mais puxa texto é livro, placa e estandarte: **nomeie o suporte liso** ("lombadas lisas sem título", "placas em
  branco", "estandartes lisos").
- **Paleta por nome de cor, nunca código hex.**
- Arte refeita é arquivo novo (nome novo); nunca sobrescreva a anterior.

## 1. Fundo de Local (fundo de batalha)

**Estilo:** pintura em estilo **anime**, câmera **na altura do olho** de uma pessoa em pé — nunca vista de cima,
isométrica ou mapa.

### Como a batalha mostra o fundo, e o que isso exige

A tela de batalha pinta a imagem do Local atrás da arena, com **`cover`**, véu escuro e vinheta. Cada regra do prompt
existe por causa de uma linha desta tabela:

| Como a tela faz | O que a arte precisa ter |
|---|---|
| `cover`: **recorta** para caber, nunca estica | paisagem **16:9**; o que importa longe das bordas |
| foco vertical em 45% no computador e 32% no celular | **horizonte no terço de cima** |
| no celular em pé sobra só ~30% da largura, o miolo | **o marco que identifica o lugar fica no terço central** |
| lutadores à esquerda e à direita, "VS" no meio, 5 cards de ação embaixo | **chão aberto e calmo no centro e na metade de baixo**; o detalhe mora nas laterais e no fundo |
| véu escuro de 34–62% no computador e 74–90% no celular, mais vinheta | **exposição média**: noite tem de ser noite *clara* |
| os monstros são desenhados por cima | **nenhuma pessoa, criatura ou animal** no primeiro ou no meio plano |
| a arte vai direto na tela, sem legenda | nada escrito, sem moldura, sem borda, sem tarja |

**Por que a luminância tem piso:** uma arte com média 40 some debaixo do véu. Artes de mapa escuras mediam 31–48; as que
funcionam ficam entre 103 e 145.

- Medidas que reprovam: **luminância média fora de 70–200**; desvio-padrão do terço central abaixo de 25 (centro
  chapado, sem silhueta); moldura; imagem não opaca ou em retrato.
- Saída: recorte 16:9 **pelo centro** permitido, depois reduz para **1672×941 JPG** (fundos dos lados: 1536×864).
- **Arte isométrica ou vista de cima lê mal como fundo** ("um mapa atrás da batalha"): reprova.

### Referência e frase obrigatória

Anexe **uma** referência de `referencias/cenarios/` (a que mais combina com o Local) e escreva junto:

> *"Use a imagem anexada só como referência de traço, luz, cor e câmera. Gere uma paisagem nova do zero; o lugar, a
> paleta e o conteúdo são os do texto."*

- **Nunca anexe** a arte do mapa (vista de cima: contamina a câmera) nem arte de monstro (põe criatura na cena).
- O **traço** vem da referência; a **paleta e a luz** vêm do texto do lugar. Mapa noturno, submerso ou de lava mantém o
  clima, com exposição média.

### Molde do prompt (abertura e fechamento fixos; mude só o `{}`)

```text
Use a imagem anexada só como referência de traço, luz, cor e câmera. Gere uma paisagem nova do
zero; o lugar, a paleta e o conteúdo são os do texto.
Paisagem de fantasia pintada, com o mesmo traço da referência. Câmera na altura dos olhos de uma
pessoa em pé, olhando reto para o horizonte: nunca vista de cima, nunca isométrica, nunca mapa.
Este lugar fica em {nome do mapa}, {identidade do mapa em 1 frase}.
O lugar: {descrição do Local em 2 frases, sem regra de jogo}.
Ao fundo, no terço central do quadro, recortado com clareza: {o marco do Local}.
Primeiro plano, só nas laterais: {o que emoldura}.
Centro e metade de baixo: chão aberto, plano e calmo de {material}, largo o bastante para
duas criaturas se enfrentarem.
Horizonte no terço de cima. Luz: {fonte, direção, hora}. Paleta: {4 a 6 cores, por nome}.
Exposição média: mesmo nas sombras as formas continuam legíveis, sem manchas de preto chapado.
Nenhuma pessoa, criatura ou animal. Sem texto, letra, número, placa legível, ícone, moldura,
borda, vinheta ou marca d'água. O cenário sangra até os quatro cantos. Formato paisagem 16:9.
```

Variante dos lados de TechTerra/Mascris (mesmas regras, traço anime): *"Paisagem pintada em estilo anime, com o mesmo
traço, luz e cor da imagem de referência de fundo anexada. Câmera na altura dos olhos de uma pessoa em pé. {O lugar
em 2 frases, com o marco — ou, no fundo de bioma, só o trecho de paisagem, sem marco único}. Horizonte no terço de cima.
Chão aberto, plano e calmo no centro e na metade de baixo; o detalhe fica nas laterais e no fundo. A silhueta que
identifica o lugar fica no terço central. Luz {do momento}, exposição média: nada muito escuro. Nenhuma pessoa, animal ou
criatura. Sem texto, placa legível, moldura, borda ou marca d'água. Formato paisagem 16:9."*

### O que costuma voltar errado

| Voltou assim | Troque no prompt |
|---|---|
| vista de cima, cara de mapa | "câmera a um metro e setenta do chão, olhando reto para o horizonte" |
| escura demais (< 70) | a hora vira "crepúsculo claro"; a fonte de luz ganha "halo largo que ilumina a névoa" |
| marco num canto | "no centro exato do quadro, entre os dois lados" antes do marco |
| chão cheio no meio | mande os objetos para "as laterais, fora do centro" |
| apareceu texto | nomeie o suporte liso |

**Conferir no olho** (a medida não vê): câmera na altura do olho; horizonte no terço de cima; cobrindo as laterais com a
mão, o que sobra ainda diz qual é o lugar; chão do centro aberto; nenhuma letra ou glifo; nenhum bicho ou pessoa em
primeiro ou meio plano (silhueta minúscula e distante no céu só se o texto pedir).

### Fundo próprio × reaproveitado

Fundo não é um por Local: o mapa ganha um conjunto pequeno, e Locais parecidos dividem a mesma imagem.

- **Fundo exclusivo (gerado para o Local):** a(s) cidade(s), o Local final, e os Locais de marco único (palácio,
  fortaleza, portão, cais, veio raro). Esses **nunca** são reaproveitados em outro lugar.
- **Fundo de bioma, compartilhado:** Locais genéricos do mesmo bioma e da mesma luz usam a mesma imagem, **2 a 4 Locais
  por fundo**.
- **Locais vizinhos nunca dividem fundo** (o jogador passaria de um para o outro sem ver mudança).
- **Teto:** fundos novos ≤ **metade** dos Locais do mapa. É teto, não meta.
- **Entre mapas, só como plano B** (o normal é o fundo do mesmo mapa): um fundo de bioma só serve a outro mapa quando tudo isto for verdade: mesmo bioma e mesmo clima
  (pinhal com neve não serve para pinhal de verão); mesma luz; nenhum marco que só existe no mapa de origem (vulcão,
  muralha, árvore colossal, cidade reconhecível); no máximo 3 mapas por fundo, de preferência longe um do outro.
- Na lista de fundos do lote, cada Local diz: "próprio" ou "usa o fundo de <Local>".

## 2. Sub-mapa de Região

- **Vista aérea oblíqua, alta, quase fotográfica**, luz de dia natural, cores vivas, no traço de
  `referencias/mapas/submapa-*.jpg` (kaiangue = principal; aita = natureza com cidade grande; ossario = bioma que ocupa o
  quadro todo, sem mar).
- Anexe também **o recorte do mapa-múndi em volta do ponto** da Região: recorte-o de
  `referencias/mapas/mundi-mascris-completo.jpg` (sem script: recorte com um editor de
  imagem e salve na pasta de trabalho, nunca na skill). Ele dá bioma, relevo e contorno. O recorte é pintado como pergaminho de atlas: **o sub-mapa copia só a geografia, nunca esse traço**.
  Frase junto: *"Use as imagens anexadas só como referência de estilo, câmera e contorno. O conteúdo é o do texto."*
- **Os pinos dos Locais vão por cima da arte**, depois. Por isso a arte precisa de **N lugares distintos, bem separados e
  fáceis de apontar**, cada um com UM marco visual e uma posição no quadro (deixe folga para pinos sem encostar uns nos
  outros nem na borda).
- **Trilhas, estradas, escadarias e pontes sobre rios pintadas** ligando os lugares (as conexões do mapa seguem o que
  está pintado). O lugar mais perigoso no ponto mais alto e mais distante do quadro.
- Paisagem **3:2**, sai **1536×1024**. **Só redimensionar, nunca recortar**: o recorte desloca os pinos.
- A execução faz **o mapa inteiro sem parar entre fases** (fundos, sub-mapa, conferência), até o fim.
- **Nenhuma ponte sobre o mar** (ponte sobre rio pode). **A muralha**, quando aparece, é sempre a mesma: pedra clara,
  altíssima, ameias, torres pequenas a intervalos regulares, sem trecho caído.

```text
Vista aérea oblíqua, alta, de {bioma}, pintura digital detalhada e quase fotográfica, luz de
dia natural, cores vivas, no mesmo estilo das imagens de referência de sub-mapa anexadas.
A terra segue o trecho de mapa anexado: {contorno e relevo do recorte}.
{Conceito em 2 frases}.
{N} lugares distintos, bem separados uns dos outros e fáceis de apontar:
  {lista, cada lugar com UM marco visual e a sua posição no quadro}
Trilhas, estradas, escadarias e pontes sobre rios ligando: {pares}.
O lugar mais perigoso no ponto mais alto e mais distante do quadro.
A pintura ocupa o quadro inteiro, até os quatro cantos: sem moldura, sem borda, sem vinheta.
Formato paisagem 3:2 (1536×1024). Sem texto, número, placa, ícone, seta, bússola, legenda,
interface, personagem, criatura ou marca d'água.
```

Acréscimos por tipo de Região: **reino** — a capital é grande e reconhecível e o palácio é o maior edifício, em destaque
(é o centro do reino, não o lugar mais perigoso); a arquitetura nasce do elemento (fogo: pedra negra, forjas, telhados
vermelhos; água: canais, terraços, cascatas; gelo: torres de gelo azul; terra: cidade escavada na rocha; vento: templos
em ilhas flutuantes). **Bastião** — a fortaleza com farol e portão ocupa um lado, encostada num trecho de muralha que
cruza a imagem; dentro, a vila de guarnição; fora, a terra de fora ou o mar aberto. **Porto** — cidade em volta de uma
baía, colada na muralha, com o grande arco de mar, cais dos dois lados, estaleiros e naus.

## 3. Mapa-múndi (padrão de traço)

O traço aprovado de mundi (ver `referencias/mapas/mundi-mascris-completo.jpg`):

- mapa de **pergaminho antigo pintado em aquarela sobre nanquim**, contorno fino de tinta marrom-sépia;
- vista de cima, levemente inclinada, quase ortogonal, relevo em pequenos volumes;
- papel bege envelhecido e manchado; oceano azul-acinzentado texturizado, com linhas de rumo finas cruzando o quadro;
- nuvens brancas volumosas **por cima** do mar, cobrindo em parte os cantos;
- moldura dupla dourada com filigrana nos quatro cantos e régua graduada nas bordas; rosa dos ventos dourada no canto
  inferior direito, **sem letras**;
- naus de velas quadradas e rotas em linha pontilhada sépia; monstros marinhos à moda antiga (serpente, kraken,
  tartaruga-ilha) em tinta sépia nos vãos de mar;
- as cores fortes de cada região aparecem **só dentro das próprias terras**, como manchas de aquarela, sem contaminar o
  mar nem a moldura;
- terras separadas e reconhecíveis de longe, cada uma com silhueta e paleta próprias; litorais contínuos, formas inteiras,
  nada borrado ou repetido em padrão; **poucas formas grandes bem desenhadas** em vez de muitas miúdas; cidade pequena
  vira ponto, só marco grande se lê;
- sem personagem, legenda, tabela, grade de meridianos moderna ou bloco de texto. Paisagem 3:2.

### Mapa-modelo (o mundi que depois é recortado em partes)

- Sai **só de texto**: as rodadas com diagrama ou esquema anexado saíram **distorcidas**; a aprovada veio do prompt sem
  diagrama.
- Anexo: no máximo **uma** imagem, só como referência de **traço**. Nunca o esquema de posições (esse é só para o dono
  conferir).
- Posições e proporções vão escritas (ex.: "no centro, cerca de 40% da largura e 50% da altura").
- Começar numa conversa nova; nova tentativa = `_v2`, `_v3`, nunca sobrescrever.

## 4. Portões da Jornada

A tela de escolha usa **uma imagem com dois portões** como fundo; o jogo escreve por cima o nome da próxima sala e a
dificuldade. Todos os temas seguem a mesma composição, porque a posição da interface é fixa.

| Item | Valor | Por quê |
|---|---|---|
| Medida | **exatamente 1600×900** (16:9), JPG | a interface é posicionada em % sobre a arte. Outro tamanho: **redimensione, nunca recorte** |
| Câmera | frontal, na altura do olho de quem está parado na bifurcação, levemente de baixo para cima | o jogador "está" na encruzilhada |
| Portão esquerdo | centro em **x≈28%**, base em **y≈80%**, topo do arco em **y≈32%**, largura **≈22%** | ali a interface desenha o hover e o selo de chefe |
| Portão direito | espelho: centro em **x≈72%** | idem |
| **Faixa livre de cima** | **y 6–28%** acima de cada portão: parede ou céu **escuro, liso e calmo** | nome da sala e barra de dificuldade |
| **Faixa livre de baixo** | **y 86–100%, x 30–70%**: chão calmo | pontos, trilha e botão de desistir |
| Centro | **x 42–58%**: um pilar ou marco dividindo o caminho | separa as duas escolhas |
| Os dois portões | **idênticos em tamanho e forma**, fechados, luz vazando pelas frestas | a diferença entre eles é da interface, nunca da arte |
| Proibido | texto, letra, número, runa legível, placa, ícone, seta, moldura, interface, personagem em primeiro plano, marca d'água | a interface escreve por cima |

- O prompt descreve as posições **em porcentagem da imagem**, uma a uma (portões, pilar, faixas lisas), e termina com
  "a imagem preenche o quadro inteiro, sem moldura, sem borda e sem vinheta, traço de pintura sem contorno preto" + a
  lista de proibidos.
- Tema novo (gelo, templo celeste, pântano…) = repetir a mesma planta trocando só material e luz.
- **Conferir** com uma grade de 10% por cima: portões e as três faixas no lugar. Portão fora do lugar = gerar de novo.

## 5. Capas de evento, expedição e raid

- Cartela **1536×2048 em retrato**, grade **2 colunas × 2 linhas**: quatro cenas independentes, cada uma também em
  **retrato 3:4**. Ordem: 1 = cima-esquerda, 2 = cima-direita, 3 = baixo-esquerda, 4 = baixo-direita.
- **Faixa branca lisa e reta de 40 pixels** separa as cenas na vertical e na horizontal (uma cruz branca). Nada
  atravessa a faixa (nem nuvem, luz, névoa ou galho); cada cena termina seca nela. Sem moldura, borda externa ou canto
  arredondado. É pela faixa que se recorta cada cena.
- **Estilo:** anexe 2 ou 3 artes do próprio jogo (cartas de monstro ou capas já usadas) só como referência de traço,
  acabamento e paleta viva. Essas artes **o usuário fornece** (ainda não há referência fixa de capa na skill); sem
  elas, peça antes de gerar. Ilustração de fantasia estilizada, pintada, formas simples, cores saturadas, luz marcada; nem
  foto nem render 3D. Mesmo traço, detalhe e enquadramento em todas, para parecerem da mesma coleção.
- **O cartão do jogo recorta 146×188 pelo centro:** composição **vertical e centrada**, **palco no meio**, nada
  importante encostando nas bordas. Sai **510×680**.

O que é cada cena:

- **Expedição:** UM elemento-símbolo forte no centro que diz a tipagem sozinho (o vulcão, a geleira, o relógio colossal),
  ocupando ~metade da cena; cenário simples em poucos planos, sem miudeza que vire ruído; uma trilha subindo até o
  símbolo e um acampamento ou bandeirola pequeno; contraste alto; **uma cor dominante por cena**, para as capas se
  distinguirem lado a lado só pela cor.
- **Raid (arena do chefe):** o mesmo lugar e a mesma paleta, no coração do lugar e em clima de ameaça: no centro, um
  **espaço de batalha aberto e vazio** visto de frente, como palco (~metade da cena); o cenário fecha em volta como
  anfiteatro; luz mais dura, céu mais carregado, marcas de combate antigo. **Nenhuma criatura**: o chefe é desenhado por
  cima depois.
- **Cartaz de evento** (campeonato, evento global, invasão): mesmo bloco, sem a exigência de trilha e acampamento; uma
  cena por tipo de evento. Campeonatos pela escala e pelo metal (Local bronze, Regional prata, Mundial ouro).
- **Proibido em todas:** texto, letra, número, logo, assinatura, interface, ícone, moldura; pessoa ou criatura em
  destaque (no máximo silhuetas minúsculas e distantes; multidão só como manchas de cor sem rosto); rosto; cena repetida
  ou parecida com a vizinha.

### Moldura de invasão (fica por cima do mapa)

- Paisagem **16:9 (1672×941)**, **fundo totalmente transparente**. Se o gerador não der transparência: fundo liso verde
  puro `#00FF00`, sem degradê nem sombra, e nenhum verde na arte.
- Anexe `referencias/capas/template_monstros_invasao.png` **só como referência de encaixe** (onde fica a arte e onde fica
  vazio), não de estilo nem de tamanho. **O template anexado é o controle**: o gerador não obedece porcentagem, então
  os números abaixo servem **só para conferir** o resultado, não como instrução no prompt.
- **A arte ocupa só as laterais:** no máximo os 22% da esquerda e os 22% da direita. **Os 56% do meio ficam 100% vazios**,
  de cima a baixo (é ali que o mapa aparece).
- A imagem é cortada ao meio e cada metade é usada separada: **nada cruza o centro**; os dois lados não precisam ser
  espelhados (melhor diferentes).
- Enfeite de canto, não moldura cheia: concentrar nos cantos (embaixo, peças apoiadas numa base imaginária; em cima,
  peças leves), o meio de cada lateral quase vazio; **menos de 15% da imagem coberta**; nenhum elemento passa de 18% da
  altura; tudo inteiro dentro do quadro.
- Recorte limpo: contorno nítido, **nenhuma névoa, fumaça, aura, brilho espalhado ou partícula solta** em volta (luz só
  dentro dos objetos); sem chão, sombra, moldura, texto ou número.
- Estilo: o mesmo das capas (anexar as mesmas artes do jogo, fornecidas pelo usuário).

## 6. Ícones de mapa

- **Medalhão circular pintado**, vista aérea em 3/4, pintura digital detalhada, cores vivas e saturadas, luz de dia; o
  **cenário preenche todo o círculo**; **borda branca fina** em volta do círculo; fora dele, nada (transparente).
- Anexe as quatro referências `referencias/icones/` (castelo, vila, cachoeira, portal_magico), com a frase: *"Use as
  imagens anexadas só como referência de estilo, traço, luz e borda. O conteúdo é o do texto. Gere do zero uma imagem
  nova."*
- **Cartela 4x4:** 1254×1254, fundo totalmente transparente (alfa de verdade; xadrez pintado ou fundo branco reprova),
  **16 medalhões do mesmo diâmetro** (cerca de 270 pixels), centralizados na célula, com **espaço vazio transparente entre
  eles**: o recorte separa por região conectada, e círculos que se tocam pela sombra viram um só. Sem sombra, brilho ou
  moldura saindo do círculo; sem grade ou linha desenhada.
- Liste os 16 na ordem "(linha L, coluna C) {cenário em 1 frase, com o marco}". **Um único tema claro por círculo**, com
  a silhueta principal no centro: tem de ser reconhecível pequeno.
- Nenhum texto, letra, número, legenda, placa legível, personagem, pessoa, animal, criatura ou marca d'água.
- Recorte com máscara circular para **300×300 RGBA**; no jogo aparece a 80×80.
- Conferir: 16 medalhões do mesmo tamanho, 4 linhas × 4 colunas, separados, sem texto.
