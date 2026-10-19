# -*- coding: utf-8 -*-
"""Recorta as páginas de personagens (3 colunas, busto em cima + corpo inteiro embaixo) e atualiza fichas.json.

Uso:
  python npc_recortar.py <lote>                  recorta todas as paginas/pagina_NNN.png
  python npc_recortar.py <lote> --paginas 1,3    só essas páginas

Saída (na pasta do lote):
  recortes/pagina_NNN_colC_rosto.png   512x512   RGBA (busto encostado embaixo)
  recortes/pagina_NNN_colC_corpo.png   512x1024  RGBA (pés embaixo)
  validacao/recortes.json              relatório por coluna (corte, método, ilhas removidas, avisos)
  fichas.json                          uma ficha por pessoa (regras/entrega.md), com os arquivos rosto/corpo

Método (porta do recortador aprovado do Lote 09):
  - rosto/corpo separados pela linha vazia entre eles (faixa transparente da coluna); sem ela, pela queda de largura;
  - corpo = só a mancha ligada aos pés, crescida ao mesmo tempo a partir dos pés de cada coluna (separa quem se toca);
  - rosto = faixa de cima da coluna, sem fiapos menores que 3% da maior mancha;
  - no fim, ilhas soltas menores que 1% da maior mancha são apagadas (resto de vizinho).
"""
import os
import re
import sys
from collections import deque

sys.dont_write_bytecode = True  # nada é gravado dentro da skill (nem __pycache__)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit("Falta a biblioteca Pillow. Rode:  python -m pip install pillow")

USO = __doc__
ALFA = 24            # alfa acima disso conta como "tem pessoa"
NCOLS = 3
ROSTO, CORPO = (512, 512), (512, 1024)
FIAPO_ROSTO = 0.03   # mancha do busto menor que 3% da maior = fiapo
ILHA_FINAL = 0.01    # ilha do recorte final menor que 1% da maior = resto de vizinho


# ---------------------------------------------------------------- utilidades de máscara

def componentes(opaco, w, h):
    """Componentes 4-conexos de uma máscara (bytearray w*h de 0/1). Retorna lista de listas de índices."""
    visto = bytearray(w * h)
    grupos = []
    for i in range(w * h):
        if not opaco[i] or visto[i]:
            continue
        visto[i] = 1
        q, g = deque([i]), []
        while q:
            k = q.popleft()
            g.append(k)
            x = k % w
            for nk in (k - 1 if x > 0 else -1, k + 1 if x < w - 1 else -1, k - w, k + w):
                if 0 <= nk < w * h and opaco[nk] and not visto[nk]:
                    visto[nk] = 1
                    q.append(nk)
        grupos.append(g)
    return grupos


def mascara_opaca(img):
    a = img.getchannel("A").tobytes()
    return bytearray(1 if v > ALFA else 0 for v in a)


def limpar_ilhas(img, limite=ILHA_FINAL):
    """Apaga ilhas menores que `limite` da maior (com 2 px de folga). Retorna (img, n_ilhas, n_pixels)."""
    w, h = img.size
    grupos = componentes(mascara_opaca(img), w, h)
    if not grupos:
        return img, 0, 0
    maior = max(map(len, grupos))
    pequenos = [g for g in grupos if len(g) < maior * limite]
    if pequenos:
        alpha = img.getchannel("A")
        px = alpha.load()
        for g in pequenos:
            for k in g:
                x, y = k % w, k // w
                for nx in range(max(0, x - 2), min(w, x + 3)):
                    for ny in range(max(0, y - 2), min(h, y + 3)):
                        px[nx, ny] = 0
        img.putalpha(alpha)
    return img, len(pequenos), sum(map(len, pequenos))


# ---------------------------------------------------------------- corte rosto / corpo

def largura_opaca(op, W, x0, x1, y):
    base = y * W
    return sum(op[base + x0:base + x1])


