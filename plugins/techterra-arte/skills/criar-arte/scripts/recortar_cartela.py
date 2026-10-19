# -*- coding: utf-8 -*-
"""Recorta as cartelas 2x2 de monstros do lote em tiles 512x512 RGBA e encaixa as avulsas por cima.

    python recortar_cartela.py <lote> [--cartelas 1,3]

Lê   <lote>/monstros.json (n, nome, tier, arquivo, cartela/linha/coluna)
     <lote>/cartelas/cartela_NNN_original.png
     <lote>/validacao/avulsas*.json  (lista {"cartela","linha","coluna","nome","arquivo"})
Grava <lote>/recortes/<arquivo da ficha>, <lote>/recortes/_visao_geral.png e <lote>/validacao/recorte.json.

- Cada criatura é localizada pelo alfa (componentes conexos, 8-conexo) e cada componente vai para a célula onde
  está a maior parte dele: cauda ou asa que passa a linha do meio sem encostar vai inteira com a dona.
- Duas criaturas encostadas viram uma peça só: aí (e só aí) corta pela linha da grade, e a célula é relatada.
- O tile leva a criatura inteira centrada, com 4% de folga. Reduzir para 512 é o normal; ampliar é limitado a
  1,5x (acima disso a imagem borra: a criatura fica menor no tile e a célula é relatada como "pequena").
- DEPOIS das cartelas, a avulsa mais recente de cada célula (maior _vK; empate = a última registrada) é recortada
  como grade 1 e sobrescreve o recorte daquela célula. Avulsa com "usar_no_recorte": false fica de fora.
- --cartelas 1,3 recorta só essas cartelas (e as avulsas delas); a visão geral sempre mostra o lote inteiro.
- Nada é apagado de recortes/: arquivo que não é de nenhuma ficha só é avisado.
Sai 1 se alguma célula ficou sem recorte.
"""
import os
import re
import sys
from collections import deque

sys.dont_write_bytecode = True  # nada é gravado dentro da skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

TILE = comum.RECORTE
MARGEM = 0.04          # 4% de folga em volta da criatura
ALFA_MIN = 32
COMPONENTE_MIN = 40    # pixels; menores que isso são poeira e são ignorados
MAX_AMPLIA = 1.5       # acima disso não amplia (borra): centraliza menor
PECA_GRANDE = 0.15     # peça >= 15% da maior peça da célula conta como "grande"
USO = "uso: python recortar_cartela.py <pasta do lote> [--cartelas 1,3]"


def componentes(alpha, w, h):
    """Rótulos por BFS (8-conexo). Devolve lista de listas de índices de pixel."""
    dados = alpha.tobytes()
    visto = bytearray(w * h)
    comps = []
    for inicio in range(w * h):
        if visto[inicio] or dados[inicio] <= ALFA_MIN:
            continue
        fila = deque([inicio])
        visto[inicio] = 1
        pix = []
        while fila:
            i = fila.popleft()
            pix.append(i)
            x, y = i % w, i // w
            for dy in (-1, 0, 1):
                ny = y + dy
                if ny < 0 or ny >= h:
                    continue
                for dx in (-1, 0, 1):
                    nx = x + dx
                    if nx < 0 or nx >= w:
                        continue
                    j = ny * w + nx
                    if not visto[j] and dados[j] > ALFA_MIN:
                        visto[j] = 1
                        fila.append(j)
        if len(pix) >= COMPONENTE_MIN:
            comps.append(pix)
    return comps


