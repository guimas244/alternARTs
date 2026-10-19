# -*- coding: utf-8 -*-
"""Valida fichas de monstros/fusões contra a entrada.json e as regras de nome, descrição e bloco.

    python valida_fichas.py <pasta_do_lote> --arquivo fichas_claude/parte_A.json   # uma parte (agente)
    python valida_fichas.py <pasta_do_lote>                                        # todas as partes (revisão cruzada)

Com --arquivo, a parte é conferida contra as outras partes do lote (nome repetido, rosto repetido na cartela, molde).
Grava <parte>_validacao.json (ou <lote>/validacao/fichas.json) e sai com código 1 se houver erro.
Regras: regras/fichas-nomes-descricoes.md e regras/fusoes.md.
"""
import difflib
import glob
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

USO = "uso: python valida_fichas.py <pasta_do_lote> [--arquivo <parte.json>]"
norm = comum.norm

PROIBIDAS = re.compile(r"\b(fusao|fusoes|sacrificio|sacrificios|fundid\w*|tier|tiers|nivel|niveis|patamar|patamares|pritz|"
                       r"mitic\w*|variacao|variacoes|variante|variantes)\b")
SISTEMAS = re.compile(r"\b(narraris|jornadas?|raids?|expedic\w*|missao|missoes|essencias?|ritua\w*|centro de cura|passe|"
                      r"mercador\w*|ranking)\b")
FILMES = re.compile(r"\b(freddy|krueger|jason|voorhees|pennywise|dracula|nosferatu|frankenstein|samara|sadako|hellraiser|"
                    r"pinhead|xenomorfos?|imhotep)\b")
_COR = r"(azu|verde|vermelh|dourad|amarel|rox|pret|branc|rosad|laranj|pratead|cinz|negr|escarlat|violet|lilas|turques)\w*"
FISICO = re.compile(r"\b(pele|peles|armadura|armaduras|luvas?|roupas?|jaleco|vestido|uniforme|olhos? " + _COR + r"|olhos? de cor|"
                    r"escamas? " + _COR + r"|pelagem " + _COR + r"|penas? " + _COR + r")\b")
COMUNS = ["n", "nome", "humanoide", "paleta", "anatomia", "rosto", "marcas_poder", "brilho", "temperamento", "conceito",
          "marca_da_habilidade", "descricao", "arquivo", "visual"]
POR_BLOCO = {"N": ["arquetipo"], "L": ["tema", "arquetipo"], "V": ["epiteto", "mantem", "muda"],
             "F": ["herda", "ascensao"], "X": ["herda", "ascensao"], "A": ["herda", "ascensao"]}
MARCAS = {1: (0, 2), 2: (0, 2), 3: (1, 2), 4: (1, 2), 5: (2, 3), 6: (2, 3), 7: (3, 4), 8: (3, 4), 9: (4, 5), 10: (4, 5)}
FIXOS = ("slot", "cartela", "linha", "coluna", "bloco", "tier", "tipo1", "tipo2")


def faixa_marcas(bloco, tier):
    a, b = MARCAS[tier]
    return (a + 1, b + 1) if bloco in ("F", "X", "A") else (a, b)


def sem_numero(nome):
    return re.sub(r"\s*#\d+\s*$", "", nome or "").strip()


def ler(caminho):
    d = comum.ler_json(caminho)
    return d["monstros"] if isinstance(d, dict) else d


def partes_do_lote(lote):
    r = {}
    for g in sorted(glob.glob(os.path.join(lote, "fichas_claude", "parte_*.json"))):
        if g.endswith("_validacao.json"):
            continue
        try:
            r[os.path.abspath(g)] = [f for f in ler(g) if isinstance(f, dict)]
        except Exception as ex:
            print(f"  aviso: não consegui ler {g}: {ex}")
    return r


def resolve(lote, caminho):
    for c in (caminho, os.path.join(lote, caminho)):
        if os.path.isfile(c):
            return os.path.abspath(c)
    print(f"parte não encontrada: {caminho}")
    sys.exit(2)


def palavras(nd):
    return set(re.findall(r"[a-z]{4,}", nd))


def cita(nd, nome):
    n = norm(sem_numero(nome)).strip()
    return len(n) >= 3 and re.search(r"(?<![a-z])" + re.escape(n) + r"(?![a-z])", nd) is not None


