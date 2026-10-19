# -*- coding: utf-8 -*-
"""Monta TUDO o que a geração de imagem precisa, a partir das fichas escritas pelo assistente (ver CONTRATO-INTERNO.md).

    python preparar_fila.py <lote>                          # ensaio: só mostra o que faria
    python preparar_fila.py <lote> --gravar                 # integra as partes validadas, escreve prompts e a fila
    python preparar_fila.py <lote> --gravar --partes A,B    # só as partes já ENTREGUES
    python preparar_fila.py <lote> --gravar --conserto 3,5  # cartela já gerada: refaz só os prompts das AVULSAS dela

Para cada parte validada em fichas_claude/parte_<L>.json (com parte_<L>_validacao.json sem erros):
1. integra as fichas em monstros.json (substitui a mesma célula, se já existir), no formato do cadastrador;
2. escreve prompts/cartela_NNN.txt — o texto FINAL (cabeçalho de templates/ + blocos da cartela), pronto para colar;
3. escreve prompts/avulsa_NNN_LxCy.txt (+ referencias/avulsas/cartela_NNN_LxCy_pais.png, o quadrante da prancha:
   pais, original, antecessor externo ou figura de referência da homenagem);
   células N/L com fidelidade "homenagem" ganham o bloco HOMAGE CELLS e a marca HOMAGE na linha (nunca o nome da figura);
4. atualiza fila.json (cartela só entra quando as 4 fichas dela existem) e escreve PROMPT_<LOTE>.md.

Cartela que já tem cartelas/cartela_NNN_original.png não é reescrita (só as avulsas dela, com --conserto).
Anexos: no máximo 5 por geração, caminhos relativos ao lote. Nada é gravado dentro da skill.
"""
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402
from comum import MAX_ANEXOS, ONDE, TIPOS  # noqa: E402

USO = ("uso: python preparar_fila.py <pasta_do_lote> [--gravar] [--partes A,B] [--conserto 3,5]\n"
       "     sem --gravar = ensaio (não grava nada)")

ORDEM = "NVFLXA"
LEVA = {"N": "novos", "V": "variacoes", "F": "fusoes_de_fusoes", "L": "prodigios", "X": "crossover", "A": "apice"}
ROTULO = {"N": "NEW CREATURES", "V": "REGIONAL VARIANTS", "F": "FUSIONS OF FUSIONS", "L": "PRODIGIES",
          "X": "CROSSOVER FUSIONS", "A": "APEX MYTHIC FUSIONS"}
NOME_PT = {"N": "Novos", "V": "Variações", "F": "Fusões de fusões", "L": "Prodígios", "X": "Crossover (base + sacrifício)",
           "A": "Ápice (base + sacrifício de míticos)"}
PRECISA_PRANCHA = set("VFXA")

# referências da skill copiadas para <lote>/referencias/ (nome no lote, caminho na skill)
REFS = {"estilo": ("referencia-estilo.png", "monstros/referencia-estilo.png"),
        "variedade": ("referencia-variedade.png", "monstros/referencia-variedade.png"),
        "guia": ("guia_enquadramento_2x2.png", "guias/guia_enquadramento_2x2.png"),
        "humanoides": ("referencia-humanoides.png", "monstros/referencia-humanoides.png")}

# ---------------------------------------------------------------- textos do prompt (inglês; o gerador lê melhor)
GRADE = ("Square image, genuine transparent alpha background. EXACTLY 4 separate creatures in an INVISIBLE 2-column by "
         "2-row grid, precise row-major order, each creature centered in its own square cell.")
LAYOUT = ("LAYOUT — follow the attached layout diagram exactly. The image is FOUR SEPARATE STICKERS on one transparent sheet, "
          "not one group scene. Each creature lives ONLY inside the gray square of its corner in the diagram: its whole body, "
          "wings, tail, weapon, hair, ribbons, aura and particles fit inside that gray square. The striped pink cross in the "
          "middle of the diagram is a forbidden gutter: nothing is ever drawn there, so the four creatures never come near each "
          "other. The creatures do NOT gather toward the middle of the image: each one leans toward its OWN outer corner; the "
          "empty space between a creature and the middle of the image is always LARGER than the space between it and the outer "
          "edge. Tall or upright creatures (humanoids, standing beasts, towers) are the most common mistake: draw them smaller "
          "so the top of the head AND the feet both stay well inside their gray square; long creatures (serpents, ribbons, "
          "tails) coil or bend inside their square instead of stretching toward the middle. Wings are half-folded or raised "
          "close to the body; weapons are held upright, close to the body. Keep each creature's natural shape and never squash "
          "it. The diagram is ONLY a placement guide: never draw the gray squares, the pink cross, the plus marks, any white or "
          "colored background, frame or line — the final background is fully transparent.")
GRADE_AVULSA = "Square image, genuine transparent alpha background. EXACTLY ONE creature, centered."
LAYOUT_AVULSA = ("Draw the creature centered with clear empty transparent space on every side: nothing touches the image "
                 "edge. Keep its natural shape.")
HUMANOID = ("HUMANOID CHARACTERS: creatures marked HUMANOID are fantasy RPG characters standing upright with a torso, two arms "
            "and a readable face, mask or helm. Use the attached humanoid reference (four approved humanoid characters) ONLY "
            "for body proportion and costume readability; do not copy them. Draw them with the SAME outline, cel-shading and "
            "finish as every other creature on this sheet. Their power follows the POWER LADDER: low tiers are novices and "
            "apprentices in simple clothes, middle tiers are adventurers and veterans, high tiers are champions and final-boss "
            "warlords. They are never realistic ordinary people: their element shows in the body itself, not only in the "
            "weapon. Tasteful, non-sexualized outfits.")
