# -*- coding: utf-8 -*-
"""Cartela de capas 2x2 (cenas 3:4 separadas por faixa branca) → 4 capas 510×680 WebP.

    python capas_converter.py <lote>            [--saida finais]   (todas as cartelas de <lote>/cartelas/)
    python capas_converter.py <cartela.png>     [--saida finais]   (uma cartela só)

Regras: regras/cenarios-mapas-capas.md §5; tamanhos: regras/formatos.md.

- Acha a cruz branca pelas linhas e colunas quase todas brancas perto do meio (tolera a cartela fora de
  1536×2048, como 1086×1448, e a faixa fora de 40 px); sem faixa achada, corta pela geometria e avisa.
- Apara sobras brancas na borda de cada cena, recorta 3:4 pelo centro e reduz para 510×680 (WebP qualidade 90).
- Confere o miolo 146×188 do centro (o que o cartão do jogo mostra): avisa se estiver uniforme/vazio ou claro
  demais, e avisa se sobrou faixa branca na borda da capa.
- Ordem: 1 = cima-esquerda, 2 = cima-direita, 3 = baixo-esquerda, 4 = baixo-direita.

Nome das capas: com `<lote>/plano.json` no formato
  {"cartelas": [{"cartela": 1, "grupo": "expedicoes", "cenas": ["agua", "marinho", "gelo", "vento"]}]}
sai `finais/<grupo>_<cena>.webp`; sem ele, `finais/<nome_da_cartela>_<1..4>.webp`.
Em <lote>/cartelas/, por número de cartela, usa a tentativa mais alta (`_vN`, senão `_original`) e ignora `_ruimN`.
Nunca sobrescreve uma capa que já existe (só mede). Registra em `<lote>/entregas.json` e grava
`conferencia/capas_<cartela>.jpg` (as 4 capas com o miolo marcado). Sai com código 1 se alguma cartela falhou.
"""
import os
import re
import sys

sys.dont_write_bytecode = True   # nada de __pycache__ dentro da skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402
from fundos_normalizar import atualizar_entregas, fora_da_skill, opcao, rel  # noqa: E402

try:
    from PIL import Image, ImageChops, ImageDraw, ImageStat
except ImportError:
    print("Falta o Pillow: pip install pillow")
    sys.exit(2)

USO = "\n".join(__doc__.strip().splitlines()[2:4])
CW, CH = 510, 680              # capa final
MW, MH = 146, 188              # miolo que o cartão recorta pelo centro
BRANCO = 228                   # canal acima disso conta como branco
LINHA_BRANCA = 0.85            # fração de pixels brancos para a linha/coluna ser faixa
DESVIO_MIOLO_MIN = 18          # abaixo disso o miolo está chapado (palco vazio/uniforme)
EXTS = (".png", ".jpg", ".jpeg", ".webp")


def mascara_branca(im):
    r, g, b = im.convert("RGB").split()
    f = lambda c: c.point(lambda v: 255 if v >= BRANCO else 0)  # noqa: E731
    return ImageChops.darker(ImageChops.darker(f(r), f(g)), f(b))


def perfil(mascara, eixo):
    """Fração de branco por coluna (eixo 'x') ou por linha (eixo 'y')."""
    w, h = mascara.size
    tira = mascara.resize((w, 1) if eixo == "x" else (1, h), Image.Resampling.BOX)
    return [v / 255 for v in tira.tobytes()]


def faixa_central(fracoes):
    """Maior sequência de linhas brancas entre 30% e 70% do eixo; devolve (início, fim) ou None."""
    n = len(fracoes)
    melhor, ini = None, None
    for i in range(int(n * 0.30), int(n * 0.70) + 1):
        branca = i < n and fracoes[i] >= LINHA_BRANCA
        if branca and ini is None:
            ini = i
        if (not branca or i == int(n * 0.70)) and ini is not None:
            fim = i if not branca else i + 1
            if melhor is None or fim - ini > melhor[1] - melhor[0]:
                melhor = (ini, fim)
            ini = None
    return melhor


