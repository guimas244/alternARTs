# -*- coding: utf-8 -*-
"""Valida o lote de monstros para entrega e escreve cadastro.json + ENTREGA.md.

    python montar_entrega.py <lote>

Obrigatório (falta = sai 1): monstros.json com fichas; em cada ficha `nome` (único), `tipo1` e `tipo2` (ids de
comum.TIPOS, diferentes), `tier` (1–10), `descricao` não vazia, `arquivo` existente em recortes/ (512x512 RGBA),
`classe` quando `humanoide` é true.

cadastro.json = {"monstros": {nome: {"corpo", "forca"}}}:
- `corpo`/`forca` da ficha, quando existem;
- senão, entrada já existente em cadastro.json SEM "sugestao": true (decisão do dono) é mantida;
- senão, sugestão: corpo por palavras de anatomia/marca_da_habilidade (sem elas: conceito/visual), força "medio",
  com "sugestao": true.

ENTREGA.md: quantas, lista (n, nome, tier, tipos, arquivo, corpo), pendências (cartela sem original, célula sem
recorte, ficha sem descrição, problemas do recorte, avulsas pendentes de conserto registradas em validacao/).
"""
import os
import re
import sys
from datetime import date

sys.dont_write_bytecode = True  # nada é gravado dentro da skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402
from PIL import Image  # noqa: E402

USO = "uso: python montar_entrega.py <pasta do lote>"
CORPOS = ("Bruto", "Muralha", "Lamina", "Artilharia", "Enxame", "Anomalo")
FORCAS = ("fraco", "medio", "forte", "muito_forte")
# palavras (sem acento, minúsculas; casam como prefixo de palavra) que puxam cada corpo
PISTAS = {
    "Muralha": ["casco", "carapaca", "couraca", "muralha", "escudo", "blindad", "armadura", "concha", "fortaleza",
                "parede", "macic", "rocha", "pedra", "tanque", "placas", "bunker", "torre", "pesad", "lento"],
    "Bruto": ["muscul", "robust", "troncud", "punho", "chifre", "investida", "esmag", "marrete", "martelo", "brutamont",
              "ombros", "touro", "pancad", "forca bruta", "corpulent", "atarracad", "mandibula", "pisote"],
    "Lamina": ["lamina", "garra", "agil", "esguio", "veloz", "rapid", "corte", "cortant", "afiad", "presa", "salto",
               "ferrao", "foice", "espada", "navalha", "bote", "dardo", "patas longas", "estocada"],
    "Artilharia": ["dispar", "projet", "raio", "feixe", "canhao", "sopro", "cusp", "distancia", "orbe", "jato",
                   "rajada", "chuva de", "lanca", "arremess", "tiro", "bomba", "explos", "antena"],
    "Enxame": ["enxame", "bando", "colonia", "multipl", "varios", "varias", "filhote", "nuvem", "cardume", "larva",
               "ninhada", "esporo", "copias", "duplic", "dezenas", "centenas"],
    "Anomalo": ["estranh", "distorc", "ilusa", "fantasm", "espectr", "sombra", "psiqu", "flutua", "impossiv", "sonho",
                "pesadelo", "vazio", "avesso", "invertid", "tempo", "runa", "maldic", "tentacul",
                "eco", "reflexo", "translucid", "nevoa"],
}


def palavras_de(texto):
    return " " + re.sub(r"[^a-z0-9]+", " ", comum.norm(texto)) + " "


def sugerir_corpo(f):
    fontes = [f.get("anatomia"), f.get("marca_da_habilidade")]
    if not any(fontes):
        fontes = [f.get("conceito"), f.get("arquetipo"), f.get("classe"), f.get("visual")]
    texto = palavras_de(" ".join(str(x) for x in fontes if x))
    pontos = {c: sum(texto.count(" " + p) for p in ps) for c, ps in PISTAS.items()}
    melhor = max(CORPOS, key=lambda c: (pontos.get(c, 0), -CORPOS.index(c)))
    if pontos.get(melhor, 0) == 0:
        return "Enxame", "sem pista no texto (equilibrado)"
    return melhor, ", ".join(f"{c} {p}" for c, p in sorted(pontos.items(), key=lambda kv: -kv[1]) if p)


