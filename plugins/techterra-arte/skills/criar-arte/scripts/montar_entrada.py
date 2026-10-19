# -*- coding: utf-8 -*-
"""Monta a entrada de um lote de monstros/fusões a partir do plano (sem banco, sem rede).

    python montar_entrada.py <pasta_do_lote>

Lê <lote>/plano.json (formato em CONTRATO-INTERNO.md), valida e gera:
- <lote>/entrada.json            células numeradas (n, slot, arquivo, evolução, recortes dos pais/original);
- <lote>/pais/<slug>.png         recorte limpo (bbox do alfa) de cada arte de origem;
- <lote>/referencias/cartela_NNN_pais.png
                                 prancha 2x2 de cada cartela que tem origem: V = original grande e centrado;
                                 X/A = base grande à esquerda + sacrifício menor à direita; F = todos os pais do mesmo
                                 tamanho; N com antecessor_externo = o antecessor grande e centrado; demais N/L =
                                 quadrante vazio (cartela só de N/L sem antecessor externo não ganha prancha);
- <lote>/referencias/            cópia das referências da skill (estilo, variedade, humanoides, guia 2x2).

Idempotente: pode rodar de novo depois de corrigir o plano.
"""
import os
import shutil
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Pillow não está instalado: rode  python -m pip install Pillow")
    sys.exit(2)

USO = "uso: python montar_entrada.py <pasta_do_lote>"
FUNDO, LINHA = (128, 128, 132, 255), (90, 90, 94, 255)
REFS_LOTE = ["monstros/referencia-estilo.png", "monstros/referencia-variedade.png", "monstros/referencia-humanoides.png",
             "guias/guia_enquadramento_2x2.png"]
CAMPOS_ORIGEM = ("nome", "tier", "tipo1", "tipo2", "descricao", "arte", "humanoide")


class Plano:
    def __init__(self):
        self.erros, self.avisos = [], []

    def erro(self, msg):
        self.erros.append(msg)

    def aviso(self, msg):
        self.avisos.append(msg)


def tier_ok(v):
    return isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= 10


def checa_origem(p, tag, o, lote, papeis=None):
    """Confere um original/ingrediente: campos, tipos, tier e se a arte existe."""
    if not isinstance(o, dict):
        p.erro(f"{tag}: tem que ser um objeto {{{', '.join(CAMPOS_ORIGEM)}}}")
        return False
    ok = True
    falta = [c for c in CAMPOS_ORIGEM if c not in o]
    if papeis is not None and "papel" not in o:
        falta.insert(0, "papel")
    if falta:
        p.erro(f"{tag}: faltam campos {falta}")
        return False
    if not str(o["nome"]).strip():
        p.erro(f"{tag}: nome vazio"); ok = False
    if not tier_ok(o["tier"]):
        p.erro(f"{tag} ({o['nome']}): tier {o['tier']!r} fora de 1–10"); ok = False
    for k in ("tipo1", "tipo2"):
        if o[k] not in comum.TIPOS:
            p.erro(f"{tag} ({o['nome']}): {k} '{o[k]}' não é tipo válido"); ok = False
    if not isinstance(o["humanoide"], bool):
        p.erro(f"{tag} ({o['nome']}): 'humanoide' tem que ser true/false"); ok = False
    if "linhagem" in o and not (isinstance(o["linhagem"], list) and all(isinstance(x, str) for x in o["linhagem"])):
        p.erro(f"{tag} ({o['nome']}): 'linhagem' tem que ser lista de nomes"); ok = False
    arte = os.path.join(lote, str(o["arte"]))
    if not os.path.isfile(arte):
        p.erro(f"{tag} ({o['nome']}): arte não encontrada: {o['arte']} (caminho relativo à pasta do lote)"); ok = False
    return ok


def recortar(lote, o, feitos, p):
    """Recorta a arte pelo bbox do alfa para pais/<slug>.png; devolve o caminho relativo."""
    sl = comum.slug(o["nome"])
    rel = f"pais/{sl}.png"
    arte = os.path.normpath(os.path.join(lote, o["arte"]))
    if sl in feitos:
        if feitos[sl] != arte:
            p.erro(f"'{o['nome']}' aparece com duas artes diferentes: {feitos[sl]} e {arte}")
        return rel
    feitos[sl] = arte
    try:
        im = Image.open(arte).convert("RGBA")
    except Exception as ex:
        p.erro(f"não consegui abrir a arte de '{o['nome']}' ({o['arte']}): {ex}")
        return rel
    bb = im.getchannel("A").getbbox()
    if not bb:
        p.aviso(f"arte de '{o['nome']}' está toda transparente")
    elif bb == (0, 0, im.width, im.height):
        p.aviso(f"arte de '{o['nome']}' não tem fundo transparente (recorte = imagem inteira); confira a prancha")
    os.makedirs(os.path.join(lote, "pais"), exist_ok=True)
    (im.crop(bb) if bb else im).save(os.path.join(lote, rel))
    return rel


