# -*- coding: utf-8 -*-
"""Valida o roster de NPC e monta as páginas da sessão de imagem (sem banco, sem rede).

Uso:
  python npc_montar_prompts.py <lote>                      só valida (roster + visual/parte_*.json) e mostra os erros
  python npc_montar_prompts.py <lote> --gravar             valida e, sem erro, grava prompts/, referencias/, fila.json
                                                           e PROMPT_IMAGEM_<LOTE>.md
  python npc_montar_prompts.py <lote> --parte visual/parte_A.json   valida só essa parte (conferência do agente)
  python npc_montar_prompts.py <lote> --contrato           grava <lote>/CONTRATO-VISUAL.md (contrato dos agentes)

Entrada: <lote>/tema.json e <lote>/roster.json (formato em modos/personagens.md). Regras: regras/npc-personagens.md.
"""
import os
import re
import shutil
import sys

sys.dont_write_bytecode = True  # nada é gravado dentro da skill (nem __pycache__)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

USO = __doc__
NPC_TPL = os.path.join(comum.TEMPLATES_DIR, "npc")
REFS_NPC = ["estilo_pagina_1.png", "prisions.png", "beleza_marta.png", "beleza_elira.png"]  # ordem fixa (regra §5)
FORMULA = "vivos (só a cor da íris, sem brilho)"
NUM = {2: "duas", 3: "três", 4: "quatro"}
MIN_LINHA, MAX_LINHA = 750, 980
PROIBIDAS = ["cicatriz", "olheira", "desgrenhad", "cansad", "neon", "reluzente", "refletiv", "lingerie", "transparen",
             "seminu", "narraris", "cibern", "espada", "machado", "adaga", "armadura", "pele de animal", "pele de raposa",
             "pele de urso", "pele de lobo", "brilhante", "luminos", "tatuagem que brilha", "fantasia de viking",
             "roupa de camponês", "roupa de camponesa"]
PROIBIDAS_PALAVRA = ["nua", "nu", "aura", "auras", "runa", "runas", "viking", "ruga", "rugas", "magia", "mago", "maga",
                     "monstro", "monstros", "bicho", "bichos", "criatura", "criaturas", "tier"]
PALAVRA_ARMA = ["arma", "armas", "pistola", "rifle", "faca", "punhal"]
TOM_FEMININO = ("meiga", "doce", "delicada", "romântica", "sensual", "feminina")
NOME_OK = re.compile(r"^[A-Za-zÁÂÃÀÉÊÍÓÔÕÚÇáâãàéêíóôõúç' -]+$")


# ---------------------------------------------------------------- template

def blocos_template():
    texto = open(os.path.join(NPC_TPL, "PREAMBULO_NPC.md"), encoding="utf-8").read()
    blocos = dict(re.findall(r"```text ([\w-]+)\n(.*?)\n```", texto, re.S))
    for k in ("preambulo", "cabecalho", "multietnico-traco", "multietnico-moda"):
        if k not in blocos:
            sys.exit(f"template quebrado: falta o bloco '{k}' em templates/npc/PREAMBULO_NPC.md")
    return blocos


def preambulo_do_tema(tema, blocos):
    var = tema.get("variante", "tema")
    if var not in ("tema", "multietnico"):
        sys.exit(f"tema.json: variante '{var}' inválida (tema | multietnico)")
    traco = tema.get("traco") or (blocos["multietnico-traco"] if var == "multietnico" else None)
    moda = tema.get("moda") or (blocos["multietnico-moda"] if var == "multietnico" else None)
    curto = tema.get("traco_curto") or ("cada um de uma etnia diferente, com o traço da própria etnia"
                                        if var == "multietnico" else None)
    faltam = [k for k, v in (("traco", traco), ("moda", moda), ("traco_curto", curto)) if not v]
    if faltam:
        sys.exit(f"tema.json: faltam {', '.join(faltam)} (variante '{var}')")
    pre = blocos["preambulo"].replace("[TEMA-TRAÇO]", traco.strip()).replace("[TEMA-MODA]", moda.strip())
    if tema.get("tirar_snow"):
        pre = pre.replace("no floor, snow, scenery", "no floor, scenery")
    cab = blocos["cabecalho"].replace("[TEMA-CURTO]", curto.strip())
    if "[TEMA-" in pre or "[TEMA-" in cab:
        sys.exit("placeholder [TEMA-…] sobrou no preâmbulo")
    return pre, cab