EVOLUCAO = ("EVOLUTION LINES: creatures marked EVOLVES FROM are evolved forms of another creature ON THIS SAME SHEET. An evolved "
            "form must be instantly recognizable as the same lineage: same two colors, same eye shape and eye color, and the same "
            "signature feature, but older, sturdier and more complex, with a different silhouette and pose.")
EVOLUCAO_ANTERIOR = ("EVOLUTION LINES: creatures marked EVOLVES FROM are evolved forms of the creature named in their line, which "
                     "is on this same sheet or on the attached earlier sheet or board. An evolved form must be instantly "
                     "recognizable as the same lineage: same two colors, same eye shape and eye color, and the same signature "
                     "feature, but older, sturdier and more complex, with a different silhouette and pose.")
EVOLUCAO_AVULSA = ("EVOLUTION: this creature is the evolved form of the creature named in its line, shown on an attached sheet. "
                   "It must be instantly recognizable as the same lineage: same two colors, same eye shape and eye color, and "
                   "the same signature feature, but older, sturdier and more complex, with a different silhouette and pose.")
# antecessor externo = monstro que JÁ EXISTE no jogo (arte enviada pelo usuário), no quadrante da prancha
EVOLUCAO_EXTERNO = ("EVOLUTION LINES: creatures marked EVOLVES FROM are evolved forms of the creature named in their line. When "
                    "that earlier stage is an EXISTING creature of this game, it is shown in the matching quadrant of the "
                    "attached earlier-stages board (same 2x2 grid as this sheet){outros}. An evolved form must be instantly "
                    "recognizable as the same lineage: same two colors, same eye shape and eye color, and the same signature "
                    "feature, but with a completely NEW body: older, sturdier and more complex, with a different silhouette "
                    "and pose. Never redraw the earlier stage as it is; redraw its features in the style of this sheet.")
EVOLUCAO_EXTERNO_OUTROS = {"mesma": "; otherwise it is on this same sheet",
                           "anterior": "; otherwise it is on this same sheet or on the attached earlier sheet"}
EVOLUCAO_AVULSA_EXTERNO = ("EVOLUTION: this creature is the evolved form of {nome}, an EXISTING creature of this game shown in "
                           "the attached quadrant image. It must be instantly recognizable as the same lineage: same two "
                           "colors, same eye shape and eye color, and the same signature feature, but with a completely NEW "
                           "body: older, sturdier and more complex, with a different silhouette and pose.")
# homenagem reconhecível (fidelidade "homenagem", células N/L): nunca o nome da figura em nenhum texto
HOMENAGEM = ("HOMAGE CELLS: creatures marked HOMAGE are ORIGINAL game creatures that pay homage to a classic horror figure; "
             "anyone who knows that figure must recognize it at first glance by the ICONIC TRAITS listed in its line (mask "
             "shape, outfit, weapon, colors, silhouette, posture). Redraw everything in the style of this sheet; never an "
             "actor's face or likeness, never a logo, never text or a name.")
HOMENAGEM_REF = (" The reference figure of each creature marked HOMAGE WITH REFERENCE is shown in the matching quadrant of "
                 "the attached board (same 2x2 grid as this sheet): keep its signature traits; do not copy it as a picture.")
HOMENAGEM_REF_AVULSA = (" The reference figure of this creature is shown in the attached quadrant image: keep its signature "
                        "traits; do not copy it as a picture.")

