# -*- coding: utf-8 -*-
"""Testes do recortar_grade.py (portados do v2.1 + grade RxC, relatório por célula, máscara, lote) e do
itens_montar_prompts.py. Só imagens sintéticas em pasta temporária:  python test_recortar_grade.py"""
import json
import os
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import recortar_grade as rg  # noqa: E402
import itens_montar_prompts as imp  # noqa: E402


def ler(caminho, binario=False):
    with open(caminho, "rb" if binario else "r", **({} if binario else {"encoding": "utf-8"})) as fh:
        return fh.read()


def ler_json(caminho):
    return json.loads(ler(caminho))


def gravar_json(caminho, dado):
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(dado, fh, ensure_ascii=False)


def cartela_v21(core_height=277):
    """A cartela de regressão do v2.1 (Fera página 2): 1600², 24 quadradinhos e um item alto com borda alfa 1."""
    image = Image.new("RGBA", (1600, 1600))
    draw = ImageDraw.Draw(image)
    nomes = []
    for index in range(25):
        row, column = divmod(index, 5)
        cx, cy = column * 320 + 160, row * 320 + 160
        if index < 24:
            draw.rectangle((cx - 15, cy - 15, cx + 15, cy + 15), fill=(40, 80, 120, 255))
        else:
            left, top = cx - 79, cy - core_height // 2
            right, bottom = left + 158, top + core_height
            draw.rectangle((left - 8, top - 8, right + 7, bottom + 7), fill=(230, 30, 40, 1))
            draw.rectangle((left, top, right - 1, bottom - 1), fill=(90, 60, 30, 255))
        nomes.append(f"item_{index + 1:02d}.png")
    return image, nomes


def grade_simples(linhas, colunas, cel=200, raio=30, pular=(), forma="quadrado"):
    im = Image.new("RGBA", (colunas * cel, linhas * cel))
    d = ImageDraw.Draw(im)
    for r in range(linhas):
        for c in range(colunas):
            if r * colunas + c + 1 in pular:
                continue
            cx, cy = c * cel + cel // 2, r * cel + cel // 2
            caixa = (cx - raio, cy - raio, cx + raio, cy + raio)
            if forma == "circulo":
                d.ellipse(caixa, fill=(200, 120, 40, 255), outline=(255, 255, 255, 255), width=3)
            else:
                d.rectangle(caixa, fill=(30 + 8 * r, 90 + 8 * c, 140, 255))
    return im


class PortadosV21(unittest.TestCase):
    def test_item_alto_preserva_rgba_em_escala_nativa(self):
        image, nomes = cartela_v21()
        sheet, crops, rel = rg.recortar(image.copy(), 5, 5, nomes)
        rec = rel["celulas"][-1]
        crop = crops["item_25.png"]
        self.assertEqual(rec["pixels_enquadrados"], [174, 293])
        self.assertEqual(rec["janela"], "contexto")
        self.assertEqual(crop.size, (320, 320))
        self.assertEqual(rec["margens"], [73, 13, 73, 14])
        self.assertTrue(rec["margem_abaixo_da_referencia"])
        self.assertEqual(rel["abaixo_da_margem_referencia"], [25])
        self.assertFalse(rel["redimensionado"])
        self.assertEqual(rel["estado"], "OK")
        ox, oy = rec["deslocamento"]
        self.assertEqual(crop.crop((ox, oy, ox + 174, oy + 293)).tobytes(),
                         image.crop(tuple(rec["janela_origem"])).tobytes())
        self.assertEqual(sheet.crop((1280, 1280, 1600, 1600)).tobytes(), crop.tobytes())
        esperado = Image.new("RGBA", (320, 320))
        esperado.paste(image.crop((137, 137, 184, 184)), (136, 136))
        self.assertEqual(crops["item_01.png"].tobytes(), esperado.tobytes())

    def test_limite_exato_de_304_cabe(self):
        image, nomes = cartela_v21(core_height=288)
        _, _, rel = rg.recortar(image, 5, 5, nomes)
        self.assertEqual(rel["celulas"][-1]["pixels_enquadrados"], [174, 304])
        self.assertEqual(min(rel["celulas"][-1]["margens"]), 8)

    def test_acima_do_limite_reprova_a_celula_sem_tocar_a_origem(self):
        with tempfile.TemporaryDirectory() as pasta:
            image, nomes = cartela_v21(core_height=289)
            fonte = os.path.join(pasta, "pai.png")
            image.save(fonte)
            antes = ler(fonte, True)
            _, crops, rel = rg.recortar_arquivo(fonte, 5, 5, nomes)
            self.assertEqual(rel["estado"], "REPROVADA")
            self.assertEqual(rel["celulas_com_erro"], [25])
            self.assertIn("margem mínima de 8px", rel["celulas"][-1]["problemas"][0])
            self.assertNotIn("item_25.png", crops)
            self.assertEqual(len(crops), 24)
            self.assertEqual(ler(fonte, True), antes)
            self.assertEqual(os.listdir(pasta), ["pai.png"])

    def test_pedaco_do_vizinho_sai_do_recorte(self):
        im = grade_simples(5, 5, cel=200, raio=40)
        d = ImageDraw.Draw(im)
        # objeto da célula 1 com uma ponta comprida que entra na janela da célula 2 (sem encostar nela)
        d.rectangle((140, 95, 255, 105), fill=(250, 0, 0, 255))
        _, crops, rel = rg.recortar(im, 5, 5, [f"c{i}.png" for i in range(1, 26)])
        c2 = next(c for c in rel["celulas"] if c["celula"] == 2)
        self.assertGreater(c2["pixels_vizinho_removidos"], 0)
        self.assertEqual(c2["vizinhos_excluidos"], [1])
        vermelho = crops["c2.png"].tobytes().count(bytes((250, 0, 0, 255)))
        self.assertEqual(vermelho, 0)


