# Sessão de imagem — ícones de mapa {LOTE}

> Modelo da skill `criar-arte` (`templates/icones/PROMPT_ICONES.md`). O Claude copia para
> `{PASTA_LOTE}/PROMPT_{LOTE}.md`, troca os `{…}` e escreve `prompts/cartela_NNN.txt` = texto fixo + a lista dos 16
> da cartela. Regras: `{SKILL}/regras/cenarios-mapas-capas.md` §6. Apague esta caixa antes de entregar.

Você **só gera**. Os prompts, a fila e os nomes já estão escritos. Você anexa, cola, gera, confere, salva e registra.
**Não** crie nem altere prompt, fila, nome ou referência. **Não recorte**: quem recorta é o Claude.

## Regras desta sessão

1. **Uma cartela por geração**, todas em ordem, sem parar.
2. **Uma geração por imagem.** Nunca edite imagem gerada. Gerar de novo do zero só por erro real: fundo sem
   transparência de verdade (xadrez pintado ou branco), não saíram 16 medalhões em 4×4, medalhões encostando (pela
   sombra também), texto/letra, criatura/pessoa/bicho. No máximo **3 imagens** (`_v2`, `_v3`); depois, pendente.
3. Anexos, em toda geração, nesta ordem: 1. `{SKILL}/referencias/icones/castelo.png` · 2. `{SKILL}/referencias/icones/vila.png` ·
   3. `{SKILL}/referencias/icones/cachoeira.png` · 4. `{SKILL}/referencias/icones/portal_magico.png`
4. Conferir: 16 medalhões do mesmo tamanho, 4 linhas × 4 colunas, separados por espaço transparente, sem texto.

## FILA

| # | prompt | salvar em |
|---|---|---|
| 1 | `prompts/cartela_{NNN}.txt` | `cartelas/cartela_{NNN}_original.png` |

## ONDE SALVAR (obrigatório)

```
{PASTA_LOTE}\cartelas\
```

- Nome: `cartela_{NNN}_original.png`; tentativas `cartela_{NNN}_v2.png`, `_v3` (minúsculas, sem acento, `_`, 3 dígitos).
  Nunca sobrescreva. **PNG com canal alfa** (nunca JPG).
- Ao lado, o prompt exato: `<arquivo>.png.prompt.txt` (UTF-8 sem BOM).
- A cópia no cache do gerador **não é entrega**: copie para a pasta acima.
- Registro: `{PASTA_LOTE}\validacao\geracoes_icones.json` (`{"cartela", "arquivo", "tentativa", "motivo_refacao"}`) e
  `{PASTA_LOTE}\LEIA-ME.txt`.
- **Não** grave dentro da pasta da skill. No fim, responda com a pasta absoluta num bloco de código.

---

## Texto fixo de cada `prompts/cartela_<NNN>.txt` (troque só a lista)

```text
Use as imagens anexadas só como referência de estilo, traço, luz e borda. O conteúdo é o do texto. Gere do zero uma imagem nova.
Uma cartela quadrada de 1254x1254 pixels com FUNDO TOTALMENTE TRANSPARENTE (PNG com canal alpha), contendo exatamente 16 ícones de mapa de jogo organizados numa grade de 4 linhas por 4 colunas.
Cada ícone é um medalhão circular pintado, no mesmo estilo dos ícones anexados: vista aérea em 3/4, pintura digital detalhada, cores vivas e saturadas, luz de dia, o cenário preenchendo todo o círculo, com uma borda branca fina ao redor do círculo.
Todos os 16 círculos têm exatamente o mesmo diâmetro (cerca de 270 pixels), ficam centralizados cada um na sua célula da grade e têm espaço vazio e transparente entre eles: nenhum círculo encosta em outro, e não há sombra, brilho ou moldura saindo do círculo.
Fora dos círculos não há nada: sem fundo, sem cor, sem textura, sem grade desenhada, sem linhas separadoras.
Os 16 ícones, na ordem da esquerda para a direita e de cima para baixo:
1. (linha 1, coluna 1) {cenário em 1 frase, com o marco}.
2. (linha 1, coluna 2) {…}.
3. (linha 1, coluna 3) {…}.
4. (linha 1, coluna 4) {…}.
5. (linha 2, coluna 1) {…}.
6. (linha 2, coluna 2) {…}.
7. (linha 2, coluna 3) {…}.
8. (linha 2, coluna 4) {…}.
9. (linha 3, coluna 1) {…}.
10. (linha 3, coluna 2) {…}.
11. (linha 3, coluna 3) {…}.
12. (linha 3, coluna 4) {…}.
13. (linha 4, coluna 1) {…}.
14. (linha 4, coluna 2) {…}.
15. (linha 4, coluna 3) {…}.
16. (linha 4, coluna 4) {…}.
Cada cenário deve ser reconhecível de imediato mesmo em tamanho pequeno: um único tema claro por círculo, com a silhueta principal no centro.
Nenhum texto, letra, número, legenda, placa legível, personagem, pessoa, animal, criatura ou marca d'água em nenhum ícone.
```
