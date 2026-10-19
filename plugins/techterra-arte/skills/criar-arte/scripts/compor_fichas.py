# -*- coding: utf-8 -*-
"""Completa uma parte de fichas escrita pelo assistente (ou por um agente dele) e valida.

    python compor_fichas.py <pasta_do_lote> fichas_claude/parte_A.json

O agente escreve SÓ o conteúdo criativo (campos em CONTRATO-INTERNO.md, seção "Fichas"). Este script copia da
entrada.json os campos fixos (n, slot, cartela, linha, coluna, bloco, tier, tipo1, tipo2, fidelidade), monta o `nome` da variação
(original sem "#N" + epíteto), `variacao_de`, `ingredientes` [{papel, nome}], `evolucao` (N; com `externo` quando o
antecessor é um monstro existente), `arquivo` e `visual` (fórmula por bloco; em N/L homenagem, com os
`tracos_iconicos` logo depois da anatomia; em N/L releitura, com as `ancoras` e a `reinvencao` logo depois da
anatomia), regrava a parte (ordenada por n) e roda
valida_fichas.py --arquivo nela (que exige, na N com antecessor, a anatomia começando com "Evolução do/da <nome>." e
nome diferente do antecessor).
O caminho da parte pode ser relativo à pasta atual ou à pasta do lote.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

USO = "uso: python compor_fichas.py <pasta_do_lote> <arquivo_da_parte>"
FIXOS = ("n", "slot", "cartela", "linha", "coluna", "bloco", "tier", "tipo1", "tipo2")
ORDEM = ["n", "slot", "cartela", "linha", "coluna", "bloco", "tier", "tipo1", "tipo2", "fidelidade", "nome", "epiteto",
         "humanoide", "classe", "tema", "arquetipo", "tracos_iconicos", "ancoras", "reinvencao", "variacao_de", "tipo_sai", "tipo_entra", "mantem",
         "muda", "ingredientes", "herda", "ascensao", "paleta", "anatomia", "rosto", "marcas_poder", "brilho", "temperamento",
         "conceito", "marca_da_habilidade", "descricao", "evolucao", "arquivo", "visual"]
FIM = "vista frontal em três quartos, criatura inteira isolada, sem letras nem símbolos escritos"
HOMENAGEM = "traços icônicos da homenagem (reconhecível à primeira vista por quem conhece a figura clássica): "
ANCORAS = "âncoras da referência (só estas ficam reconhecíveis): "
REINVENCAO = "reinvenção pelos tipos: "


def homenagem(f):
    """Trecho do visual com os traços icônicos (só célula N/L com fidelidade homenagem)."""
    tr = f.get("tracos_iconicos")
    if f.get("fidelidade") != "homenagem" or not tr:
        return None
    if not isinstance(tr, list):   # formato errado: o validador acusa
        tr = [tr]
    return HOMENAGEM + " ".join(f"({k}) {t}" for k, t in enumerate(tr, 1))


def releitura(f):
    """Trechos do visual com as âncoras e a reinvenção (só célula N/L com fidelidade releitura)."""
    if f.get("fidelidade") != "releitura":
        return []
    an, re_ = f.get("ancoras"), str(f.get("reinvencao") or "").strip()
    if an and not isinstance(an, list):   # formato errado: o validador acusa
        an = [an]
    return [(ANCORAS + " ".join(f"({k}) {t}" for k, t in enumerate(an, 1))) if an else None,
            (REINVENCAO + re_) if re_ else None]


def sem_numero(nome):
    return re.sub(r"\s*#\d+\s*$", "", nome or "").strip()


def camera(tier):
    if tier <= 2:
        return "câmera ligeiramente acima, postura curiosa e leve"
    if tier <= 4:
        return "câmera à altura dos olhos, postura jovem e ágil"
    if tier <= 6:
        return "câmera à altura dos olhos, postura adulta e perigosa"
    if tier <= 8:
        return "câmera ligeiramente abaixo, postura imponente e ameaçadora"
    return "câmera baixa em perspectiva heroica, postura colossal de chefe final"


def marcas(f):
    mp = f.get("marcas_poder")
    return ("marcas de poder: " + " ".join(f"({k}) {m}" for k, m in enumerate(mp, 1))) if mp else None


def visual(f, e):
    b = f["bloco"]
    cor = f"corpo {f['paleta'][0]} e acento {f['paleta'][1]}"
    fim = f"{camera(f['tier'])}, {FIM}"
    rosto = f"rosto e olhos: {f['rosto']}"
    so_ele = f"brilho: {f['brilho']}, halo curto aderido, somente esse sistema emite luz"
    mais_forte = f"brilho: {f['brilho']}, halo curto aderido, é a luz mais forte do corpo"
    if b in ("N", "L"):
        partes = [f["anatomia"], homenagem(f), *releitura(f), cor, rosto, marcas(f), so_ele, fim]
    elif b == "V":
        partes = [f"a MESMA criatura do original da prancha, agora do tipo {comum.TIPOS[e['tipo_entra']]}",
                  f"fica igual ao original: {f['mantem']}", f"muda com o tipo novo: {f['muda']}", f["anatomia"], cor, rosto,
                  marcas(f), so_ele, "mesmo porte, mesma idade e mesmo tier do original; não é fusão nem evolução", fim]
    elif b == "F":
        herda = "; ".join(f"de {k}: {v}" for k, v in f["herda"].items())
        partes = [f["anatomia"], cor, rosto, f"o que veio de cada pai: {herda}", f"a ascensão: {f['ascensao']}", marcas(f),
                  mais_forte,
                  "criatura inteiramente nova, claramente um degrau acima de todos os pais; não se parece com nenhum deles sozinho",
                  fim]
    else:   # X / A
        base, sac = (i["nome"] for i in e["ingredientes"])
        partes = [f"a BASE {base} ascendida, reconhecível à primeira vista: {f['herda'][base]}", f["anatomia"], cor, rosto,
                  f"o que veio do SACRIFÍCIO {sac}: {f['herda'][sac]}", f"a ascensão: {f['ascensao']}", marcas(f), mais_forte,
                  "nunca metade-metade nem os dois pais lado a lado; claramente mais forte que os dois pais", fim]
    return "; ".join(str(p) for p in partes if p) + "."


def resolve(lote, caminho):
    if os.path.isfile(caminho):
        return os.path.abspath(caminho)
    alt = os.path.join(lote, caminho)
    if os.path.isfile(alt):
        return alt
    print(f"parte não encontrada: {caminho} (nem relativa à pasta atual nem à do lote)")
    sys.exit(2)


def main():
    lote = comum.pasta_lote(sys.argv, USO)
    pos = [a for a in sys.argv[2:] if not a.startswith("--")]
    if not pos:
        print(USO)
        sys.exit(2)
    caminho = resolve(lote, pos[0])
    try:
        entrada = {e["n"]: e for e in comum.ler_json(os.path.join(lote, "entrada.json"))}
    except FileNotFoundError:
        print("falta entrada.json: rode antes  python montar_entrada.py <pasta_do_lote>")
        sys.exit(2)
    try:
        dado = comum.ler_json(caminho)
    except ValueError as ex:
        print(f"{caminho} não é JSON válido: {ex}")
        sys.exit(2)
    fichas = dado["monstros"] if isinstance(dado, dict) else dado
    if not isinstance(fichas, list):
        print(f"{caminho}: esperava uma lista de fichas")
        sys.exit(2)
    saida, problemas = [], 0
    for f in fichas:
        if not isinstance(f, dict) or f.get("n") not in entrada:
            print(f"ficha sem 'n' válido (fica como está; o validador acusa): {str(f)[:80]}")
            problemas += 1
            if isinstance(f, dict):
                saida.append(f)
            continue
        e = entrada[f["n"]]
        for k in FIXOS:
            f[k] = e[k]
        f["fidelidade"] = e.get("fidelidade", "arquetipo")
        b = e["bloco"]
        if b == "V":
            o = e["original"]
            f["variacao_de"] = o["nome"]
            f["tipo_sai"], f["tipo_entra"] = e["tipo_sai"], e["tipo_entra"]
            f["nome"] = f"{sem_numero(o['nome'])} {str(f.get('epiteto', '')).strip()}".strip()
        if b in ("F", "X", "A"):
            f["ingredientes"] = [{"papel": i["papel"], "nome": i["nome"]} for i in e["ingredientes"]]
        if b == "N":
            f["evolucao"] = e.get("evolucao")
        if b == "L" and e.get("tema") and not f.get("tema"):
            f["tema"] = e["tema"]
        nome = str(f.get("nome") or "").strip()
        f["arquivo"] = comum.arquivo_recorte(e["n"], e["tier"], nome) if nome else ""
        try:
            f["visual"] = visual(f, e)
        except (KeyError, IndexError, TypeError, AttributeError) as ex:
            print(f"#{f['n']}: não deu para montar o visual (campo faltando ou errado: {ex!r})")
            f["visual"] = ""
            problemas += 1
        saida.append({**{k: f[k] for k in ORDEM if k in f}, **{k: v for k, v in f.items() if k not in ORDEM}})
    saida.sort(key=lambda f: f.get("n") if isinstance(f.get("n"), int) else 10 ** 9)
    comum.gravar_json(caminho, saida)
    print(f"{len(saida)} fichas compostas em {caminho}" + (f" ({problemas} com problema)" if problemas else ""), flush=True)
    r = subprocess.run([sys.executable, "-B", os.path.join(comum.SCRIPTS_DIR, "valida_fichas.py"), lote, "--arquivo", caminho])
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
