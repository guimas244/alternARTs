# Modo: Itens e equipamentos (equipamento de monstro, livro, essência, pedra ritual, campeonato, agenda)

Fluxo completo de um lote de itens em cartela 5x5, do pedido ao pacote de entrega. A regra da arte (estilo, o que é
equipamento de monstro, faixas, grade, texto fixo do prompt, casos especiais) está em
[../regras/itens.md](../regras/itens.md) — este arquivo só diz **como executar**. `{SKILL}` = `${CLAUDE_SKILL_DIR}`;
`<lote>` = a pasta de trabalho do lote (fora da skill). Joia e item de passe: sem regra própria ainda, pergunte ao usuário.

## 0. Plano do lote

1. Entenda o pedido e escolha a **organização da página** ([../regras/itens.md](../regras/itens.md) §4):
   - `faixa_por_linha` — coleção de **uma tipagem**: 2 páginas de 25 (página 1 = faixas 1–5, página 2 = 6–10), cada
     linha é uma faixa;
   - `tipagem_por_linha` — **pacote misto**: 5 tipagens por cartela, linha = tipagem, coluna = faixa (uma cartela com
     as faixas 1–5 e a seguinte com as 6–10).
2. Mostre ao criador a tabela página × linha × coluna (tipagem, faixa, slot). Slot = `arma`, `armadura` ou `orb`
   (varie: em cada tipagem nenhum slot domina). Ajuste até ele aprovar. Sempre 25 por página.
3. Categoria: `equipamento` (padrão; usa o texto fixo do equipamento de monstro). Livro, essência, pedra ritual,
   campeonato, agenda: `categoria` própria **e** escreva `<lote>/cabecalho_pagina.txt` a partir de
   `{SKILL}/templates/itens/PROMPT_PAGINA_ITENS.txt`, trocando só o parágrafo do equipamento pelo do caso especial
   (§7 da regra); os marcadores `{…}` continuam os mesmos. Pedra ritual sai em 512 (`"lado": 512`).

## 1. `itens.json` (o contrato)

```json
{
  "lote": "marinho_v2",
  "titulo": "Coleção Marinho v2",
  "colecao": "collection Marinho",
  "organizacao": "faixa_por_linha",
  "categoria": "equipamento",
  "lado": 320,
  "itens": [
    {"nome": "Arpão de Osso", "tipagem": "marinho", "faixa": 1, "slot": "arma",
     "descricao": "o que é, em português (vai para a ficha do jogo)",
     "visual": "a hollow fang cap of ivory whale bone ... tied by a tan rope cuff",
     "pagina": 1, "linha": 1, "coluna": 1}
  ]
}
```

- `tipagem` = id de `comum.TIPOS` (`agua`, `marinho`, `subterraneo`…). `colecao` vai em inglês no cabeçalho
  (`MONSTER EQUIPMENT {colecao}, sheet N of T`).
- `descricao`: frase curta do que o item é (português, sem número, sem termo de jogo).
- `visual`: a linha da célula **em inglês**, 20–45 palavras, começando por artigo + objeto: material, forma, cores e
  **como prende** (correia, argola, presilha, punho, encaixe). Nunca o nome em português, nunca acento.
- `arquivo` é preenchido pelo script: `<tipagem>/faixa_NN_<slug do nome>.png`.

## 2. Visual por agentes (lote grande)

- Divida por tipagem (ou por par de páginas). Cada agente escreve **só** o `visual` (e `nome`/`descricao`, se for dele)
  dos itens da sua parte, num arquivo próprio (`partes/<tipagem>.json`); um só junta tudo no `itens.json`.
- Antes de soltar os agentes, faça a **alocação nominal** das ideias por tipagem (que referência — anatomia, fenômeno,
  material, artefato — vai para qual célula), para não convergirem para o mesmo objeto (regra de orquestração em
  [../regras/fluxo-sessoes.md](../regras/fluxo-sessoes.md)). Cada agente lê o que os outros já escreveram.
- Padrão de criatividade: a primeira cartela Marinho — cada célula um conceito novo; a tipagem não impõe cor.

## 3. Validar e montar a fila

```
python "{SKILL}/scripts/itens_montar_prompts.py" <lote>            # só valida
python "{SKILL}/scripts/itens_montar_prompts.py" <lote> --gravar   # grava
```

- **ERRO** (bloqueia): página sem exatamente 25 itens ou com posição repetida, organização incoerente (linha que mistura
  faixa/tipagem, faixas fora de ordem), campo faltando, tipagem desconhecida, nome/arquivo repetido, slot inválido,
  acento ou nome em português no visual, **objeto de gente** no visual de equipamento (sword, staff, handle, hilt,
  glove, gauntlet, helmet, boot, spear, axe, dagger…).
