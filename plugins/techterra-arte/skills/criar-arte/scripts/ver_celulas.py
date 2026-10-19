# -*- coding: utf-8 -*-
"""Mostra as células de algumas cartelas, de forma compacta, para o agente de fichas.

    python ver_celulas.py <pasta_do_lote> 1,2
    python ver_celulas.py <pasta_do_lote> 3-5
    python ver_celulas.py <pasta_do_lote> todas

Lê <lote>/entrada.json (gerada por montar_entrada.py). Não grava nada.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum  # noqa: E402

USO = "uso: python ver_celulas.py <pasta_do_lote> <cartelas>   (ex.: 1,2  ou  3-5  ou  todas)"
NOME_BLOCO = {"N": "novo", "V": "variação", "F": "fusão de fusões", "L": "prodígio", "X": "fusão base + sacrifício",
              "A": "ápice (base + sacrifício)"}


def faixa(txt):
    r = set()
    for p in txt.replace(" ", "").split(","):
        if not p:
            continue
        if "-" in p:
            a, b = p.split("-", 1)
            r |= set(range(int(a), int(b) + 1))
        else:
            r.add(int(p))
    return r


def corta(s, k):
    s = " ".join(str(s or "").split())
    return s if len(s) <= k else s[:k - 1] + "…"


def origem(i, rot):
    hum = "humanoide" if i.get("humanoide") else "não humanoide"
    lin = f" | linhagem: {', '.join(i['linhagem'])}" if i.get("linhagem") else ""
    print(f"   - {rot} {i['nome']} (tier {i['tier']}, {i['tipo1']}/{i['tipo2']}, {hum}) {i.get('recorte', '')}{lin}")
    if i.get("visual"):
        print(f"     visual: {corta(i['visual'], 420)}")
    print(f"     descrição: {corta(i.get('descricao'), 320)}")


def main():
    lote = comum.pasta_lote(sys.argv, USO)
    pos = [a for a in sys.argv[2:] if not a.startswith("--")]
    try:
        entrada = comum.ler_json(os.path.join(lote, "entrada.json"))
    except FileNotFoundError:
        print("falta entrada.json: rode antes  python montar_entrada.py <pasta_do_lote>")
        sys.exit(2)
    if not pos:
        print(USO)
        sys.exit(2)
    try:
        cart = None if pos[0].lower() == "todas" else faixa(",".join(pos))
    except ValueError:
        print(f"cartelas inválidas: {' '.join(pos)}\n{USO}")
        sys.exit(2)
    por_n = {e["n"]: e for e in entrada}
    mostradas = 0
    ultima = None
    for e in entrada:
        if cart is not None and e["cartela"] not in cart:
            continue
        if e["cartela"] != ultima:
            ultima = e["cartela"]
            prancha = os.path.join("referencias", f"cartela_{e['cartela']:03d}_pais.png")
            tem = os.path.exists(os.path.join(lote, prancha))
            print(f"\n######## cartela {e['cartela']:03d}" + (f" | prancha: {prancha} (olhe antes de escrever)" if tem else "")
                  + (f" | TEMA do plano: {e['tema']}" if e.get("tema") else ""))
        mostradas += 1
        b = e["bloco"]
        print(f"\n== n {e['n']} | {e['slot']} L{e['linha']}C{e['coluna']} | bloco {b} ({NOME_BLOCO[b]}) | tier {e['tier']} | "
              f"tipos {e['tipo1']}/{e['tipo2']} | humanoide_previsto {e['humanoide_previsto']}")
        if e.get("leitura"):
            print(f"   LEITURA (direção do plano): {e['leitura']}")
        if b in ("N", "L") and e.get("fidelidade") == "homenagem":
            rc = e.get("referencia_conteudo") or {}
            print("   HOMENAGEM reconhecível: escreva 'tracos_iconicos' (3–6 traços visuais: máscara, figurino, arma/objeto, "
                  "cores, silhueta, postura, detalhe-assinatura); nunca o nome da figura, da obra ou do ator em campo nenhum")
            if rc.get("descricao"):
                print(f"   FIGURA (interno, não copie o nome): {corta(rc['descricao'], 320)}")
            if rc.get("recorte"):
                print(f"   referência no quadrante da prancha: {rc['recorte']} (olhe antes de escrever)")
        if b in ("N", "L") and e.get("fidelidade") == "releitura":
            rc = e.get("referencia_conteudo") or {}
            print("   RELEITURA: escreva 'ancoras' (2–3 traços que fazem entender a referência: em geral o rosto/máscara/"
                  "cabeça e UMA silhueta ou objeto-assinatura) e 'reinvencao' (1–2 frases: como os DOIS tipos reinventam "
                  "corpo, material, paleta, detalhes e pose). Proibido: figurino inteiro, paleta original inteira, réplica "
                  "de arma/objeto além da âncora, pessoa fantasiada; nunca o nome da figura, da obra ou do ator")
            if rc.get("descricao"):
                print(f"   FIGURA (interno, não copie o nome): {corta(rc['descricao'], 320)}")
            if rc.get("recorte") and e.get("usar_imagem") is True:
                print(f"   referência no quadrante da prancha: {rc['recorte']} (use só para ler as âncoras)")
        if b == "N":
            ev = e.get("evolucao") or {}
            ant, seg, ext = por_n.get(ev.get("anterior")), por_n.get(ev.get("seguinte")), ev.get("externo")
            if ant or seg or ext:
                txt = []
                if ext:
                    txt.append(f"evolui de {ext['nome']} (monstro EXISTENTE, fora do lote; no quadrante da prancha) — a "
                               f"anatomia começa com 'Evolução do/da {ext['nome']}.'; mantém as 2 cores, os olhos e um "
                               f"traço; corpo NOVO, mais velho e robusto; nome novo diferente do antecessor")
                if ant:
                    txt.append(f"evolui de n {ant['n']} ({ant['slot']}, tier {ant['tier']}) — anatomia começa com "
                               f"\"Evolução do/da <nome>.\"; mantém as 2 cores, os olhos e um traço")
                if seg:
                    txt.append(f"evolui para n {seg['n']} ({seg['slot']}, tier {seg['tier']})")
                print("   EVOLUÇÃO: " + " | ".join(txt))
                if ext:
                    origem(ext, "ANTECESSOR")
        elif b == "V":
            o = e["original"]
            print(f"   sai {e['tipo_sai']} -> entra {e['tipo_entra']} | nome final = \"{o['nome']} <epíteto>\" (sem #N)")
            origem(o, "ORIGINAL")
        elif b == "L":
            print("   prodígio: tema único para as 4 da cartela (campo 'tema' igual nas 4 fichas)")
        for i in e.get("ingredientes") or []:
            origem(i, i.get("papel", "PAI"))
    if not mostradas:
        print("nenhuma célula nessas cartelas")
        sys.exit(1)


if __name__ == "__main__":
    main()
