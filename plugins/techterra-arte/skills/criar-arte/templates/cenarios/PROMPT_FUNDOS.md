# Sessão de imagem — fundos de {LOTE}

> Modelo da skill `criar-arte` (`templates/cenarios/PROMPT_FUNDOS.md`). O Claude copia para
> `{PASTA_LOTE}/PROMPT_{LOTE}.md`, troca os `{…}`, preenche a FILA e escreve cada `prompts/<id>.txt` com o texto fixo
> do fim deste modelo. Por que cada regra existe: `{SKILL}/regras/cenarios-mapas-capas.md` §1 (fundo de Local) e §4
> (portão). Apague esta caixa e o "Texto fixo" do fim antes de entregar à sessão de imagem.

Você **só gera**. Os prompts, a fila e os nomes já foram escritos e validados pelo Claude. Você anexa, cola, gera,
confere, salva onde está mandado e registra. **Não** crie nem altere prompt, fila, nome ou referência.

## Regras desta sessão

1. Gere a fila **inteira, em ordem, sem parar** entre os itens. Item que já tem imagem em `brutos/`: pule.
2. Cole o prompt **exatamente** como está no arquivo da fila. Anexe só o que a fila manda, na ordem.
3. **Uma geração por imagem.** Nunca edite imagem gerada (nada de inpaint, "corrija isto", variação de imagem).
4. Gerar de novo, do zero, **só por erro real**: vista de cima/isométrica, texto ou letra na arte, pessoa/criatura/bicho
   em primeiro ou meio plano, escura demais (noite que virou preto), moldura/borda, marco fora do terço central,
   portão fora do lugar (conferido com grade de 10%). No máximo **3 imagens** por item (`<id>.png`, `<id>_v2.png`,
   `<id>_v3.png`); a única edição de texto permitida é acrescentar no fim do prompt a frase da tabela abaixo, salvando
   o prompt usado ao lado (`<id>_v2.png.prompt.txt`). Esgotou: anote como pendente e siga.
5. Paisagem **16:9** sempre (nunca quadrado, nunca retrato).

| Voltou assim | Frase de correção (acrescentar no fim) |
|---|---|
| vista de cima, cara de mapa | "Câmera a um metro e setenta do chão, olhando reto para o horizonte." |
| escura demais | "Hora: crepúsculo claro; a fonte de luz tem um halo largo que ilumina a névoa." |
| marco num canto | "O marco fica no centro exato do quadro, entre os dois lados." |
| chão cheio no meio | "Todos os objetos ficam nas laterais, fora do centro." |
| apareceu texto | "Placas em branco, lombadas lisas sem título, estandartes lisos." |

## FILA

| # | id | tipo | prompt | anexo (1 só) | salvar em |
|---|---|---|---|---|---|
| 1 | {id_1} | local | `prompts/{id_1}.txt` | `{SKILL}/referencias/cenarios/{referencia}.jpg` | `brutos/{id_1}.png` |
| 2 | {id_2} | lados | `prompts/{id_2}.txt` | `{SKILL}/referencias/cenarios/{referencia}.jpg` | `brutos/{id_2}.png` |
| 3 | {id_3} | portao | `prompts/{id_3}.txt` | (sem anexo: o texto é autossuficiente) | `brutos/portao/{id_3}.png` |

Locais que **reaproveitam** fundo não entram na fila (estão no plano como "usa o fundo de <Local>").

## ONDE SALVAR (obrigatório)

Todas as imagens desta sessão vão para esta pasta, e nenhuma outra:

```
{PASTA_LOTE}\brutos\          (fundos de Local e dos lados)
{PASTA_LOTE}\brutos\portao\   (portões da Jornada, se houver)
```

- Nome: o `id` da fila, **minúsculas, sem acento, `_` entre palavras**; tentativas `_v2`, `_v3` (ex.:
  `03_praca_central.png`, `03_praca_central_v2.png`). Nunca sobrescreva uma imagem.
- Ao lado de cada imagem, o prompt exato usado: `<arquivo>.png.prompt.txt` (UTF-8 sem BOM).
- A cópia no cache do gerador **não é entrega**: copie sempre para a pasta acima.
- Registro: `{PASTA_LOTE}\validacao\geracoes_fundos.json` — lista `{"id", "arquivo", "tentativa", "motivo_refacao"}`;
  e `{PASTA_LOTE}\LEIA-ME.txt` com o que ficou pendente e por quê.
- **Não** grave dentro da pasta da skill. **Não** redimensione nem recorte: quem normaliza é o Claude, depois.
- No fim, responda com a pasta absoluta num bloco de código.

---

## Texto fixo (o Claude usa para escrever `prompts/<id>.txt`; não vai para a sessão)

### Fundo de Local (Narraris, Jornada, expansões) — abertura e fechamento fixos, mude só o `{}`

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

### Fundo dos lados (TechTerra/Mascris) — mesmas regras, traço anime

```text
Use a imagem anexada só como referência de traço, luz, cor e câmera. Gere uma paisagem nova do
zero; o lugar, a paleta e o conteúdo são os do texto.
Paisagem pintada em estilo anime, com o mesmo traço, luz e cor da imagem de referência de fundo
anexada. Câmera na altura dos olhos de uma pessoa em pé. {O lugar em 2 frases, com o marco — ou,
no fundo de bioma, só o trecho de paisagem, sem marco único}. Horizonte no terço de cima. Chão
aberto, plano e calmo no centro e na metade de baixo; o detalhe fica nas laterais e no fundo. A
silhueta que identifica o lugar fica no terço central. Luz {do momento}, exposição média: nada
muito escuro. Nenhuma pessoa, animal ou criatura. Sem texto, placa legível, moldura, borda ou
marca d'água. Formato paisagem 16:9.
```

### Portão da Jornada — planta fixa (tema novo = troque só material, luz e paleta)

```text
Pintura digital detalhada em vista frontal ao nível do olho, câmera levemente de baixo para cima,
formato paisagem 1600 por 900 pixels, de {o lugar da bifurcação} vista por alguém parado no centro
dela: ao fundo, {a parede ou o fundo}, onde se abrem DOIS portões idênticos em tamanho e forma,
simétricos, lado a lado — o portão da esquerda com o centro a 28% da largura da imagem e o da
direita com o centro a 72%, cada um ocupando cerca de um quinto da largura, com a base apoiada a
80% da altura e o topo do arco a 32% da altura; cada portão é {o arco e as folhas}, fechado, com
uma luz {cor} vazando pelas frestas e pela soleira, desenhando um leque de luz no chão à frente de
cada um; entre os dois portões, no centro exato da composição, {o pilar ou marco}, dividindo em
dois {o caminho} que vem do primeiro plano e se bifurca, um ramo para cada portão; acima de cada
portão, ocupando a faixa de 6% a 28% da altura, {a parede ou o céu} é liso, escuro e calmo, sem
entalhe, tocha ou detalhe forte; no primeiro plano, a faixa inferior central do chão (de 86% a
100% da altura) é lisa, escura e calma; iluminação {de onde vem, clima}, paleta de {4 a 6 cores,
por nome}; a imagem preenche o quadro inteiro, sem moldura, sem borda e sem vinheta, traço de
pintura sem contorno preto. É absolutamente proibido incluir na imagem qualquer texto, letra,
palavra, número, runa legível, inscrição, placa, título, marca d'água, assinatura, ícone, seta,
bússola, moldura decorativa, elemento de interface de jogo, personagem, criatura ou figura humana.
```
