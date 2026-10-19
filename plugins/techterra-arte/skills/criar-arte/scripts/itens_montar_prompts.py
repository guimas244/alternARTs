# -*- coding: utf-8 -*-
"""Valida o itens.json de um lote de itens e monta os prompts das cartelas 5x5, a fila e o prompt da sessão de imagem.

    python itens_montar_prompts.py <lote>                 # só valida (não grava nada)
    python itens_montar_prompts.py <lote> --gravar        # valida e grava (com ERRO não grava)
    python itens_montar_prompts.py <lote> --gravar --forcar   # ensaio: grava mesmo com ERRO, fila "bloqueada"

Lê <lote>/itens.json (formato em modos/itens.md) e grava em <lote>: prompts/pagina_NN.txt, referencias/ (estilo +
guia da grade, copiados da skill), fila.json, PROMPT_ITENS_<LOTE>.md e o campo `arquivo` de cada item no itens.json
(só quando falta). Regras: regras/itens.md. Nada é gravado dentro da skill.
"""
import os
import re
import shutil
import sys
from itertools import combinations

sys.dont_write_bytecode = True  # nada de __pycache__ dentro da skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

USO = __doc__
POR_PAGINA, LADO_GRADE = 25, 5
ORGANIZACOES = ("faixa_por_linha", "tipagem_por_linha")
SLOT_EN = {"arma": "weapon", "armadura": "armor", "orb": "orb"}
ANEXOS = [("itens", "estilo_03_miniatura_3d.png"), ("guias", "guia_grade_5x5.png")]
TEMPLATE_PAGINA = os.path.join(comum.TEMPLATES_DIR, "itens", "PROMPT_PAGINA_ITENS.txt")
TEMPLATE_SESSAO = os.path.join(comum.TEMPLATES_DIR, "itens", "PROMPT_SESSAO_ITENS.md")

# Escada de materiais (regras/itens.md §3), uma frase por nível; níveis = faixas 1-2, 3-4, 5-6, 7-8, 9-10.
ESCADA = [
    ("humble raw materials", "(bone, rawhide, wood, chipped stone, cord)"),
    ("honest craft", "(plain metal, firm stitching, rivets)"),
    ("fine work", "(polished metal, one gem or one rare material of the type)"),
    ("enchanted pieces", "(living or impossible material, light held inside the piece; living means a material that "
                         "glows or grows, never an animal, a face or an eye)"),
    ("relics", "(rich ornament, several noble materials, unique presence)"),
]

# Palavra inteira proibida na linha de arte de equipamento de monstro (ERRO): arma/armadura de gente.
GENTE = {"handle", "handles", "hilt", "hilts", "crossguard", "pommel", "sword", "swords", "staff", "wand", "glove",
         "gloves", "gauntlet", "gauntlets", "person", "human", "humans", "hand", "hands", "mannequin", "torso",
         "spear", "axe", "dagger", "crossbow", "helmet", "boot", "boots"}
# AVISO: pode ser de gente, pode não ser (confira o teste do monstro).
GENTE_TALVEZ = {"bow", "shield", "belt", "crown", "necklace", "cloak", "spellbook", "flail", "trident", "harpoon",
                "lance", "scythe", "hammer", "whip"}
# AVISO: escrita (o gerador escreve) e marca de campeonato fora do lugar.
TEXTO = {"letter", "letters", "lettering", "inscription", "inscriptions", "rune", "runes", "text", "writing",
         "word", "words", "logo", "label", "numeral", "numerals", "number", "numbers"}
CAMPEONATO = {"laurel", "laurels", "wreath", "medal"}
# Fora da comparação de "objeto recolorido": cor, metal e enchimento.
CORES = set("""red orange yellow green blue purple violet pink black white grey gray brown tan cream ivory beige gold
golden silver bronze brass copper tin iron steel teal turquoise cyan aqua navy indigo magenta crimson scarlet amber
olive emerald jade ruby sapphire pearl pearly rose peach plum burgundy wine maroon charcoal graphite sand ochre rust
russet lilac lavender mint coral azure dark pale light deep bright warm cool muted dull rich soft vivid glowing
polished aged worn satin matte glossy""".split())
VAZIAS = set("""a an the of with and or one two three four five its it to on in at by for from into onto around over
under each side top bottom front small large big short long thick thin tiny compact single set piece pieces that this
is are as like shaped made fixed set inside outside along across between which their them very little few several
all no not only""".split())


