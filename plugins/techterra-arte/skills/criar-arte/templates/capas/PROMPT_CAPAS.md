# Sessão de imagem — capas {LOTE}

> Modelo da skill `criar-arte` (`templates/capas/PROMPT_CAPAS.md`). O assistente copia para
> `{PASTA_LOTE}/PROMPT_{LOTE}.md`, troca os `{…}`, escolhe o parágrafo "O que é cada cena" do tipo (expedição, raid ou
> cartaz de evento), lista as 4 cenas de cada cartela e, se houver, a moldura de invasão. Regras:
> `{SKILL}/regras/cenarios-mapas-capas.md` §5. Apague esta caixa e os parágrafos de tipo que não se aplicam.

Siga este roteiro nesta conversa ou numa nova (ChatGPT ou Codex, com ferramenta de imagem). Se esta mesma conversa
preparou o lote, a partir daqui ela está na etapa de geração.

Você **só gera**. As cenas, a fila e os nomes já estão escritos. Você anexa, cola, gera, confere, salva e registra.
**Não** crie nem altere cena, prompt, fila, nome ou referência. **Não recorte** as cartelas: o recorte vem depois da
geração, com o script de conversão. Anexo que a ferramenta de imagem não alcança: mostre ao usuário a lista, na ordem,
e peça para ele anexar as imagens na conversa. Imagem gerada que o ambiente de código não enxerga: peça ao usuário para
baixá-la e reenviá-la por upload, e salve no caminho mandado.

## Regras desta sessão

1. Uma geração por cartela = **BLOCO FIXO + a lista de UMA cartela**. Todas as cartelas, em ordem, sem parar.
2. **Uma geração por imagem.** Nunca edite imagem gerada. Gerar de novo do zero só por erro real: a cruz branca
   faltando ou atravessada (nuvem, luz ou névoa cruzando a faixa), cena que não é retrato, texto/letra/logo, criatura
   ou pessoa em destaque, rosto, cena repetida. No máximo **3 imagens** por cartela (`_v2`, `_v3`); depois, pendente.
3. Anexos de estilo (as artes do jogo que o usuário forneceu), em toda geração, na ordem:
   1. `{PASTA_LOTE}/referencias/{estilo_1}.png` · 2. `{PASTA_LOTE}/referencias/{estilo_2}.png` · 3. (opcional) `{PASTA_LOTE}/referencias/{estilo_3}.png`

## BLOCO FIXO (vai em toda geração de cartela)

```text
Use as imagens anexadas só como referência de ESTILO: copie delas o traço, o acabamento e a paleta
viva; não copie o conteúdo. Gere do zero uma imagem nova.

Gere UMA imagem em RETRATO 3:4 (1536 × 2048), dividida numa grade de 2 colunas × 2 fileiras:
quatro cenas independentes, cada uma também em RETRATO 3:4 (mais alta que larga).

Separação (obrigatório): uma faixa BRANCA LISA, reta, de 40 pixels, separa as cenas na vertical e
na horizontal (uma cruz branca no meio da imagem). Nada atravessa a faixa: nem nuvem, nem luz, nem
névoa, nem galho. Cada cena termina de forma seca na faixa. Sem moldura, sem borda externa, sem
cantos arredondados.

{O QUE É CADA CENA — um dos três parágrafos abaixo}

Proibido em todas as cenas: texto, letras, números, logotipos, assinaturas, marcas-d'água,
interface, ícones, molduras; pessoas ou criaturas em destaque (no máximo silhuetas minúsculas e
distantes; multidão só como manchas de cor sem rosto); rostos; cena repetida ou parecida com a
vizinha.

Estilo (igual em todas): o das artes anexadas — ilustração de fantasia estilizada, pintada, de
formas simples e bem desenhadas, cores vivas e saturadas, luz marcada. Não é foto nem render 3D
realista. Mesmo traço, mesmo nível de detalhe e mesmo enquadramento em todas, para parecerem da
mesma coleção.

Ordem das cenas na grade: 1 = cima-esquerda, 2 = cima-direita, 3 = baixo-esquerda, 4 = baixo-direita.
```

### O que é cada cena — expedição

```text
O que é cada cena: a capa em retrato de uma expedição, que aparece pequena num cartão do jogo e
tem que ser lida de relance, em miniatura: UM elemento-símbolo forte no centro que diz o tema
sozinho, ocupando cerca de metade da cena; o cenário em volta simples e em poucos planos, sem
miudeza que vire ruído; uma trilha que leva até o símbolo e um acampamento ou bandeirola pequeno;
silhueta clara e contraste alto entre o símbolo e o fundo; uma cor dominante por cena, para as
capas se distinguirem lado a lado só pela cor; composição VERTICAL e centrada (o símbolo no meio,
céu ou teto em cima, a trilha subindo de baixo): o cartão recorta pelo centro, então nada
importante encosta nas bordas.
```