def aparar(cena):
    """Tira linhas/colunas quase brancas das bordas (sobra da faixa ou moldura) + 2 px de segurança."""
    m = mascara_branca(cena)
    fx, fy = perfil(m, "x"), perfil(m, "y")
    w, h = cena.size
    x0, x1, y0, y1 = 0, w, 0, h
    lim_x, lim_y = int(w * 0.08), int(h * 0.08)
    while x0 < lim_x and fx[x0] >= 0.6:
        x0 += 1
    while w - x1 < lim_x and fx[x1 - 1] >= 0.6:
        x1 -= 1
    while y0 < lim_y and fy[y0] >= 0.6:
        y0 += 1
    while h - y1 < lim_y and fy[y1 - 1] >= 0.6:
        y1 -= 1
    return cena.crop((x0 + 2, y0 + 2, x1 - 2, y1 - 2)), (x0, y0, w - x1, h - y1)


def cover_34(cena):
    w, h = cena.size
    if w / h > CW / CH:
        nw = round(h * CW / CH)
        x = (w - nw) // 2
        cena = cena.crop((x, 0, x + nw, h))
    else:
        nh = round(w * CH / CW)
        y = (h - nh) // 2
        cena = cena.crop((0, y, w, y + nh))
    return cena.resize((CW, CH), Image.Resampling.LANCZOS)


def conferir_capa(capa):
    avisos = []
    x, y = (CW - MW) // 2, (CH - MH) // 2
    miolo = capa.crop((x, y, x + MW, y + MH)).convert("L")
    st = ImageStat.Stat(miolo)
    media, desvio = round(st.mean[0], 1), round(st.stddev[0], 1)
    if desvio < DESVIO_MIOLO_MIN:
        avisos.append(f"miolo 146×188 uniforme (desvio {desvio}): palco vazio no centro?")
    if media > 235:
        avisos.append(f"miolo quase branco (média {media})")
    m = mascara_branca(capa)
    for nome, caixa in dict(topo=(0, 0, CW, 4), base=(0, CH - 4, CW, CH), esquerda=(0, 0, 4, CH),
                            direita=(CW - 4, 0, CW, CH)).items():
        if ImageStat.Stat(m.crop(caixa)).mean[0] / 255 > 0.5:
            avisos.append(f"faixa branca sobrou na borda ({nome})")
    return {"miolo_media": media, "miolo_desvio": desvio}, avisos