def main():
    lote = comum.pasta_lote(sys.argv, USO)
    arquivo = None
    if "--arquivo" in sys.argv:
        i = sys.argv.index("--arquivo")
        if i + 1 >= len(sys.argv):
            print(USO)
            sys.exit(2)
        arquivo = resolve(lote, sys.argv[i + 1])
    try:
        entrada = {e["n"]: e for e in comum.ler_json(os.path.join(lote, "entrada.json"))}
    except FileNotFoundError:
        print("falta entrada.json: rode antes  python montar_entrada.py <pasta_do_lote>")
        sys.exit(2)
    existentes = comum.nomes_existentes()
    exist_uma = {x for x in existentes if " " not in x and "-" not in x}
    exist_multi = [x for x in existentes if (" " in x or "-" in x) and len(x) >= 6]

    partes = partes_do_lote(lote)
    if arquivo:
        try:
            alvo = [f for f in ler(arquivo) if isinstance(f, dict)]
        except ValueError as ex:
            print(f"{arquivo} não é JSON válido: {ex}")
            sys.exit(2)
        partes[arquivo] = alvo
    # visão da leva: uma ficha por n (a do alvo manda)
    leva = {}
    for caminho, fs in partes.items():
        for f in fs:
            if caminho == arquivo or f.get("n") not in leva:
                leva[f.get("n")] = f
    if not arquivo:
        alvo = sorted((f for f in leva.values() if isinstance(f.get("n"), int)), key=lambda f: f["n"])
        ns_dup = Counter(f.get("n") for fs in partes.values() for f in fs)
    else:
        ns_dup = Counter(f.get("n") for f in alvo)
    ns_alvo = {f.get("n") for f in alvo}
    nomes_leva = Counter(norm(str(f.get("nome", ""))).strip() for f in leva.values() if f.get("nome"))

    erros, avisos, descs = [], [], {}
    for n, q in ns_dup.items():
        if q > 1:
            erros.append(f"n {n} aparece em {q} fichas" + ("" if arquivo else " (partes diferentes)"))

    for f in alvo:
        tag = f"#{f.get('n')} {f.get('nome') or f.get('epiteto') or ''}".strip()
        e = entrada.get(f.get("n"))
        if not e:
            erros.append(f"{tag}: n inexistente na entrada"); continue
        b = e["bloco"]
        falta = [c for c in COMUNS + POR_BLOCO[b] if c not in f or f[c] in (None, "")]
        if falta:
            erros.append(f"{tag}: faltam campos {falta}"); continue
        for k in FIXOS:
            if f.get(k) != e.get(k):
                erros.append(f"{tag}: {k} = {f.get(k)!r}, entrada diz {e.get(k)!r} (rode compor_fichas.py)")
        # humanoide
        if not isinstance(f["humanoide"], bool):
            erros.append(f"{tag}: 'humanoide' tem que ser true/false")
        elif f["humanoide"] and not str(f.get("classe") or "").strip():
            erros.append(f"{tag}: humanoide precisa de 'classe'")
        if e.get("humanoide_previsto") and f["humanoide"] is not True:
            erros.append(f"{tag}: o plano pede HUMANOIDE nesta célula")
        # nome
        nome = str(f["nome"]).strip()
        nn = norm(nome)
        if len(nome) > 60:
            erros.append(f"{tag}: nome com mais de 60 caracteres")
        if nn in existentes:
            erros.append(f"{tag}: nome já existe no jogo (dados/nomes_existentes.json)")
        if nomes_leva[nn] > 1:
            erros.append(f"{tag}: nome repetido dentro da leva")
        if re.search(r"[\d#]", nome):
            erros.append(f"{tag}: nome com número ou #")
        if b == "V":
            o = sem_numero(e["original"]["nome"])
            ep = str(f["epiteto"]).strip()
            if nome != f"{o} {ep}" or not ep:
                erros.append(f"{tag}: variação = nome do original '{o}' + epíteto (rode compor_fichas.py)")
            if len(ep.split()) > 3:
                erros.append(f"{tag}: epíteto com mais de 3 palavras")
            if norm(ep) in existentes:
                erros.append(f"{tag}: epíteto '{ep}' é nome de monstro no jogo")
            for pal in sorted(palavras(norm(ep)) & exist_uma):
                erros.append(f"{tag}: epíteto usa '{pal}', que é nome de monstro no jogo")
        else:
            if " " in nome:
                avisos.append(f"{tag}: nome próprio costuma ser de UMA palavra")
            if b in ("F", "X", "A"):
                for i in e["ingredientes"]:
                    for ref in [i["nome"]] + list(i.get("linhagem") or []):
                        s4 = comum.seq4(nome, ref)
                        if s4:
                            erros.append(f"{tag}: nome carrega pedaço de '{ref}' ({s4})")
        # arquivo
        esperado = comum.arquivo_recorte(e["n"], e["tier"], nome)
        if f["arquivo"] != esperado:
            erros.append(f"{tag}: arquivo deveria ser {esperado} (rode compor_fichas.py)")
        # paleta, ciano, marcas
        if not isinstance(f["paleta"], list) or len(f["paleta"]) != 2 or not all(str(x).strip() for x in f["paleta"]):
            erros.append(f"{tag}: paleta precisa de exatamente 2 cores [escura, clara]")
        tudo = norm(" ".join(map(str, f["paleta"] if isinstance(f["paleta"], list) else [f["paleta"]]))
                    + " " + str(f["visual"]) + " " + str(f["brilho"]))
        if re.search(r"\b(ciano|cyan)\b", tudo) and "eletrico" not in (e["tipo1"], e["tipo2"]):
            erros.append(f"{tag}: ciano só em tipo elétrico")
        mp = f["marcas_poder"] if isinstance(f["marcas_poder"], list) else None
        lim = faixa_marcas(b, e["tier"])
        if mp is None or not lim[0] <= len(mp) <= lim[1]:
            erros.append(f"{tag}: marcas_poder precisa ter de {lim[0]} a {lim[1]} itens (tier {e['tier']}, bloco {b})")
        # bloco
        if b in ("F", "X", "A"):
            nomes_ing = [i["nome"] for i in e["ingredientes"]]
            if not isinstance(f["herda"], dict) or sorted(f["herda"]) != sorted(nomes_ing) \
                    or not all(str(v).strip() for v in f["herda"].values()):
                erros.append(f"{tag}: 'herda' precisa de uma entrada por pai, com o nome exato: {nomes_ing}")
            if len(str(f["ascensao"]).strip()) < 20:
                erros.append(f"{tag}: 'ascensao' precisa dizer o que a torna um degrau acima dos pais")
        if b == "L" and len(str(f["tema"]).strip()) < 3:
            erros.append(f"{tag}: prodígio precisa de 'tema'")
        if b == "N":
            ev = e.get("evolucao") or {}
            ant_nome, tem_ant = None, bool(ev.get("anterior") or ev.get("externo"))
            if ev.get("externo"):
                ant_nome = ev["externo"]["nome"]
            elif ev.get("anterior"):
                ant_nome = str((leva.get(ev["anterior"]) or {}).get("nome") or "").strip() or None
            if tem_ant:
                an = " ".join(norm(str(f["anatomia"])).split())
                if ant_nome:
                    alvos = {norm(f"evolucao {art} {x}") for art in ("do", "da") for x in (ant_nome, sem_numero(ant_nome))}
                    if not any(re.match(re.escape(x) + r"(?![a-z0-9])", an) for x in alvos):
                        erros.append(f"{tag}: estágio de evolução — a anatomia tem que começar com "
                                     f"\"Evolução do {ant_nome}.\" ou \"Evolução da {ant_nome}.\"")
                    if norm(sem_numero(nome)).strip() == norm(sem_numero(ant_nome)).strip():
                        erros.append(f"{tag}: nome igual ao do antecessor '{ant_nome}' — a evolução tem nome próprio")
                else:
                    if not re.match(r"evolucao d[oa] ", an):
                        erros.append(f"{tag}: estágio de evolução — a anatomia tem que começar com \"Evolução do/da <nome>.\"")
                    avisos.append(f"{tag}: ficha do antecessor n {ev['anterior']} ainda não existe — o nome na anatomia "
                                  f"não foi conferido (a revisão cruzada confere)")
        # descrição
        d = str(f["descricao"]).strip()
        nd = norm(d)
        frases = [x for x in re.split(r"[.!?]+", d) if x.strip()]
        if not 4 <= len(frases) <= 6:
            erros.append(f"{tag}: descrição com {len(frases)} frases (4 a 6)")
        if not 300 <= len(d) <= 620:
            avisos.append(f"{tag}: descrição com {len(d)} caracteres (alvo ~440, faixa 300–620)")
        if re.search(r"\d", d):
            erros.append(f"{tag}: descrição com algarismo (escreva por extenso)")
        for rx, oque in ((PROIBIDAS, "palavra proibida"), (SISTEMAS, "sistema do jogo"), (FISICO, "aparência (vai no visual)")):
            m = rx.search(nd)
            if m:
                erros.append(f"{tag}: descrição com {oque} ({m.group(0)})")
        for campo, rot in ((nd, "descrição"), (nn, "nome")):
            m = FILMES.search(campo)
            if m:
                erros.append(f"{tag}: {rot} cita filme/personagem ({m.group(0)}) — use só o arquétipo")
        if nd.startswith("mede"):
            erros.append(f"{tag}: descrição começa com 'Mede'")
        cit = [nome]
        if b == "V":
            cit.append(e["original"]["nome"])
        for i in e.get("ingredientes") or []:
            cit += [i["nome"]] + list(i.get("linhagem") or [])
        for x in dict.fromkeys(cit):
            if cita(nd, x):
                erros.append(f"{tag}: descrição cita o nome '{x}'")
        for pal in sorted(palavras(nd) & exist_uma):
            erros.append(f"{tag}: descrição usa '{pal}', que é nome de monstro no jogo — troque a palavra")
        pad = " " + " ".join(re.findall(r"[a-z]+", nd)) + " "
        for x in exist_multi:
            xx = " " + " ".join(re.findall(r"[a-z]+", x)) + " "
            if xx in pad:
                erros.append(f"{tag}: descrição contém '{x}', que é nome de monstro no jogo")

    # por cartela (visão da leva, com o alvo por cima)
    cartelas_alvo = {entrada[n]["cartela"] for n in ns_alvo if n in entrada}
    por_cart = defaultdict(list)
    for f in leva.values():
        if f.get("n") in entrada:
            por_cart[entrada[f["n"]]["cartela"]].append(f)
    for c in sorted(cartelas_alvo):
        fs = por_cart[c]
        blocos = {e["bloco"] for e in entrada.values() if e["cartela"] == c}
        cheia = len(fs) == sum(1 for e in entrada.values() if e["cartela"] == c)
        h = sum(f.get("humanoide") is True for f in fs)
        if blocos <= {"N", "L"}:
            if h > 2 or (cheia and h < 1):
                erros.append(f"cartela {c:03d}: {h} humanoides (blocos N/L pedem 1 ou 2)")
        elif h > 2:
            avisos.append(f"cartela {c:03d}: {h} humanoides (o normal é até 2)")
        rostos = {}
        for f in sorted(fs, key=lambda f: f["n"]):
            r = norm(str(f.get("rosto", ""))).strip()
            if not r:
                continue
            if r in rostos:
                erros.append(f"cartela {c:03d}: #{f['n']} tem o mesmo rosto de #{rostos[r]}")
            rostos[r] = f["n"]
        if "L" in blocos:
            temas = {norm(str(f.get("tema", ""))).strip() for f in fs if entrada[f["n"]]["bloco"] == "L"}
            if len(temas) > 1:
                erros.append(f"cartela {c:03d}: as fichas do prodígio têm que ter o MESMO 'tema' ({sorted(temas)})")

    # molde: semelhança entre descrições (alvo × leva) e trecho de 5 palavras
    for f in leva.values():
        if isinstance(f.get("descricao"), str) and f.get("n") in entrada:
            descs[f["n"]] = (f"#{f['n']} {f.get('nome', '')}", norm(f["descricao"]))
    ns = sorted(descs)
    for i, a in enumerate(ns):
        for bn in ns[i + 1:]:
            if a not in ns_alvo and bn not in ns_alvo:
                continue
            sm = difflib.SequenceMatcher(None, descs[a][1], descs[bn][1], autojunk=False)
            if sm.real_quick_ratio() >= 0.5 and sm.quick_ratio() >= 0.5 and sm.ratio() >= 0.5:
                erros.append(f"{descs[a][0]} x {descs[bn][0]}: descrições parecidas demais ({sm.ratio():.2f})")
    cinco, onde = Counter(), defaultdict(set)
    for n, (_, nd) in descs.items():
        w = re.findall(r"[a-z]+", nd)
        tr = {" ".join(w[k:k + 5]) for k in range(len(w) - 4)}
        cinco.update(tr)
        for t in tr:
            onde[t].add(n)
    for t, q in sorted(cinco.items()):
        if q > 8 and onde[t] & ns_alvo:
            erros.append(f"molde: o trecho '{t}' aparece em {q} descrições")

    destino = (os.path.splitext(arquivo)[0] + "_validacao.json") if arquivo else os.path.join(lote, "validacao", "fichas.json")
    comum.gravar_json(destino, {"fichas": len(alvo), "erros": erros, "avisos": avisos})
    print(f"fichas: {len(alvo)} | erros: {len(erros)} | avisos: {len(avisos)} | relatório: {destino}")
    for x in erros[:120]:
        print("  ERRO", x)
    for x in avisos[:40]:
        print("  aviso", x)
    print("OK" if not erros else "FALHOU")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
