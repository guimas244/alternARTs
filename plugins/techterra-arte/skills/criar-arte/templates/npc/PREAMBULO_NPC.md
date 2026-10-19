# Preâmbulo NPC (template de máquina)

Fonte que o `scripts/npc_montar_prompts.py` lê para montar cada `prompts/pagina_NNN.txt`. A regra (o que cada bloco
exige, por quê, e o que troca por tema) está em [../../regras/npc-personagens.md](../../regras/npc-personagens.md) §3–§4;
este arquivo só guarda o texto. **Não edite os blocos** sem o dono aprovar: o preâmbulo vai sem mudar uma vírgula.

Cada página = **preâmbulo** + linha em branco + **cabeçalho da página** + as 3 linhas `Coluna N: <visual>`.

- `[TEMA-TRAÇO]` e `[TEMA-MODA]` vêm do `tema.json` do lote (`traco`, `moda`), em inglês.
- `[TEMA-CURTO]` (cabeçalho, em português) vem de `tema.json` → `traco_curto`.
- `{NNN}` = número da página com 3 dígitos.
- `tema.json` com `"tirar_snow": true` tira "snow" da lista de proibidos do fundo (tema sem neve; regra §4).

## Preâmbulo (inglês, igual em toda página)

```text preambulo
Create ONE square PNG character sheet for TechTerra: exactly THREE different adult humans in three equal columns. Reference 1 is ONLY a layout/technique reference, do not copy its people. Reference 2 defines the small capture devices called prisions. References 3 and 4 define the TARGET LEVEL OF BEAUTY AND FINISH ONLY: do not copy their faces, hair or clothes.

BEAUTY (the main goal of this sheet): every person is strikingly beautiful or handsome, like a top fashion model on a magazine editorial cover. [TEMA-TRAÇO] Each of the three is a DIFFERENT sub-type with a different face shape, hair color and style, never the same face repeated. Harmonious, symmetrical, photogenic faces; flawless even skin with only a fine natural texture (never plastic, never airbrushed wax); salon-quality glossy hair; well-done makeup matching the described style; healthy bright smile when smiling; elegant confident posture. Forbidden on faces: scars, broken or crooked noses, crooked or missing teeth, eye bags, deep wrinkles, blemishes, acne, windburn or sunburn, red cold noses, dirty or greasy hair, awkward grimaces, unflattering angles, tired, cold or sick look. Bodies are fit and well proportioned. Charisma: each expression must feel alive and inviting, as described.

WOMEN (very important): every woman is clearly FEMININE, sweet and sensual in an elegant, tasteful way. Soft delicate facial features, full soft lips, long lashes, big expressive eyes with a warm, deep, captivating gaze that connects with the viewer; gentle, tender or playful expression, never stern, hard, tough or tomboyish. Graceful feminine body language (relaxed shoulders, soft hands, slight hip or head tilt), feminine silhouette with a defined waist, long flowing or beautifully styled hair, soft glamorous makeup. Their clothes are feminine and flattering: fitted waists, dresses, skirts, soft knits, off-shoulder or elegant necklines as described. Never give a woman a masculine face, masculine build, mannish stance or boxy menswear unless described. Men are handsome and masculine with a warm, charming look.

EYES: render each iris EXACTLY in the color described, vivid and saturated, clearly visible from the bust view (ice blue, silver, violet, amber and other fantasy colors are natural iris colors in this world). It is ONLY iris pigment: no glow, no light emission, no glowing pupils, no special effects. Heterochromia only when described, on the described side.

FASHION: [TEMA-MODA] Adults may show shoulders, arms, legs through a skirt slit or an elegant fashion neckline when described; sensual but classy, like a luxury fashion campaign; never nudity, lingerie, see-through fabric or vulgar poses. No armor, no horned helmets and no weapons unless described.

Photoreal fashion studio photography, 85mm lens, no illustration, no painting, no 3D or CGI look. Soft beauty key light 45 degrees from left, gentle fill, cool rim light. Truly transparent alpha background: no floor, snow, scenery, ground shadow, checkerboard, gradient, text, letters, numerals, logos, borders or dividers. No monsters, animals or creatures.

LAYOUT: each column = one person. Top third: front-facing head-and-shoulders bust looking at camera, eyes around 42% of this third, straight horizontal crop at the bottom of the bust. Bottom two thirds: the SAME person with identical face, hair, makeup, marks and clothing, standing full length, front-facing (slight 3/4 allowed), head near 5% and both feet fully visible near 95% of this area. Bust artwork ends at y=380; rows y=381 to y=420 completely transparent across the ENTIRE sheet; full-body hair starts at y=440 or lower; bust hair starts below y=15. No element may cross x=418 or x=836 on the 1254 px canvas; keep clear transparent margins between columns. Nothing cut off: hair, hands, coat tails, shoes. Long dresses and coats stop above the shoes so both shoes stay visible.

WORLD RULES: humans have NO magic. No auras, runes, glowing tattoos, glowing eyes, glowing jewelry or spell effects; no mage robes. No cybernetics. Prisions are palm-sized translucent faceted crystal capture capsules inside ornate brass or steel cages with tiny gems, with a luminous vortex around a dark core inside; each person carries them exactly as described. ONLY the prisions glow. LEFT/RIGHT always means the person's own anatomical side; every small style mark (beauty spot, piercing, earring, ring, fine tattoo, colored streak) stays on the described side in both views and never glows.

Output one 1254 x 1254 PNG with real RGBA alpha.
```