# ---------------------------------------------------------------- roster

def genero(p):
    g = comum.norm(str(p.get("genero", ""))).strip()[:1]
    return {"f": "F", "m": "M", "h": "M"}.get(g)


def carregar(lote):
    tema = comum.ler_json(os.path.join(lote, "tema.json"))
    roster = comum.ler_json(os.path.join(lote, "roster.json"))
    paginas = roster.get("paginas") if isinstance(roster, dict) else None
    if not paginas:
        sys.exit("roster.json: falta a lista 'paginas'")
    return tema, roster, paginas


def visuais_das_partes(lote, so=None):
    """visual/parte_*.json = lista {"nome", "visual"} escrita pelos agentes. Retorna {nome: (visual, arquivo)}."""
    pasta = os.path.join(lote, "visual")
    arquivos = [so] if so else (sorted(f for f in os.listdir(pasta) if f.startswith("parte_") and f.endswith(".json"))
                                if os.path.isdir(pasta) else [])
    out, erros = {}, []
    for f in arquivos:
        cam = f if os.path.isabs(f) else os.path.join(lote, f) if so else os.path.join(pasta, f)
        nome_arq = os.path.basename(cam)
        try:
            itens = comum.ler_json(cam)
        except Exception as ex:  # agente ainda escrevendo
            erros.append(f"{nome_arq}: ilegível agora ({ex})")
            continue
        for v in itens:
            n = v.get("nome")
            if n in out:
                erros.append(f"{nome_arq}: {n} já tem visual em {out[n][1]}")
            out[n] = (v.get("visual", ""), nome_arq)
    return out, erros


def checar_linha(p, visual):
    """Erros de uma linha de pessoa (regra §6–§8)."""
    e, t = [], visual or ""
    tl = t.lower()
    g = genero(p)
    if not t:
        return ["sem visual"]
    art = "cria a " if g == "F" else "cria o "
    abertura = f"{art}{p['nome']}, {p['idade']} anos, "
    if not t.startswith(abertura):
        e.append(f'abertura fora do formato "{abertura}<papel>."')
    if "\n" in t:
        e.append("quebra de linha no visual")
    if not MIN_LINHA <= len(t) <= MAX_LINHA:
        e.append(f"tamanho {len(t)} fora de {MIN_LINHA}–{MAX_LINHA}")
    numeros = re.findall(r"\d+", t)
    if numeros != [str(p["idade"])]:
        e.append(f"número além da idade: {', '.join(x for x in numeros if x != str(p['idade'])) or 'idade repetida'}")
    if FORMULA not in t:
        e.append(f'falta a frase literal "{FORMULA}"')
    molde = "Beleza de top model " if g == "F" else "Beleza de modelo masculino "
    if molde not in t:
        e.append(f'falta "{molde.strip()} <subtipo>"')
    elif p.get("subtipo") and f"{molde}{p['subtipo']}".lower() not in tl:
        e.append(f'subtipo do roster ausente depois de "{molde.strip()}" ({p["subtipo"]})')
    if p.get("olho") and p["olho"].lower() not in tl:
        e.append(f"cor do olho do roster ausente ({p['olho']})")
    if p.get("cabelo") and p["cabelo"].lower() not in tl:
        e.append(f"cor do cabelo do roster ausente ({p['cabelo']})")
    if len(re.findall(r"ESQUERD|DIREIT", t)) < 2:
        e.append("menos de duas marcas com LADO em MAIÚSCULAS")
    pr = p.get("prisions")
    if pr:
        alvo = f"{NUM.get(pr.get('n'), '?')} prisions {pr.get('cor', '')}".strip().lower()
        if alvo not in tl:
            e.append(f"prisions fora do roster ({alvo})")
    elif not re.search(r"\b(duas|três|quatro) prisions\b", tl):
        e.append("prisions fora do formato '<duas|três|quatro> prisions <cor>'")
    if "expressão" not in tl:
        e.append("falta a expressão")
    if "escrit" in tl and "sem nada escrit" not in tl:
        e.append("texto escrito em objeto (use 'sem nada escrito')")
    # palavras proibidas: fora da frase de abertura (nome, idade, papel: "criador de monstros de neve" pode)
    m = re.match(r"cria [ao] .*?, \d+ anos, (.*?)\. ", t)
    papel_linha = m.group(1) if m else ""
    if m and comum.norm(p.get("papel", "")) not in comum.norm(papel_linha):
        e.append(f"aviso: papel do roster escrito diferente na abertura ({p.get('papel')})")
    corpo = tl[m.end():] if m else tl.replace(p["nome"].lower(), " ")
    for x in PROIBIDAS:
        if x in corpo:
            e.append(f"palavra proibida: {x}")
    lista = PROIBIDAS_PALAVRA + ([] if p.get("arma") else PALAVRA_ARMA)
    for x in lista:
        if re.search(rf"(?<![a-zà-ú]){x}(?![a-zà-ú])", corpo):
            e.append(f"palavra proibida: {x}")
    if g == "F" and not any(x in tl for x in TOM_FEMININO):
        e.append("mulher sem tom meigo/sensual (" + "/".join(TOM_FEMININO) + ")")
    return e


