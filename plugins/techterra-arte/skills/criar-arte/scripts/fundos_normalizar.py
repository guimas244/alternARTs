# -*- coding: utf-8 -*-
"""Leva cada bruto de cenário/mapa ao tamanho do destino, mede e registra em entregas.json.

    python fundos_normalizar.py <lote> --destino local|lados|portao|submapa|mundi|narraris_mapa|wallpaper|moldura
                                [--entrada brutos] [--saida finais] [--aceitar]

Tamanhos e formatos: regras/formatos.md. Regras de composição: regras/cenarios-mapas-capas.md.

- Fundos (local, lados, wallpaper): recorte `cover` pelo centro até a proporção do destino (o horizonte fica onde
  estava) e redução; JPG qualidade 92.
- Portão e mapas (portao, submapa, mundi, narraris_mapa): SÓ redimensiona, nunca recorta (a interface e os pinos são
  posições na arte); portão sai JPG, mapa sai PNG. Proporção muito diferente da do destino vira aviso (distorce).
- Moldura de invasão (moldura): PNG RGBA 1672×941, só redimensiona; fundo verde puro vira transparente.

Mede luminância média (alvo 70–200), desvio-padrão do terço central (≥ 25), bordas (moldura suspeita), opacidade e
orientação. Nos fundos de Local/lados isso REPROVA: o final não é gravado (gere de novo do zero) — salvo com
--aceitar, que grava e marca o aviso. Nos demais destinos é só aviso.

Nunca sobrescreve um final que já existe (arte refeita = nome novo, `_v2`): só mede de novo. Ignora `*_ruimN.*`.
Prompt usado: procura `prompts/<nome>.txt` (também sem o `_vN`) ou `<bruto>.prompt.txt`; copia para
`<final>.prompt.txt`. Escreve/atualiza `<lote>/entregas.json` (preserva os campos que o assistente escreveu, como
`nome`, `locais`, `usa_fundo_de`) e grava `conferencia/prancha_<destino>.jpg` (e a grade de 10% dos portões).
Sai com código 1 se alguma imagem reprovou.
"""
import os
import re
import shutil
import sys

sys.dont_write_bytecode = True   # nada de __pycache__ dentro da skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps, ImageStat
except ImportError:
    print("Falta o Pillow: pip install pillow")
    sys.exit(2)

USO = "\n".join(__doc__.strip().splitlines()[2:4])

# destino: (largura, altura, modo, formato, reprova_por_medida)
#   modo "cover" = recorta pelo centro e reduz; "redimensiona" = nunca recorta
DESTINOS = {
    "local": (1672, 941, "cover", "jpg", True),
    "lados": (1536, 864, "cover", "jpg", True),
    "wallpaper": (1672, 941, "cover", "jpg", False),
    "portao": (1600, 900, "redimensiona", "jpg", False),
    "submapa": (1536, 1024, "redimensiona", "png", False),
    "mundi": (1536, 1024, "redimensiona", "png", False),
    "narraris_mapa": (1586, 992, "redimensiona", "png", False),
    "moldura": (1672, 941, "redimensiona", "png", False),
}
LUM_MIN, LUM_MAX = 70, 200
DESVIO_MIN = 25
EXTS = (".png", ".jpg", ".jpeg", ".webp")
TOL_PROPORCAO = 0.03          # acima disso, redimensionar sem recortar distorce de forma visível


def opcao(argv, nome, padrao=None):
    if nome in argv:
        i = argv.index(nome)
        if i + 1 < len(argv):
            return argv[i + 1]
        print(f"falta o valor de {nome}")
        sys.exit(2)
    return padrao


def fora_da_skill(caminho):
    """Aborta se o caminho cair dentro da pasta da skill (ela é trocada a cada atualização)."""
    a, s = os.path.normcase(os.path.abspath(caminho)), os.path.normcase(comum.SKILL_DIR)
    if a == s or a.startswith(s + os.sep):
        print(f"recusado: {caminho} fica dentro da skill. Use a pasta de trabalho do usuário.")
        sys.exit(2)
    return caminho


def rel(caminho, base):
    return os.path.relpath(caminho, base).replace("\\", "/")