class RelatorioPorCelula(unittest.TestCase):
    def test_celula_vazia(self):
        im = grade_simples(5, 5, pular={7})
        _, crops, rel = rg.recortar(im, 5, 5, [f"c{i}.png" for i in range(1, 26)])
        self.assertEqual(rel["estado"], "REPROVADA")
        self.assertEqual(rel["celulas_com_erro"], [7])
        self.assertIn("vazia", rel["celulas"][6]["problemas"][0])
        self.assertEqual(len(crops), 24)

    def test_celula_cortada_na_borda(self):
        im = grade_simples(5, 5, pular={5})
        ImageDraw.Draw(im).rectangle((930, 60, 999, 140), fill=(10, 10, 10, 255))
        _, _, rel = rg.recortar(im, 5, 5, [f"c{i}.png" for i in range(1, 26)])
        self.assertEqual(rel["celulas_com_erro"], [5])
        self.assertIn("cortada", rel["celulas"][4]["problemas"][0])

    def test_dupla_vira_atencao_e_e_recortada_junta(self):
        im = grade_simples(5, 5, pular={13})
        d = ImageDraw.Draw(im)
        d.rectangle((420, 450, 470, 500), fill=(0, 200, 0, 255))
        d.rectangle((530, 450, 580, 500), fill=(0, 0, 200, 255))
        _, crops, rel = rg.recortar(im, 5, 5, [f"c{i}.png" for i in range(1, 26)])
        self.assertEqual(rel["estado"], "ATENCAO")
        self.assertEqual(rel["celulas_com_atencao"], [13])
        self.assertIn("c13.png", crops)

    def test_fundo_opaco_reprova_a_pagina(self):
        im = Image.new("RGBA", (500, 500), (255, 255, 255, 255))
        _, crops, rel = rg.recortar(im, 5, 5, [f"c{i}.png" for i in range(1, 26)])
        self.assertEqual(rel["estado"], "REPROVADA")
        self.assertTrue(rel["problemas_pagina"])
        self.assertEqual(crops, {})
        _, _, rel = rg.recortar(Image.new("RGB", (500, 500)), 5, 5, [None] * 25)
        self.assertIn("sem alfa", rel["problemas_pagina"][0])

    def test_celula_sem_nome_e_pulada(self):
        im = grade_simples(2, 2)
        _, crops, rel = rg.recortar(im, 2, 2, ["a.png", None, "c.png", "d.png"])
        self.assertEqual(sorted(crops), ["a.png", "c.png", "d.png"])
        self.assertEqual(rel["celulas_sem_nome_com_objeto"], [2])

    def test_janela_justa_quando_o_contexto_nao_cabe(self):
        im = Image.new("RGBA", (1000, 1000))
        ImageDraw.Draw(im).rectangle((10, 10, 299, 299), fill=(9, 9, 9, 255))  # 290 px, contexto daria 306
        _, crops, rel = rg.recortar(im, 1, 1, ["x.png"], lado=320)
        self.assertEqual(rel["celulas"][0]["janela"], "justa")
        self.assertEqual(rel["celulas"][0]["margens"], [15, 15, 15, 15])