def ler_validacao(lote):
    """Avulsas pendentes de conserto e avulsas reprovadas no enquadramento."""
    pend = []
    pasta = os.path.join(lote, "validacao")
    if not os.path.isdir(pasta):
        return pend
    for nome in sorted(os.listdir(pasta)):
        if not nome.endswith(".json") or not (nome.startswith("avulsas") or nome.startswith("cartelas")):
            continue
        dado = comum.ler_json(os.path.join(pasta, nome), [])
        if isinstance(dado, dict):
            dado = dado.get("avulsas") or dado.get("cartelas") or []
        for a in dado if isinstance(dado, list) else []:
            if not isinstance(a, dict):
                continue
            onde = f"cartela {a.get('cartela', '?')}" + (f" L{a['linha']}C{a['coluna']}" if "linha" in a else "")
            textos = " ".join(str(v) for v in a.values() if isinstance(v, str))
            motivo = []
            if a.get("pendente") or "pendente de conserto" in comum.norm(textos):
                motivo.append("pendente de conserto")
            if nome.startswith("avulsas"):
                if a.get("usar_no_recorte") is False:
                    motivo.append("marcada fora do recorte")
                if a.get("arquivo") and not os.path.exists(os.path.join(lote, a["arquivo"])):
                    motivo.append(f"arquivo não existe ({a['arquivo']})")
            if motivo:
                pend.append(f"{onde} {a.get('nome', '')} [{nome}]: {'; '.join(motivo)}".replace("  ", " "))
    enq = os.path.join(pasta, "enquadramento")
    if os.path.isdir(enq):
        for nome in sorted(os.listdir(enq)):
            if nome.startswith("avulsa_") and nome.endswith(".json"):
                r = comum.ler_json(os.path.join(enq, nome), {})
                if r.get("veredito") == "REPROVADA":
                    pend.append(f"avulsa {r.get('arquivo', nome)} REPROVADA no enquadramento: "
                                + "; ".join(r.get("reprovas", [])))
    return pend