def atualizar_entregas(lote, itens, tipo):
    """Mescla `itens` em <lote>/entregas.json pela chave `arquivo` (ou `id`), preservando campos alheios."""
    caminho = os.path.join(lote, "entregas.json")
    dado = comum.ler_json(caminho, {"lote": os.path.basename(lote), "entregas": []})
    if isinstance(dado, list):
        dado = {"lote": os.path.basename(lote), "entregas": dado}
    dado.setdefault("tipo", tipo)
    lista = dado.setdefault("entregas", [])
    for novo in itens:
        alvo = next((e for e in lista if (novo.get("arquivo") and e.get("arquivo") == novo["arquivo"])
                     or (e.get("id") == novo["id"] and e.get("destino") == novo.get("destino"))), None)
        if alvo is None:
            lista.append(novo)
        else:
            alvo.update(novo)
    comum.gravar_json(caminho, dado)
    return caminho


def tem_transparencia(im):
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        return im.convert("RGBA").getchannel("A").getextrema()[0] < 250
    return False


def cover(im, w, h):
    iw, ih = im.size
    if iw / ih > w / h:
        nw = round(ih * w / h)
        x = (iw - nw) // 2
        caixa = (x, 0, x + nw, ih)
    else:
        nh = round(iw * h / w)
        y = (ih - nh) // 2
        caixa = (0, y, iw, y + nh)
    return im.crop(caixa).resize((w, h), Image.Resampling.LANCZOS), list(caixa)