def expressao_inicio(t):
    m = re.search(r"Expressão\s+(.*)$", t or "")
    return " ".join(re.findall(r"[a-zà-ú]+", m.group(1).lower())[:3]) if m else None


def validar(lote, tema, paginas, partes):
    erros, avisos, vistos, nums = [], [], {}, set()
    existentes_cam = os.path.join(lote, "nomes_npc_existentes.json")
    existentes = {comum.norm(x) for x in comum.ler_json(existentes_cam, [])}
    if not os.path.exists(existentes_cam):
        avisos.append("sem nomes_npc_existentes.json (lista do usuário): nome único só dentro do lote")
    primeiros, inicios = {}, {}
    for pg in paginas:
        n = pg.get("pagina")
        if not isinstance(n, int) or n < 1 or n in nums:
            erros.append(f"página {n!r}: número inválido ou repetido")
            continue
        nums.add(n)
        rot = f"p{n:03d}"
        pessoas = pg.get("pessoas") or []
        if pg.get("tipo") == "atualizar":  # prompt escrito à mão (templates/npc/ATUALIZAR_PERSONAGEM.md)
            anexos = pg.get("anexos") or []
            if not os.path.exists(os.path.join(lote, "prompts", f"atualizar_{n:03d}.txt")):
                erros.append(f"{rot}: página de atualizar sem prompts/atualizar_{n:03d}.txt")
            def existe(a):  # referências fixas da skill são copiadas no --gravar
                return os.path.exists(os.path.join(lote, a)) or a.replace("\\", "/") in [f"referencias/{f}" for f in REFS_NPC]
            if not 1 <= len(anexos) <= comum.MAX_ANEXOS or not all(existe(a) for a in anexos):
                erros.append(f"{rot}: 'anexos' da página de atualizar: 1 a {comum.MAX_ANEXOS} arquivos que existam no lote")
            continue
        if len(pessoas) != 3:
            erros.append(f"{rot}: {len(pessoas)} pessoas (tem de ser 3)")
        gs = [genero(p) for p in pessoas]
        if sorted(gs, key=str) != ["F", "F", "M"]:
            erros.append(f"{rot}: página tem de ser 2 mulheres + 1 homem (veio {gs})")
        ref = pg.get("rosto_ref")
        if ref and (ref.get("coluna") not in (1, 2, 3) or not ref.get("arquivo")
                    or not os.path.exists(os.path.join(lote, ref["arquivo"]))):
            erros.append(f"{rot}: rosto_ref precisa de coluna 1–3 e de um arquivo que exista na pasta do lote")
        for campo, rotulo in (("olho", "cor de olho"), ("estilo_roupa", "estilo de roupa")):
            vals = [comum.norm(p[campo]) for p in pessoas if p.get(campo)]
            if len(vals) != len(set(vals)):
                erros.append(f"{rot}: {rotulo} repetido na página")
        cab = [comum.norm(p["cabelo"]) for p in pessoas if p.get("cabelo")]
        if len(cab) != len(set(cab)):
            avisos.append(f"{rot}: cor de cabelo repetida na página")
        for c, p in enumerate(pessoas, 1):
            nome = str(p.get("nome", "")).strip()
            r = f"{rot}c{c} {nome or '?'}"
            faltam = [k for k in ("nome", "genero", "idade", "papel", "subtipo") if p.get(k) in (None, "")]
            if faltam:
                erros.append(f"{r}: faltam {', '.join(faltam)}")
                continue
            if re.search(r"\d|\btier\b", str(p["papel"]), re.I):
                erros.append(f"{r}: papel do roster com número ou 'Tier' (nenhum número além da idade, regra §6)")
            if not isinstance(p["idade"], int) or p["idade"] < 18:
                erros.append(f"{r}: idade {p['idade']!r} (método de beleza = só adultos, regra §8)")
            if not NOME_OK.match(nome):
                erros.append(f"{r}: nome com caractere/diacrítico estrangeiro (regra §10)")
            k = comum.norm(nome)
            if k in vistos:
                erros.append(f"{r}: nome repetido no lote ({vistos[k]})")
            vistos[k] = rot
            if k in existentes:
                erros.append(f"{r}: nome já existe (nomes_npc_existentes.json)")
            pn = k.split()[0]
            if pn in primeiros:
                avisos.append(f"{r}: primeiro nome igual ao de {primeiros[pn]}")
            primeiros.setdefault(pn, r)
            visual = p.get("visual") or partes.get(nome, ("", ""))[0]
            p["_visual"] = visual
            for x in checar_linha(p, visual):
                if x.startswith("aviso: "):
                    avisos.append(f"{r}: {x[7:]}")
                else:
                    erros.append(f"{r}: {x}")
            ini = expressao_inicio(visual)
            if ini and ini in inicios:
                avisos.append(f"{r}: expressão começa igual à de {inicios[ini]} ('{ini}')")
            if ini:
                inicios.setdefault(ini, r)
    for nome in partes:
        if comum.norm(nome) not in vistos:
            erros.append(f"visual de '{nome}' ({partes[nome][1]}) não é de ninguém do roster")
    return erros, avisos


