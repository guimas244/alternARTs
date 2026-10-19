# -*- coding: utf-8 -*-
"""Confere o ENQUADRAMENTO de uma cartela 2x2 de monstros (ou de uma avulsa) antes de aceitá-la.

    python checa_enquadramento.py <lote>/cartelas/cartela_001_original.png
    python checa_enquadramento.py <lote>/cartelas/avulsa_001_L1C2_v1.png --avulsa

Mede pelo alfa (Pillow puro, meia resolução), do mesmo jeito que o recortar_cartela.py enxerga a cartela.
O recorte separa as criaturas por CONTORNO (componentes conexos), não pela linha do meio. Então:
- invadir o quadrado do vizinho SEM encostar nele NÃO perde nada (o recorte leva a criatura inteira);
- o que PERDE de verdade: (1) duas criaturas ENCOSTADAS (viram uma peça; o recorte corta pela linha e
  mutila as duas); (2) criatura cortada na BORDA da imagem; (3) PEDAÇO SOLTO (faísca, segmento flutuante,
  folha) que fica no quadrado do vizinho: o recorte entrega o pedaço para o vizinho; (4) número de
  criaturas diferente de 4; (5) fundo não transparente (o diagrama de layout vazou).
Medidas por célula, em fração da célula: ocupação (maior lado / célula), folga_ext (até a borda da imagem),
folga_linha (até a linha do meio; negativo = invadiu).

Veredito:
  REPROVADA  encostadas, borda cortada (folga externa < 0,005), pedaço solto no quadrado vizinho, != 4,
             fundo não transparente nos cantos/centro -> conserto (avulsa da célula ou cartela inteira)
  ATENÇÃO    invade a linha do meio, ocupação > 0,95 ou folga externa < 0,03 -> aceitável, nunca refazer
  OK         tudo folgado

Avulsa (uma criatura só, grade 1; também ligado sozinho quando o arquivo começa com "avulsa_"):
  REPROVADA só se estiver vazia ou CORTADA na borda (folga < 0,005); perto da borda é ATENÇÃO (o recorte reenquadra).

Grava <lote>/validacao/enquadramento/<imagem>.json (um registro por imagem, para vários agentes medirem ao
mesmo tempo). O lote é a pasta-pai de cartelas/ (ou --lote <pasta>). Sai com código 1 se REPROVADA.
"""
import os
import sys
from collections import deque
from datetime import datetime

sys.dont_write_bytecode = True  # nada é gravado dentro da skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402
from PIL import Image  # noqa: E402

F, ALFA, MIN_COMP = 2, 32, 10
USO = "uso: python checa_enquadramento.py <imagem.png> [--avulsa] [--lote <pasta do lote>]"