# blocos: (cabeça quando a cartela é toda desse bloco, cabeça quando a cartela mistura blocos, corpo)
BLOCO = {
    "V": ("REGIONAL VARIANT SHEET: each creature", "REGIONAL VARIANT cells: each creature marked REGIONAL VARIANT",
          " is an EXISTING creature of this game, shown on the attached originals board (same 2x2 grid as this sheet), "
          "reborn in a different element. Keep its silhouette, anatomy, head, face, eye layout and body language so that "
          "anyone who knows the original recognizes it at first glance (about 70% the same). Change the material, surface "
          "texture, palette, accent and elemental details to the NEW type named in its line. Same size, same age and same "
          "tier as the original: never bigger, never evolved, never fused with anything else. Redraw it in the style of this "
          "sheet even if the original was drawn in another style (sketch, realistic, anime); ignore any text, number or logo "
          "on the board."),
    "F": ("FUSION-OF-FUSIONS SHEET: every creature", "FUSION-OF-FUSIONS cells: every creature marked FUSION OF FUSIONS",
          " is born from 2 or 3 creatures that were THEMSELVES already born of fusions; they are shown on the attached "
          "parents board in the SAME 2x2 grid, all at the same size, and none of them is the base. Draw a COMPLETELY NEW "
          "creature that does not look like any single parent: take from EACH parent only the elements listed in its line (a "
          "material, a color, a motif, a weapon, an eye shape) and unite them in ONE coherent body with its own silhouette. It "
          "is the next step of an evolution chain: clearly more refined, more complete and more powerful than every parent at "
          "its tier (follow the POWER LADDER). Never a chimera of stitched halves, never several creatures side by side, never "
          "a rider or pet. Redraw everything in the style of this sheet; ignore any text, number or logo on the parents "
          "board."),
    "L": ("PRODIGY SHEET: four free-concept creatures", "PRODIGY cells: the creatures marked PRODIGY are free-concept creatures",
          " that share the THEME written below, each from a rare and unexpected pair of types. The theme unites them as a "
          "set, but each one has its own anatomy, silhouette, face and palette; never variations of one design. Bold, "
          "surprising concepts are welcome as long as each one reads clearly as a creature of this game."),
    "X": ("CROSSOVER FUSION SHEET: each creature", "CROSSOVER FUSION cells: each creature marked CROSSOVER FUSION",
          " is the FUSION of two existing creatures of this game. In each quadrant of the attached parents board, the LARGE "
          "creature on the left is the BASE and the SMALLER one on the right is the SACRIFICE. Draw the BASE ASCENDED by its "
          "sacrifice: keep the base's silhouette, anatomy, head, face and eyes so it is instantly recognizable; take from the "
          "sacrifice the material of some body parts, the accent color, one or two signature features and its DOMAIN shown "
          "as an aura, weapon or emanation, exactly as its line says. Never a half-and-half chimera, never the two creatures "
          "side by side, never the sacrifice as a separate creature, rider or pet. Each one must look clearly MORE powerful "
          "than both parents at its own tier (follow the POWER LADDER): an ascended form, never the base with a few "
          "decorations. Redraw everything in the style of this sheet; ignore any text on the parents board."),
    "A": ("APEX MYTHIC FUSION SHEET: each creature", "APEX MYTHIC FUSION cells: each creature marked APEX MYTHIC FUSION",
          " is the FUSION of two MYTHIC creatures of this game, the most overwhelming creatures of this pack. In its "
          "quadrant of the attached parents board, the LARGE creature on the left is the BASE and the SMALLER one on the "
          "right is the SACRIFICE. Keep the base's silhouette, head, face and eyes and every mythic sign of the BASE (its "
          "halo, crown, fire, chains or relic), and add the DOMAIN of the SACRIFICE on top of them, with two of its "
          "signature features; a final-boss ascended form with greater presence, richer armor and ornaments and the "
          "strongest glow of the sheet. Never a half-and-half chimera, never the two creatures side by side, never the "
          "sacrifice as a separate creature, rider or pet. Redraw everything in the style of this sheet; ignore any text on "
          "the parents board."),
}
APEX_ESPELHO = (" The two apex cells use the same two parents in opposite roles: they must look like two completely different "
                "beings, each one ruled by its own BASE.")

PESO_ESTILO = "Image {k} sets the base style: clean dark outline and cel-shading."
PESO_VARIEDADE = ("Image {k} must influence the result MORE than the style image: follow it for the level of detail, the richness "
                  "of materials and ornaments, the intensity of glow and the presence of each creature, and for how different "
                  "each creature's anatomy and face must be. Style references only — never copy their creatures.")
PESO_GUIA = ("Image {k} is a LAYOUT DIAGRAM, not art: it only shows WHERE each creature may be (inside its gray square) and "
             "where nothing may be (the pink cross); never draw anything from it.")
PESO_HUM = "Image {k} is only a reference for humanoid proportions and costume readability."
PESO_PROPRIA = ("Image {k} is the finished sheet this creature belongs to: match its line weight, finish and scale of detail "
                "exactly, and redraw ONLY the creature of {onde}, alone, complete and uncut — do not draw the other three.")
PESO_ANTERIOR = ("Image {k} is the finished sheet {cartela} that holds the earlier stage of the creature(s) marked EVOLVES FROM: "
                 "keep that stage's two colors, eye shape, eye color and signature feature, but draw a new body and pose; do "
                 "not copy it as a picture and ignore the other creatures on it.")
FIM_PRANCHA = "; do not copy it as a picture and ignore any text on it."
PESO_PRANCHA = {
    "XA": ("Image {k} is the parents board: in each quadrant the LARGE creature on the left is the BASE (keep it recognizable) "
           "and the SMALLER one on the right is the SACRIFICE (take from it only what the line says)"),
    "V": "Image {k} is the originals board: keep each original recognizable and change only what its line says",
    "F": "Image {k} is the parents board: take from each parent only what its line says",
    "N": ("Image {k} is the earlier-stages board, in the same 2x2 grid as this sheet: the quadrant of each creature marked "
          "EVOLVES FROM an existing creature shows that earlier stage (empty quadrants show nothing); keep its two colors, "
          "eye shape, eye color and signature feature, but draw a new body and pose"),
    "MISTA": ("Image {k} is the board of origins, in the same 2x2 grid as this sheet: each quadrant shows what its cell's line "
              "refers to (in BASE + SACRIFICE fusions, the LARGE creature on the left is the BASE and the SMALLER one on the "
              "right is the SACRIFICE); take from it only what each line says"),
    "HOMENAGEM": ("Image {k} is the board of reference figures, in the same 2x2 grid as this sheet: the quadrant of each "
                  "creature marked HOMAGE WITH REFERENCE shows the classic figure it pays homage to (empty quadrants show "
                  "nothing); keep its signature traits and redraw it in the style of this sheet"),
}
PESO_QUADRANTE = {
    "X": ("Image {k} is this creature's quadrant of the parents board: the LARGE creature on the left is the BASE (keep it "
          "recognizable) and the SMALLER one on the right is the SACRIFICE (take from it only what the line says)"),
    "V": "Image {k} is the original of this creature: keep it recognizable and change only what the line says",
    "F": "Image {k} shows the parents of this creature: take from each parent only what the line says",
    "N": ("Image {k} shows the earlier stage of this creature: keep its two colors, eye shape, eye color and signature "
          "feature, but draw a new body and pose"),
}
PESO_QUADRANTE["A"] = PESO_QUADRANTE["X"]
PESO_QUADRANTE["L"] = PESO_QUADRANTE["N"]
PESO_QUADRANTE["HOMENAGEM"] = ("Image {k} shows the classic figure this HOMAGE creature pays homage to: keep its signature "
                               "traits (the ICONIC TRAITS in its line) and redraw it in the style of this sheet")