class MascaraCircularIcones(unittest.TestCase):
    def test_4x4_300px_com_mascara(self):
        cel = 313
        im = Image.new("RGBA", (cel * 4, cel * 4))
        d = ImageDraw.Draw(im)
        for r in range(4):
            for c in range(4):
                cx, cy = c * cel + cel // 2, r * cel + cel // 2
                d.ellipse((cx - 135, cy - 135, cx + 135, cy + 135), fill=(60, 140, 60, 255),
                          outline=(255, 255, 255, 255), width=4)
                # sombra fraca fora do círculo (deve sumir)
                d.rectangle((cx + 120, cy + 120, cx + 145, cy + 145), fill=(0, 0, 0, 20))
        _, crops, rel = rg.recortar(im, 4, 4, [f"ic{i:02d}.png" for i in range(1, 17)], lado=300, mascara=True)
        self.assertEqual(rel["estado"], "OK", rel)
        self.assertEqual(len(crops), 16)
        for c in rel["celulas"]:
            self.assertEqual(c["janela"], "justa")
            self.assertGreater(c["pixels_fora_do_circulo"], 0)
            self.assertGreaterEqual(min(c["margens"]), 8)
        a = crops["ic01.png"].getchannel("A")
        self.assertEqual(a.getpixel((2, 2)), 0)
        self.assertEqual(crops["ic01.png"].size, (300, 300))

    def test_medalhao_de_293_em_celula_de_313_e_reduzido_com_borda_suave(self):
        cel = 313
        im = Image.new("RGBA", (cel * 4, cel * 4))
        d = ImageDraw.Draw(im)
        for r in range(4):
            for c in range(4):
                cx, cy = c * cel + cel // 2, r * cel + cel // 2
                d.ellipse((cx - 146, cy - 146, cx + 146, cy + 146), fill=(40, 90, 160, 255),
                          outline=(255, 255, 255, 255), width=5)
        nomes = [f"ic{i:02d}.png" for i in range(1, 17)]
        _, _, rel = rg.recortar(im, 4, 4, nomes, lado=300, mascara=True, reduzir=False)
        self.assertEqual(rel["celulas_com_erro"], list(range(1, 17)))  # sem reduzir não cabe
        _, crops, rel = rg.recortar(im, 4, 4, nomes, lado=300, mascara=True)  # máscara liga reduzir
        self.assertEqual(rel["estado"], "OK", rel["celulas"][0])
        self.assertTrue(rel["redimensionado"])
        self.assertEqual(len(rel["celulas_reduzidas"]), 16)
        ic = crops["ic01.png"]
        bb = ic.getchannel("A").getbbox()
        self.assertLessEqual(max(bb[2] - bb[0], bb[3] - bb[1]), 284)
        self.assertGreaterEqual(min(bb[0], bb[1], 300 - bb[2], 300 - bb[3]), 8)
        self.assertEqual(ic.getpixel((150, 150))[3], 255)

    def test_borda_da_mascara_tem_anti_alias_e_o_miolo_nao_muda(self):
        im = Image.new("RGBA", (313, 313))
        ImageDraw.Draw(im).ellipse((21, 21, 291, 291), fill=(200, 60, 60, 255))
        _, crops, rel = rg.recortar(im, 1, 1, ["x.png"], lado=300, mascara=True)
        self.assertEqual(rel["estado"], "OK")
        self.assertNotIn("reduzido", rel["celulas"][0])
        alfas = crops["x.png"].getchannel("A").tobytes()
        self.assertGreater(sum(1 for a in alfas if 0 < a < 255), 50)  # borda suave
        self.assertEqual(crops["x.png"].getpixel((150, 150)), (200, 60, 60, 255))

    def test_item_grande_com_reduzir_cabe_sem_reduzir_reprova(self):
        image, nomes = cartela_v21(core_height=300)
        _, _, rel = rg.recortar(image, 5, 5, nomes)
        self.assertEqual(rel["celulas_com_erro"], [25])
        self.assertFalse(rel["redimensionado"])
        _, crops, rel = rg.recortar(image, 5, 5, nomes, reduzir=True)
        self.assertEqual(rel["estado"], "OK")
        self.assertEqual(rel["celulas_reduzidas"], [25])
        self.assertLessEqual(max(rel["celulas"][-1]["pixels_reduzidos"]), 304)

    def test_icone_sem_mascara_cabe_pela_janela_justa(self):
        cel = 313
        im = Image.new("RGBA", (cel, cel))
        ImageDraw.Draw(im).ellipse((21, 21, 291, 291), fill=(60, 140, 60, 255))
        _, _, rel = rg.recortar(im, 1, 1, ["x.png"], lado=300)
        self.assertEqual(rel["estado"], "OK")
        self.assertEqual(rel["celulas"][0]["janela"], "justa")


