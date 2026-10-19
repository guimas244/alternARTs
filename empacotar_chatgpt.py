# -*- coding: utf-8 -*-
"""Gera dist/criar-arte.zip para subir no ChatGPT (Skills -> Create -> Upload from your computer).

    python empacotar_chatgpt.py

O zip tem a pasta da skill na raiz (criar-arte/SKILL.md, regras/, modos/, templates/, scripts/, referencias/, dados/),
sem cache do Python. Rodar de novo a cada atualização da skill e reenviar o zip.
"""
import os
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(AQUI, "plugins", "techterra-arte", "skills", "criar-arte")
DIST = os.path.join(AQUI, "dist")
FORA = {"__pycache__", ".pytest_cache"}


def main():
    if not os.path.isfile(os.path.join(SKILL, "SKILL.md")):
        sys.exit(f"SKILL.md não encontrado em {SKILL}")
    os.makedirs(DIST, exist_ok=True)
    destino = os.path.join(DIST, "criar-arte.zip")
    n = 0
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for raiz, pastas, arquivos in os.walk(SKILL):
            pastas[:] = sorted(p for p in pastas if p not in FORA)
            for a in sorted(arquivos):
                if a.endswith((".pyc", ".tmp")):
                    continue
                caminho = os.path.join(raiz, a)
                z.write(caminho, os.path.join("criar-arte", os.path.relpath(caminho, SKILL)).replace(os.sep, "/"))
                n += 1
    print(f"{destino}  ({n} arquivos, {os.path.getsize(destino) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