# ---------------------------------------------------------------- textos do PROMPT_<LOTE>.md (pt-BR, para conferir)
DESCRICAO_PT = {
    "N": ('NOVOS ("leva": "novos"): criaturas inéditas. A criatura marcada EVOLVES FROM é a forma evoluída de outra (da '
          "mesma cartela, de uma anterior, que vai anexada, ou de um monstro que JÁ EXISTE no jogo, mostrado no quadrante "
          "dela na prancha): mesmas 2 cores, mesmos olhos, mesmo traço marcante; corpo novo, mais velha e robusta, outra "
          "silhueta e outra pose."),
    "V": ('VARIAÇÕES ("leva": "variacoes"): cada criatura é uma espécie que JÁ EXISTE no jogo (a prancha mostra o original '
          "na mesma grade 2x2), nascida em outro elemento. Reconhecível como o original à primeira vista (~70%: silhueta, "
          "anatomia, rosto, pose), com material, superfície, paleta e detalhes do tipo novo. Mesmo porte, mesma idade e "
          "mesmo tier; nunca maior, nunca evoluída. Original em outro traço (foto, rascunho, anime): sai no traço do jogo."),
    "F": ('FUSÕES DE FUSÕES ("leva": "fusoes_de_fusoes"): cada criatura nasce de 2 ou 3 monstros que JÁ ERAM fusões (a '
          "prancha mostra os pais, todos do mesmo tamanho; nenhum é a base). Criatura TOTALMENTE nova, que não lembra "
          "nenhum pai sozinho, leva 1–2 elementos de cada um e é um degrau acima de todos no tier dela."),
    "L": ('PRODÍGIOS ("leva": "prodigios"): criaturas livres unidas por um TEMA por cartela (escrito no prompt), cada uma de '
          "um par de tipos raro. Todas bem diferentes entre si."),
    "X": ('CROSSOVER ("leva": "crossover"): cada criatura é a FUSÃO de dois monstros do jogo. A prancha dos pais mostra, em '
          "cada quadrante, a BASE grande à esquerda e o SACRIFÍCIO pequeno à direita. O resultado é a BASE ASCENDIDA: "
          "reconhecível de cara pela base (silhueta, cabeça, rosto, traço marcante), com material, cor de acento, 1–2 traços "
          "e o domínio do sacrifício, e claramente MAIS FORTE que os dois pais no tier dela."),
    "A": ('ÁPICE ("leva": "apice"): fusão de dois MÍTICOS (base + sacrifício, prancha igual à do crossover), as criaturas '
          "mais avassaladoras do lote: todo sinal mítico da base fica e o domínio do sacrifício entra por cima. Ápices com "
          "os mesmos pais em papéis trocados têm que sair dois seres bem diferentes."),
}
CONFERE_PT = {
    "N": ("  NOVOS: a evolução é reconhecível como o estágio anterior (cores, olhos, traço marcante; o do monstro existente "
          "está no quadrante da prancha), com corpo novo — não é o antecessor redesenhado."),
    "V": "  VARIAÇÕES: reconhecível como o original; o tipo novo aparece no material e nas cores; não cresceu nem envelheceu.",
    "F": "  FUSÕES DE FUSÕES: não lembra nenhum pai sozinho; traz algo de cada pai; um degrau acima dos pais.",
    "L": "  PRODÍGIOS: as 4 conversam com o tema da cartela e são bem diferentes entre si.",
    "X": ("  CROSSOVER: a BASE é reconhecível; dá para ver algo do SACRIFÍCIO; parece mais forte que os dois pais; nunca "
          "metade-metade nem os dois lado a lado."),
    "A": ("  ÁPICE: os sinais míticos da base ficaram e o domínio do sacrifício está por cima; ápices com os mesmos pais "
          "trocados são bem diferentes entre si."),
}
DESCRICAO_HOMENAGEM_PT = ("HOMENAGEM: as criaturas marcadas HOMAGE são criaturas novas do jogo que homenageiam uma figura "
                          "clássica do terror: quem conhece a figura reconhece de cara pelos traços icônicos da linha "
                          "(máscara, figurino, arma, cores, silhueta, postura); a marcada HOMAGE WITH REFERENCE tem a figura "
                          "no quadrante dela na prancha. Redesenho no traço do jogo; sem nome, rosto de ator, logo ou texto.")
CONFERE_HOMENAGEM_PT = ("  HOMENAGEM: quem conhece a figura clássica reconhece à primeira vista (traços icônicos da linha); não "
                        "é cópia da referência; sem rosto de ator, logo, letra ou nome.")


def ler_cabecalho():
    """Cabeçalho aprovado, sem o parágrafo FILL THE CELL (substituído pelo LAYOUT do diagrama)."""
    with open(os.path.join(comum.TEMPLATES_DIR, "CABECALHO_CARTELA.txt"), encoding="utf-8-sig") as fh:
        t = fh.read()
    a = t.index("FILL THE CELL:")
    fim = "never touch, cross or overlap neighboring cells."
    b = t.index(fim) + len(fim)
    return t[:a], t[b:]


def progressao(tiers):
    ts = sorted(set(tiers))
    return "- tiers " + ", ".join(map(str, ts)) + ": follow the POWER LADDER above for each creature."