class LoteEmDisco(unittest.TestCase):
    def _lote(self, pasta):
        im = grade_simples(5, 5, cel=250, raio=40)
        os.makedirs(os.path.join(pasta, "cartelas"))
        im.save(os.path.join(pasta, "cartelas", "pagina_01_original.png"))
        itens = [{"nome": f"Item {r}{c}", "tipagem": "marinho", "faixa": r, "pagina": 1, "linha": r, "coluna": c,
                  "arquivo": f"marinho/faixa_{r:02d}_item_{r}{c}.png"} for r in range(1, 6) for c in range(1, 6)]
        gravar_json(os.path.join(pasta, "itens.json"), {"lote": "t", "organizacao": "faixa_por_linha", "itens": itens})

    def test_lote_grava_por_tipagem_e_protege_edicao(self):
        with tempfile.TemporaryDirectory() as pasta:
            self._lote(pasta)
            self.assertEqual(rg.main([pasta, "--simular"]), 0)
            self.assertFalse(os.path.exists(os.path.join(pasta, "marinho")))
            self.assertEqual(rg.main([pasta]), 0)
            arquivos = sorted(os.listdir(os.path.join(pasta, "marinho")))
            self.assertEqual(len(arquivos), 25)
            self.assertTrue(os.path.exists(os.path.join(pasta, "cartelas", "pagina_01_grade.png")))
            rel = ler_json(os.path.join(pasta, "validacao", "recorte_pagina_01.json"))
            self.assertEqual(len(rel["saidas"]), 26)
            # rodar de novo: nada muda
            self.assertEqual(rg.main([pasta]), 0)
            # edição externa num recorte = conflito, nada gravado
            alvo = os.path.join(pasta, "marinho", arquivos[0])
            Image.new("RGBA", (320, 320), (1, 2, 3, 255)).save(alvo)
            os.remove(os.path.join(pasta, "marinho", arquivos[1]))
            self.assertEqual(rg.main([pasta]), 1)
            self.assertFalse(os.path.exists(os.path.join(pasta, "marinho", arquivos[1])))
            self.assertEqual(rg.main([pasta, "--substituir"]), 0)
            self.assertTrue(os.path.exists(os.path.join(pasta, "marinho", arquivos[1])))

    def test_imagem_solta_com_nomes(self):
        with tempfile.TemporaryDirectory() as pasta:
            fonte = os.path.join(pasta, "avulsa.png")
            grade_simples(1, 1, cel=400, raio=100).save(fonte)
            nomes = os.path.join(pasta, "nomes.json")
            gravar_json(nomes, ["marinho/faixa_03_x.png"])
            self.assertEqual(rg.main([fonte, "--grade", "1x1", "--nomes", nomes, "--saida", pasta]), 0)
            self.assertTrue(os.path.exists(os.path.join(pasta, "marinho", "faixa_03_x.png")))

    def test_nunca_grava_dentro_da_skill(self):
        with self.assertRaises(ValueError):
            rg.publicar(os.path.join(rg.comum.SKILL_DIR, "x"), {}, os.path.join(tempfile.gettempdir(), "r.json"), {})


