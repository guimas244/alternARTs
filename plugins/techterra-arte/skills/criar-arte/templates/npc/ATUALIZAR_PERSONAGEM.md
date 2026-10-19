# Atualizar personagem que já existe (jogador ou NPC com arte)

Regra: [../../regras/npc-personagens.md](../../regras/npc-personagens.md) §11. Aqui **a arte atual é a referência**:
o preâmbulo de beleza **não** entra e a pessoa **não** é embelezada. É o único uso do modo antigo ("pele real, sem
filtro de beleza").

## Antes de escrever

1. O usuário fornece o `rosto.png` e o `corpo.png` **atuais** de cada pessoa (a skill não tem acervo) e diz, em uma
   frase, o que muda ("envelhece para 30 anos", "cabelo curto", "troca a roupa para uniforme de soldado", "usa esta
   foto como novo rosto"). Copie-os para `<lote>/artes/<slug_do_nome>_rosto.png` e `_corpo.png`.
2. Olhe as duas imagens e escreva o **DNA do rosto** em inglês, uma vez (formato do rosto, pele, olhos com cor e forma,
   sobrancelhas, nariz, boca, cabelo, barba, idade aparente). Ele é **copiado sem mudar** em toda geração dessa pessoa.
3. Escolha **2 âncoras**: marcas visíveis com LADO que já estão na arte (pinta, piercing, brinco, tatuagem, mecha — e,
   se a arte atual tiver, cicatriz: aqui não se tira nada que a pessoa já tem).
4. Anote se a ficha da pessoa diz **físico extremamente avançado** e se ela tem **menos de 18 anos**.

## Anexos (máximo 5)

| # | Arquivo | No prompt |
|---|---|---|
| 1 | `artes/<slug>_rosto.png` (rosto atual) | Reference 1 |
| 2 | `artes/<slug>_corpo.png` (corpo atual) | Reference 2 |
| 3 | `referencias/estilo_pagina_1.png` | Reference 3 (só layout) |
| 4 | `referencias/prisions.png` | Reference 4 |

Uma pessoa por geração (rosto + corpo atuais ocupam 2 vagas). As outras colunas ficam totalmente transparentes.

## Onde fica cada coisa no lote

- Prompt: `prompts/atualizar_NNN.txt` (escrito à mão a partir do bloco abaixo; `NNN` = número da página).
- Imagem: `paginas/pagina_NNN.png` → o `npc_recortar.py` recorta igual a uma página nova (colunas vazias são puladas).
- Roster: a página entra com `"tipo": "atualizar"`, `"anexos": [os 4 caminhos acima, relativos ao lote]` e a pessoa
  com `"coluna"`. O `npc_montar_prompts.py --gravar` não valida o texto dessa página (é escrito à mão), mas a põe na
  `fila.json` com o prompt `prompts/atualizar_NNN.txt` e esses anexos; o recortador usa o roster para a `fichas.json`.

## O prompt (troque os marcadores; apague as linhas entre colchetes que não se aplicam)

```text
Update ONE existing TechTerra character. Reference 1 is the character's CURRENT face and Reference 2 the CURRENT full body: this is the SAME PERSON and must stay clearly recognizable. Reference 3 is ONLY a layout/technique reference, do not copy its people. Reference 4 defines the small capture devices called prisions.

CHANGE (the ONLY thing that changes): <PEDIDO, em inglês, uma frase>

KEEP everything else exactly as in References 1 and 2: face shape, eye color and shape, eyebrows, nose, mouth, skin tone, hair color and style, beard, marks, piercings, tattoos, clothing and physique. Do not beautify, do not change identity, ethnicity or apparent age unless the change asks for it.
FACE DNA (identical in every generation of this person): <DNA DO ROSTO>
ANCHORS (stay on the same side in both views): <MARCA 1 com LEFT/RIGHT>; <MARCA 2 com LEFT/RIGHT>.
[AGE CHANGE: it is the SAME person at another age: keep face shape, eyes, nose, mouth, marks and tattoos; change only the signs of age (skin, wrinkles, grey hair, posture, body).]
[EXTREMELY ADVANCED PHYSIQUE: peak-human elite athlete body, dense and defined musculature, broad powerful frame, visible even through the clothes; natural, no bodybuilder exaggeration.]
[UNDER 18: fully clothed and modest, natural pose, nothing sensual; same idea of an elite young athlete if the physique line applies.]

Photoreal studio photography, 85mm lens, real skin texture, no illustration, no painting, no 3D or CGI look. Soft key light 45 degrees from left, gentle fill, cool rim light. Truly transparent alpha background: no floor, scenery, ground shadow, checkerboard, gradient, text, letters, numerals, logos, borders or dividers. No monsters, animals or creatures.

LAYOUT: one 1254 x 1254 sheet with three equal columns; this person in column <1|2|3>, the other columns completely transparent. Top third: front-facing head-and-shoulders bust looking at camera, eyes around 42% of this third, straight horizontal crop at the bottom of the bust. Bottom two thirds: the SAME person with identical face, hair, marks and clothing, standing full length, front-facing (slight 3/4 allowed), head near 5% and both feet fully visible near 95% of this area. Bust artwork ends at y=380; rows y=381 to y=420 completely transparent across the ENTIRE sheet; full-body hair starts at y=440 or lower; bust hair starts below y=15. No element may cross x=418 or x=836. Nothing cut off: hair, hands, coat tails, shoes.

WORLD RULES: humans have NO magic. No auras, runes, glowing tattoos, glowing eyes, glowing jewelry or spell effects; no mage robes. No cybernetics unless the change asks for it. Prisions are palm-sized translucent faceted crystal capture capsules inside ornate brass or steel cages with tiny gems, with a luminous vortex around a dark core inside. ONLY the prisions glow. LEFT/RIGHT always means the person's own anatomical side.

Output one 1254 x 1254 PNG with real RGBA alpha.
```

## Conferir

- É **a mesma pessoa** das imagens anexadas (o esperado é "claramente a mesma pessoa", não um clone).
- Mudou só o que foi pedido; as âncoras estão do lado certo nas duas vistas.
- Fundo transparente; pés visíveis; nada brilha além das prisions.
- Refação: no máximo 1, só por erro grave (não saiu a pessoa, fundo todo opaco, nudez). Ficou diferente demais? Anote
  para o dono em vez de gerar de novo.

## Refação fiel de alguém do lote (não é "atualizar")

Mesma pessoa de uma página já gerada, de novo: fica no fluxo normal (`npc_montar_prompts.py`), com a página levando
`"rosto_ref": {"coluna": N, "arquivo": "referencias/rosto_<slug>.png", "dna": "<DNA do rosto em inglês>"}`. O tile do
rosto aprovado vira o 5º anexo e a página ganha a linha `Column N: same person as reference image 5. Face DNA: …`.
As outras colunas pegam os próximos pendentes do lote (regra §11). O script aceita **uma** refação com tile por página
(4 anexos fixos + 1 = limite de 5); para juntar 2–3 refações numa grade, monte à mão uma folha única com os tiles
(regras/fluxo-sessoes.md, "Limite de anexos") e ajuste a frase.