def montar(cab, grade, layout, tipo, rotulo, prog, extras, linhas, pagina, total, peso_txt):
    antes, depois = cab
    corpo = antes.replace("{GRADE}", grade) + layout + depois
    if tipo is None:   # cartela sem uma tipagem só
        corpo = corpo.replace("The primary type ({TIPO})", "The first type named in each line")
    corpo = re.sub(r"TYPE PACK: \{TIPO\}\. PAGE \{N\}/\d+\.", f"TYPE PACK: {rotulo}. PAGE {pagina}/{total}.", corpo)
    corpo = (corpo.replace("{TIPO}", tipo or rotulo).replace("{PROGRESSAO}", prog)
             .replace("{EVOLUCAO}", "".join(x + "\n" for x in extras))
             .replace("{LINHAS}", "\n".join(linhas)))
    return corpo.rstrip() + "\n\n" + peso_txt + "\n"


def tipos_txt(a, b):
    return f"{TIPOS[a]}/{TIPOS[b]}"


def externo(e):
    """Antecessor externo (monstro existente, fora do lote) de uma célula N, ou None."""
    return (e.get("evolucao") or {}).get("externo")


def ingr(e, papel):
    return next(i for i in e.get("ingredientes", []) if i.get("papel") == papel)


def homenagem(e):
    """Célula N/L em modo homenagem reconhecível."""
    return e["bloco"] in ("N", "L") and e.get("fidelidade") == "homenagem"


def ref_arte(e):
    """Recorte da figura de referência da homenagem (no quadrante da prancha), ou None."""
    return (e.get("referencia_conteudo") or {}).get("recorte") if homenagem(e) else None


def linha(f, e, nomes, avulsa=False):
    pos = "" if avulsa else f"Row {e['linha']}, column {e['coluna']}, "
    hum = ", HUMANOID" if f.get("humanoide") else ""
    fim = f": {f['nome']} ({tipos_txt(e['tipo1'], e['tipo2'])}) — {f['visual']}"
    b = e["bloco"]
    if b in ("N", "L"):
        ant = (e.get("evolucao") or {}).get("anterior")
        ext = externo(e)
        hom = (", HOMAGE WITH REFERENCE" if ref_arte(e) else ", HOMAGE") if homenagem(e) else ""
        de = f", EVOLVES FROM {ext['nome']}" if ext else (f", EVOLVES FROM {nomes[ant]}" if ant else "")
        return f"{pos}tier {e['tier']}{hum}{hom}{de}{fim}"
    if b == "V":
        o = e["original"]
        return (f"{pos}tier {e['tier']}{hum}, REGIONAL VARIANT of {o['nome']} ({tipos_txt(o['tipo1'], o['tipo2'])}) now "
                f"{TIPOS[e['tipo_entra']]}{fim}")
    if b == "F":
        pais = " + ".join(i["nome"] for i in e["ingredientes"])
        return f"{pos}tier {e['tier']}{hum}, FUSION OF FUSIONS born from {pais}{fim}"
    rot = "APEX MYTHIC FUSION" if b == "A" else "CROSSOVER FUSION"
    return (f"{pos}tier {e['tier']}{hum}, {rot} of {ingr(e, 'BASE')['nome']} (BASE) + "
            f"{ingr(e, 'SACRIFICIO')['nome']} (SACRIFICE){fim}")


def texto_bloco(b, mista, tema=None, espelho=False):
    if b not in BLOCO:
        return None
    folha, cel, corpo = BLOCO[b]
    t = (cel if mista else folha) + corpo
    if b == "L" and tema:
        t += f" THEME OF THIS SHEET: {tema}."
    if b == "A" and espelho:
        t += APEX_ESPELHO
    return t


def peso(anexos, blocos, avulsa_bloco=None, onde=None, prancha_hom=None):
    """Explica cada anexo pela posição real na lista. anexos = [(tipo, caminho)].
    prancha_hom: None (prancha sem figura de homenagem), "so" (só figuras de homenagem) ou "mista" (com antecessor externo);
    na avulsa, avulsa_bloco = "HOMENAGEM" quando o quadrante é a figura de referência."""
    p = []
    for k, (tipo, cam) in enumerate(anexos, 1):
        if tipo == "estilo":
            p.append(PESO_ESTILO.format(k=k))
        elif tipo == "variedade":
            p.append(PESO_VARIEDADE.format(k=k))
        elif tipo == "prancha":
            if set(blocos) <= set("XA"):
                chave = "XA"
            elif set(blocos) <= set("NL"):
                chave = {"so": "HOMENAGEM", "mista": "MISTA"}.get(prancha_hom, "N")
            elif len(set(blocos)) == 1:
                chave = blocos[0]
            else:
                chave = "MISTA"
            p.append(PESO_PRANCHA[chave].format(k=k) + FIM_PRANCHA)
        elif tipo == "quadrante":
            p.append(PESO_QUADRANTE[avulsa_bloco].format(k=k) + FIM_PRANCHA)
        elif tipo == "anterior":
            num = re.search(r"cartela_(\d{3})_original", cam).group(1)
            p.append(PESO_ANTERIOR.format(k=k, cartela=num))
        elif tipo == "guia":
            p.append(PESO_GUIA.format(k=k))
        elif tipo == "humanoides":
            p.append(PESO_HUM.format(k=k))
        elif tipo == "propria":
            p.append(PESO_PROPRIA.format(k=k, onde=onde))
    return "\n".join(p)


def ref(tipo):
    return (tipo, "referencias/" + REFS[tipo][0])


def faixas(total, passo=4):
    return [(a, min(a + passo - 1, total)) for a in range(1, total + 1, passo)]