def linha_de_corte(op, W, H, x0, x1):
    """Retorna (y, método). Prefere a linha vazia entre busto e corpo; sem ela, a queda de largura (Lote 09)."""
    ini, fim = int(H * 0.20), int(H * 0.45)
    larg = [largura_opaca(op, W, x0, x1, y) for y in range(ini, fim)]
    corridas, comeco = [], None
    for i, v in enumerate(larg + [1]):
        if v == 0 and comeco is None:
            comeco = i
        elif v != 0 and comeco is not None:
            corridas.append((comeco + ini, i + ini))  # [y0, y1)
            comeco = None
    # a corrida tem de ter algo opaco acima (o busto) e algo abaixo (o corpo)
    corridas = [c for c in corridas if c[0] > ini and c[1] < fim]
    if corridas:
        alvo = H * 0.32
        y0, y1 = max(corridas, key=lambda c: (c[1] - c[0], -abs((c[0] + c[1]) / 2 - alvo)))
        if y1 - y0 >= 4:
            return y0, f"linha vazia {y0}-{y1 - 1}"
    cw = x1 - x0
    a, b = int(H * 0.26), int(H * 0.40)
    prev = largura_opaca(op, W, x0, x1, a - 1)
    for y in range(a, b):
        cur = largura_opaca(op, W, x0, x1, y)
        if prev > 0.36 * cw and cur < 0.5 * prev:
            return y, "queda de largura"
        prev = cur
    y = min(range(int(H * 0.24), int(H * 0.38)), key=lambda yy: largura_opaca(op, W, x0, x1, yy))
    return y, "linha mais vazia (sem vão: conferir)"


# ---------------------------------------------------------------- página