def recortar(caminho, grade=2):
    """Devolve {(l, c): (tile RGBA 512 ou None, info)} com l, c a partir de 0."""
    im = Image.open(caminho).convert("RGBA")
    w, h = im.size
    comps = componentes(im.getchannel("A"), w, h)
    grupos = {(l, c): [] for l in range(grade) for c in range(grade)}
    encostada = set()

    def celula(i):
        return (min(grade - 1, int((i // w) / (h / grade))), min(grade - 1, int((i % w) / (w / grade))))

    for pix in comps:
        por_celula = {}
        for i in pix:
            por_celula.setdefault(celula(i), []).append(i)
        # duas criaturas encostadas viram uma peça só: se mais de uma célula tem fatia grande (>= 35%),
        # corta pela linha da grade. Fatia menor (cabeça ou cauda que INVADE a vizinha) fica com a dominante.
        fatias_grandes = [k for k, v in por_celula.items() if len(v) >= 0.35 * len(pix)]
        if len(fatias_grandes) > 1:
            for k, v in por_celula.items():
                grupos[k].append(v)
                encostada.add(k)
        else:
            dono = max(por_celula, key=lambda k: len(por_celula[k]))
            grupos[dono].append(pix)
    saida = {}
    for (l, c), lista in grupos.items():
        info = {"pecas": len(lista), "pecas_grandes": 0, "encostada": (l, c) in encostada, "borda": False,
                "escala": None, "problemas": []}
        if not lista:
            info["problemas"].append("sem criatura na célula")
            saida[(l, c)] = (None, info)
            continue
        maior = max(len(p) for p in lista)
        info["pecas_grandes"] = sum(1 for p in lista if len(p) >= PECA_GRANDE * maior)
        mascara = Image.new("L", (w, h), 0)
        m = mascara.load()
        x0 = y0 = 10 ** 9
        x1 = y1 = -1
        for pix in lista:
            for i in pix:
                x, y = i % w, i // w
                m[x, y] = 255
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
        info["borda"] = x0 <= 0 or y0 <= 0 or x1 >= w - 1 or y1 >= h - 1
        # inclui o anti-aliasing da borda (alfa baixo) em volta dos pixels do grupo
        mascara = mascara.filter(ImageFilter.MaxFilter(5))
        so = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        so.paste(im, (0, 0), mascara)
        x0, y0 = max(0, x0 - 3), max(0, y0 - 3)
        x1, y1 = min(w, x1 + 4), min(h, y1 + 4)
        criatura = so.crop((x0, y0, x1, y1))
        lado = max(criatura.size)
        escala = TILE / max(lado_total_min(lado), 1)
        if escala > MAX_AMPLIA:
            escala = MAX_AMPLIA
            info["problemas"].append(f"criatura pequena ({lado}px): ampliada só {MAX_AMPLIA}x, fica menor no tile")
        nova = (max(1, round(criatura.width * escala)), max(1, round(criatura.height * escala)))
        if nova != criatura.size:
            criatura = criatura.resize(nova, Image.LANCZOS)
        tile = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
        tile.paste(criatura, ((TILE - criatura.width) // 2, (TILE - criatura.height) // 2))
        info["escala"] = round(escala, 3)
        if info["encostada"]:
            info["problemas"].append("encostada na vizinha: cortada pela linha da grade")
        if info["borda"]:
            info["problemas"].append("criatura cortada na borda da imagem")
        if info["pecas_grandes"] > 1:
            info["problemas"].append(f"{info['pecas_grandes']} peças grandes separadas (segunda criatura ou parte solta?)")
        saida[(l, c)] = (tile, info)
    return saida


def lado_total_min(lado):
    return int(round(lado / (1 - 2 * MARGEM)))


def arquivo_cartela(lote, n):
    for nome in (f"cartela_{n:03d}_original.png", f"cartela_{n:02d}_original.png"):
        p = os.path.join(lote, "cartelas", nome)
        if os.path.exists(p):
            return p
    return None


def versao(arq):
    m = re.search(r"_v(\d+)\.png$", arq or "", re.I)
    return int(m.group(1)) if m else 0


def ler_avulsas(lote):
    """{(cartela, linha, coluna): entrada} com a avulsa mais recente de cada célula."""
    pasta = os.path.join(lote, "validacao")
    escolha, ordem = {}, 0
    if not os.path.isdir(pasta):
        return escolha
    for nome in sorted(os.listdir(pasta)):
        if not (nome.startswith("avulsas") and nome.endswith(".json")):
            continue
        dado = comum.ler_json(os.path.join(pasta, nome), [])
        if isinstance(dado, dict):
            dado = dado.get("avulsas", [])
        for a in dado:
            ordem += 1
            if not isinstance(a, dict) or a.get("usar_no_recorte") is False or not a.get("arquivo"):
                continue
            try:
                chave = (int(a["cartela"]), int(a["linha"]), int(a["coluna"]))
            except (KeyError, TypeError, ValueError):
                print(f"  avulsa mal registrada em {nome}: {a}")
                continue
            rank = (versao(a["arquivo"]), ordem)
            if chave not in escolha or rank >= escolha[chave][0]:
                escolha[chave] = (rank, dict(a, _registro=nome))
    return {k: v[1] for k, v in escolha.items()}


def fonte(tam):
    for f in ("arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(f, tam)
        except OSError:
            pass
    return ImageFont.load_default()


def visao_geral(lote, fichas, estado):
    col, cel, rot = 8, 200, 34
    lin = max(1, (len(fichas) + col - 1) // col)
    folha = Image.new("RGB", (col * cel, lin * (cel + rot)), (48, 48, 52))
    d = ImageDraw.Draw(folha)
    f = fonte(14)
    for k, m in enumerate(fichas):
        x, y = (k % col) * cel, (k // col) * (cel + rot)
        p = os.path.join(lote, "recortes", m["arquivo"])
        est = estado.get(m["arquivo"], {})
        if os.path.exists(p):
            t = Image.open(p).convert("RGBA")
            mini = t.resize((cel - 10, cel - 10), Image.LANCZOS)
            folha.paste(mini, (x + 5, y + 5), mini)
        else:
            d.rectangle((x + 5, y + 5, x + cel - 6, y + cel - 6), outline=(200, 60, 60), width=2)
            d.text((x + 20, y + cel // 2 - 8), "SEM RECORTE", fill=(230, 90, 90), font=f)
        if est.get("problemas"):
            d.rectangle((x + 2, y + 2, x + cel - 3, y + cel - 3), outline=(230, 170, 40), width=2)
        marca = "*" if est.get("origem") == "avulsa" else ""
        d.text((x + 6, y + cel + 2), f"{m.get('n', k + 1):02d}{marca} T{m.get('tier', '?')} {m.get('nome', '?')}"[:26],
               fill=(235, 235, 235), font=f)
    caminho = os.path.join(lote, "recortes", "_visao_geral.png")
    folha.save(caminho)
    return caminho


def main(argv):
    lote = comum.pasta_lote(argv, USO)
    so_cartelas = None
    if "--cartelas" in argv:
        i = argv.index("--cartelas")
        try:
            so_cartelas = {int(x) for x in argv[i + 1].split(",") if x.strip()}
        except (IndexError, ValueError):
            print(USO)
            sys.exit(2)
    dado = comum.ler_json(os.path.join(lote, "monstros.json"))
    fichas = dado["monstros"] if isinstance(dado, dict) else dado
    fichas = sorted(fichas, key=lambda m: (m.get("n") or 0, m.get("cartela", 0), m.get("linha", 0), m.get("coluna", 0)))
    erros_ficha = []
    for m in fichas:
        if not m.get("arquivo") and m.get("n") and m.get("nome") and m.get("tier"):
            m["arquivo"] = comum.arquivo_recorte(int(m["n"]), int(m["tier"]), m["nome"])
        if not m.get("arquivo") or not all(m.get(k) for k in ("cartela", "linha", "coluna")):
            erros_ficha.append(m.get("nome") or f"n={m.get('n')}")
    fichas_ok = [m for m in fichas if m.get("arquivo") and all(m.get(k) for k in ("cartela", "linha", "coluna"))]
    os.makedirs(os.path.join(lote, "recortes"), exist_ok=True)
    reg_path = os.path.join(lote, "validacao", "recorte.json")
    anterior = comum.ler_json(reg_path, {}).get("celulas", {}) if os.path.exists(reg_path) else {}
    estado = dict(anterior)
    avulsas = ler_avulsas(lote)
    cartelas = sorted({int(m["cartela"]) for m in fichas_ok})
    alvo = [c for c in cartelas if so_cartelas is None or c in so_cartelas]
    faltas, n_avulsas, gravados = [], 0, 0
    for n in alvo:
        doc = [m for m in fichas_ok if int(m["cartela"]) == n]
        arq = arquivo_cartela(lote, n)
        tiles = recortar(arq) if arq else {}
        if not arq:
            print(f"cartela {n:03d}: sem cartelas/cartela_{n:03d}_original.png")
        # 1) recorte geral da cartela
        for m in doc:
            l, c = int(m["linha"]), int(m["coluna"])
            tile, info = tiles.get((l - 1, c - 1), (None, {"problemas": ["cartela sem original"] if not arq else
                                                                  ["sem criatura na célula"]}))
            estado[m["arquivo"]] = {"nome": m.get("nome"), "cartela": n, "linha": l, "coluna": c, "origem": "cartela",
                                    "fonte": os.path.relpath(arq, lote).replace("\\", "/") if arq else None,
                                    "problemas": list(info.get("problemas", [])), "escala": info.get("escala")}
            if tile is not None:
                tile.save(os.path.join(lote, "recortes", m["arquivo"]))
                gravados += 1
        # 2) avulsas por cima (sempre DEPOIS do recorte geral)
        for m in doc:
            l, c = int(m["linha"]), int(m["coluna"])
            a = avulsas.get((n, l, c))
            if not a:
                continue
            p = os.path.join(lote, a["arquivo"])
            if not os.path.exists(p):
                estado[m["arquivo"]]["problemas"].append(f"avulsa registrada não existe: {a['arquivo']}")
                continue
            tile, info = recortar(p, grade=1)[(0, 0)]
            if tile is None:
                estado[m["arquivo"]]["problemas"].append(f"avulsa vazia: {a['arquivo']}")
                continue
            tile.save(os.path.join(lote, "recortes", m["arquivo"]))
            n_avulsas += 1
            if a.get("nome") and m.get("nome") and comum.norm(a["nome"]) != comum.norm(m["nome"]):
                info["problemas"].append(f"avulsa registrada com outro nome ({a['nome']})")
            estado[m["arquivo"]].update(origem="avulsa", fonte=a["arquivo"], registro=a["_registro"],
                                        problemas=list(info["problemas"]), escala=info["escala"])
        if arq:
            print(f"cartela {n:03d}: ok")
    for m in fichas_ok:
        if not os.path.exists(os.path.join(lote, "recortes", m["arquivo"])):
            faltas.append(f"cartela {int(m['cartela']):03d} L{m['linha']}C{m['coluna']} {m.get('nome')} -> {m['arquivo']}")
    validos = {m["arquivo"] for m in fichas_ok}
    estado = {k: v for k, v in estado.items() if k in validos}
    sobras = sorted(x for x in os.listdir(os.path.join(lote, "recortes"))
                    if x.lower().endswith(".png") and not x.startswith("_") and x not in validos)
    comum.gravar_json(reg_path, {"celulas": estado, "faltando": faltas, "sobras": sobras})
    vg = visao_geral(lote, fichas_ok, estado)
    print(f"{gravados} recortes de cartela + {n_avulsas} de avulsas | faltando: {len(faltas)}")
    print(f"visão geral: {os.path.relpath(vg, lote)} (* = avulsa; moldura amarela = problema)")
    problemas = [(k, v) for k, v in estado.items() if v.get("problemas")]
    for k, v in problemas:
        print(f"  PROBLEMA {v['cartela']:03d} L{v['linha']}C{v['coluna']} {v.get('nome')} [{v['origem']}]: "
              + "; ".join(v["problemas"]))
    for x in faltas:
        print("  falta:", x)
    for x in erros_ficha:
        print("  ficha sem arquivo/cartela/linha/coluna:", x)
    for x in sobras:
        print("  aviso: recortes/" + x + " não é de nenhuma ficha")
    sys.exit(1 if faltas or erros_ficha else 0)


if __name__ == "__main__":
    main(sys.argv)