## Cabeçalho da página (português)

```text cabecalho
Página {NNN} (3 personagens, todos adultos e muito bonitos, [TEMA-CURTO], beleza de top model, cada um de um subtipo diferente; as mulheres meigas, femininas e sensuais, de olhar expressivo). Nenhum monstro, animal ou criatura na imagem, só as pessoas. Nenhum texto, letra ou número escrito:
```

## Exemplo aprovado — Nórdicos e Eslavos (`variante: "tema"`)

É o `tema.json` que reproduz o Lote 09 (aprovado em 09/10/2026) letra por letra:

```json
{
  "lote": "nordicos_eslavos",
  "titulo": "Nórdicos e Eslavos",
  "variante": "tema",
  "traco": "All three have clearly NORDIC or SLAVIC features (Scandinavian, Finnish, Icelandic, Baltic, Russian, Ukrainian, Polish, Czech, Balkan looks): high sculpted cheekbones, defined jawline, straight refined nose, almond or slightly deep-set eyes, strong elegant brows, fair to light skin with cool, rosy or golden undertones.",
  "moda": "contemporary northern high fashion exactly as described: Scandinavian minimalism, modern Slavic folk embroidery, winter tailoring, knitwear, shearling, wool and leather, with real fabrics, tailoring and accessories, ready for a fashion editorial. Not historical costume, not Viking cosplay, not peasant clothing.",
  "traco_curto": "traço nórdico e eslavo"
}
```

Para outro povo ou região, escreva os dois trechos no mesmo molde (regra §4): `traco` = "All three have clearly
<POVO> features (<povos de referência>): <traços do rosto>, <pele e subtom>."; `moda` = "contemporary <tema> high
fashion exactly as described: <estilos>, with real fabrics, tailoring and accessories, ready for a fashion editorial.
Not <o que não pode virar>.". Lore e linha da pessoa nunca citam país da Terra (só o `subtipo`).

## Variante multiétnica (`variante: "multietnico"`)

Para lote em que cada página mistura etnias (cada pessoa com o traço do próprio `subtipo`). O script usa os dois
textos abaixo quando o `tema.json` não traz `traco`/`moda`; `traco_curto` padrão: "cada um de uma etnia diferente,
com o traço da própria etnia". Cuidado com o molde de etnia (regra §10): pele clara + loira + olho claro repetido em
lote que não é nórdico.

```text multietnico-traco
The three come from DIFFERENT ethnic backgrounds, each exactly as named in its column (the sub-type): render the authentic, flattering features of that background (face shape, eye shape, nose, lips, skin tone and undertone, hair texture) with editorial beauty; never lighten, westernize or blend them into one generic face.
```

```text multietnico-moda
contemporary high fashion exactly as described, in the style named for each person, with real fabrics, tailoring and accessories, ready for a fashion editorial. Not historical costume, not cosplay, not peasant clothing.
```