def intervalos(nums):
    nums = sorted(set(nums))
    out, ini, ant = [], None, None
    for x in nums:
        if ini is None:
            ini = ant = x
        elif x == ant + 1:
            ant = x
        else:
            out.append((ini, ant))
            ini = ant = x
    if ini is not None:
        out.append((ini, ant))
    return ", ".join(f"{a:03d}" if a == b else f"{a:03d}–{b:03d}" for a, b in out)


# ---------------------------------------------------------------- integração das partes
def integrar(lote, entrada, doc, partes):
    por_n = {f["n"]: f for f in doc.get("monstros", [])}
    pasta = os.path.join(lote, "fichas_claude")
    arquivos = sorted(x for x in (os.listdir(pasta) if os.path.isdir(pasta) else [])
                      if re.fullmatch(r"parte_[A-Za-z0-9]+\.json", x))
    for nome_arq in arquivos:
        letra = nome_arq[len("parte_"):-len(".json")]
        if partes and letra not in partes:
            continue
        v = comum.ler_json(os.path.join(pasta, f"parte_{letra}_validacao.json"), {})
        if not v or v.get("erros") is None or v["erros"]:
            print(f"PULEI {nome_arq}: ainda não validou sem erros (rode compor_fichas.py)")
            continue
        fichas = comum.ler_json(os.path.join(pasta, nome_arq))
        problemas = []
        for f in fichas:
            e = entrada.get(f.get("n"))
            if e is None:
                problemas.append(f"n={f.get('n')} não existe na entrada")
            elif not f.get("visual") or not (f.get("nome") or f.get("epiteto")):
                problemas.append(f"n={f['n']} sem nome/visual (rode compor_fichas.py)")
        if problemas:
            print(f"PULEI {nome_arq}: " + "; ".join(problemas))
            continue
        for f in fichas:
            por_n[f["n"]] = normalizar(dict(f), entrada[f["n"]])
        print(f"{nome_arq}: {len(fichas)} fichas integradas")
    nomes = {n: f["nome"] for n, f in por_n.items()}
    for n, f in por_n.items():   # evolução no formato do cadastrador (precisa de todos os nomes)
        e = entrada.get(n, {})
        ant = (e.get("evolucao") or {}).get("anterior")
        ext = externo(e)
        f.pop("evolucao", None)
        de = ext["nome"] if ext else (nomes[ant] if ant and ant in nomes else None)
        if de:
            ev = {"de": de, "modo": e.get("evolucao_modo") or "a_definir"}
            if e.get("level_requerido") is not None:
                ev["level_requerido"] = e["level_requerido"]
            f["evolucao"] = ev
    doc["monstros"] = sorted(por_n.values(), key=lambda f: f["n"])
    return doc


def normalizar(f, e):
    for k in ("cartela", "linha", "coluna", "slot", "bloco", "tier", "tipo1", "tipo2"):
        if k in e:
            f[k] = e[k]
    if e["bloco"] == "V":
        f.setdefault("nome", f"{e['original']['nome']} {f.get('epiteto', '').strip()}".strip())
        f["variacao_de"] = e["original"]["nome"]
    if e.get("ingredientes"):
        f["ingredientes"] = [{"papel": i.get("papel"), "nome": i["nome"]} for i in e["ingredientes"]]
    if not f.get("arquivo"):
        f["arquivo"] = comum.arquivo_recorte(f["n"], f["tier"], f["nome"])
    f["humanoide"] = bool(f.get("humanoide"))
    return f