class MontarPrompts(unittest.TestCase):
    def _dados(self, org="faixa_por_linha"):
        slots = ["arma", "armadura", "orb"]
        itens = []
        for r in range(1, 6):
            for c in range(1, 6):
                tip = "marinho" if org == "faixa_por_linha" else ["normal", "planta", "inseto", "fera", "agua"][r - 1]
                fx = r if org == "faixa_por_linha" else c
                itens.append({"nome": f"Peça {r}{c}", "tipagem": tip, "faixa": fx, "slot": slots[(r + c) % 3],
                              "descricao": "o que é", "pagina": 1, "linha": r, "coluna": c,
                              "visual": f"a distinct object shaped like concept{chr(96 + r)}{chr(96 + c)} "
                                        f"variant{chr(96 + c)}{chr(96 + r)} made of material{chr(96 + r)}{chr(96 + c)} "
                                        f"with motif{chr(96 + c)}{chr(96 + r)}, fixed by a buckled strap"})
        return {"lote": "teste", "organizacao": org, "itens": itens}

    def test_valido_nos_dois_arranjos(self):
        for org in imp.ORGANIZACOES:
            erros, _, paginas = imp.validar(self._dados(org))
            self.assertEqual(erros, [], org)
            self.assertEqual(len(paginas[1]), 25)

    def test_erros_de_regra(self):
        d = self._dados()
        d["itens"][0]["visual"] = "a steel sword with a leather handle and a buckled strap"
        d["itens"][1]["visual"] = "a peca 12 made of bone with a cord"
        d["itens"][2]["linha"] = 1
        d["itens"][2]["coluna"] = 1
        erros, _, _ = imp.validar(d)
        txt = "\n".join(erros)
        self.assertIn("objeto de gente", txt)
        self.assertIn("nome em português", txt)
        self.assertIn("posições", txt)

    def test_aviso_de_recolorido(self):
        d = self._dados()
        d["itens"][0]["visual"] = "a red coral claw cap with three curved hooks, tied by a leather strap"
        d["itens"][5]["visual"] = "a blue coral claw cap with three curved hooks, tied by a leather strap"
        _, avisos, _ = imp.validar(d)
        self.assertTrue(any("recolorido" in a for a in avisos))

    def test_prompt_e_progressao(self):
        self.assertEqual(imp.progressao([1, 2, 3, 4, 5]).split(";")[2].strip()[:22], "tier 5 is fine work (p")
        d = self._dados("tipagem_por_linha")
        _, _, paginas = imp.validar(d)
        cab = ler(imp.TEMPLATE_PAGINA)
        txt = imp.montar_prompt(d, 1, paginas[1], 2, cab)
        self.assertIn("LAYOUT OF THIS SHEET: each ROW is one elemental type (row 1 = Normal; row 2 = Planta; "
                      "row 3 = Inseto; row 4 = Fera; row 5 = Agua).", txt)
        self.assertIn("sheet 1 of 2 (types Normal, Planta, Inseto, Fera, Agua; tiers 1–5)", txt)
        self.assertIn("Row 5, column 5 (Agua, tier 5, armor):", txt)
        self.assertIn("monster equipment, no handle, no hilt, no human glove/torso", txt.lower())
        self.assertNotIn("{", txt)
        self.assertNotIn("Peça", txt)

    def test_gravar_lote(self):
        with tempfile.TemporaryDirectory() as pasta:
            gravar_json(os.path.join(pasta, "itens.json"), self._dados())
            self.assertEqual(imp.main(["x", pasta, "--gravar"]), 0)
            for f in ("prompts/pagina_01.txt", "fila.json", "PROMPT_ITENS_TESTE.md",
                      "referencias/estilo_03_miniatura_3d.png", "referencias/guia_grade_5x5.png"):
                self.assertTrue(os.path.exists(os.path.join(pasta, f)), f)
            fila = ler_json(os.path.join(pasta, "fila.json"))
            self.assertEqual(fila[0]["estado"], "pronta")
            self.assertEqual(fila[0]["itens"][0]["arquivo"], "marinho/faixa_01_peca_11.png")
            doc = ler(os.path.join(pasta, "PROMPT_ITENS_TESTE.md"))
            self.assertNotIn("{PASTA_LOTE}", doc)
            self.assertIn(pasta, doc)
            dados = ler_json(os.path.join(pasta, "itens.json"))
            self.assertEqual(dados["itens"][0]["arquivo"], "marinho/faixa_01_peca_11.png")


if __name__ == "__main__":
    unittest.main()
