# Modo: Capas (expedição, raid, cartaz de evento, moldura de invasão, wallpaper de passe)

Regras: [../regras/cenarios-mapas-capas.md](../regras/cenarios-mapas-capas.md) §5. Tamanhos:
[../regras/formatos.md](../regras/formatos.md). Anexos: [../referencias/REFERENCIAS.md](../referencias/REFERENCIAS.md).
Sessões e ONDE SALVAR: [../regras/fluxo-sessoes.md](../regras/fluxo-sessoes.md). Ambiente (ChatGPT, Codex, Claude
Code): [../regras/ambiente.md](../regras/ambiente.md). `{SKILL}` = a pasta desta skill (onde está o SKILL.md);
`<lote>` = a pasta do lote (no ChatGPT web, `/mnt/data/<lote>`; no ChatGPT desktop, a pasta local).

- **Entra:** a lista de cenas (uma por tipagem, tipo de evento ou raid) e **2 ou 3 artes do próprio jogo** como
  referência de estilo — **o usuário fornece** (no ChatGPT, por upload; ainda não há referência fixa de capa na skill). Sem elas, peça antes de
  gerar.
- **Sai:** `finais/<grupo>_<cena>.webp` **510×680** (uma por cena) e, se houver, `finais/moldura_<tema>.png`
  **1672×941** RGBA; mais `entregas.json` e `ENTREGA.md`.
- **Wallpaper de passe:** sem regra de composição própria ainda — pergunte ao usuário; o ajuste de tamanho é
  `fundos_normalizar.py <lote> --destino wallpaper` (1672×941, recorte pelo centro, JPG).

## Pasta do lote

```
<lote>/
├── plano.json           cartelas e nomes das cenas (formato abaixo)
├── referencias/         estilo_1.png, estilo_2.png (estilo_3.png) — as artes do jogo que o usuário forneceu
├── PROMPT_<LOTE>.md     sessão de imagem (de templates/capas/PROMPT_CAPAS.md)
├── cartelas/            cartela_NNN_original.png (+ _v2, _v3) — a sessão de imagem não recorta
├── brutos/              moldura_<tema>.png (se houver)
├── finais/              as capas WebP e a moldura PNG
├── conferencia/         capas_<cartela>.jpg (as 4 capas com o miolo 146×188 marcado), prancha_moldura.jpg
├── validacao/           geracoes_capas.json (sessão de imagem)
├── entregas.json
└── ENTREGA.md
```

`plano.json`:

```json
{"lote": "capas_expedicoes", "cartelas": [
  {"cartela": 1, "grupo": "expedicoes", "cenas": ["agua", "marinho", "gelo", "vento"]},
  {"cartela": 2, "grupo": "raids", "cenas": ["agua", "marinho", "gelo", "vento"]}]}
```

Ordem das cenas: 1 = cima-esquerda, 2 = cima-direita, 3 = baixo-esquerda, 4 = baixo-direita. O `grupo` vira prefixo
do arquivo (expedição e raid da mesma tipagem não colidem).

## Fluxo

1. **Plano:** 4 cenas por cartela, nenhuma parecida com a vizinha; uma cor dominante por cena (expedição); raid = o mesmo
   lugar e paleta da expedição, em clima de ameaça, palco vazio no centro; campeonatos pela escala e pelo metal.
   Grave `plano.json`.
2. **PROMPT da sessão:** copie [`templates/capas/PROMPT_CAPAS.md`](../templates/capas/PROMPT_CAPAS.md) para
   `<lote>/PROMPT_<LOTE>.md`, troque `{PASTA_LOTE}`, `{SKILL}`, `{LOTE}`, deixe só o parágrafo "O que é cada cena" do
   tipo, escreva a lista de cada cartela (nome — cena em 1–2 frases com o símbolo central; cor dominante por nome) e,
   se houver, a seção da moldura. Fila cheia antes de gerar.
3. **Geração das imagens:** no ChatGPT/Codex, a própria conversa segue o `PROMPT_<LOTE>.md` e gera; no Claude Code,
   entregue a frase para colar no ChatGPT/Codex. BLOCO FIXO + uma cartela por geração, todas em ordem; moldura numa
   geração separada.
4. **Converter as cartelas:**

   ```
   python "{SKILL}/scripts/capas_converter.py" <lote>
   python "{SKILL}/scripts/capas_converter.py" <lote>/cartelas/cartela_003_v2.png   # uma só
   ```

   Acha a cruz branca (tolera cartela fora de 1536×2048, como 1086×1448, e faixa fora de 40 px; sem faixa, corta pela
   geometria e avisa), apara sobra branca, recorta 3:4 pelo centro, reduz para 510×680 e confere o miolo 146×188 (o que
   o cartão mostra): avisa se estiver uniforme (palco vazio) ou se sobrou faixa na borda. Usa a tentativa mais alta de
   cada cartela (`_vN` > `_original`), ignora `_ruimN` e nunca sobrescreve uma capa.
5. **Moldura de invasão:**

   ```
   python "{SKILL}/scripts/fundos_normalizar.py" <lote> --destino moldura
   ```

   Só redimensiona para 1672×941 RGBA; fundo verde puro vira transparente; mede a cobertura (alvo < 15%) e avisa se há
   arte nos 56% do meio. Confira no olho contra `referencias/capas/template_monstros_invasao.png`: arte só nas laterais,
   concentrada nos cantos, nada cruzando o centro, recorte limpo sem névoa ou brilho solto.
6. **Conferir no olho** por `conferencia/capas_*.jpg`: composição vertical e centrada, palco no meio, nada importante
   nas bordas, nenhum texto, rosto ou criatura em destaque, as 4 cenas da mesma coleção.
7. **Entrega:** `entregas.json` já traz cada capa (cartela, posição, miolo); acrescente o `nome` de exibição se quiser.
   `ENTREGA.md` com pendências (cartela que esgotou as 3 imagens, aviso de miolo) e a linha no `ENTREGAS.md`. No
   ChatGPT web, entregue o lote como `.zip` (no desktop, a própria pasta).