def arquivo_item(item):
    """Nome do recorte: <tipagem>/faixa_NN_<slug do nome>.png (regras/itens.md §6)."""
    return f"{comum.slug(item.get('tipagem', ''))}/faixa_{int(item.get('faixa', 0)):02d}_{comum.slug(item.get('nome', ''))}.png"


def tipo_en(tid):
    """Nome da tipagem para o prompt, sem acento (o gerador não precisa do acento)."""
    return comum.norm(comum.TIPOS.get(tid, tid)).title()


def palavras(texto):
    return re.findall(r"[a-z]+", (texto or "").lower())


def conteudo(texto):
    return {p for p in palavras(texto) if p not in CORES and p not in VAZIAS and len(p) > 2}


def progressao(faixas):
    """Frase da escada para as faixas presentes, agrupando as do mesmo nível (ex.: 'tiers 1–2 are ...; tier 5 is ...')."""
    grupos = []
    for f in sorted(set(faixas)):
        nivel = min(4, (f - 1) // 2)
        if grupos and grupos[-1][0] == nivel and grupos[-1][1][-1] == f - 1:
            grupos[-1][1].append(f)
        else:
            grupos.append((nivel, [f]))
    partes = []
    for nivel, fs in grupos:
        nome, exemplo = ESCADA[nivel]
        quem = f"tier {fs[0]} is" if len(fs) == 1 else f"tiers {fs[0]}–{fs[-1]} are"
        partes.append(f"{quem} {nome} {exemplo}")
    return "; ".join(partes) + "."


def validar(dados):
    """Devolve (erros, avisos, paginas) — paginas = {n: [item, ...] ordenados por linha/coluna}."""
    erros, avisos = [], []
    if not isinstance(dados, dict) or not isinstance(dados.get("itens"), list) or not dados["itens"]:
        return ["itens.json precisa de {\"lote\": ..., \"organizacao\": ..., \"itens\": [...]}"], [], {}
    org = dados.get("organizacao")
    if org not in ORGANIZACOES:
        erros.append(f"organizacao deve ser {' ou '.join(ORGANIZACOES)} (veio {org!r})")
    if not comum.slug(dados.get("lote", "")):
        erros.append("falta o campo lote")
    categoria = dados.get("categoria", "equipamento")
    equip = categoria == "equipamento"
    nomes, arquivos, paginas = {}, {}, {}
    for k, it in enumerate(dados["itens"], start=1):
        onde = f"item {k} ({it.get('nome') or 'sem nome'})"

        def erro(msg):
            erros.append(f"{onde}: {msg}")

        def aviso(msg):
            avisos.append(f"{onde}: {msg}")

        for campo in ("nome", "tipagem", "faixa", "descricao", "visual", "pagina", "linha", "coluna"):
            if it.get(campo) in (None, ""):
                erro(f"falta {campo}")
        if any(it.get(c) in (None, "") for c in ("nome", "tipagem", "faixa", "pagina", "linha", "coluna")):
            continue
        if it["tipagem"] not in comum.TIPOS:
            erro(f"tipagem desconhecida {it['tipagem']!r} (use o id de comum.TIPOS, ex.: marinho, agua)")
        try:
            faixa, pg, lin, col = (int(it[c]) for c in ("faixa", "pagina", "linha", "coluna"))
        except (TypeError, ValueError):
            erro("faixa/pagina/linha/coluna precisam ser números")
            continue
        if not 1 <= faixa <= 10:
            erro("faixa fora de 1–10")
        if not (1 <= lin <= LADO_GRADE and 1 <= col <= LADO_GRADE) or pg < 1:
            erro("pagina/linha/coluna fora da grade 5x5")
        chave = comum.norm(it["nome"]).strip()
        if chave in nomes:
            erro(f"nome repetido (igual ao {nomes[chave]})")
        nomes[chave] = onde
        arq = it.get("arquivo") or arquivo_item(it)
        if it.get("arquivo") and not re.fullmatch(r"[a-z0-9_]+/faixa_(0[1-9]|10)_[a-z0-9_]+\.png", it["arquivo"]):
            erro(f"arquivo fora do padrão <tipagem>/faixa_NN_<descricao>.png: {it['arquivo']}")
        if arq in arquivos:
            erro(f"arquivo repetido ({arquivos[arq]}): {arq}")
        arquivos[arq] = onde
        if equip and it.get("slot") not in SLOT_EN:
            erro(f"slot deve ser arma, armadura ou orb (veio {it.get('slot')!r})")
        visual = (it.get("visual") or "").strip()
        if visual:
            ps = palavras(visual)
            if re.search(r"[À-ÿ]", visual):
                erro("visual com acento: a linha de arte é em inglês")
            nome_n = " ".join(palavras(comum.norm(it["nome"])))
            if nome_n and re.search(r"\b" + re.escape(nome_n) + r"\b", " ".join(ps)):
                erro("o nome em português aparece no visual (o gerador escreve o nome na imagem)")
            else:
                pt = [p for p in palavras(comum.norm(it["nome"])) if len(p) >= 6 and p in ps]
                if pt:
                    aviso(f"palavra do nome em português no visual: {', '.join(pt)} (confira se é inglês)")
            if equip:
                ruins = sorted(GENTE & set(ps))
                if ruins:
                    erro(f"objeto de gente no visual ({', '.join(ruins)}): é equipamento DE MONSTRO "
                         f"(garra, presa, ferrão, peitoral de fera, orbe de coleira)")
                talvez = sorted(GENTE_TALVEZ & set(ps))
                if talvez:
                    aviso(f"confira o teste do monstro ({', '.join(talvez)}): uma pessoa seguraria ou vestiria isso?")
                if not re.search(r"\b(strap|straps|ring|rings|clasp|clasps|cuff|cuffs|socket|loop|collar|buckle|"
                                 r"buckled|band|cord|chain|tie|ties|lashed|tied|harness|mount|mounted|hinge|hinged)\b",
                                 visual.lower()):
                    aviso("o visual não diz como a peça prende (correia, argola, presilha, punho, encaixe)")
                if categoria != "campeonato" and CAMPEONATO & set(ps):
                    aviso("louro/medalha é marca dos itens de campeonato")
            if TEXTO & set(ps):
                aviso(f"palavra de escrita no visual ({', '.join(sorted(TEXTO & set(ps)))}): risco de texto na imagem")
            n = len(visual.split())
            if not 12 <= n <= 60:
                aviso(f"visual com {n} palavras (ideal 20–45)")
        paginas.setdefault(pg, []).append({**it, "faixa": faixa, "pagina": pg, "linha": lin, "coluna": col,
                                           "arquivo": arq})
    # páginas: 25 itens, posições únicas, organização coerente
    for pg, its in sorted(paginas.items()):
        its.sort(key=lambda i: (i["linha"], i["coluna"]))
        pos = [(i["linha"], i["coluna"]) for i in its]
        if len(its) != POR_PAGINA or len(set(pos)) != POR_PAGINA:
            erros.append(f"página {pg}: {len(its)} itens / {len(set(pos))} posições (precisa de exatamente 25, uma por "
                         f"célula da grade 5x5)")
            continue
        linhas_ = [[i for i in its if i["linha"] == r] for r in range(1, 6)]
        if org == "faixa_por_linha":
            if len({i["tipagem"] for i in its}) != 1:
                erros.append(f"página {pg}: faixa_por_linha exige a página inteira da mesma tipagem")
            fx = []
            for r, ln in enumerate(linhas_, start=1):
                if len({i["faixa"] for i in ln}) != 1:
                    erros.append(f"página {pg}: linha {r} mistura faixas (cada linha é uma faixa)")
                fx.append(ln[0]["faixa"])
            if fx != sorted(fx) or len(set(fx)) != 5:
                erros.append(f"página {pg}: as faixas devem crescer de cima para baixo, uma por linha (veio {fx})")
        elif org == "tipagem_por_linha":
            for r, ln in enumerate(linhas_, start=1):
                if len({i["tipagem"] for i in ln}) != 1:
                    erros.append(f"página {pg}: linha {r} mistura tipagens (cada linha é uma tipagem)")
            fx = []
            for c in range(1, 6):
                coluna = [i for i in its if i["coluna"] == c]
                if len({i["faixa"] for i in coluna}) != 1:
                    erros.append(f"página {pg}: coluna {c} mistura faixas (cada coluna é uma faixa)")
                fx.append(coluna[0]["faixa"])
            if fx != sorted(fx) or len(set(fx)) != 5:
                erros.append(f"página {pg}: as faixas devem crescer da esquerda para a direita (veio {fx})")
            if len({ln[0]["tipagem"] for ln in linhas_}) != 5:
                erros.append(f"página {pg}: tipagem_por_linha usa 5 tipagens diferentes, uma por linha")
    if sorted(paginas) != list(range(1, len(paginas) + 1)):
        erros.append(f"páginas devem ser 1..N sem buraco (vieram {sorted(paginas)})")
    # objeto recolorido: mesma tipagem, faixas diferentes, texto parecido
    por_tipo = {}
    for its in paginas.values():
        for i in its:
            por_tipo.setdefault(i["tipagem"], []).append(i)
    for tid, its in por_tipo.items():
        for a, b in combinations(its, 2):
            ca, cb = conteudo(a.get("visual")), conteudo(b.get("visual"))
            if not ca or not cb:
                continue
            sim = len(ca & cb) / len(ca | cb)
            if sim >= 0.5:
                avisos.append(f"{tid}: '{a['nome']}' (faixa {a['faixa']}) e '{b['nome']}' (faixa {b['faixa']}) têm "
                              f"visual {sim:.0%} parecido — possível objeto recolorido; cada célula é um conceito novo")
    return erros, avisos, paginas


def montar_prompt(dados, pg, its, total, cabecalho):
    org = dados["organizacao"]
    faixas = sorted({i["faixa"] for i in its})
    tipos = []
    for i in its:
        if tipo_en(i["tipagem"]) not in tipos:
            tipos.append(tipo_en(i["tipagem"]))
    if org == "faixa_por_linha":
        layout = (f"the whole sheet is type {tipos[0]}; each ROW is one tier, from tier {faixas[0]} at the top to tier "
                  f"{faixas[-1]} at the bottom.")
        direcao, rot_tipos = "top to bottom", f"type {tipos[0]}"
    else:
        linhas_ = "; ".join(f"row {r} = {tipo_en(next(i for i in its if i['linha'] == r)['tipagem'])}"
                            for r in range(1, 6))
        layout = (f"each ROW is one elemental type ({linhas_}). Each COLUMN is one tier, from tier {faixas[0]} on the "
                  f"left to tier {faixas[-1]} on the right.")
        direcao, rot_tipos = "left to right", "types " + ", ".join(tipos)
    celulas = []
    for i in its:
        slot = SLOT_EN.get(i.get("slot"))
        meta = f"{tipo_en(i['tipagem'])}, tier {i['faixa']}" + (f", {slot}" if slot else "")
        celulas.append(f"Row {i['linha']}, column {i['coluna']} ({meta}): {i['visual'].strip().rstrip('.')}.")
    trocas = {"{COLECAO}": dados.get("colecao") or "collection", "{PAGINA}": str(pg), "{TOTAL}": str(total),
              "{TIPAGENS}": rot_tipos, "{FAIXA_DE}": str(faixas[0]), "{FAIXA_ATE}": str(faixas[-1]),
              "{LAYOUT}": layout, "{DIRECAO}": direcao, "{PROGRESSAO}": progressao(faixas),
              "{CELULAS}": "\n".join(celulas)}
    texto = cabecalho
    for k, v in trocas.items():
        texto = texto.replace(k, v)
    return texto


def conferencia(dados, pg, its):
    org = dados["organizacao"]
    if org == "faixa_por_linha":
        cab = "| Faixa | " + " | ".join(f"Coluna {c}" for c in range(1, 6)) + " |"
        rot = lambda r: f"**{next(i for i in its if i['linha'] == r)['faixa']}**"  # noqa: E731
    else:
        fx = [next(i for i in its if i["coluna"] == c)["faixa"] for c in range(1, 6)]
        cab = "| Tipagem | " + " | ".join(f"Faixa {f}" for f in fx) + " |"
        rot = lambda r: f"**{comum.TIPOS.get(next(i for i in its if i['linha'] == r)['tipagem'])}**"  # noqa: E731
    linhas_ = [cab, "|---|---|---|---|---|---|"]
    for r in range(1, 6):
        linhas_.append(f"| {rot(r)} | " + " | ".join(i["nome"] for i in its if i["linha"] == r) + " |")
    return f"### Cartela {pg}\n\n" + "\n".join(linhas_)


def main(argv=None):
    argv = argv or sys.argv
    lote = comum.pasta_lote(argv, USO)
    gravar, forcar = "--gravar" in argv, "--forcar" in argv
    caminho = os.path.join(lote, "itens.json")
    dados = comum.ler_json(caminho)
    erros, avisos, paginas = validar(dados)
    categoria = dados.get("categoria", "equipamento") if isinstance(dados, dict) else "equipamento"
    cab_lote = os.path.join(lote, "cabecalho_pagina.txt")
    if categoria != "equipamento" and not os.path.exists(cab_lote):
        erros.append(f"categoria {categoria!r}: escreva <lote>/cabecalho_pagina.txt (mesmos marcadores do "
                     f"templates/itens/PROMPT_PAGINA_ITENS.txt; casos especiais em regras/itens.md §7)")
    for a in avisos:
        print("AVISO " + a)
    for e in erros:
        print("ERRO " + e)
    n_itens = len(dados.get("itens", [])) if isinstance(dados, dict) else 0
    print(f"{len(erros)} erro(s), {len(avisos)} aviso(s) em {n_itens} itens, {len(paginas)} página(s)")
    if not gravar:
        return 1 if erros else 0
    if erros and not forcar:
        print("nada gravado: corrija os erros (ou --forcar para ensaio, com a fila bloqueada)")
        return 1
    if not paginas or (erros and any(len(v) != POR_PAGINA for v in paginas.values())):
        print("nada gravado: as páginas não têm 25 itens")
        return 1
    with open(cab_lote if categoria != "equipamento" else TEMPLATE_PAGINA, encoding="utf-8-sig") as fh:
        cabecalho = fh.read()
    with open(TEMPLATE_SESSAO, encoding="utf-8-sig") as fh:
        sessao = fh.read()
    # anexos copiados para o lote (a sessão de imagem trabalha só dentro dele)
    anexos = []
    for sub, nome in ANEXOS:
        origem, destino = os.path.join(comum.REFS_DIR, sub, nome), os.path.join(lote, "referencias", nome)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        if not os.path.exists(destino) or os.path.getsize(destino) != os.path.getsize(origem):
            shutil.copyfile(origem, destino)
        anexos.append(f"referencias/{nome}")
    total = len(paginas)
    fila_antiga = {f.get("pagina"): f for f in comum.ler_json(os.path.join(lote, "fila.json"), [])
                   if isinstance(f, dict)}
    fila, mapa, conf = [], ["| Cartela | Tipagens | Faixas | Prompt |", "|---|---|---|---|"], []
    estado_base = "bloqueada" if erros else "pronta"
    for pg, its in sorted(paginas.items()):
        texto = montar_prompt(dados, pg, its, total, cabecalho)
        rel = f"prompts/pagina_{pg:02d}.txt"
        comum.gravar_texto(os.path.join(lote, rel), texto)
        estado = estado_base
        velho = fila_antiga.get(pg, {}).get("estado")
        if velho in ("gerada", "pendente de conserto") and os.path.exists(
                os.path.join(lote, "cartelas", f"pagina_{pg:02d}_original.png")):
            estado = velho
        faixas = sorted({i["faixa"] for i in its})
        tipos = []
        for i in its:
            if i["tipagem"] not in tipos:
                tipos.append(i["tipagem"])
        fila.append({"pagina": pg, "estado": estado, "organizacao": dados["organizacao"], "prompt": rel,
                     "anexos": anexos, "salvar": f"cartelas/pagina_{pg:02d}_original.png",
                     "salvar_prompt": f"cartelas/pagina_{pg:02d}.prompt.txt",
                     "tentativas": f"cartelas/pagina_{pg:02d}_vK.png", "faixas": faixas, "tipagens": tipos,
                     "itens": [{"linha": i["linha"], "coluna": i["coluna"], "nome": i["nome"], "arquivo": i["arquivo"]}
                               for i in its]})
        mapa.append(f"| {pg} | {', '.join(comum.TIPOS.get(t, t) for t in tipos)} | {faixas[0]}–{faixas[-1]} | `{rel}` |")
        conf.append(conferencia(dados, pg, its))
    comum.gravar_json(os.path.join(lote, "fila.json"), fila)
    nome_lote = comum.slug(dados["lote"])
    trocas = {"{PASTA_LOTE}": lote, "{SKILL}": comum.SKILL_DIR, "{LOTE}": dados.get("titulo") or dados["lote"],
              "{TOTAL_PAGINAS}": str(total), "{MAPA}": "\n".join(mapa), "{CONFERENCIA}": "\n\n".join(conf)}
    if erros:
        sessao = ("> **BLOQUEADO — ensaio gravado com ERRO de validação. Não gerar.** Rode de novo "
                  "`itens_montar_prompts.py --gravar` depois de corrigir.\n\n") + sessao
    for k, v in trocas.items():
        sessao = sessao.replace(k, v)
    doc = f"PROMPT_ITENS_{nome_lote.upper()}.md"
    comum.gravar_texto(os.path.join(lote, doc), sessao)
    # `arquivo` de cada item no itens.json (só onde falta; o recortador e o cadastrador leem dali)
    faltando = [it for it in dados["itens"] if not it.get("arquivo")]
    for it in faltando:
        it["arquivo"] = arquivo_item(it)
    if faltando:
        comum.gravar_json(caminho, dados)
    print(f"gravado: {total} prompt(s) em prompts/, fila.json ({estado_base}), {doc}, referencias/"
          + (f", arquivo em {len(faltando)} item(ns)" if faltando else ""))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
