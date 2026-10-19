# -*- coding: utf-8 -*-
"""Funções comuns dos scripts da skill criar-arte (sem banco, sem rede). Ver CONTRATO-INTERNO.md."""
import json
import os
import re
import sys
import unicodedata

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPTS_DIR)
REFS_DIR = os.path.join(SKILL_DIR, "referencias")
TEMPLATES_DIR = os.path.join(SKILL_DIR, "templates")
DADOS_DIR = os.path.join(SKILL_DIR, "dados")

LADO, CEL = 1254, 627          # cartela 2x2
RECORTE = 512                  # recorte final de monstro
MAX_ANEXOS = 5

TIPOS = {"agua": "Água", "alien": "Alien", "desconhecido": "Desconhecido", "deus": "Deus", "docrates": "Dócrates",
         "dragao": "Dragão", "eletrico": "Elétrico", "fantasma": "Fantasma", "fera": "Fera", "fogo": "Fogo", "gelo": "Gelo",
         "inseto": "Inseto", "luz": "Luz", "magico": "Mágico", "marinho": "Marinho", "mistico": "Místico", "normal": "Normal",
         "nostalgico": "Nostálgico", "pedra": "Pedra", "planta": "Planta", "psiquico": "Psíquico", "subterraneo": "Subterrâneo",
         "tecnologia": "Tecnologia", "tempo": "Tempo", "terrestre": "Terrestre", "trevas": "Trevas", "venenoso": "Venenoso",
         "vento": "Vento", "voador": "Voador", "zumbi": "Zumbi"}
BLOCOS = ("N", "V", "F", "L", "X", "A")
ONDE = {(1, 1): "the top-left cell", (1, 2): "the top-right cell", (2, 1): "the bottom-left cell",
        (2, 2): "the bottom-right cell"}


def norm(s):
    """minúsculo, sem acento."""
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", norm(s)).strip("_")


def arquivo_recorte(n, tier, nome):
    return f"{n:02d}_t{tier:02d}_{slug(nome)}.png"


def ler_json(caminho, padrao=None):
    if not os.path.exists(caminho):
        if padrao is not None:
            return padrao
        raise FileNotFoundError(caminho)
    with open(caminho, encoding="utf-8-sig") as fh:
        return json.load(fh)


def gravar_json(caminho, dado, indent=1):
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dado, fh, ensure_ascii=False, indent=indent)
        fh.write("\n")
    os.replace(tmp, caminho)


def gravar_texto(caminho, texto):
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)


def pasta_lote(argv, uso):
    """Primeiro argumento posicional = pasta do lote (precisa existir)."""
    pos = [a for a in argv[1:] if not a.startswith("--")]
    if not pos:
        print(uso)
        sys.exit(2)
    p = os.path.abspath(pos[0])
    if not os.path.isdir(p):
        print(f"pasta do lote não existe: {p}")
        sys.exit(2)
    return p


def nomes_existentes():
    """Conjunto normalizado (sem acento, minúsculo) dos nomes de monstro já usados no jogo."""
    lista = ler_json(os.path.join(DADOS_DIR, "nomes_existentes.json"), [])
    return {norm(x) for x in lista}


def seq4(a, b):
    """Primeira sequência de 4 letras de `a` que aparece em `b` (ou None)."""
    a, b = re.sub(r"[^a-z]", "", norm(a)), re.sub(r"[^a-z]", "", norm(b))
    for i in range(len(a) - 3):
        if a[i:i + 4] in b:
            return a[i:i + 4]
    return None