# ---------------------------------------------------------------- gravar

def texto_pagina(pre, cab, pg):
    linhas = [f"Coluna {c}: {p['_visual']}" for c, p in enumerate(pg["pessoas"], 1)]
    ref = pg.get("rosto_ref")
    if ref:  # refação fiel (regra §11): tile do rosto aprovado como 5º anexo + DNA do rosto em inglês
        dna = f" Face DNA: {ref['dna'].strip()}" if ref.get("dna") else ""
        linhas.append(f"Column {ref['coluna']}: same person as reference image 5.{dna}")
    return pre + "\n\n" + cab.replace("{NNN}", f"{pg['pagina']:03d}") + "\n" + "\n".join(linhas) + "\n"


def versoes_prompt(pp, n):
    return sorted((int(m.group(1)), f) for f in (os.listdir(pp) if os.path.isdir(pp) else [])
                  for m in [re.match(rf"pagina_{n:03d}_v(\d+)\.txt$", f)] if m)


def prompt_atual(lote, n):
    v = versoes_prompt(os.path.join(lote, "prompts"), n)
    return f"prompts/{v[-1][1]}" if v else f"prompts/pagina_{n:03d}.txt"


def gravar_prompt(lote, n, texto):
    """Não sobrescreve página que já tem imagem. Se a imagem foi reprovada (_ruimN), grava o próximo _vK."""
    pp = os.path.join(lote, "prompts")
    base = os.path.join(pp, f"pagina_{n:03d}.txt")
    imagem = os.path.join(lote, "paginas", f"pagina_{n:03d}.png")
    versoes = versoes_prompt(pp, n)
    atual = os.path.join(pp, versoes[-1][1]) if versoes else base
    if os.path.exists(atual) and open(atual, encoding="utf-8").read() == texto:
        return "igual"
    if os.path.exists(imagem):
        return "tem imagem (prompt mantido; para refazer, renomeie a imagem para _ruimN)"
    ruins = [f for f in os.listdir(os.path.dirname(imagem))
             if f.startswith(f"pagina_{n:03d}_ruim")] if os.path.isdir(os.path.dirname(imagem)) else []
    if os.path.exists(base) and ruins:
        k = (versoes[-1][0] if versoes else 1) + 1
        comum.gravar_texto(os.path.join(pp, f"pagina_{n:03d}_v{k}.txt"), texto)
        return f"_v{k}"
    comum.gravar_texto(base, texto)
    return "gravada"