### O que é cada cena — raid (arena do chefe)

```text
O que é cada cena: a ARENA onde um chefe é enfrentado, no mesmo lugar e na mesma paleta da lista,
só que no coração do lugar e em clima de ameaça: no centro, um espaço de batalha aberto e vazio
(clareira, plataforma, cratera, salão), visto de frente, como um palco, ocupando cerca de metade da
cena; o cenário fecha em volta como um anfiteatro; luz mais dura e céu mais carregado, marcas de
combate antigo (chão rachado, pilares quebrados, arranhões enormes); NENHUMA criatura na cena (o
chefe é desenhado por cima depois); palco no centro e contraste alto, lido de relance em miniatura.
```

### O que é cada cena — cartaz de evento (campeonato, evento global, invasão)

```text
O que é cada cena: o cartaz de um TIPO de evento, que aparece pequeno num cartão do jogo: UM
elemento forte no centro que diz o evento sozinho, ocupando cerca de metade da cena; cenário simples
em poucos planos; contraste alto; composição VERTICAL e centrada, com o palco no meio e nada
importante encostando nas bordas. Campeonatos se distinguem pela escala e pelo metal (Local bronze,
Regional prata, Mundial ouro).
```

## CARTELAS

### Cartela {NNN}

```text
1. {Nome} — {a cena em 1–2 frases, com o símbolo central}; {cor dominante, por nome}.
2. {Nome} — …
3. {Nome} — …
4. {Nome} — …
```

## MOLDURA DE INVASÃO (se houver — geração separada, sem o BLOCO FIXO)

Anexos, na ordem: 1. `{SKILL}/referencias/capas/template_monstros_invasao.png` (só ENCAIXE: onde fica a arte e onde
fica vazio; não estilo nem tamanho) · 2–3. as mesmas artes de estilo acima.

```text
A primeira imagem anexada serve só como referência de ENCAIXE (onde fica a arte e onde fica
vazio), não de estilo nem de tamanho; as outras são referência de estilo. Gere do zero UMA imagem
em paisagem 16:9 (1672 × 941) com fundo totalmente transparente (PNG com canal alfa). Se não for
possível gerar transparência, use um fundo liso verde puro, sem degradê, sem sombra projetada e sem
nenhum verde na arte.
O que desenhar: {enfeites pequenos e simbólicos do tema}, soltos, em dois grupos: um encostado na
borda esquerda e outro na borda direita, como no encaixe anexado; o meio da imagem fica vazio de
cima a baixo. A imagem é cortada ao meio e cada metade é usada separada: nada cruza o centro, e os
dois lados não precisam ser espelhados. Os grupos se concentram nos cantos (embaixo, peças apoiadas
numa base imaginária; em cima, peças leves), o meio de cada lateral quase vazio; bem menos massa que
o encaixe anexado: enfeite de canto, não moldura cheia; elementos soltos e pequenos, com respiro;
tudo inteiro dentro do quadro.
Recorte limpo: contorno nítido em todos os elementos, sem névoa, fumaça, aura, brilho espalhado ou
partículas soltas em volta (luz só dentro dos objetos). Sem chão, sem sombra, sem moldura, sem
texto, sem números. Estilo: o das artes de estilo anexadas; paleta: {cores do tema, por nome}.
```

## ONDE SALVAR (obrigatório)

```
{PASTA_LOTE}\cartelas\     (cartelas)
{PASTA_LOTE}\brutos\       (moldura)
```

- Cartelas: `cartela_{NNN}_original.png`; tentativas `cartela_{NNN}_v2.png`, `_v3` (minúsculas, sem acento, `_`,
  número com 3 dígitos). Moldura: `brutos/moldura_{tema}.png`. Nunca sobrescreva.
- Ao lado de cada imagem, o texto exato enviado: `<arquivo>.png.prompt.txt` (UTF-8 sem BOM).
- A cópia no cache do gerador **não é entrega**: copie para as pastas acima.
- Registro: `{PASTA_LOTE}\validacao\geracoes_capas.json` (`{"cartela", "arquivo", "tentativa", "motivo_refacao"}`) e
  `{PASTA_LOTE}\LEIA-ME.txt` com o que faltou ou saiu diferente (inclusive a medida que o gerador entregou).
- **Não** grave dentro da pasta da skill e **não** recorte. No fim, responda com a pasta absoluta num bloco de código.