def separar(im):
    """Devolve as 4 cenas (ordem de leitura), as faixas achadas e os avisos."""
    w, h = im.size
    avisos = []
    if w >= h:
        avisos.append(f"cartela não é retrato ({w}×{h})")
    elif abs((w / h) / 0.75 - 1) > 0.05:
        avisos.append(f"cartela {w}×{h} fora de 3:4")
    m = mascara_branca(im)
    vx, hy = faixa_central(perfil(m, "x")), faixa_central(perfil(m, "y"))
    meia = max(1, round(40 * w / 1536 / 2))
    if vx is None:
        vx = (w // 2 - meia, w // 2 + meia)
        avisos.append("faixa branca vertical não achada: cortado pela geometria")
    if hy is None:
        hy = (h // 2 - meia, h // 2 + meia)
        avisos.append("faixa branca horizontal não achada: cortado pela geometria")
    caixas = [(0, 0, vx[0], hy[0]), (vx[1], 0, w, hy[0]), (0, hy[1], vx[0], h), (vx[1], hy[1], w, h)]
    return [im.crop(c) for c in caixas], {"vertical": list(vx), "horizontal": list(hy)}, avisos


def escolher_cartelas(pasta):
    """Por número de cartela, a tentativa mais alta (_vN > _original > sem sufixo); ignora _ruimN."""
    grupos = {}
    for f in sorted(os.listdir(pasta)):
        low = f.lower()
        if not low.endswith(EXTS) or re.search(r"_ruim\d*\.", low):
            continue
        stem = os.path.splitext(f)[0]
        base = re.sub(r"_(v\d+|original)$", "", stem)
        mv = re.search(r"_v(\d+)$", stem)
        peso = int(mv.group(1)) + 1 if mv else (0 if stem.endswith("_original") else -1)
        if base not in grupos or peso > grupos[base][0]:
            grupos[base] = (peso, os.path.join(pasta, f))
    return [v[1] for _, v in sorted(grupos.items())]


def nomes_do_plano(lote, caminho):
    plano = comum.ler_json(os.path.join(lote, "plano.json"), {})
    num = re.search(r"(\d+)", os.path.basename(caminho))
    for c in plano.get("cartelas", []) if isinstance(plano, dict) else []:
        cenas = c.get("cenas") or []
        if num and int(num.group(1)) == int(c.get("cartela", -1)) and len(cenas) == 4:
            pre = comum.slug(c["grupo"]) + "_" if c.get("grupo") else ""
            return [pre + comum.slug(x) for x in cenas]
    base = re.sub(r"_(v\d+|original)$", "", os.path.splitext(os.path.basename(caminho))[0])
    return [f"{comum.slug(base)}_{k}" for k in range(1, 5)]


def conferencia(capas, destino_img):
    folha = Image.new("RGB", (4 * (CW // 2) + 50, CH // 2 + 20), (32, 28, 30))
    d = ImageDraw.Draw(folha)
    for k, capa in enumerate(capas):
        x = 10 + k * (CW // 2 + 10)
        folha.paste(capa.resize((CW // 2, CH // 2)), (x, 10))
        mx, my = x + (CW - MW) // 4, 10 + (CH - MH) // 4
        d.rectangle([mx, my, mx + MW // 2, my + MH // 2], outline=(255, 0, 255), width=2)
    folha.save(destino_img, "JPEG", quality=88)


def main():
    argv = sys.argv
    pos = [a for a in argv[1:] if not a.startswith("--") and a != opcao(argv, "--saida")]
    if not pos:
        print(USO)
        sys.exit(2)
    alvo = os.path.abspath(pos[0])
    if os.path.isfile(alvo):
        pasta = os.path.dirname(alvo)
        lote = os.path.dirname(pasta) if os.path.basename(pasta).lower() == "cartelas" else pasta
        cartelas = [alvo]
    elif os.path.isdir(alvo):
        lote = alvo
        pasta = os.path.join(lote, "cartelas")
        if not os.path.isdir(pasta):
            print(f"pasta de cartelas não existe: {pasta}")
            sys.exit(2)
        cartelas = escolher_cartelas(pasta)
    else:
        print(f"não existe: {alvo}")
        sys.exit(2)
    fora_da_skill(lote)
    saida = fora_da_skill(os.path.join(lote, opcao(argv, "--saida", "finais")))
    conf = fora_da_skill(os.path.join(lote, "conferencia"))
    os.makedirs(saida, exist_ok=True)
    os.makedirs(conf, exist_ok=True)
    if not cartelas:
        print(f"nenhuma cartela em {pasta}")
        sys.exit(2)

    itens, falhas = [], 0
    for caminho in cartelas:
        try:
            im = Image.open(caminho).convert("RGB")
        except OSError as e:
            print(f"FALHOU    {caminho}: {e}")
            falhas += 1
            continue
        cenas, faixas, av_cartela = separar(im)
        nomes = nomes_do_plano(lote, caminho)
        print(f"{os.path.basename(caminho)}  {im.size[0]}×{im.size[1]}  faixas x{faixas['vertical']} "
              f"y{faixas['horizontal']}")
        for a in av_cartela:
            print(f"          aviso: {a}")
        capas = []
        for k, (cena, nome) in enumerate(zip(cenas, nomes), 1):
            final = os.path.join(saida, nome + ".webp")
            limpa, aparado = aparar(cena)
            avisos = list(av_cartela)
            prop = limpa.size[0] / limpa.size[1]
            if abs(prop / 0.75 - 1) > 0.08:
                avisos.append(f"cena {limpa.size[0]}×{limpa.size[1]} longe de 3:4: o recorte central perde borda")
            if os.path.isfile(final):
                capa = Image.open(final).convert("RGB")
                avisos.append("capa já existia: só medida")
            else:
                capa = cover_34(limpa)
                capa.save(final, "WEBP", quality=90, method=6)
            medidas, av = conferir_capa(capa)
            avisos += av
            capas.append(capa)
            reais = [a for a in avisos if not a.startswith("capa já")]
            item = {"id": nome, "destino": "capa", "cartela": rel(caminho, lote), "posicao": k,
                    "arquivo": rel(final, lote), "medida": [CW, CH], "cena_original": list(cena.size),
                    "aparado": list(aparado), "veredito": "aviso" if reais else "ok", "avisos": avisos}
            item.update(medidas)
            itens.append(item)
            print(f"  {'AVISO' if reais else 'OK':6} {k} → {rel(final, lote)}  miolo desvio {medidas['miolo_desvio']}")
            for a in av:
                print(f"          aviso: {a}")
        stem = os.path.splitext(os.path.basename(caminho))[0]
        conferencia(capas, os.path.join(conf, f"capas_{stem}.jpg"))

    ent = atualizar_entregas(lote, itens, "capas")
    print(f"\n{len(itens)} capas de {len(cartelas) - falhas} cartela(s); registro: {ent}")
    print(f"conferência: {conf}")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