- **AVISO** (revise, não bloqueia): visual parecido com outro da mesma tipagem (possível **objeto recolorido**), palavra
  que pede o teste do monstro (bow, shield, crown, cloak, trident…), sem dizer como prende, palavra de escrita,
  louro/medalha fora do campeonato, tamanho do visual fora de 12–60 palavras.
- Com `--gravar` (e sem erro) grava em `<lote>`: `prompts/pagina_NN.txt` (cabeçalho + `LAYOUT OF THIS SHEET` + células
  na ordem de leitura), `referencias/estilo_03_miniatura_3d.png` + `referencias/guia_grade_5x5.png`, `fila.json`,
  `PROMPT_ITENS_<LOTE>.md` (sessão de imagem, com ONDE SALVAR e a **tabela de conferência** linha × coluna → nome) e o
  `arquivo` de cada item no `itens.json`. `--forcar` grava mesmo com erro, só para ensaio: fila `bloqueada`.
- Leia 1 prompt inteiro antes de liberar: a ordem das células é o que dá nome a cada recorte.

## 4. Sessão de imagem

Entregue ao usuário o caminho de `<lote>/PROMPT_ITENS_<LOTE>.md` (modos piloto / FAIXA / TODOS, como em
[../regras/fluxo-sessoes.md](../regras/fluxo-sessoes.md)). A sessão só gera, confere, simula o recorte e salva
`cartelas/pagina_NN_original.png` (+ `_vK` e `.prompt.txt`); refaz só por erro real, até 3 imagens por cartela
(regra §6). Você não gera imagem nem pede ao usuário para colar prompt.

## 5. Recortar

```
python "{SKILL}/scripts/recortar_grade.py" <lote> --simular      # confere sem gravar
python "{SKILL}/scripts/recortar_grade.py" <lote>                # grava
```

- Recorta todas as `cartelas/pagina_NN_original.png` que existirem: um PNG por item no `arquivo` dele
  (`<lote>/<tipagem>/faixa_NN_<descricao>.png`, `lado` × `lado` RGBA, sem redimensionar, margem 16 / mínimo 8),
  `cartelas/pagina_NN_grade.png` e `validacao/recorte_pagina_NN.json`. Opções: `--pagina N`, `--lado`, `--margem`,
  `--saida`, `--substituir` (sem ela, recorte editado à mão nunca é sobrescrito: a página inteira fica parada e avisa),
  `--reduzir` (objeto que não cabe é reduzido, mesma proporção; itens **não** reduzem por padrão — use só por decisão
  do dono).
- Resposta por página: **OK**, **ATENÇÃO** (duas manchas grandes separadas na célula, máscara cortando objeto — olhe)
  ou **REPROVADA** (fundo opaco/xadrez, célula vazia, objeto cortado na borda, objeto grande demais). As células boas
  são gravadas mesmo com outra reprovada.
- Célula reprovada vira **avulsa**: gere só aquele objeto (grade 1, mesmo estilo e mesma linha de célula), salve
  `cartelas/avulsa_NN_LxCy_vK.png` e recorte com
  `python "{SKILL}/scripts/recortar_grade.py" <lote>/cartelas/avulsa_NN_LxCy_vK.png --grade 1x1 --nomes <lote>/nomes/avulsa_NN_LxCy.json --saida <lote>`,
  onde o JSON é uma lista com o `arquivo` do item (ex.: `["marinho/faixa_03_arpao_de_osso.png"]`). A avulsa não lê o
  `lado` do `itens.json`: lote de 512 (pedra ritual) passa `--lado 512`. Esse passo é à mão (o script não acha a
  avulsa sozinho).
- Confira no olho 3 ou 4 recortes por página (objeto inteiro, sem pedaço do vizinho). Quem aprova a arte é o dono.

## 6. Entrega

Layout em [../regras/entrega.md](../regras/entrega.md) (Itens): `itens.json` (já com `arquivo`), `cartelas/`,
`<tipagem>/faixa_NN_*.png` e um `ENTREGA.md` escrito por você — quantas páginas e itens, quais células ficaram como
avulsa ou pendentes, os avisos que sobraram e o que precisa de olho humano. Acrescente a linha em `ENTREGAS.md` da
pasta de trabalho. Por tipagem, a descrição mínima de cada item e o índice ficam no `itens.json`; nome e classificação
nunca na arte.

Tamanhos: [../regras/formatos.md](../regras/formatos.md). Anexos: [../referencias/REFERENCIAS.md](../referencias/REFERENCIAS.md).
