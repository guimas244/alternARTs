# Modo: Ícones (ícone de mapa; ícone de tipo e selo)

Regras: [../regras/cenarios-mapas-capas.md](../regras/cenarios-mapas-capas.md) §6. Tamanhos:
[../regras/formatos.md](../regras/formatos.md). Anexos: [../referencias/REFERENCIAS.md](../referencias/REFERENCIAS.md).
Sessões e ONDE SALVAR: [../regras/fluxo-sessoes.md](../regras/fluxo-sessoes.md). Ambiente (ChatGPT, Codex, Claude
Code): [../regras/ambiente.md](../regras/ambiente.md). `{SKILL}` = a pasta desta skill (onde está o SKILL.md);
`<lote>` = a pasta do lote (no ChatGPT web, `/mnt/data/<lote>`; no ChatGPT desktop, a pasta local).

- **Entra:** a lista de ícones de mapa (id + cenário em 1 frase, com o marco), em grupos de 16.
- **Sai:** `recortes/<id>.png` **300×300 RGBA** (medalhão redondo, borda branca, fora do círculo transparente; no jogo
  aparece a 80×80), mais `entregas.json` e `ENTREGA.md`.
- **Ícone de tipo** (512×512) e **selo:** sem regra própria ainda — pergunte ao usuário antes de gerar.

## Pasta do lote

```
<lote>/
├── plano.json           as cartelas: {"cartelas": [{"cartela": 1, "icones": [{"id": "trilha", "cenario": "…"}, … 16]}]}
├── nomes/cartela_NNN.json   lista dos 16 ids na ordem de leitura (o recortador lê; null pula a célula)
├── prompts/cartela_NNN.txt  texto fixo + a lista dos 16
├── PROMPT_<LOTE>.md     sessão de imagem (de templates/icones/PROMPT_ICONES.md)
├── cartelas/            cartela_NNN_original.png (+ _v2, _v3), PNG com alfa
├── recortes/            <id>.png 300×300 RGBA
├── validacao/           geracoes_icones.json (sessão de imagem)
├── entregas.json
└── ENTREGA.md
```

`id`: minúsculas, sem acento, `_` (ex.: `castelo_assombrado`); único no lote.

## Fluxo

1. **Plano:** 16 ícones por cartela, **um único tema claro por círculo**, silhueta principal no centro (tem de ser
   reconhecível pequeno); nenhum texto, pessoa ou bicho. Grave `plano.json` e, para cada cartela,
   `nomes/cartela_NNN.json` com os 16 ids na ordem (linha 1 coluna 1 … linha 4 coluna 4).
2. **Prompts:** `prompts/cartela_NNN.txt` = texto fixo de
   [`templates/icones/PROMPT_ICONES.md`](../templates/icones/PROMPT_ICONES.md) + os 16 itens
   "(linha L, coluna C) {cenário}". Copie o template para `<lote>/PROMPT_<LOTE>.md` e troque `{PASTA_LOTE}`, `{SKILL}`,
   `{LOTE}` e a FILA. Fila cheia antes de gerar.
3. **Geração das imagens:** no ChatGPT/Codex, a própria conversa segue o `PROMPT_<LOTE>.md` e gera; no Claude Code,
   entregue a frase para colar no ChatGPT/Codex. Uma cartela por geração, com as 4 referências `referencias/icones/` (castelo, vila, cachoeira,
   portal_magico); fundo **transparente de verdade** (xadrez pintado ou branco reprova); medalhões separados por espaço
   transparente (círculos que se tocam pela sombra viram um só no recorte).
4. **Recortar** cada cartela com o recortador único de grade:

   ```
   python "{SKILL}/scripts/recortar_grade.py" <lote>/cartelas/cartela_001_original.png --grade 4x4 --lado 300 --mascara-circular --nomes <lote>/nomes/cartela_001.json --saida <lote>/recortes
   ```

   Ele separa os medalhões por região conectada, apaga o que fica fora do círculo e centraliza em 300×300 RGBA;
   `--mascara-circular` liga `--reduzir`, então medalhão maior que cabe em 300 é reduzido (mesma proporção) em vez de
   reprovar. Célula vazia, cortada na borda ou grudada no vizinho sai como erro daquela célula (as boas são gravadas).
   Use `--simular` para conferir sem gravar e `--substituir` para trocar de propósito um recorte que já existe.
   Opções e saída: docstring de `scripts/recortar_grade.py`.
5. **Conferir no olho:** 16 medalhões do mesmo tamanho, círculo inteiro com a borda branca, sem resto do vizinho, sem
   texto; reconhecível reduzido a 80×80. Célula reprovada: gere a cartela de novo do zero (máximo 3 imagens) ou anote
   como pendente.
6. **Entrega:** `entregas.json` com um registro por ícone (`id`, `arquivo: recortes/<id>.png`, `medida: [300, 300]`,
   `cartela`, `linha`, `coluna`, `prompt`), `ENTREGA.md` com pendências e a linha no `ENTREGAS.md`. No ChatGPT web,
   entregue o lote como `.zip` (no desktop, a própria pasta).

Atribuir o ícone a cada Local no jogo é do processo de cadastro, fora da skill.
