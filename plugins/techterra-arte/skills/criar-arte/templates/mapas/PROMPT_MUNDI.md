# Sessão de imagem — mapa-múndi {NOME_DO_MUNDI} ({LOTE})

> Modelo da skill `criar-arte` (`templates/mapas/PROMPT_MUNDI.md`), para mundi e mapa-modelo dos lados (o mundi que
> depois é recortado em partes). O Claude copia para `{PASTA_LOTE}/PROMPT_{LOTE}.md`, troca os `{…}` e escreve
> `prompts/mundi_{id}.txt` com o texto fixo do fim. Regras: `{SKILL}/regras/cenarios-mapas-capas.md` §3. Apague esta
> caixa e o "Texto fixo" antes de entregar.

Você **só gera**. O prompt já está escrito. Você anexa, cola, gera, confere, salva e registra. **Não** crie nem altere
prompt, nome ou referência.

## Regras desta sessão

1. **Comece numa conversa nova** (nada de imagem anterior no contexto).
2. **Só texto + no máximo UMA imagem**, a de traço da fila. **Nunca** anexe esquema, diagrama ou rascunho de posições:
   com diagrama o mapa sai distorcido.
3. **Uma geração por imagem.** Nunca edite imagem gerada. Gerar de novo do zero só por erro real: terras grudadas ou
   faltando, texto/legenda/letra na rosa dos ventos, personagem, grade de meridianos moderna. No máximo **3 imagens**
   (`_v2`, `_v3`); depois, pendente.
4. Paisagem **3:2**. Não recorte nem redimensione (o ajuste do Claude nunca recorta).

## FILA

| # | id | prompt | anexo (1 só, traço) | salvar em |
|---|---|---|---|---|
| 1 | mundi_{id} | `prompts/mundi_{id}.txt` | `{SKILL}/referencias/mapas/mundi-mascris-completo.jpg` | `brutos/mundi_{id}.png` |

## ONDE SALVAR (obrigatório)

```
{PASTA_LOTE}\brutos\
```

- Nome: `mundi_{id}.png`; tentativas `mundi_{id}_v2.png`, `_v3` (minúsculas, sem acento, `_`). Nunca sobrescreva.
- Ao lado, o prompt exato: `<arquivo>.png.prompt.txt` (UTF-8 sem BOM).
- A cópia no cache do gerador **não é entrega**: copie para a pasta acima.
- Registro: `{PASTA_LOTE}\validacao\geracoes_mundi.json` (`{"id", "arquivo", "tentativa", "motivo_refacao"}`) e
  `{PASTA_LOTE}\LEIA-ME.txt`.
- **Não** grave dentro da pasta da skill. No fim, responda com a pasta absoluta num bloco de código.

---

## Texto fixo (o Claude usa para escrever `prompts/mundi_<id>.txt`; não vai para a sessão)

```text
Use a imagem anexada só como REFERÊNCIA DE TRAÇO E ESTILO. Copie dela: a técnica (mapa de
pergaminho antigo pintado em aquarela sobre nanquim, contorno fino de tinta marrom-sépia), a vista
(de cima, levemente inclinada, quase ortogonal, com o relevo desenhado em pequenos volumes), o
papel bege envelhecido e manchado, o oceano azul-acinzentado texturizado com linhas de rumo finas
cruzando o quadro, as nuvens brancas volumosas desenhadas POR CIMA do mar cobrindo em parte os
cantos, a moldura dupla dourada com filigrana nos quatro cantos e régua graduada nas bordas, a rosa
dos ventos dourada no canto inferior direito, sem letras, as naus de velas quadradas e os monstros
marinhos à moda antiga. NÃO copie o conteúdo geográfico da referência: as terras são as descritas
abaixo.

Formato paisagem 3:2. Mapa-múndi completo, o oceano preenchendo tudo, moldura desenhada dentro do
próprio quadro.

{Como o mundo se organiza em 1–2 frases: quantas terras, separadas por mar aberto, nenhuma
encostando na outra.}

{Uma terra por item, com a POSIÇÃO e a PROPORÇÃO escritas (ex.: "no centro, cerca de 40% da
largura e 50% da altura"), a silhueta e a paleta próprias, e só os marcos grandes que se leem de
longe — cidade pequena vira ponto:}
1. {posição, proporção} — {terra}: {silhueta, relevo, marco grande, paleta}.
2. …

Ligando as terras, rotas marítimas em linha pontilhada sépia com pequenas naus de velas quadradas
em cima de algumas. Nos vãos de mar vazio, monstros marinhos desenhados à moda antiga (serpente
enrolada, kraken, tartaruga-ilha), em tinta sépia com leve aguada.

Paleta geral: papel bege envelhecido, sépia, azul-acinzentado do oceano, dourado da moldura e da
rosa dos ventos. As cores fortes de cada região aparecem só dentro das próprias terras, como
manchas localizadas de aquarela, sem contaminar o oceano nem a moldura. Litorais contínuos, formas
inteiras, nada borrado nem repetido em padrão; poucas formas grandes bem desenhadas em vez de
muitas miúdas.

Sem personagens, sem legenda, sem tabela, sem grade de meridianos moderna, sem texto, letra ou
número em lugar nenhum (nem na rosa dos ventos nem na régua). Estética de mapa de aventura pintado
à mão, aparência de página de atlas antigo emoldurada.
```