def main(argv):
    lote = comum.pasta_lote(argv, USO)
    caminho = os.path.join(lote, "monstros.json")
    if not os.path.exists(caminho):
        print("falta monstros.json no lote")
        sys.exit(1)
    dado = comum.ler_json(caminho)
    fichas = dado.get("monstros", []) if isinstance(dado, dict) else dado
    nome_lote = (dado.get("lote") if isinstance(dado, dict) else None) or os.path.basename(lote)
    fichas = sorted(fichas, key=lambda m: (m.get("n") or 0, m.get("cartela") or 0, m.get("linha") or 0,
                                           m.get("coluna") or 0))
    erros, avisos, pend = [], [], []
    if not fichas:
        erros.append("monstros.json sem fichas")
    vistos_nome, vistos_arq = {}, {}
    for f in fichas:
        quem = f"n{f.get('n', '?')} {f.get('nome') or '(sem nome)'}"
        nome = (f.get("nome") or "").strip()
        if not nome:
            erros.append(f"{quem}: sem nome")
        elif comum.norm(nome) in vistos_nome:
            erros.append(f"{quem}: nome repetido no lote")
        vistos_nome[comum.norm(nome)] = 1
        for k in ("tipo1", "tipo2"):
            if f.get(k) not in comum.TIPOS:
                erros.append(f"{quem}: {k} inválido ({f.get(k)!r})")
        if f.get("tipo1") and f.get("tipo1") == f.get("tipo2"):
            erros.append(f"{quem}: tipo1 e tipo2 iguais (monstro tem sempre 2 tipos)")
        if not isinstance(f.get("tier"), int) or not 1 <= f["tier"] <= 10:
            erros.append(f"{quem}: tier inválido ({f.get('tier')!r})")
        if not (f.get("descricao") or "").strip():
            erros.append(f"{quem}: ficha sem descrição")
            pend.append(f"{quem}: ficha sem descrição")
        if "humanoide" not in f:
            avisos.append(f"{quem}: sem campo humanoide (lido como false)")
        elif f.get("humanoide") is True and not (f.get("classe") or "").strip():
            erros.append(f"{quem}: humanoide sem classe")
        arq = f.get("arquivo")
        if not arq:
            erros.append(f"{quem}: sem arquivo")
            continue
        if arq in vistos_arq:
            erros.append(f"{quem}: arquivo repetido ({arq})")
        vistos_arq[arq] = 1
        if f.get("n") and f.get("tier") and nome:
            esperado = comum.arquivo_recorte(int(f["n"]), int(f["tier"]), nome)
            if arq != esperado:
                avisos.append(f"{quem}: arquivo {arq} fora do padrão (esperado {esperado})")
        p = os.path.join(lote, "recortes", arq)
        if not os.path.exists(p):
            erros.append(f"{quem}: sem recorte (recortes/{arq})")
            pend.append(f"célula sem recorte: cartela {f.get('cartela')} L{f.get('linha')}C{f.get('coluna')} {nome}")
            continue
        with Image.open(p) as im:
            if im.size != (comum.RECORTE, comum.RECORTE) or im.mode != "RGBA":
                erros.append(f"{quem}: recorte {im.size[0]}x{im.size[1]} {im.mode} (esperado 512x512 RGBA)")
    for n in sorted({int(f["cartela"]) for f in fichas if f.get("cartela")}):
        if not any(os.path.exists(os.path.join(lote, "cartelas", x))
                   for x in (f"cartela_{n:03d}_original.png", f"cartela_{n:02d}_original.png")):
            pend.append(f"cartela {n:03d} sem cartelas/cartela_{n:03d}_original.png")
    pend += ler_validacao(lote)
    reg = comum.ler_json(os.path.join(lote, "validacao", "recorte.json"), {})
    olho = [f"{v.get('cartela', 0):03d} L{v.get('linha')}C{v.get('coluna')} {v.get('nome')} [{v.get('origem')}]: "
            + "; ".join(v["problemas"]) for v in reg.get("celulas", {}).values() if v.get("problemas")]
    if not reg:
        avisos.append("validacao/recorte.json não existe: rode recortar_cartela.py antes")
    origem = {k: v.get("origem") for k, v in reg.get("celulas", {}).items()}

    # cadastro.json
    cad_path = os.path.join(lote, "cadastro.json")
    antigo = comum.ler_json(cad_path, {}).get("monstros", {}) if os.path.exists(cad_path) else {}
    cad, n_sug = {}, 0
    for f in fichas:
        nome = (f.get("nome") or "").strip()
        if not nome:
            continue
        corpo, forca, sug, porque = f.get("corpo"), f.get("forca"), False, "ficha"
        velho = antigo.get(nome, {})
        if not corpo and velho.get("corpo") and not velho.get("sugestao"):
            corpo, porque = velho["corpo"], "cadastro.json (decisão)"
            forca = forca or velho.get("forca")
        if corpo and corpo not in CORPOS:
            erros.append(f"{nome}: corpo inválido ({corpo!r}; use {', '.join(CORPOS)})")
        if forca and forca not in FORCAS:
            erros.append(f"{nome}: forca inválida ({forca!r}; use {', '.join(FORCAS)})")
        if not corpo:
            corpo, porque = sugerir_corpo(f)
            sug = True
        if not forca:
            forca, sug = "medio", True
        item = {"corpo": corpo, "forca": forca}
        if sug:
            item["sugestao"] = True
            item["pista"] = porque
            n_sug += 1
        cad[nome] = item
    comum.gravar_json(cad_path, {"_leia": "corpo/forca por monstro. 'sugestao': true = escolhido por heurística, o dono "
                                          "confirma (força é balanceamento). Tire 'sugestao' ao decidir.",
                                 "monstros": cad})

    # ENTREGA.md
    pronto = not erros
    L = [f"# Entrega — {nome_lote}", "",
         f"Gerado por montar_entrega.py em {date.today().isoformat()}. Situação: **{'PRONTO' if pronto else 'NÃO PRONTO'}**.",
         "", f"- Monstros: **{len(fichas)}** (recortes 512x512 RGBA em `recortes/`; conferência em "
         "`recortes/_visao_geral.png`)",
         f"- Corpo/força: `cadastro.json` ({n_sug} sugestão(ões) por heurística — o dono confirma)", "",
         "| n | nome | tier | tipos | arquivo | corpo / força |", "|---|---|---|---|---|---|"]
    for f in fichas:
        nome = f.get("nome") or "?"
        t1, t2 = comum.TIPOS.get(f.get("tipo1"), f.get("tipo1")), comum.TIPOS.get(f.get("tipo2"), f.get("tipo2"))
        c = cad.get(nome, {})
        marca = " *(avulsa)*" if origem.get(f.get("arquivo")) == "avulsa" else ""
        L.append(f"| {f.get('n', '')} | {nome} | {f.get('tier', '')} | {t1} / {t2} | `{f.get('arquivo', '')}`{marca} | "
                 f"{c.get('corpo', '')} / {c.get('forca', '')}{' (sugestão)' if c.get('sugestao') else ''} |")
    L += ["", "## Pendências", ""]
    L += [f"- {x}" for x in pend] or ["- nenhuma"]
    L += ["", "## Precisa de olho humano (relatório do recorte)", ""]
    L += [f"- {x}" for x in olho] or ["- nada relatado pelo recortador"]
    if erros:
        L += ["", "## Falta (obrigatório)", ""] + [f"- {x}" for x in erros]
    if avisos:
        L += ["", "## Avisos", ""] + [f"- {x}" for x in avisos]
    L += ["", "Conferir antes de cadastrar: 1 criatura inteira por arquivo, fundo transparente, sem pedaço do vizinho; "
          "corpo/força sugeridos.", ""]
    comum.gravar_texto(os.path.join(lote, "ENTREGA.md"), "\n".join(L))

    print(("PRONTO" if pronto else "NÃO PRONTO") + f": {len(fichas)} monstros | {n_sug} corpo/força sugeridos | "
          f"{len(pend)} pendência(s) | {len(olho)} célula(s) para olho humano")
    for x in erros:
        print("  FALTA:", x)
    for x in pend:
        print("  pendência:", x)
    for x in avisos:
        print("  aviso:", x)
    print("  escrito: cadastro.json, ENTREGA.md")
    sys.exit(0 if pronto else 1)


if __name__ == "__main__":
    main(sys.argv)