def fundo_vazou(alfa):
    """Cantos e centro da cruz têm que ser transparentes; se não, o diagrama (ou um fundo) foi desenhado."""
    w, h = alfa.size
    pontos = [(4, 4), (w - 5, 4), (4, h - 5), (w - 5, h - 5), (w // 2, h // 2), (w // 2, 4), (4, h // 2)]
    return [p for p in pontos if alfa.getpixel(p) > 8]


def medir(caminho):
    im = Image.open(caminho).convert("RGBA").getchannel("A")
    vazou = fundo_vazou(im)
    im = im.resize((im.width // F, im.height // F), Image.BOX)
    w, h = im.size
    m = bytearray(1 if v >= ALFA else 0 for v in im.tobytes())
    mx, my = w / 2, h / 2
    vis = bytearray(len(m))
    comps = []
    for s in range(len(m)):
        if not m[s] or vis[s]:
            continue
        q = deque([s])
        vis[s] = 1
        pix = []
        while q:
            i = q.popleft()
            pix.append(i)
            x, y = i % w, i // w
            for yy in (y - 1, y, y + 1):
                if 0 <= yy < h:
                    for xx in (x - 1, x, x + 1):
                        if 0 <= xx < w:
                            j = yy * w + xx
                            if m[j] and not vis[j]:
                                vis[j] = 1
                                q.append(j)
        if len(pix) >= MIN_COMP:
            comps.append(pix)
    encostadas, grupos, pecas = 0, {}, []
    for pix in comps:
        por = {}
        for i in pix:
            por.setdefault((int(i // w >= my), int(i % w >= mx)), []).append(i)
        grandes = [k for k, v in por.items() if len(v) >= 0.35 * len(pix)]
        if len(grandes) > 1:
            encostadas += 1
            for k, v in por.items():
                grupos.setdefault(k, []).extend(v)
        else:
            dono = max(por, key=lambda k: len(por[k]))
            grupos.setdefault(dono, []).extend(pix)
            xs = [i % w for i in pix]
            ys = [i // w for i in pix]
            pecas.append(dict(celula=dono, n=len(pix), bb=(min(xs), min(ys), max(xs), max(ys))))
    # pedaço solto: peça que não é o corpo principal da célula e cujo corpo principal MAIS PERTO é o de outra
    # célula -> o recorte a entrega para o vizinho
    principal = {}
    for p in pecas:
        if p["n"] > principal.get(p["celula"], {"n": 0})["n"]:
            principal[p["celula"]] = p

    def dist(a, b):
        dx = max(b[0] - a[2], a[0] - b[2], 0)
        dy = max(b[1] - a[3], a[1] - b[3], 0)
        return (dx * dx + dy * dy) ** 0.5

    soltos = []
    for p in pecas:
        if principal.get(p["celula"]) is p:
            continue
        perto = min(principal.values(), key=lambda q: dist(p["bb"], q["bb"]))
        if perto["celula"] != p["celula"]:
            soltos.append(f"pedaço solto de linha{perto['celula'][0] + 1}_coluna{perto['celula'][1] + 1} "
                          f"no quadrado linha{p['celula'][0] + 1}_coluna{p['celula'][1] + 1}")
    cel = w / 2
    celulas = {}
    for (l, c), pix in sorted(grupos.items()):
        xs = [i % w for i in pix]
        ys = [i // w for i in pix]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        ext = min(x0 if c == 0 else w - 1 - x1, y0 if l == 0 else h - 1 - y1)
        lin = min((mx - 1 - x1) if c == 0 else (x0 - mx), (my - 1 - y1) if l == 0 else (y0 - my))
        celulas[f"linha{l + 1}_coluna{c + 1}"] = dict(ocupacao=round(max(x1 - x0 + 1, y1 - y0 + 1) / cel, 3),
                                                     folga_ext=round(ext / cel, 3), folga_linha=round(lin / cel, 3))
    return dict(encostadas=encostadas, n_criaturas=len(grupos), celulas=celulas, soltos=soltos, fundo_vazou=len(vazou))


def veredito(r):
    rep, at = [], []
    if r["n_criaturas"] != 4:
        rep.append(f"{r['n_criaturas']} criaturas separadas (esperado 4)")
    if r["encostadas"]:
        rep.append(f"{r['encostadas']} par(es) de criaturas encostadas")
    for x in r.get("soltos", []):
        rep.append(x)
    if r.get("fundo_vazou"):
        rep.append(f"fundo NÃO transparente em {r['fundo_vazou']} ponto(s) de controle (diagrama vazou?) "
                   "-> cartela inteira de novo")
    for k, c in r["celulas"].items():
        if c["folga_ext"] < 0.005:
            rep.append(f"{k}: cortada na borda da imagem (folga {c['folga_ext']})")
        elif c["folga_ext"] < 0.03:
            at.append(f"{k}: perto da borda da imagem (folga {c['folga_ext']})")
        if c["ocupacao"] > 0.95:
            at.append(f"{k}: ocupação {c['ocupacao']}")
        if c["folga_linha"] < 0:
            at.append(f"{k}: invade a linha do meio (folga {c['folga_linha']}) — sem perda se não encostar")
    return ("REPROVADA" if rep else "ATENÇÃO" if at else "OK"), rep, at


def medir_avulsa(caminho):
    """Imagem AVULSA (uma criatura só, grade 1): a célula é a imagem inteira."""
    im = Image.open(caminho).convert("RGBA").getchannel("A")
    im = im.resize((im.width // F, im.height // F), Image.BOX)
    w, h = im.size
    bb = im.point(lambda v: 255 if v >= ALFA else 0).getbbox()
    if not bb:
        return dict(encostadas=0, n_criaturas=0, celulas={})
    x0, y0, x1, y1 = bb[0], bb[1], bb[2] - 1, bb[3] - 1
    ext = min(x0, y0, w - 1 - x1, h - 1 - y1)
    return dict(encostadas=0, n_criaturas=1, celulas={"avulsa": dict(
        ocupacao=round(max(x1 - x0 + 1, y1 - y0 + 1) / w, 3), folga_ext=round(ext / w, 3), folga_linha=1.0)})


def veredito_avulsa(r):
    rep, at = [], []
    if r["n_criaturas"] != 1:
        rep.append("imagem vazia")
    for k, c in r["celulas"].items():
        # o recorte reenquadra a avulsa no tile: só perde arte se ela estiver CORTADA na borda
        if c["folga_ext"] < 0.005:
            rep.append(f"cortada na borda da imagem (folga {c['folga_ext']})")
        elif c["folga_ext"] < 0.03:
            at.append(f"perto da borda (folga {c['folga_ext']}) — sem perda")
    return ("REPROVADA" if rep else "ATENÇÃO" if at else "OK"), rep, at


def achar_lote(caminho, argv):
    """--lote explícito; senão a pasta-pai do 'cartelas/' mais próximo acima da imagem."""
    if "--lote" in argv:
        i = argv.index("--lote")
        if i + 1 < len(argv):
            return os.path.abspath(argv[i + 1])
    d = os.path.dirname(caminho)
    while True:
        if os.path.basename(d).lower() == "cartelas":
            return os.path.dirname(d)
        pai = os.path.dirname(d)
        if pai == d:
            break
        d = pai
    print("a imagem não está dentro de uma pasta cartelas/ — informe --lote <pasta do lote>")
    sys.exit(2)


def main(argv):
    pos, pula = [], False
    for k, a in enumerate(argv[1:], 1):
        if pula:
            pula = False
            continue
        if a == "--lote":
            pula = True
        elif not a.startswith("--"):
            pos.append(a)
    if not pos:
        print(USO)
        sys.exit(2)
    caminho = os.path.abspath(pos[0])
    if not os.path.isfile(caminho):
        print(f"imagem não existe: {caminho}")
        sys.exit(2)
    lote = achar_lote(caminho, argv)
    avulsa = "--avulsa" in argv or os.path.basename(caminho).lower().startswith("avulsa_")
    r = medir_avulsa(caminho) if avulsa else medir(caminho)
    v, rep, at = veredito_avulsa(r) if avulsa else veredito(r)
    r.update(arquivo=os.path.relpath(caminho, lote).replace("\\", "/"), modo="avulsa" if avulsa else "cartela",
             veredito=v, reprovas=rep, atencao=at, medido_em=datetime.now().isoformat(timespec="seconds"))
    reg = os.path.join(lote, "validacao", "enquadramento", os.path.splitext(os.path.basename(caminho))[0] + ".json")
    comum.gravar_json(reg, r)
    print(v + (" (avulsa)" if avulsa else ""))
    for k, c in r["celulas"].items():
        print(f"  {k}: ocupação {c['ocupacao']:.2f} | folga borda {c['folga_ext']:.3f} | folga linha {c['folga_linha']:.3f}")
    for x in rep:
        print("  REPROVA:", x)
    for x in at:
        print("  atenção:", x)
    print(f"  registro: {os.path.relpath(reg, lote)}")
    sys.exit(1 if v == "REPROVADA" else 0)


if __name__ == "__main__":
    main(sys.argv)
