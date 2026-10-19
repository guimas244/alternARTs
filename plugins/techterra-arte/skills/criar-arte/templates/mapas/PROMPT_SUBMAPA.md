# Sessão de imagem — sub-mapa {NOME_DA_REGIAO} ({LOTE})

> Modelo da skill `criar-arte` (`templates/mapas/PROMPT_SUBMAPA.md`). O Claude copia para
> `{PASTA_LOTE}/PROMPT_{LOTE}.md`, troca os `{…}` e escreve `prompts/mapa_{id}.txt` com o texto fixo do fim. Se o
> mapa também tem fundos de Local, cola a FILA e as regras de `templates/cenarios/PROMPT_FUNDOS.md` na seção
> "Fase 2". Regras: `{SKILL}/regras/cenarios-mapas-capas.md` §2. Apague esta caixa e o "Texto fixo" antes de entregar.

Você **só gera**. Prompts, fila e nomes já estão escritos. Você anexa, cola, gera, confere, salva e registra.
**Não** crie nem altere prompt, fila, nome ou referência. **Faça o mapa inteiro sem parar entre as fases**, até o fim.

## Regras desta sessão

1. **Uma geração por imagem.** Nunca edite imagem gerada. Gerar de novo do zero só por erro real: texto/número/seta/
   bússola na arte, moldura ou borda, criatura ou personagem, lugares que não dá para apontar (grudados ou faltando),
   ponte sobre o mar, geografia que não segue o recorte anexado. No máximo **3 imagens** (`_v2`, `_v3`), depois
   pendente.
2. Paisagem **3:2** (1536×1024). Não recorte nem redimensione: quem ajusta é o Claude (e o ajuste nunca recorta, porque
   os pinos dos Locais vão por cima desta arte depois).
3. No máximo 5 anexos por geração, na ordem da fila.

## Fase 1 — o sub-mapa

| # | id | prompt | anexos (ordem) | salvar em |
|---|---|---|---|---|
| 1 | mapa_{id} | `prompts/mapa_{id}.txt` | 1. `{SKILL}/referencias/mapas/submapa-kaiangue.jpg` · 2. `{SKILL}/referencias/mapas/{submapa-aita ou submapa-ossario}.jpg` (se a fila pedir) · 3. `{PASTA_LOTE}/referencias/mundi_recorte_{id}.jpg` | `brutos/mapa/mapa_{id}.png` |

Conferir antes de seguir: os {N} lugares aparecem separados e apontáveis; as trilhas estão pintadas; nada escrito,
sem moldura; a geografia lembra o recorte; nenhuma ponte sobre o mar.

## Fase 2 — fundos dos Locais deste mapa (se houver)

{colar aqui a FILA, as regras e a tabela de correção de PROMPT_FUNDOS.md}

## ONDE SALVAR (obrigatório)

```
{PASTA_LOTE}\brutos\mapa\     (o sub-mapa)
{PASTA_LOTE}\brutos\          (os fundos dos Locais, se houver)
```

- Nomes: os da fila, **minúsculas, sem acento, `_` entre palavras**, tentativas `_v2`, `_v3`. Nunca sobrescreva.
- Ao lado de cada imagem, o prompt exato: `<arquivo>.png.prompt.txt` (UTF-8 sem BOM).
- A cópia no cache do gerador **não é entrega**: copie para a pasta acima.
- Registro: `{PASTA_LOTE}\validacao\geracoes_mapa.json` (`{"id", "arquivo", "tentativa", "motivo_refacao"}`) e
  `{PASTA_LOTE}\LEIA-ME.txt` com o que ficou pendente.
- **Não** grave dentro da pasta da skill. No fim, responda com a pasta absoluta num bloco de código.

---

## Texto fixo (o Claude usa para escrever `prompts/mapa_<id>.txt`; não vai para a sessão)

Frase dos anexos (primeira linha do prompt):

```text
Use as imagens anexadas só como referência de estilo, câmera e contorno. O conteúdo é o do texto.
O trecho de mapa anexado é pintado como pergaminho de atlas: copie dele só a geografia (contorno,
relevo, bioma), nunca esse traço; o traço é o das imagens de sub-mapa.
```

Molde (mude só o `{}`):

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

Acréscimo por tipo de Região (uma linha, antes de "Trilhas…"; texto completo em regras §2):

- reino: `A capital é uma cidade grande e reconhecível, e o palácio é o maior edifício do quadro, num ponto de destaque; a arquitetura inteira nasce de {elemento}: {materiais}.`
- bastião: `A fortaleza com farol e portão ocupa um lado do quadro, encostada num trecho de muralha que cruza a imagem: pedra clara, altíssima, ameias, torres pequenas a intervalos regulares, sem trecho caído. Dentro do muro, a vila de guarnição; fora, {a terra de fora / o mar aberto}.`
- porto: `Cidade portuária em volta de uma baía, colada na muralha, com o grande arco de mar, cais dos dois lados, estaleiros e muitas naus. Nenhuma ponte sobre o mar.`