def recortar_pagina(caminho, saida, nome):
    im = Image.open(caminho).convert("RGBA")
    W, H = im.size
    rel = {"pagina": nome, "tamanho": [W, H], "colunas": [], "avisos": []}
    if (W, H) != (comum.LADO, comum.LADO):
        rel["avisos"].append(f"página {W}x{H} (esperado {comum.LADO}x{comum.LADO}); recortei na proporção")
    alpha = im.getchannel("A")
    if alpha.getextrema()[0] > ALFA:
        rel["avisos"].append("página SEM fundo transparente: não recortei (refazer pedindo PNG transparente)")
        return rel
    op = mascara_opaca(im)
    cw = W / NCOLS
    cols = []
    for c in range(NCOLS):
        x0, x1 = int(round(c * cw)), int(round((c + 1) * cw))
        cheios = sum(largura_opaca(op, W, x0, x1, y) for y in range(0, H, 4))
        if cheios < 0.01 * (x1 - x0) * (H // 4):
            rel["colunas"].append({"coluna": c + 1, "vazia": True})
            continue
        y, metodo = linha_de_corte(op, W, H, x0, x1)
        cols.append((c + 1, x0, x1, y, metodo))
    if not cols:
        rel["avisos"].append("nenhuma pessoa encontrada")
        return rel

    # CORPO: cresce ao mesmo tempo a partir dos pés de cada coluna
    dono = bytearray(W * H)  # 0 = ninguém; c = coluna dona
    corte = {c: y for c, _, _, y, _ in cols}
    fila = deque()
    for c, x0, x1, cut, _ in cols:
        ymax = next((y for y in range(H - 1, cut - 1, -1) if largura_opaca(op, W, x0, x1, y)), None)
        if ymax is None:
            continue
        for y in range(max(cut, ymax - int(H * 0.02)), ymax + 1):
            for x in range(x0, x1):
                k = y * W + x
                if op[k] and not dono[k]:
                    dono[k] = c
                    fila.append(k)
    while fila:
        k = fila.popleft()
        c = dono[k]
        x, y = k % W, k // W
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and corte[c] <= ny < H:
                nk = ny * W + nx
                if op[nk] and not dono[nk]:
                    dono[nk] = c
                    fila.append(nk)

    os.makedirs(saida, exist_ok=True)
    zero = Image.new("L", (W, H), 0)
    for c, x0, x1, cut, metodo in cols:
        info = {"coluna": c, "corte_y": cut, "metodo": metodo}
        pts = [k for k in range(cut * W, W * H) if dono[k] == c]
        if len(pts) < 500:
            info["erro"] = "corpo não encontrado (os pés precisam estar na parte de baixo da coluna)"
            rel["colunas"].append(info)
            continue
        xs = [k % W for k in pts]
        ys = [k // W for k in pts]
        if min(xs) < x0 - 6 or max(xs) > x1 + 6:
            info["aviso_corpo"] = "o corpo passa da linha da coluna (conferir se não levou pedaço do vizinho)"
        if max(ys) < H * 0.90:
            info["aviso_pes"] = f"pés em y={max(ys)} (esperado perto de {int(H * 0.966)})"
        mask = Image.new("L", (W, H), 0)
        mb = bytearray(W * H)
        for k in pts:
            mb[k] = 255
        mask.frombytes(bytes(mb))
        mask = mask.filter(ImageFilter.MaxFilter(3))
        corpo = im.copy()
        corpo.putalpha(Image.composite(alpha, zero, mask))
        corpo = corpo.crop((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
        w, h = corpo.size
        HH = int(h / 0.96)
        WW = HH // 2
        if WW < w:
            WW, HH = w, 2 * w
        tela = Image.new("RGBA", (WW, HH), (0, 0, 0, 0))
        tela.paste(corpo, ((WW - w) // 2, HH - h - int(HH * 0.02)), corpo)
        tela = tela.resize(CORPO, Image.LANCZOS)
        tela, n_il, px_il = limpar_ilhas(tela)
        arq_corpo = f"{nome}_col{c}_corpo.png"
        tela.save(os.path.join(saida, arq_corpo))
        info["corpo"] = f"recortes/{arq_corpo}"
        info["ilhas_corpo"] = n_il

        # ROSTO: faixa de cima da coluna; descarta fiapos (< 3% da maior mancha)
        face = im.crop((x0, 0, x1, cut))
        fw, fh = face.size
        fa = face.getchannel("A")
        grupos = componentes(mascara_opaca(face), fw, fh)
        if not grupos:
            info["erro"] = "rosto não encontrado"
            rel["colunas"].append(info)
            continue
        maior = max(map(len, grupos))
        fb = bytearray(fw * fh)
        fiapos = 0
        for g in grupos:
            if len(g) >= FIAPO_ROSTO * maior:
                for k in g:
                    fb[k] = 255
            else:
                fiapos += 1
        fm = Image.new("L", (fw, fh), 0)
        fm.frombytes(bytes(fb))
        fm = fm.filter(ImageFilter.MaxFilter(3))
        face.putalpha(Image.composite(fa, Image.new("L", (fw, fh), 0), fm))
        face = face.crop(face.getchannel("A").point(lambda v: 255 if v > ALFA else 0).getbbox())
        w, h = face.size
        L = max(w, h)
        tela = Image.new("RGBA", (L, L), (0, 0, 0, 0))
        tela.paste(face, ((L - w) // 2, L - h), face)
        tela = tela.resize(ROSTO, Image.LANCZOS)
        tela, n_il2, _ = limpar_ilhas(tela)
        arq_rosto = f"{nome}_col{c}_rosto.png"
        tela.save(os.path.join(saida, arq_rosto))
        info.update(rosto=f"recortes/{arq_rosto}", fiapos_rosto=fiapos, ilhas_rosto=n_il2)
        rel["colunas"].append(info)
    rel["colunas"].sort(key=lambda x: x["coluna"])
    return rel


# ---------------------------------------------------------------- fichas

def pessoas_do_roster(lote):
    cam = os.path.join(lote, "roster.json")
    if not os.path.exists(cam):
        return None
    roster = comum.ler_json(cam)
    try:
        import npc_montar_prompts as nmp
        partes, _ = nmp.visuais_das_partes(lote)
    except Exception:
        partes = {}
    out = {}
    for pg in roster.get("paginas", []):
        for i, p in enumerate(pg.get("pessoas") or [], 1):
            c = p.get("coluna", i)
            out[(pg["pagina"], c)] = dict(p, _visual=p.get("visual") or partes.get(p.get("nome"), ("", ""))[0])
    return out


def atualizar_fichas(lote, recortes_feitos):
    tema = comum.ler_json(os.path.join(lote, "tema.json"), {})
    cam = os.path.join(lote, "fichas.json")
    atual = comum.ler_json(cam, {"lote": tema.get("lote") or os.path.basename(lote), "fichas": []})
    por_pos = {(f.get("pagina"), f.get("coluna")): f for f in atual.get("fichas", [])}
    roster = pessoas_do_roster(lote)
    avisos = []
    chaves = set(por_pos) | set(recortes_feitos) | (set(roster) if roster else set())
    for chave in chaves:
        pg, c = chave
        f = por_pos.get(chave, {"pagina": pg, "coluna": c})
        p = (roster or {}).get(chave)
        if p:
            for campo_f, campo_r in (("nome", "nome"), ("genero", "genero"), ("idade", "idade"), ("papel", "papel"),
                                     ("etnia", "subtipo")):
                if p.get(campo_r) not in (None, ""):
                    f[campo_f] = p[campo_r]
            if p.get("descricao"):
                f["descricao"] = p["descricao"]
            if p.get("_visual"):
                f["visual"] = p["_visual"]
        f.setdefault("nome", None)
        if tema.get("titulo"):
            f["tema"] = tema["titulo"]
        f.setdefault("descricao", "")
        for tipo in ("rosto", "corpo"):
            rel = f"recortes/pagina_{pg:03d}_col{c}_{tipo}.png"
            f[tipo] = rel if os.path.exists(os.path.join(lote, rel)) else None
        por_pos[chave] = f
        rot = f"p{pg:03d}c{c} {f.get('nome') or '?'}"
        if not f.get("nome"):
            avisos.append(f"{rot}: ficha sem nome (sem roster.json para esta posição)")
        if not f.get("descricao"):
            avisos.append(f"{rot}: ficha sem descrição (lore curta obrigatória na entrega)")
        if not f["rosto"] or not f["corpo"]:
            avisos.append(f"{rot}: falta recorte ({'rosto' if not f['rosto'] else ''} {'corpo' if not f['corpo'] else ''})".strip())
    ordem = ["nome", "genero", "idade", "papel", "etnia", "tema", "descricao", "visual", "pagina", "coluna", "rosto", "corpo"]
    fichas = []
    for chave in sorted(por_pos):
        f = por_pos[chave]
        fichas.append({**{k: f[k] for k in ordem if k in f}, **{k: v for k, v in f.items() if k not in ordem}})
    atual["fichas"] = fichas
    comum.gravar_json(cam, atual)
    return len(fichas), avisos


# ---------------------------------------------------------------- main

def main():
    lote = comum.pasta_lote(sys.argv, USO)
    args = sys.argv[1:]
    pasta = os.path.join(lote, "paginas")
    if "--paginas" in args:
        try:
            nums = [int(x) for x in args[args.index("--paginas") + 1].split(",") if x.strip()]
        except (IndexError, ValueError):
            sys.exit("--paginas espera números separados por vírgula (ex.: --paginas 1,3)")
    else:
        nums = sorted(int(m.group(1)) for f in (os.listdir(pasta) if os.path.isdir(pasta) else [])
                      for m in [re.match(r"pagina_(\d{3})\.png$", f)] if m)
    if not nums:
        sys.exit(f"nenhuma página em {pasta} (pagina_NNN.png)")
    rel_cam = os.path.join(lote, "validacao", "recortes.json")
    relatorio = {r["pagina"]: r for r in comum.ler_json(rel_cam, [])}
    feitos = set()
    for n in nums:
        nome = f"pagina_{n:03d}"
        src = os.path.join(pasta, nome + ".png")
        if not os.path.exists(src):
            print(f"{nome}: sem imagem, pulei")
            continue
        r = recortar_pagina(src, os.path.join(lote, "recortes"), nome)
        relatorio[nome] = r
        ok = [x for x in r["colunas"] if x.get("rosto") and x.get("corpo")]
        feitos |= {(n, x["coluna"]) for x in ok}
        print(f"{nome}: {len(ok)} pessoa(s) recortada(s)")
        for x in r["avisos"]:
            print(f"  ! {x}")
        for x in r["colunas"]:
            for k in ("erro", "aviso_corpo", "aviso_pes"):
                if x.get(k):
                    print(f"  ! coluna {x['coluna']}: {x[k]}")
            if x.get("metodo", "").startswith("linha mais vazia"):
                print(f"  ! coluna {x['coluna']}: sem vão entre busto e corpo; corte em y={x['corte_y']} (conferir)")
    comum.gravar_json(rel_cam, [relatorio[k] for k in sorted(relatorio)])
    total, avisos = atualizar_fichas(lote, feitos)
    for x in sorted(avisos):
        print(f"aviso: {x}")
    print(f"fichas.json: {total} fichas; relatório em validacao/recortes.json")


if __name__ == "__main__":
    main()