def externo(cel):
    """Antecessor externo (monstro existente, fora do lote) de uma célula N, ou None."""
    return (cel.get("evolucao") or {}).get("externo")


def encaixa(img, w, h):
    f = min(w / img.width, h / img.height)
    return img.resize((max(1, int(img.width * f)), max(1, int(img.height * f))), Image.LANCZOS)


def quadrante(board, lote, cel, x0, y0):
    C = comum.CEL
    abre = lambda rel: Image.open(os.path.join(lote, rel)).convert("RGBA")  # noqa: E731
    b = cel["bloco"]
    if b in ("V", "N"):
        o = cel["original"] if b == "V" else externo(cel)
        if not o:
            return
        s = encaixa(abre(o["recorte"]), int(C * 0.8), int(C * 0.8))
        board.alpha_composite(s, (x0 + (C - s.width) // 2, y0 + (C - s.height) // 2))
    elif b in ("X", "A"):
        base, sac = (abre(i["recorte"]) for i in cel["ingredientes"])
        ib = encaixa(base, int(C * 0.58), int(C * 0.86))
        isc = encaixa(sac, int(C * 0.32), int(C * 0.48))
        board.alpha_composite(ib, (x0 + 14 + (int(C * 0.6) - ib.width) // 2, y0 + (C - ib.height) // 2))
        board.alpha_composite(isc, (x0 + int(C * 0.64) + (int(C * 0.34) - isc.width) // 2, y0 + (C - isc.height) // 2))
    elif b == "F":
        ims = [abre(i["recorte"]) for i in cel["ingredientes"]]
        k = len(ims)
        if k <= 2:   # lado a lado, mesmo tamanho
            w, h = C // k, int(C * 0.8)
            for j, im in enumerate(ims):
                s = encaixa(im, w - 24, h)
                board.alpha_composite(s, (x0 + j * w + (w - s.width) // 2, y0 + (C - s.height) // 2))
        else:        # 2 em cima, 1 embaixo, mesmo tamanho
            w, h = C // 2, C // 2
            for j, im in enumerate(ims):
                s = encaixa(im, w - 24, h - 24)
                lin, col = divmod(j, 2)
                off = (C - w) // 2 if lin == 1 and k == 3 else col * w
                board.alpha_composite(s, (x0 + off + (w - s.width) // 2, y0 + lin * h + (h - s.height) // 2))


def prancha(lote, cels, saida):
    L, C = comum.LADO, comum.CEL
    board = Image.new("RGBA", (L, L), FUNDO)
    d = ImageDraw.Draw(board)
    d.line([(C, 0), (C, L)], fill=LINHA, width=4)
    d.line([(0, C), (L, C)], fill=LINHA, width=4)
    for cel in cels:
        quadrante(board, lote, cel, (cel["coluna"] - 1) * C, (cel["linha"] - 1) * C)
    board.save(saida)


def main():
    lote = comum.pasta_lote(sys.argv, USO)
    p = Plano()
    try:
        plano = comum.ler_json(os.path.join(lote, "plano.json"))
    except FileNotFoundError:
        print(f"falta {os.path.join(lote, 'plano.json')} (formato em CONTRATO-INTERNO.md)")
        sys.exit(2)
    except ValueError as ex:
        print(f"plano.json não é JSON válido: {ex}")
        sys.exit(2)
    cartelas = plano.get("cartelas") if isinstance(plano, dict) else None
    if not isinstance(cartelas, list) or not cartelas:
        print("plano.json precisa de uma lista 'cartelas' não vazia")
        sys.exit(2)

    nums = [c.get("cartela") if isinstance(c, dict) else None for c in cartelas]
    if sorted(x for x in nums if isinstance(x, int)) != list(range(1, len(cartelas) + 1)):
        print(f"as cartelas têm que ser numeradas 1..{len(cartelas)}, sem buraco nem repetição (veio {nums})")
        sys.exit(2)
    cartelas = sorted(cartelas, key=lambda c: c["cartela"])

    # 1) células cruas + validação de campos
    celulas = []
    for c in cartelas:
        cn = c["cartela"]
        cels = c.get("celulas")
        if not isinstance(cels, list) or len(cels) != 4:
            p.erro(f"cartela {cn:03d}: precisa de exatamente 4 células (veio {len(cels) if isinstance(cels, list) else 0})")
            continue
        for q, cel in enumerate(cels):
            lin, col = q // 2 + 1, q % 2 + 1
            tag = f"cartela {cn:03d} L{lin}C{col}"
            if not isinstance(cel, dict):
                p.erro(f"{tag}: célula tem que ser um objeto"); continue
            e = dict(cel)
            b = e.get("bloco")
            if b not in comum.BLOCOS:
                p.erro(f"{tag}: bloco {b!r} inválido (use {', '.join(comum.BLOCOS)})"); continue
            if not tier_ok(e.get("tier")):
                p.erro(f"{tag}: tier {e.get('tier')!r} fora de 1–10")
            for k in ("tipo1", "tipo2"):
                if e.get(k) not in comum.TIPOS:
                    p.erro(f"{tag}: {k} {e.get(k)!r} não é tipo válido")
            if e.get("tipo1") == e.get("tipo2"):
                p.erro(f"{tag}: tipo1 e tipo2 iguais ({e.get('tipo1')})")
            if "humanoide_previsto" in e and not isinstance(e["humanoide_previsto"], bool):
                p.erro(f"{tag}: humanoide_previsto tem que ser true/false")
            e["humanoide_previsto"] = bool(e.get("humanoide_previsto", False))
            if b == "N":
                ev = e.get("evolui_de")
                ext = e.get("antecessor_externo")
                if ev is not None and not (isinstance(ev, list) and len(ev) == 3 and all(isinstance(x, int) for x in ev)):
                    p.erro(f"{tag}: evolui_de tem que ser [cartela, linha, coluna]")
                if ev is not None and ext is not None:
                    p.erro(f"{tag}: use evolui_de (antecessor no lote) OU antecessor_externo (monstro existente), nunca os dois")
                elif ext is not None and checa_origem(p, f"{tag} antecessor_externo", ext, lote):
                    if tier_ok(e.get("tier")):
                        if e["tier"] < ext["tier"]:
                            p.erro(f"{tag}: evolução com tier {e['tier']} menor que o do antecessor {ext['nome']} ({ext['tier']})")
                        elif e["tier"] == ext["tier"]:
                            p.aviso(f"{tag}: evolução não sobe de tier ({ext['nome']} {ext['tier']} → {e['tier']})")
                    if {ext["tipo1"], ext["tipo2"]} != {e.get("tipo1"), e.get("tipo2")}:
                        p.aviso(f"{tag}: evolução troca de tipos ({ext['tipo1']}/{ext['tipo2']} → {e.get('tipo1')}/{e.get('tipo2')})")
                    if ext["humanoide"] and not e["humanoide_previsto"]:
                        e["humanoide_previsto"] = True
                        p.aviso(f"{tag}: antecessor externo humanoide → humanoide_previsto = true")
                if "evolucao_modo" in e and not (isinstance(e["evolucao_modo"], str) and e["evolucao_modo"].strip()):
                    p.erro(f"{tag}: evolucao_modo tem que ser texto (ex.: \"level\")")
                lv = e.get("level_requerido")
                if lv is not None and not (isinstance(lv, int) and not isinstance(lv, bool) and lv >= 1):
                    p.erro(f"{tag}: level_requerido tem que ser inteiro ≥ 1")
                if ev is None and ext is None and ("evolucao_modo" in e or lv is not None):
                    p.aviso(f"{tag}: evolucao_modo/level_requerido sem antecessor (evolui_de ou antecessor_externo): ignorados")
            elif b == "V":
                o = e.get("original")
                if checa_origem(p, f"{tag} original", o, lote):
                    if e.get("tipo_sai") not in (o["tipo1"], o["tipo2"]):
                        p.erro(f"{tag}: tipo_sai {e.get('tipo_sai')!r} não é tipo do original {o['nome']} ({o['tipo1']}/{o['tipo2']})")
                    if e.get("tipo_entra") not in comum.TIPOS or e.get("tipo_entra") not in (e.get("tipo1"), e.get("tipo2")):
                        p.erro(f"{tag}: tipo_entra {e.get('tipo_entra')!r} tem que ser tipo válido e um dos tipos da célula")
                    elif e.get("tipo_entra") in (o["tipo1"], o["tipo2"]):
                        p.erro(f"{tag}: tipo_entra {e['tipo_entra']!r} o original já tem")
                    fica = {o["tipo1"], o["tipo2"]} - {e.get("tipo_sai")}
                    if fica and not fica <= {e.get("tipo1"), e.get("tipo2")}:
                        p.erro(f"{tag}: o tipo que fica do original ({', '.join(fica)}) tem que estar na célula")
                    if tier_ok(e.get("tier")) and e["tier"] != o["tier"]:
                        p.erro(f"{tag}: variação tem o mesmo tier do original ({o['tier']}), veio {e['tier']}")
                    if o["humanoide"] and not e["humanoide_previsto"]:
                        e["humanoide_previsto"] = True
                        p.aviso(f"{tag}: original humanoide → humanoide_previsto = true")
            else:
                ing = e.get("ingredientes")
                if b == "L" and ing:
                    p.erro(f"{tag}: bloco L não tem ingredientes")
                if b in ("X", "A", "F"):
                    nomes_ing = [comum.norm(str(i.get("nome", ""))) for i in ing if isinstance(i, dict)] \
                        if isinstance(ing, list) else []
                    if len(set(nomes_ing)) < len(nomes_ing):
                        p.erro(f"{tag}: o mesmo pai aparece duas vezes nos ingredientes")
                    if not isinstance(ing, list):
                        p.erro(f"{tag}: bloco {b} precisa de 'ingredientes'")
                    elif b in ("X", "A"):
                        papeis = [i.get("papel") if isinstance(i, dict) else None for i in ing]
                        if papeis != ["BASE", "SACRIFICIO"]:
                            p.erro(f"{tag}: bloco {b} = exatamente 2 ingredientes, papéis BASE e depois SACRIFICIO (veio {papeis})")
                        elif all(checa_origem(p, f"{tag} {i['papel']}", i, lote, papeis=True) for i in ing):
                            bs, sc = ing
                            if tier_ok(e.get("tier")) and e["tier"] != min(10, max(bs["tier"], sc["tier"]) + 1):
                                p.aviso(f"{tag}: tier {e['tier']} ≠ maior pai + 1 (teto 10) = {min(10, max(bs['tier'], sc['tier']) + 1)}")
                            if e.get("tipo1") not in (bs["tipo1"], bs["tipo2"]):
                                p.aviso(f"{tag}: tipo1 {e.get('tipo1')} não vem da base {bs['nome']}")
                            if e.get("tipo2") not in (sc["tipo1"], sc["tipo2"]):
                                p.aviso(f"{tag}: tipo2 {e.get('tipo2')} não vem do sacrifício {sc['nome']}")
                            if bs["humanoide"] and not e["humanoide_previsto"]:
                                e["humanoide_previsto"] = True
                                p.aviso(f"{tag}: base humanoide → humanoide_previsto = true")
                    else:
                        papeis = [i.get("papel") if isinstance(i, dict) else None for i in ing]
                        if not 2 <= len(ing) <= 3 or any(x != "PAI" for x in papeis):
                            p.erro(f"{tag}: bloco F = 2 ou 3 ingredientes com papel PAI (veio {papeis})")
                        else:
                            for i in ing:
                                checa_origem(p, f"{tag} PAI", i, lote, papeis=True)
            if b == "L" and not str(c.get("tema", "")).strip():
                p.aviso(f"cartela {cn:03d}: bloco L sem 'tema' no plano (o agente escolhe e escreve na ficha)")
            n = (cn - 1) * 4 + q + 1
            e.update(n=n, cartela=cn, linha=lin, coluna=col, slot=f"{b}{cn:03d}_{q + 1}", bloco=b,
                     leitura=str(e.get("leitura") or "").strip())
            if b == "L" and c.get("tema"):
                e["tema"] = c["tema"]
            if tier_ok(e.get("tier")):
                e["arquivo"] = f"{n:02d}_t{e['tier']:02d}_{{slug_do_nome}}.png"
            celulas.append(e)

    if p.erros:
        fim(p, None)

    # 2) evolução (N)
    por_pos = {(e["cartela"], e["linha"], e["coluna"]): e for e in celulas}
    for e in celulas:
        if e["bloco"] == "N":
            e["evolucao"] = {"anterior": None, "seguinte": None}
    for e in celulas:
        ev = e.get("evolui_de")
        if e["bloco"] != "N" or not ev:
            continue
        tag = f"cartela {e['cartela']:03d} L{e['linha']}C{e['coluna']}"
        a = por_pos.get(tuple(ev))
        if not a:
            p.erro(f"{tag}: evolui_de {ev} não existe no plano"); continue
        if a["n"] >= e["n"]:
            p.erro(f"{tag}: o antecessor {ev} tem que vir antes na ordem de leitura (mesma cartela ou anterior)"); continue
        if a["bloco"] != "N":
            p.erro(f"{tag}: o antecessor {ev} tem que ser bloco N"); continue
        if a["evolucao"]["seguinte"] is not None:
            p.erro(f"{tag}: duas células evoluem de {ev}"); continue
        if a.get("tier") and e.get("tier") and e["tier"] <= a["tier"]:
            p.aviso(f"{tag}: evolução não sobe de tier ({a['tier']} → {e['tier']})")
        if {a["tipo1"], a["tipo2"]} != {e["tipo1"], e["tipo2"]}:
            p.aviso(f"{tag}: evolução troca de tipos ({a['tipo1']}/{a['tipo2']} → {e['tipo1']}/{e['tipo2']})")
        e["evolucao"]["anterior"] = a["n"]
        a["evolucao"]["seguinte"] = e["n"]

    # avisos de leva
    pares = Counter(frozenset((e["tipo1"], e["tipo2"])) for e in celulas if e["bloco"] in ("X", "A", "F"))
    for par, q in pares.items():
        if q > 1:
            p.aviso(f"par de tipos {'/'.join(sorted(par))} repete {q}× entre as fusões da leva")
    for c in cartelas:
        h = sum(e["humanoide_previsto"] for e in celulas if e["cartela"] == c["cartela"])
        if h > 2:
            p.aviso(f"cartela {c['cartela']:03d}: {h} humanoides previstos (o normal é 1–2)")

    # 3) recortes
    feitos = {}
    for e in celulas:
        if e["bloco"] == "V":
            e["original"]["recorte"] = recortar(lote, e["original"], feitos, p)
        ext = e.pop("antecessor_externo", None) if e["bloco"] == "N" else None
        if ext:
            e["evolucao"]["externo"] = {**{k: ext[k] for k in ("nome", "tier", "tipo1", "tipo2", "descricao")},
                                        "recorte": recortar(lote, ext, feitos, p), "humanoide": ext["humanoide"]}
        for i in e.get("ingredientes") or []:
            i["recorte"] = recortar(lote, i, feitos, p)
            i.setdefault("linhagem", [])
    if p.erros:
        fim(p, None)

    # 4) entrada.json
    ordem = ["n", "slot", "cartela", "linha", "coluna", "bloco", "tier", "tipo1", "tipo2", "humanoide_previsto", "leitura",
             "tema", "evolui_de", "evolucao", "original", "tipo_sai", "tipo_entra", "ingredientes", "arquivo"]
    saida = [{**{k: e[k] for k in ordem if k in e}, **{k: v for k, v in e.items() if k not in ordem}}
             for e in sorted(celulas, key=lambda e: e["n"])]
    comum.gravar_json(os.path.join(lote, "entrada.json"), saida)

    # 5) pranchas + referências
    refs = os.path.join(lote, "referencias")
    os.makedirs(refs, exist_ok=True)
    pranchas = 0
    for c in cartelas:
        cels = [e for e in saida if e["cartela"] == c["cartela"]]
        alvo = os.path.join(refs, f"cartela_{c['cartela']:03d}_pais.png")
        if any(e["bloco"] in ("V", "F", "X", "A") or externo(e) for e in cels):
            prancha(lote, cels, alvo)
            pranchas += 1
        elif os.path.exists(alvo):
            os.remove(alvo)   # cartela virou N/L sem origem: prancha antiga sai
    for r in REFS_LOTE:
        orig = os.path.join(comum.REFS_DIR, *r.split("/"))
        if os.path.isfile(orig):
            shutil.copyfile(orig, os.path.join(refs, os.path.basename(r)))
        else:
            p.aviso(f"referência da skill não encontrada: referencias/{r}")
    fim(p, f"células: {len(saida)} | cartelas: {len(cartelas)} | recortes em pais/: {len(feitos)} | pranchas: {pranchas} "
           f"| referências copiadas: {len(REFS_LOTE)}")


def fim(p, resumo):
    for a in p.avisos:
        print("  aviso", a)
    for x in p.erros:
        print("  ERRO", x)
    if p.erros:
        print(f"plano com {len(p.erros)} erro(s): entrada.json não foi gerada. Corrija o plano.json e rode de novo.")
        sys.exit(1)
    print(resumo)
    print("OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
