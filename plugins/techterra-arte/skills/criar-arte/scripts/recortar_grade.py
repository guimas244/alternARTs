# -*- coding: utf-8 -*-
"""Recortador ÚNICO de grade da skill criar-arte (porta o "techterra-isolamento-v2.1").

    python recortar_grade.py <lote|imagem> [--grade 5x5|4x4|RxC] [--lado 320] [--margem 16]
           [--mascara-circular] [--saida pasta] [--nomes arquivo.json] [--pagina N] [--simular] [--substituir]

- <lote>: pasta com itens.json + cartelas/pagina_NN_original.png. Cada página vira um recorte por item, gravado no
  `arquivo` do item (ex.: marinho/faixa_01_arpao_de_osso.png), mais cartelas/pagina_NN_grade.png e
  validacao/recorte_pagina_NN.json.
- <imagem>: uma cartela solta. Nomes pela ordem de leitura vindos de --nomes (lista JSON; null pula a célula) ou
  <stem>_L<r>C<c>.png. Saída padrão: <pasta da imagem>/recortes_<stem>/. Avulsa de item = --grade 1x1 + --nomes.

Algoritmo (igual ao v2.1): acha os objetos por manchas conectadas (alfa > 32, vizinhança 8, mancha < 32 px ignorada),
dá cada mancha à célula do seu centro de massa (várias manchas na mesma célula = um objeto), trava o núcleo e estende
a posse 8 px sobre as bordas suaves; enquadra com 8 px de contexto, apaga só o que é do vizinho e centraliza num
quadrado RGBA de --lado px SEM redimensionar. Margem de referência --margem (16), mínimo 8. Os pixels mantidos não
mudam e a cartela original nunca é alterada.

Diferenças do v2.1 (só onde ele abortaria): célula vazia, cortada na borda ou grande demais vira ERRO daquela célula
(as boas são gravadas); duas manchas grandes separadas na mesma célula viram ATENÇÃO; se a janela com contexto não
cabe, tenta a janela justa (bbox do alfa) antes de reprovar. --reduzir: objeto que ainda não cabe é reduzido com
LANCZOS, mesma proporção, até caber com a margem mínima (itens NÃO reduzem por padrão, como o v2.1).
--mascara-circular (ícone de mapa, 300 px): apaga o que fica fora do círculo do medalhão com borda suave (máscara
desenhada em 4x e reduzida), usa a janela justa e liga --reduzir.
Saída 0 = tudo OK/ATENÇÃO; 1 = alguma célula ou página reprovada (ou conflito de arquivo); 2 = uso.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
from collections import deque

sys.dont_write_bytecode = True  # nada de __pycache__ dentro da skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    raise SystemExit("Pillow não encontrado. Instale com: python -m pip install pillow")

ALGORITMO = "criar-arte-grade-1 (porta techterra-isolamento-v2.1)"
LOCALIZA_ALFA = 32
MIN_PIXELS = 32
CONTEXTO = 8
MARGEM_MIN = 8
BORDA_CORTE = 2           # mancha a menos disso da borda da imagem = cortada
DUPLA_FRACAO = 0.25       # 2ª mancha >= 25% da maior (e >= DUPLA_MIN px) = possível objeto duplo
DUPLA_MIN = 400
SUPERAMOSTRA = 4          # máscara circular desenhada em 4x e reduzida (anti-alias)


# ------------------------------------------------------------------ núcleo (sem disco)

def segmentar(imagem, linhas, colunas):
    """Mancha conectada -> célula (1..R*C, ordem de leitura) pelo centro de massa; depois estende a posse."""
    largura, altura = imagem.size
    alfa = imagem.getchannel("A").tobytes()
    visto = bytearray(len(alfa))
    dono = bytearray(len(alfa))
    caixas, nucleo_qtd, manchas = {}, {}, {}
    fragmentos = 0
    for inicio, valor in enumerate(alfa):
        if valor <= LOCALIZA_ALFA or visto[inicio]:
            continue
        visto[inicio] = 1
        fila = deque([inicio])
        pixels = []
        sx = sy = 0
        x0, y0, x1, y1 = largura, altura, -1, -1
        while fila:
            i = fila.popleft()
            x, y = i % largura, i // largura
            pixels.append(i)
            sx += x
            sy += y
            if x < x0:
                x0 = x
            if x > x1:
                x1 = x
            if y < y0:
                y0 = y
            if y > y1:
                y1 = y
            for ny in range(max(0, y - 1), min(altura, y + 2)):
                base = ny * largura
                for nx in range(max(0, x - 1), min(largura, x + 2)):
                    n = base + nx
                    if not visto[n] and alfa[n] > LOCALIZA_ALFA:
                        visto[n] = 1
                        fila.append(n)
        if len(pixels) < MIN_PIXELS:
            fragmentos += 1
            continue
        col = min(colunas - 1, int((sx / len(pixels)) / (largura / colunas)))
        lin = min(linhas - 1, int((sy / len(pixels)) / (altura / linhas)))
        cel = lin * colunas + col + 1
        caixa = (x0, y0, x1 + 1, y1 + 1)
        if cel in caixas:
            v = caixas[cel]
            caixas[cel] = (min(v[0], caixa[0]), min(v[1], caixa[1]), max(v[2], caixa[2]), max(v[3], caixa[3]))
        else:
            caixas[cel] = caixa
        nucleo_qtd[cel] = nucleo_qtd.get(cel, 0) + len(pixels)
        manchas.setdefault(cel, []).append({"pixels": len(pixels), "caixa": list(caixa)})
        for i in pixels:
            dono[i] = cel
    nucleo = bytes(dono)
    fila = deque(i for i, d in enumerate(dono) if d)
    for _ in range(CONTEXTO):
        for _ in range(len(fila)):
            i = fila.popleft()
            d = dono[i]
            x, y = i % largura, i // largura
            for ny in range(max(0, y - 1), min(altura, y + 2)):
                base = ny * largura
                for nx in range(max(0, x - 1), min(largura, x + 2)):
                    n = base + nx
                    if not dono[n]:
                        dono[n] = d
                        fila.append(n)
        if not fila:
            break
    for lista in manchas.values():
        lista.sort(key=lambda m: -m["pixels"])
    return dono, nucleo, caixas, nucleo_qtd, manchas, fragmentos


def _enquadrar(imagem, dono, nucleo, cel, caixa, nucleo_total, lado, margem, mascara, reduzir=False):
    """Uma célula -> (recorte lado×lado ou None, registro)."""
    largura, altura = imagem.size
    reg = {"problemas": [], "atencao": []}
    janela = (caixa[0] - CONTEXTO, caixa[1] - CONTEXTO, caixa[2] + CONTEXTO, caixa[3] + CONTEXTO)
    quadro = imagem.crop(janela)
    original = quadro.tobytes()
    isolado = bytearray(original)
    vizinho_px = vizinho_nucleo_px = nucleo_mantido = 0
    vizinhos = set()
    for fy in range(quadro.height):
        sy = janela[1] + fy
        if not 0 <= sy < altura:
            continue
        for fx in range(quadro.width):
            sx = janela[0] + fx
            if not 0 <= sx < largura:
                continue
            i = sy * largura + sx
            p = (fy * quadro.width + fx) * 4
            if nucleo[i] == cel:
                nucleo_mantido += 1
            if dono[i] and dono[i] != cel and original[p + 3]:
                vizinhos.add(dono[i])
                vizinho_px += 1
                vizinho_nucleo_px += int(bool(nucleo[i]))
                isolado[p:p + 4] = b"\0\0\0\0"
    if nucleo_mantido != nucleo_total:  # garantia do v2.1: o núcleo inteiro está na janela
        raise ValueError(f"célula {cel}: o enquadramento deixou parte do objeto de fora")
    reg.update(pixels_vizinho_removidos=vizinho_px, pixels_nucleo_vizinho_removidos=vizinho_nucleo_px,
               vizinhos_excluidos=sorted(vizinhos), pixels_nucleo=nucleo_mantido)
    fora_circulo = nucleo_cortado = 0
    if mascara:
        # círculo do medalhão = centro e maior lado da caixa do núcleo; máscara desenhada em 4x e reduzida (borda
        # suave). Alfa novo = min(alfa, máscara): dentro do círculo nada muda; fora some; na borda, anti-alias.
        cx = (caixa[0] + caixa[2]) / 2 - janela[0]
        cy = (caixa[1] + caixa[3]) / 2 - janela[1]
        raio = max(caixa[2] - caixa[0], caixa[3] - caixa[1]) / 2
        s = SUPERAMOSTRA
        grande = Image.new("L", (quadro.width * s, quadro.height * s), 0)
        ImageDraw.Draw(grande).ellipse(((cx - raio) * s, (cy - raio) * s, (cx + raio) * s - 1, (cy + raio) * s - 1),
                                       fill=255)
        mapa = grande.reduce(s).tobytes()  # média de caixa: borda suave sem o halo que o LANCZOS deixaria fora
        for k, m in enumerate(mapa):
            p = k * 4
            a = isolado[p + 3]
            if a and m < 255:
                if m == 0:
                    fora_circulo += 1
                if m < 128:
                    fy, fx = divmod(k, quadro.width)
                    sy, sx = janela[1] + fy, janela[0] + fx
                    if 0 <= sy < altura and 0 <= sx < largura and nucleo[sy * largura + sx] == cel:
                        nucleo_cortado += 1
                if m == 0:
                    isolado[p:p + 4] = b"\0\0\0\0"
                elif m < a:
                    isolado[p + 3] = m
        reg.update(pixels_fora_do_circulo=fora_circulo, pixels_nucleo_fora_do_circulo=nucleo_cortado)
        if nucleo_cortado > 0.02 * nucleo_total:
            reg["atencao"].append(f"máscara circular cortou {nucleo_cortado} px do objeto (não parece redondo)")
    quadro = Image.frombytes("RGBA", quadro.size, bytes(isolado))
    limite = lado - 2 * MARGEM_MIN
    tipo_janela = "contexto"
    if mascara or quadro.width > limite or quadro.height > limite:
        bb = quadro.getchannel("A").getbbox()
        if bb is None:
            reg["problemas"].append("vazia depois de isolar")
            return None, reg
        janela = (janela[0] + bb[0], janela[1] + bb[1], janela[0] + bb[2], janela[1] + bb[3])
        quadro = quadro.crop(bb)
        tipo_janela = "justa"
    reg.update(janela=tipo_janela, janela_origem=list(janela), pixels_enquadrados=list(quadro.size))
    if reduzir and (quadro.width > limite or quadro.height > limite):
        fator = limite / max(quadro.width, quadro.height)
        novo = (max(1, min(limite, round(quadro.width * fator))), max(1, min(limite, round(quadro.height * fator))))
        quadro = quadro.resize(novo, Image.LANCZOS)  # RGBA: o Pillow reduz com alfa pré-multiplicado
        reg.update(reduzido=round(fator, 4), pixels_reduzidos=list(novo))
    if quadro.width > limite or quadro.height > limite:
        reg["problemas"].append(f"objeto grande demais: {quadro.width}x{quadro.height}; não cabe em {lado}x{lado} "
                                f"com margem mínima de {MARGEM_MIN}px (refazer a célula menor)")
        return None, reg
    desloc = ((lado - quadro.width) // 2, (lado - quadro.height) // 2)
    recorte = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    recorte.paste(quadro, desloc)  # sem máscara alfa: copia o RGBA exato
    if recorte.crop((desloc[0], desloc[1], desloc[0] + quadro.width, desloc[1] + quadro.height)).tobytes() \
            != quadro.tobytes():
        raise ValueError(f"célula {cel}: falha na preservação dos pixels ao centralizar")
    bb = recorte.getchannel("A").getbbox()
    margens = [bb[0], bb[1], lado - bb[2], lado - bb[3]] if bb else [lado // 2] * 4
    if min(margens) < MARGEM_MIN:
        reg["problemas"].append(f"margem {min(margens)}px menor que {MARGEM_MIN}px")
        return None, reg
    reg.update(deslocamento=list(desloc), margens=margens, margem_abaixo_da_referencia=min(margens) < margem)
    return recorte, reg


def recortar(imagem, linhas, colunas, nomes, lado=320, margem=16, mascara=False, reduzir=None):
    """Recorta uma cartela já aberta. nomes = lista R*C (ordem de leitura; None pula a célula).

    reduzir: None = igual à máscara (ícone reduz, item não, como o v2.1). Devolve (grade RGBA ou None,
    {nome: recorte}, relatório). Nunca levanta por célula ruim: relata.
    """
    if reduzir is None:
        reduzir = bool(mascara)
    total = linhas * colunas
    if len(nomes) != total:
        raise ValueError(f"esperava {total} nomes, vieram {len(nomes)}")
    rel = {"algoritmo": ALGORITMO, "grade": f"{linhas}x{colunas}", "lado": lado, "margem_referencia": margem,
           "margem_minima": MARGEM_MIN, "contexto": CONTEXTO, "mascara_circular": bool(mascara),
           "reduzir": bool(reduzir),
           "pixels_origem": list(imagem.size), "redimensionado": False, "problemas_pagina": [], "celulas": []}
    if total > 255:
        raise ValueError("grade grande demais (máximo 255 células)")
    if imagem.mode != "RGBA":
        rel["problemas_pagina"].append(f"imagem sem alfa (modo {imagem.mode}): fundo opaco")
    elif imagem.getchannel("A").getextrema()[0] != 0:
        rel["problemas_pagina"].append("fundo não é transparente (nenhum pixel com alfa 0): xadrez pintado ou fundo opaco")
    if rel["problemas_pagina"]:
        rel["estado"] = "REPROVADA"
        return None, {}, rel
    largura, altura = imagem.size
    dono, nucleo, caixas, nucleo_qtd, manchas, fragmentos = segmentar(imagem, linhas, colunas)
    rel["fragmentos_ignorados"] = fragmentos
    extras = sorted(c for c in caixas if nomes[c - 1] is None)
    if extras:
        rel["celulas_sem_nome_com_objeto"] = extras
    recortes = {}
    grade = Image.new("RGBA", (lado * colunas, lado * linhas), (0, 0, 0, 0)) if total > 1 else None
    for cel in range(1, total + 1):
        nome = nomes[cel - 1]
        if nome is None:
            continue
        lin, col = (cel - 1) // colunas + 1, (cel - 1) % colunas + 1
        base = {"celula": cel, "linha": lin, "coluna": col, "arquivo": nome}
        if cel not in caixas:
            rel["celulas"].append({**base, "estado": "erro", "problemas": ["vazia: nenhum objeto nesta célula"],
                                   "atencao": []})
            continue
        caixa = caixas[cel]
        lista = manchas[cel]
        base["manchas"] = len(lista)
        if min(caixa[0], caixa[1], largura - caixa[2], altura - caixa[3]) < BORDA_CORTE:
            rel["celulas"].append({**base, "estado": "erro", "atencao": [],
                                   "problemas": ["cortada: o objeto encosta na borda da imagem"]})
            continue
        recorte, reg = _enquadrar(imagem, dono, nucleo, cel, caixa, nucleo_qtd[cel], lado, margem, mascara, reduzir)
        if len(lista) >= 2 and lista[1]["pixels"] >= max(DUPLA_MIN, DUPLA_FRACAO * lista[0]["pixels"]):
            reg["atencao"].append(f"{len(lista)} manchas separadas na célula (par solto, objeto duplo ou pedaço "
                                  f"de vizinho?): conferir no olho")
        reg = {**base, **reg}
        reg["estado"] = "erro" if reg["problemas"] else ("atencao" if reg["atencao"] else "ok")
        rel["celulas"].append(reg)
        if recorte is not None:
            recortes[nome] = recorte
            if grade is not None:
                grade.paste(recorte, ((col - 1) * lado, (lin - 1) * lado))
    estados = [c["estado"] for c in rel["celulas"]]
    rel["estado"] = "REPROVADA" if "erro" in estados else ("ATENCAO" if "atencao" in estados or extras else "OK")
    rel["recortes"] = len(recortes)
    rel["redimensionado"] = any("reduzido" in c for c in rel["celulas"])
    rel["celulas_reduzidas"] = [c["celula"] for c in rel["celulas"] if "reduzido" in c]
    rel["celulas_com_erro"] = [c["celula"] for c in rel["celulas"] if c["estado"] == "erro"]
    rel["celulas_com_atencao"] = [c["celula"] for c in rel["celulas"] if c["estado"] == "atencao"]
    rel["abaixo_da_margem_referencia"] = [c["celula"] for c in rel["celulas"] if c.get("margem_abaixo_da_referencia")]
    ok = [c for c in rel["celulas"] if "margens" in c and c["estado"] != "erro"]
    rel["margem_minima_real"] = min((min(c["margens"]) for c in ok), default=None)
    rel["pixels_vizinho_removidos"] = sum(c.get("pixels_vizinho_removidos", 0) for c in rel["celulas"])
    return grade, recortes, rel


def recortar_arquivo(caminho, linhas, colunas, nomes, **kw):
    with Image.open(caminho) as im:
        im.load()
        return recortar(im, linhas, colunas, nomes, **kw)


# ------------------------------------------------------------------ disco

def _sha(caminho):
    with open(caminho, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _mesmos_pixels(caminho, imagem):
    try:
        with Image.open(caminho) as ex:
            return ex.mode == imagem.mode and ex.size == imagem.size and ex.tobytes() == imagem.tobytes()
    except (OSError, ValueError):
        return False


def _dentro_da_skill(caminho):
    a, b = os.path.normcase(os.path.realpath(caminho)), os.path.normcase(os.path.realpath(comum.SKILL_DIR))
    return a == b or a.startswith(b + os.sep)


def publicar(base, saidas, rel_caminho, relatorio, substituir=False):
    """Grava {caminho relativo a base: Image}. Arquivo existente com pixels diferentes que não saiu deste
    recortador (hash do relatório anterior) = conflito: nada da página é gravado. Devolve (gravados, conflitos)."""
    if _dentro_da_skill(base):
        raise ValueError("saída dentro da pasta da skill: proibido (use a pasta de trabalho)")
    anterior = comum.ler_json(rel_caminho, {}) if os.path.exists(rel_caminho) else {}
    gerenciados = anterior.get("saidas", {}) if isinstance(anterior, dict) else {}
    mudar, conflitos = {}, []
    for nome, im in saidas.items():
        destino = os.path.join(base, nome)
        if os.path.exists(destino):
            if _mesmos_pixels(destino, im):
                continue
            if not substituir and gerenciados.get(nome) != _sha(destino):
                conflitos.append(nome)
                continue
        mudar[nome] = im
    if conflitos:
        return 0, conflitos
    for nome, im in mudar.items():
        destino = os.path.join(base, nome)
        os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
        tmp = destino + ".tmp.png"
        im.save(tmp)
        if not _mesmos_pixels(tmp, im):
            os.remove(tmp)
            raise ValueError(f"erro ao salvar {nome}")
        os.replace(tmp, destino)
    relatorio["saidas"] = {n: _sha(os.path.join(base, n)) for n in saidas}
    comum.gravar_json(rel_caminho, relatorio)
    return len(mudar), []


def _grade(texto):
    m = re.fullmatch(r"(\d+)[xX](\d+)", texto or "")
    if not m or int(m.group(1)) < 1 or int(m.group(2)) < 1:
        raise argparse.ArgumentTypeError("use RxC, por exemplo 5x5 ou 4x4")
    return int(m.group(1)), int(m.group(2))


def nomes_da_pagina(itens, pagina, linhas, colunas):
    """Lista R*C com o `arquivo` de cada item da página (None nas células sem item)."""
    try:
        from itens_montar_prompts import arquivo_item
    except ImportError:  # pragma: no cover
        arquivo_item = None
    nomes = [None] * (linhas * colunas)
    for it in itens:
        if int(it.get("pagina", 0)) != pagina:
            continue
        lin, col = int(it["linha"]), int(it["coluna"])
        if not (1 <= lin <= linhas and 1 <= col <= colunas):
            raise ValueError(f"página {pagina}: item {it.get('nome')!r} fora da grade {linhas}x{colunas}")
        i = (lin - 1) * colunas + col - 1
        if nomes[i] is not None:
            raise ValueError(f"página {pagina}: duas entradas na linha {lin}, coluna {col}")
        arq = it.get("arquivo") or (arquivo_item(it) if arquivo_item else None)
        if not arq:
            raise ValueError(f"página {pagina}: item {it.get('nome')!r} sem arquivo")
        nomes[i] = arq.replace("\\", "/")
    usados = [n for n in nomes if n]
    if len(set(usados)) != len(usados):
        raise ValueError(f"página {pagina}: nome de arquivo repetido")
    return nomes


def _imprimir(rotulo, rel):
    print(f"[{rel['estado']}] {rotulo}: {rel.get('recortes', 0)} recortes"
          + (f", margem mínima {rel['margem_minima_real']} px" if rel.get("margem_minima_real") is not None else ""))
    for p in rel["problemas_pagina"]:
        print(f"   ERRO página: {p}")
    for c in rel["celulas"]:
        for p in c.get("problemas", []):
            print(f"   ERRO L{c['linha']}C{c['coluna']} ({c['arquivo']}): {p}")
        for a in c.get("atencao", []):
            print(f"   ATENÇÃO L{c['linha']}C{c['coluna']} ({c['arquivo']}): {a}")
    if rel.get("celulas_sem_nome_com_objeto"):
        print(f"   ATENÇÃO: objeto em célula sem item: {rel['celulas_sem_nome_com_objeto']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Recorta cartelas em grade (itens 5x5, ícones 4x4, avulsa 1x1).")
    ap.add_argument("alvo", help="pasta do lote (itens.json + cartelas/) ou uma imagem PNG")
    ap.add_argument("--grade", type=_grade, default=(5, 5), help="RxC (padrão 5x5)")
    ap.add_argument("--lado", type=int, default=None, help="lado do recorte (padrão: itens.json 'lado' ou 320)")
    ap.add_argument("--margem", type=int, default=16, help="margem de referência (mínimo fixo de 8)")
    ap.add_argument("--mascara-circular", action="store_true",
                    help="ícone de mapa: apaga fora do círculo (borda suave) e liga --reduzir")
    ap.add_argument("--reduzir", action="store_true",
                    help="objeto que não cabe é reduzido (LANCZOS, mesma proporção) até caber com a margem mínima")
    ap.add_argument("--saida", help="pasta base de saída (lote: padrão o próprio lote)")
    ap.add_argument("--nomes", help="modo imagem: JSON com a lista de nomes em ordem de leitura")
    ap.add_argument("--pagina", type=int, help="modo lote: só esta página")
    ap.add_argument("--simular", action="store_true", help="só confere, não grava nada")
    ap.add_argument("--substituir", action="store_true", help="permite trocar recortes existentes diferentes")
    a = ap.parse_args(argv)
    linhas, colunas = a.grade
    alvo = os.path.abspath(a.alvo)
    erros = 0
    if os.path.isdir(alvo):
        dados = comum.ler_json(os.path.join(alvo, "itens.json"))
        itens = dados.get("itens", []) if isinstance(dados, dict) else dados
        lado = a.lado or (dados.get("lado") if isinstance(dados, dict) else None) or 320
        base = os.path.abspath(a.saida) if a.saida else alvo
        fontes = sorted(glob.glob(os.path.join(alvo, "cartelas", "pagina_[0-9][0-9]_original.png")))
        paginas = sorted({int(i.get("pagina", 0)) for i in itens})
        if a.pagina:
            paginas = [p for p in paginas if p == a.pagina]
        if not paginas:
            print("nenhuma página no itens.json")
            return 2
        for pg in paginas:
            fonte = os.path.join(alvo, "cartelas", f"pagina_{pg:02d}_original.png")
            if fonte not in fontes:
                print(f"[--] página {pg:02d}: cartela ainda não gerada (cartelas/pagina_{pg:02d}_original.png)")
                continue
            try:
                nomes = nomes_da_pagina(itens, pg, linhas, colunas)
                grade, recortes, rel = recortar_arquivo(fonte, linhas, colunas, nomes, lado=lado, margem=a.margem,
                                                        mascara=a.mascara_circular,
                                                        reduzir=a.reduzir or a.mascara_circular)
            except (OSError, ValueError, KeyError, TypeError) as e:
                erros += 1
                print(f"[ERRO] página {pg:02d}: {e}")
                continue
            rel.update(pagina=pg, origem=os.path.relpath(fonte, alvo).replace("\\", "/"), origem_sha256=_sha(fonte),
                       revisao_visual="do dono (o script não aprova arte)")
            _imprimir(f"página {pg:02d}", rel)
            erros += rel["estado"] == "REPROVADA"
            if a.simular:
                continue
            saidas = dict(recortes)
            if grade is not None:
                saidas[os.path.relpath(os.path.join(alvo, "cartelas", f"pagina_{pg:02d}_grade.png"), base)
                       .replace("\\", "/")] = grade
            gravados, conflitos = publicar(base, saidas, os.path.join(alvo, "validacao", f"recorte_pagina_{pg:02d}.json"),
                                           rel, a.substituir)
            if conflitos:
                erros += 1
                print(f"   CONFLITO: arquivo existente diferente, não saiu deste recortador: {', '.join(conflitos)}."
                      f" Nada desta página foi gravado. Use --substituir para trocar de propósito.")
            else:
                print(f"   {gravados} arquivo(s) novo(s)/atualizado(s)")
        return 1 if erros else 0
    if not os.path.isfile(alvo):
        print(f"não existe: {alvo}")
        return 2
    stem = os.path.splitext(os.path.basename(alvo))[0]
    total = linhas * colunas
    if a.nomes:
        nomes = comum.ler_json(a.nomes)
        if isinstance(nomes, dict):
            nomes = nomes.get("arquivos", [])
        nomes = [n or None for n in nomes]
    else:
        nomes = [f"{stem}_L{r}C{c}.png" for r in range(1, linhas + 1) for c in range(1, colunas + 1)]
    if len(nomes) != total:
        print(f"--nomes tem {len(nomes)} nomes; a grade {linhas}x{colunas} pede {total}")
        return 2
    base = os.path.abspath(a.saida) if a.saida else os.path.join(os.path.dirname(alvo), f"recortes_{stem}")
    grade, recortes, rel = recortar_arquivo(alvo, linhas, colunas, nomes, lado=a.lado or 320, margem=a.margem,
                                            mascara=a.mascara_circular, reduzir=a.reduzir or a.mascara_circular)
    rel.update(origem=os.path.basename(alvo), origem_sha256=_sha(alvo))
    _imprimir(os.path.basename(alvo), rel)
    erros += rel["estado"] == "REPROVADA"
    if not a.simular and (recortes or grade is not None):
        saidas = dict(recortes)
        if grade is not None:
            saidas[f"{stem}_grade.png"] = grade
        try:
            gravados, conflitos = publicar(base, saidas, os.path.join(base, f"recorte_{stem}.json"), rel, a.substituir)
        except ValueError as e:
            print(f"   ERRO: {e}")
            return 1
        if conflitos:
            erros += 1
            print(f"   CONFLITO: {', '.join(conflitos)}. Nada gravado. Use --substituir para trocar de propósito.")
        else:
            print(f"   {gravados} arquivo(s) em {base}")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