# ---------------------------------------------------------------- principal
def main(argv):
    lote = comum.pasta_lote(argv, USO)
    gravar = "--gravar" in argv
    consertos = [int(x) for x in argv[argv.index("--conserto") + 1].split(",")] if "--conserto" in argv else []
    partes = argv[argv.index("--partes") + 1].split(",") if "--partes" in argv else []

    plano = comum.ler_json(os.path.join(lote, "plano.json"), {})
    nome_lote = plano.get("lote") or os.path.basename(lote)
    clima = (plano.get("clima") or "").strip()
    temas_plano = {c.get("cartela"): c.get("tema") for c in plano.get("cartelas", [])}
    entrada = {e["n"]: e for e in comum.ler_json(os.path.join(lote, "entrada.json"))}
    mj = os.path.join(lote, "monstros.json")
    doc = comum.ler_json(mj, {"lote": nome_lote, "status": "em produção", "monstros": []})
    doc.setdefault("lote", nome_lote)
    doc.setdefault("status", "em produção")
    doc = integrar(lote, entrada, doc, partes)
    fichas = {f["n"]: f for f in doc["monstros"]}
    nomes = {n: f["nome"] for n, f in fichas.items()}

    cab = ler_cabecalho()
    cartelas = sorted({e["cartela"] for e in entrada.values()})
    total = max(cartelas) if cartelas else 0
    fila_p = os.path.join(lote, "fila.json")
    fila = {x["cartela"]: x for x in comum.ler_json(fila_p, [])}
    textos, crops, refs_usadas = {}, [], set()
    feitos = 0

    for c in cartelas:
        es = sorted([e for e in entrada.values() if e["cartela"] == c], key=lambda e: (e["linha"], e["coluna"]))
        fs = [fichas.get(e["n"]) for e in es]
        if len(es) != 4 or any(f is None for f in fs):
            continue
        tem_imagem = os.path.exists(os.path.join(lote, "cartelas", f"cartela_{c:03d}_original.png"))
        if tem_imagem and c not in consertos:
            continue
        blocos = sorted({e["bloco"] for e in es}, key=ORDEM.index)
        mista = len(blocos) > 1
        # antecessores: nome precisa existir; os de cartela anterior viram anexo (a prancha só mostra antecessor EXTERNO)
        falta_ant, anteriores = [], {}
        tem_ext = any(externo(e) for e in es)
        for e in es:
            ant = (e.get("evolucao") or {}).get("anterior")
            if ant:
                if ant not in nomes:
                    falta_ant.append(ant)
                elif entrada[ant]["cartela"] < c:
                    anteriores[e["n"]] = entrada[ant]["cartela"]
        if falta_ant:
            print(f"cartela {c:03d}: aguardando a ficha do antecessor n={falta_ant}")
            continue
        prancha_rel = f"referencias/cartela_{c:03d}_pais.png"
        tem_prancha = os.path.exists(os.path.join(lote, prancha_rel))
        tem_hom = any(homenagem(e) for e in es)
        tem_ref = any(ref_arte(e) for e in es)
        prancha_hom = ("mista" if tem_ext else "so") if tem_ref else None
        if (PRECISA_PRANCHA & set(blocos) or tem_ext or tem_ref) and not tem_prancha:
            print(f"cartela {c:03d}: falta {prancha_rel} (rode montar_entrada.py)")
            continue
        hum = any(f["humanoide"] for f in fs)
        ant_cartelas = sorted(set(anteriores.values()))
        anexos = [ref("estilo"), ref("variedade")] + ([("prancha", prancha_rel)] if tem_prancha else []) + \
                 [("anterior", f"cartelas/cartela_{a:03d}_original.png") for a in ant_cartelas] + \
                 [ref("guia")] + ([ref("humanoides")] if hum else [])
        if len(anexos) > MAX_ANEXOS:
            print(f"cartela {c:03d}: {len(anexos)} anexos (máx. {MAX_ANEXOS}); monte uma prancha dos antecessores")
            continue
        tema = None
        if "L" in blocos:
            tema = next((f.get("tema") for f, e in zip(fs, es) if e["bloco"] == "L" and f.get("tema")), None) \
                or temas_plano.get(c)
        pares_a = [(ingr(e, "BASE")["nome"], ingr(e, "SACRIFICIO")["nome"]) for e in es if e["bloco"] == "A"]
        espelho = any((s, b) in pares_a for b, s in pares_a)
        tem_int = any((e.get("evolucao") or {}).get("anterior") for e in es)
        if tem_ext:
            evol = [EVOLUCAO_EXTERNO.format(outros=EVOLUCAO_EXTERNO_OUTROS["anterior" if anteriores else "mesma"]
                                            if tem_int else "")]
        elif tem_int:
            evol = [EVOLUCAO_ANTERIOR if anteriores else EVOLUCAO]
        else:
            evol = []
        extras = ([clima] if clima else []) + \
                 [t for t in (texto_bloco(b, mista, tema, espelho) for b in blocos) if t] + \
                 ([HOMENAGEM + (HOMENAGEM_REF if tem_ref else "")] if tem_hom else []) + \
                 ([HUMANOID] if hum else []) + evol
        tipo1s = {e["tipo1"] for e in es}
        tipo = TIPOS[tipo1s.pop()] if blocos == ["N"] and len(tipo1s) == 1 else None
        rotulo = tipo or " + ".join(ROTULO[b] for b in blocos)
        txt = montar(cab, GRADE, LAYOUT, tipo, rotulo, progressao([e["tier"] for e in es]), extras,
                     [linha(f, e, nomes) for f, e in zip(fs, es)], c, total, peso(anexos, blocos, prancha_hom=prancha_hom))
        estado = "pendente de conserto" if (c in consertos and tem_imagem) else fila.get(c, {}).get("estado", "pronta")
        salvar = f"cartelas/cartela_{c:03d}_original.png"
        item = dict(cartela=c, leva="+".join(LEVA[b] for b in blocos), estado=estado, prompt=f"prompts/cartela_{c:03d}.txt",
                    anexos=[a for _, a in anexos], salvar=salvar, monstros=[f["nome"] for f in fs],
                    depende_de=ant_cartelas, avulsas=[])
        refs_usadas.update(t for t, _ in anexos if t in REFS)
        for f, e in zip(fs, es):
            l, k, b = e["linha"], e["coluna"], e["bloco"]
            ant_c = anteriores.get(e["n"])
            ext = externo(e)
            ref_e = ref_arte(e)
            quad = None
            if tem_prancha and (b in PRECISA_PRANCHA or ext or ref_e):
                quad = f"referencias/avulsas/cartela_{c:03d}_L{l}C{k}_pais.png"
                crops.append((prancha_rel, quad, l, k))
            an = [ref("estilo"), ref("variedade")] + ([("quadrante", quad)] if quad else []) + \
                 ([("anterior", f"cartelas/cartela_{ant_c:03d}_original.png")] if ant_c and not quad else []) + \
                 [("propria", salvar)] + ([ref("humanoides")] if f["humanoide"] else [])
            assert len(an) <= MAX_ANEXOS, (c, an)
            ex = ([clima] if clima else []) + [t for t in [texto_bloco(b, False, tema, False)] if t] + \
                 ([HOMENAGEM + (HOMENAGEM_REF_AVULSA if ref_e else "")] if homenagem(e) else []) + \
                 ([HUMANOID] if f["humanoide"] else []) + \
                 ([EVOLUCAO_AVULSA_EXTERNO.format(nome=ext["nome"])] if ext else
                  [EVOLUCAO_AVULSA] if (e.get("evolucao") or {}).get("anterior") else [])
            ta = montar(cab, GRADE_AVULSA, LAYOUT_AVULSA, tipo, rotulo, progressao([e["tier"]]), ex,
                        [linha(f, e, nomes, avulsa=True)], c, total,
                        peso(an, [b], "HOMENAGEM" if ref_e else b, ONDE[(l, k)]))
            item["avulsas"].append(dict(linha=l, coluna=k, nome=f["nome"], prompt=f"prompts/avulsa_{c:03d}_L{l}C{k}.txt",
                                        anexos=[a for _, a in an], salvar=f"cartelas/avulsa_{c:03d}_L{l}C{k}_v1.png"))
            textos[f"prompts/avulsa_{c:03d}_L{l}C{k}.txt"] = ta
        if not tem_imagem:
            textos[f"prompts/cartela_{c:03d}.txt"] = txt
        fila[c] = item
        feitos += 1
        print(f"cartela {c:03d}: {item['leva']}, {len(anexos)} anexos" + (" (conserto)" if tem_imagem else ""))

    arq_md = f"PROMPT_{comum.slug(nome_lote).upper()}.md"
    md = prompt_lote(lote, plano, nome_lote, entrada, total, arq_md, clima)
    if gravar:
        copiar_refs(lote, refs_usadas)
        recortar_quadrantes(lote, crops)
        for rel, t in textos.items():
            comum.gravar_texto(os.path.join(lote, rel), t)
        comum.gravar_json(mj, doc, indent=2)
        comum.gravar_json(fila_p, [fila[c] for c in sorted(fila)])
        comum.gravar_texto(os.path.join(lote, arq_md), md)
    prontas = sum(1 for x in fila.values() if x["estado"] == "pronta")
    print(f"{'GRAVADO' if gravar else 'ENSAIO'}: {feitos} cartelas preparadas | fila: {len(fila)} de {len(cartelas)} "
          f"cartelas, {prontas} prontas | {len(textos)} prompts | {arq_md}")