def medir(im):
    """Luminância média, desvio do terço central e média das bordas de 8 px."""
    lum = im.convert("L")
    w, h = lum.size
    media = ImageStat.Stat(lum).mean[0]
    desvio = ImageStat.Stat(lum.crop((w // 3, 0, 2 * w // 3, h))).stddev[0]
    bordas = {k: round(ImageStat.Stat(lum.crop(b)).mean[0], 1) for k, b in
              dict(topo=(0, 0, w, 8), base=(0, h - 8, w, h), esquerda=(0, 0, 8, h), direita=(w - 8, 0, w, h)).items()}
    return round(media, 1), round(desvio, 1), bordas


def chroma_verde(im):
    """Fundo liso verde puro (#00FF00) vira transparente (moldura gerada sem alfa)."""
    rgba = im.convert("RGBA")
    r, g, b, a = rgba.split()
    verde = ImageChops.multiply(ImageChops.multiply(g.point(lambda v: 255 if v > 200 else 0),
                                                    r.point(lambda v: 255 if v < 90 else 0)),
                                b.point(lambda v: 255 if v < 90 else 0))
    rgba.putalpha(ImageChops.subtract(a, verde))
    return rgba


def conferir_moldura(im):
    """Encaixe da moldura de invasão (números só para conferir, regras §5)."""
    a = im.getchannel("A")
    w, h = a.size
    cheio = a.point(lambda v: 255 if v > 24 else 0)
    total = ImageStat.Stat(cheio).mean[0] / 255
    meio = ImageStat.Stat(cheio.crop((round(w * 0.22), 0, round(w * 0.78), h))).mean[0] / 255
    avisos = []
    if meio > 0.002:
        avisos.append(f"arte nos 56% do meio ({meio:.1%} coberto): o meio tem de ficar vazio")
    if total > 0.15:
        avisos.append(f"cobre {total:.0%} da imagem (alvo < 15%)")
    return {"cobertura": round(total, 4), "cobertura_meio": round(meio, 4)}, avisos


def grade_portao(final, destino_img):
    im = Image.open(final).convert("RGB")
    d = ImageDraw.Draw(im)
    w, h = im.size
    for i in range(1, 10):
        d.line([(w * i // 10, 0), (w * i // 10, h)], fill=(255, 255, 0), width=1)
        d.line([(0, h * i // 10), (w, h * i // 10)], fill=(255, 255, 0), width=1)
    for cx in (0.28, 0.72):  # portões: centro x, base 80%, topo 32%, largura ~22%; faixa livre de cima 6–28%
        d.rectangle([w * (cx - 0.11), h * 0.32, w * (cx + 0.11), h * 0.80], outline=(0, 255, 0), width=3)
        d.rectangle([w * (cx - 0.11), h * 0.06, w * (cx + 0.11), h * 0.28], outline=(255, 0, 255), width=2)
    d.rectangle([w * 0.30, h * 0.86, w * 0.70, h - 1], outline=(255, 0, 255), width=2)   # faixa livre de baixo
    d.rectangle([w * 0.42, h * 0.30, w * 0.58, h * 0.84], outline=(0, 200, 255), width=2)  # pilar do centro
    im.save(destino_img, "JPEG", quality=85)


def achar_prompt(lote, entrada, nome_arquivo, stem):
    base = re.sub(r"_v\d+$", "", stem)
    for c in (os.path.join(lote, "prompts", stem + ".txt"), os.path.join(lote, "prompts", base + ".txt"),
              os.path.join(entrada, nome_arquivo + ".prompt.txt"), os.path.join(entrada, stem + ".prompt.txt")):
        if os.path.isfile(c):
            return c
    return None


def prancha(lote, itens, destino, saida_img):
    finais = [i for i in itens if i.get("arquivo") and os.path.isfile(os.path.join(lote, i["arquivo"]))]
    if not finais:
        return None
    tw, th, cols = 400, 0, 4
    w0, h0 = DESTINOS[destino][:2]
    th = round(tw * h0 / w0)
    linhas = (len(finais) + cols - 1) // cols
    folha = Image.new("RGB", (cols * tw, linhas * (th + 22)), (32, 28, 30))
    d = ImageDraw.Draw(folha)
    fonte = ImageFont.load_default()
    for k, it in enumerate(finais):
        x, y = (k % cols) * tw, (k // cols) * (th + 22)
        im = Image.open(os.path.join(lote, it["arquivo"]))
        if im.mode == "RGBA":
            fundo = Image.new("RGB", im.size, (90, 90, 90))
            fundo.paste(im, (0, 0), im)
            im = fundo
        folha.paste(ImageOps.fit(im.convert("RGB"), (tw, th)), (x, y))
        marca = "" if it.get("veredito") == "ok" else f"  [{it.get('veredito')}]"
        d.text((x + 4, y + th + 4), f"{it['id']}  lum {it.get('luminancia', '?')}{marca}", fill=(255, 255, 255),
               font=fonte)
    folha.save(saida_img, "JPEG", quality=90)
    return saida_img


def main():
    argv = sys.argv
    lote = comum.pasta_lote(argv, USO)
    destino = opcao(argv, "--destino")
    if destino not in DESTINOS:
        print(USO)
        print("destinos: " + ", ".join(DESTINOS))
        sys.exit(2)
    W, H, modo, fmt, reprova = DESTINOS[destino]
    entrada = os.path.join(lote, opcao(argv, "--entrada", "brutos"))
    saida = fora_da_skill(os.path.join(lote, opcao(argv, "--saida", "finais")))
    conf = fora_da_skill(os.path.join(lote, "conferencia"))
    fora_da_skill(lote)
    aceitar = "--aceitar" in argv
    if not os.path.isdir(entrada):
        print(f"pasta de brutos não existe: {entrada}")
        sys.exit(2)
    os.makedirs(saida, exist_ok=True)

    brutos = sorted(f for f in os.listdir(entrada)
                    if f.lower().endswith(EXTS) and not re.search(r"_ruim\d*\.", f.lower()))
    if not brutos:
        print(f"nenhum bruto em {entrada}")
        sys.exit(2)

    itens, reprovados = [], 0
    for nome in brutos:
        stem = os.path.splitext(nome)[0]
        caminho_bruto = os.path.join(entrada, nome)
        final = os.path.join(saida, f"{stem}.{fmt}")
        im = Image.open(caminho_bruto)
        iw, ih = im.size
        erros, avisos, extra = [], [], {}
        transparente = tem_transparencia(im)

        if destino == "moldura":
            if not transparente:
                im = chroma_verde(im)
                if not tem_transparencia(im):
                    erros.append("sem transparência e sem fundo verde puro para remover")
                else:
                    avisos.append("fundo verde removido (gerador não deu alfa)")
            im = im.convert("RGBA")
        else:
            if transparente:
                erros.append("bruto tem transparência: cenário e mapa precisam ser opacos")
            im = im.convert("RGB")
        if iw <= ih:
            erros.append(f"não é paisagem ({iw}×{ih})")

        if modo == "cover":
            cand, caixa = cover(im, W, H)
            extra["recorte"] = caixa
        else:
            desvio_prop = abs((iw / ih) / (W / H) - 1)
            if desvio_prop > TOL_PROPORCAO:
                avisos.append(f"proporção {iw}×{ih} difere {desvio_prop:.0%} da do destino: redimensionar distorce "
                              "(nunca recortar; gere de novo na proporção certa se a distorção aparecer)")
            cand = im.resize((W, H), Image.Resampling.LANCZOS)

        ja_existia = os.path.isfile(final)
        if ja_existia:
            cand = Image.open(final)
            cand = cand.convert("RGBA" if destino == "moldura" else "RGB")
            avisos.append("final já existia: só medido (arte refeita = nome novo)")

        if destino == "moldura":
            m, av = conferir_moldura(cand)
            extra.update(m)
            avisos += av
            lum = desvio = None
        else:
            lum, desvio, bordas = medir(cand)
            extra["bordas"] = bordas
            medidas = []
            if not LUM_MIN <= lum <= LUM_MAX:
                medidas.append(f"luminância {lum} fora de {LUM_MIN}–{LUM_MAX}")
            if destino in ("local", "lados", "wallpaper") and desvio < DESVIO_MIN:
                medidas.append(f"desvio do terço central {desvio} < {DESVIO_MIN} (centro chapado)")
            if destino != "mundi" and not all(8 <= v <= 235 for v in bordas.values()):
                medidas.append("borda suspeita de moldura/vinheta")
            if reprova and not ja_existia and not aceitar:
                erros += medidas
            elif reprova and not ja_existia:
                avisos += [f"aceito com --aceitar: {x}" for x in medidas]
            else:
                avisos += medidas

        prompt = achar_prompt(lote, entrada, nome, stem)
        gravado = ja_existia
        if not ja_existia and not erros:
            if fmt == "jpg":
                cand.save(final, "JPEG", quality=92, optimize=True, progressive=True, subsampling=0)
            else:
                cand.save(final, "PNG", optimize=True)
            gravado = True
            if prompt:
                shutil.copyfile(prompt, final + ".prompt.txt")
            if destino == "portao":
                os.makedirs(conf, exist_ok=True)
                grade_portao(final, os.path.join(conf, f"{stem}_grade.jpg"))

        veredito = "reprovada" if erros else ("aviso" if [a for a in avisos if not a.startswith("final já")] else "ok")
        if erros:
            reprovados += 1
        item = {"id": stem, "destino": destino, "bruto": rel(caminho_bruto, lote),
                "arquivo": rel(final, lote) if gravado else None, "medida": [W, H], "original": [iw, ih],
                "prompt": rel(prompt, lote) if prompt else None, "luminancia": lum, "desvio_central": desvio,
                "veredito": veredito, "erros": erros, "avisos": avisos}
        item.update(extra)
        itens.append(item)
        marca = {"ok": "OK", "aviso": "AVISO", "reprovada": "REPROVADA"}[veredito]
        lum_txt = f"lum {lum} desvio {desvio}" if lum is not None else f"cobertura {extra.get('cobertura')}"
        print(f"{marca:9} {stem}  {iw}×{ih} → {W}×{H}  {lum_txt}")
        for e in erros:
            print(f"          erro: {e}")
        for a in avisos:
            print(f"          aviso: {a}")

    ent = atualizar_entregas(lote, itens, "cenarios-mapas")
    os.makedirs(conf, exist_ok=True)
    pr = prancha(lote, itens, destino, os.path.join(conf, f"prancha_{destino}.jpg"))
    lums = [i["luminancia"] for i in itens if i["luminancia"] is not None]
    print(f"\n{len(itens) - reprovados} de {len(itens)} sem reprovação; "
          f"luminância mínima {min(lums) if lums else '-'}.")
    print(f"registro: {ent}")
    if pr:
        print(f"prancha:  {pr}")
    if reprovados:
        print("Reprovada = gere de novo do zero com o texto ajustado (tabela 'O que costuma voltar errado'),"
              " no máximo 3 imagens; depois, anote como pendente.")
    sys.exit(1 if reprovados else 0)


if __name__ == "__main__":
    main()