def gravar(lote, tema, paginas, pre, cab):
    lote_slug = comum.slug(tema.get("lote") or os.path.basename(lote)) or "lote"
    refs = os.path.join(lote, "referencias")
    os.makedirs(refs, exist_ok=True)
    for f in REFS_NPC:
        src = os.path.join(comum.REFS_DIR, "personagens", f)
        if not os.path.exists(src):
            sys.exit(f"referência da skill não encontrada: {src}")
        shutil.copy2(src, os.path.join(refs, f))
    os.makedirs(os.path.join(lote, "paginas"), exist_ok=True)
    fila, resumo = [], {}
    for pg in sorted(paginas, key=lambda x: x["pagina"]):
        n = pg["pagina"]
        anexos = [f"referencias/{f}" for f in REFS_NPC]
        gerada = os.path.exists(os.path.join(lote, "paginas", f"pagina_{n:03d}.png"))
        if pg.get("tipo") == "atualizar":
            fila.append({"pagina": n, "piloto": False, "tipo": "atualizar", "estado": "gerada" if gerada else "pronta",
                         "prompt": f"prompts/atualizar_{n:03d}.txt", "anexos": pg["anexos"],
                         "salvar": f"paginas/pagina_{n:03d}.png", "pessoas": [p.get("nome") for p in pg["pessoas"]]})
            continue
        ref = pg.get("rosto_ref")
        if ref:
            anexos.append(ref["arquivo"].replace("\\", "/"))
        st = gravar_prompt(lote, n, texto_pagina(pre, cab, pg))
        resumo[st] = resumo.get(st, 0) + 1
        fila.append({"pagina": n, "piloto": n <= 4,
                     "estado": "gerada" if gerada else "pronta",
                     "prompt": prompt_atual(lote, n),
                     "anexos": anexos, "salvar": f"paginas/pagina_{n:03d}.png",
                     "pessoas": [p["nome"] for p in pg["pessoas"]]})
    comum.gravar_json(os.path.join(lote, "fila.json"), fila)
    nums = [x["pagina"] for x in fila]
    tpl = open(os.path.join(NPC_TPL, "PROMPT_IMAGEM_NPC.md"), encoding="utf-8").read()
    troca = {"{PASTA_LOTE}": lote, "{SKILL}": comum.SKILL_DIR, "{LOTE}": lote_slug,
             "{TITULO}": tema.get("titulo") or lote_slug, "{TOTAL}": str(len(nums)),
             "{PRIMEIRA}": f"{min(nums):03d}" if nums else "001", "{ULTIMA}": f"{max(nums):03d}" if nums else "001"}
    for k, v in troca.items():
        tpl = tpl.replace(k, v)
    nome_prompt = f"PROMPT_IMAGEM_{lote_slug.upper()}.md"
    comum.gravar_texto(os.path.join(lote, nome_prompt), tpl)
    print(f"prompts: {resumo}")
    print(f"fila.json: {len(fila)} páginas; referencias/: {len(REFS_NPC)} anexos; {nome_prompt}")


def gravar_contrato(lote, tema):
    tpl = open(os.path.join(NPC_TPL, "CONTRATO-VISUAL-NPC.md"), encoding="utf-8").read()
    for k, v in {"{PASTA_LOTE}": lote, "{SKILL}": comum.SKILL_DIR,
                 "{TITULO}": tema.get("titulo") or os.path.basename(lote)}.items():
        tpl = tpl.replace(k, v)
    comum.gravar_texto(os.path.join(lote, "CONTRATO-VISUAL.md"), tpl)
    os.makedirs(os.path.join(lote, "visual"), exist_ok=True)
    print("CONTRATO-VISUAL.md gravado; partes dos agentes em visual/parte_<LETRA>.json")


def main():
    lote = comum.pasta_lote(sys.argv, USO)
    args = sys.argv[1:]
    tema, _roster, paginas = carregar(lote)
    if "--contrato" in args:
        gravar_contrato(lote, tema)
        return
    so = args[args.index("--parte") + 1] if "--parte" in args else None
    partes, err_partes = visuais_das_partes(lote, so)
    pre, cab = preambulo_do_tema(tema, blocos_template())
    erros, avisos = validar(lote, tema, paginas, partes)
    if so:  # só as pessoas dessa parte
        meus = {comum.norm(n) for n in partes}
        erros = [x for x in erros if any(m in comum.norm(x) for m in meus)]
    erros = err_partes + erros
    for x in avisos:
        print(f"aviso: {x}")
    for x in erros:
        print(f"ERRO: {x}")
    total = sum(len(pg.get("pessoas") or []) for pg in paginas if pg.get("tipo") != "atualizar")
    print(f"{total} pessoas, {len(paginas)} páginas, {len(erros)} erros, {len(avisos)} avisos")
    if erros:
        sys.exit(1)
    if "--gravar" in args and not so:
        gravar(lote, tema, paginas, pre, cab)
    elif not so:
        print("validado (nada gravado; use --gravar)")


if __name__ == "__main__":
    main()