def copiar_refs(lote, tipos):
    for t in tipos:
        destino = os.path.join(lote, "referencias", REFS[t][0])
        if not os.path.exists(destino):
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copyfile(os.path.join(comum.REFS_DIR, REFS[t][1]), destino)


def recortar_quadrantes(lote, crops):
    if not crops:
        return
    from PIL import Image
    abertas = {}
    for prancha, quad, l, k in crops:
        if prancha not in abertas:
            abertas[prancha] = Image.open(os.path.join(lote, prancha))
        img = abertas[prancha]
        w, h = img.width // 2, img.height // 2
        destino = os.path.join(lote, quad)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        img.crop(((k - 1) * w, (l - 1) * h, k * w, l * h)).save(destino)


def prompt_lote(lote, plano, nome_lote, entrada, total, arq_md, clima):
    with open(os.path.join(comum.TEMPLATES_DIR, "PROMPT_LOTE.md"), encoding="utf-8-sig") as fh:
        t = fh.read()
    por_bloco = {}
    for e in entrada.values():
        por_bloco.setdefault(e["bloco"], []).append(e["cartela"])
    blocos = sorted(por_bloco, key=lambda b: (min(por_bloco[b]), ORDEM.index(b)))
    tabela = "\n".join(f"| {intervalos(por_bloco[b])} | {NOME_PT[b]} | {len(por_bloco[b])} |" for b in blocos)
    arq_abs = os.path.join(lote, arq_md)
    fx = [f"{a:03d}–{b:03d}" for a, b in faixas(total)]
    descricao = "\n".join(DESCRICAO_PT[b] for b in blocos)
    confere = [CONFERE_PT[b] for b in blocos]
    if any(homenagem(e) for e in entrada.values()):
        descricao += "\n" + DESCRICAO_HOMENAGEM_PT
        confere.append(CONFERE_HOMENAGEM_PT)
    if clima:
        descricao += ("\nCLIMA DO LOTE (vai no começo de todo prompt; o que ele proíbe é erro de criatura): " + clima)
        confere.append("  CLIMA: a imagem respeita o bloco de clima do lote (nada do que ele proíbe aparece).")
    valores = {
        "{TITULO}": plano.get("titulo") or nome_lote, "{LOTE}": nome_lote, "{TOTAL}": str(total),
        "{MONSTROS}": str(len(entrada)), "{ULTIMA}": f"{total:03d}", "{PASTA_LOTE}": lote,
        "{PASTA_CARTELAS}": os.path.join(lote, "cartelas"), "{ARQUIVO_PROMPT}": arq_abs, "{SKILL}": comum.SKILL_DIR.replace(os.sep, "/"),
        "{TABELA}": tabela, "{FAIXAS}": "\n\n".join(f"> Leia e execute `{arq_abs}` — FAIXA {x}" for x in fx),
        "{LISTA_FAIXAS}": ", ".join(fx), "{NUM_FAIXAS}": str(len(fx)), "{PRIMEIRA_FAIXA}": fx[0] if fx else "",
        "{LEVAS}": " | ".join(LEVA[b] for b in blocos), "{DESCRICAO_LEVA}": descricao,
        "{CONFERENCIA_BLOCOS}": "\n".join(confere),
    }
    for k, v in valores.items():
        t = t.replace(k, v)
    sobra = sorted(set(re.findall(r"\{[A-Z_]{3,}\}", t)))
    if sobra:
        print(f"AVISO: placeholders sem valor em {arq_md}: {sobra}")
    return t


if __name__ == "__main__":
    main(sys.argv)
