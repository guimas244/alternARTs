# Pacote de entrega — o que a skill entrega no fim de cada lote

Para que serve: todo lote termina numa pasta padronizada com as **imagens recortadas** e as **fichas com descrição de
jogo**, no formato que o cadastrador do jogo já lê. A skill não cadastra (sem banco), mas deixa o lote pronto para quem
for inserir: é só apontar o cadastrador para a pasta.

> A descrição é obrigatória em toda ficha. Sem descrição o lote não está pronto: é ela que vira o texto do monstro no
> jogo e é dela que o jogo tira o porte (tamanho).

## Monstros, fusões, variações (layout da pasta do lote)

```
<lote>/
├── monstros.json        fichas (uma por criatura) — schema abaixo
├── cadastro.json        corpo de cada criatura (sugestão; a força é decisão do dono)
├── recortes/            NN_tTT_<slug>.png — 512×512 RGBA, um por criatura
├── cartelas/            cartela_NNN_original.png (+ _vN, avulsas) — histórico do lote
├── prompts/  fila.json  PROMPT_<LOTE>.md   — o que foi para a sessão de imagem
└── ENTREGA.md           resumo: quantas, quais, pendências, o que precisa de olho humano
```

- `NN` = ordem do lote (01, 02…, a "dex" do pacote), `TT` = tier com 2 dígitos, `slug` = nome em minúsculas sem acento,
  `_` no lugar de espaço. Ex.: `07_t03_ampulovo.png`.
- O recorte sai da cartela aprovada (`cartela_NNN_original.png`) já com as avulsas aplicadas por cima.

### `monstros.json`

```json
{
  "lote": "<nome_do_lote>",
  "monstros": [
    {
      "n": 1,
      "nome": "Nomeproprio",
      "tipo1": "zumbi",
      "tipo2": "psiquico",
      "tier": 3,
      "humanoide": true,
      "classe": "sonâmbulo",
      "descricao": "4 a 6 frases de jogo, sem aparência (regras/fichas-nomes-descricoes.md).",
      "visual": "o texto de arte que foi para o prompt",
      "arquivo": "01_t03_nomeproprio.png",
      "cartela": 1, "linha": 1, "coluna": 1,
      "evolucao": {"de": "Nome do antecessor", "modo": "level", "level_requerido": 10},
      "ingredientes": [
        {"papel": "BASE", "nome": "Nome exato do pai"},
        {"papel": "SACRIFICIO", "nome": "Nome exato do pai"}
      ]
    }
  ]
}
```

- Campos obrigatórios: `nome`, `tipo1`, `tipo2`, `tier`, `descricao`, `arquivo`, `humanoide` (+ `classe` se humanoide).
- `evolucao` só em quem evolui de outro (modo e level são decisão do criador — escreva o que ele disse; se ele não
  disse, deixe `"modo": "a_definir"`).
- `ingredientes` só em fusão, sempre pelo **NOME** exato dos pais (nunca id: id muda entre ambientes).
- Variação: acrescente `"variacao_de": "<nome do original>"`.
- Campos de arte que a skill usou (paleta, anatomia, rosto, marcas_poder, brilho, temperamento, conceito,
  marca_da_habilidade, herda, ascensao) podem ficar na ficha — o cadastrador ignora o que não conhece.

### `cadastro.json` (corpo)

```json
{"monstros": {"Nomeproprio": {"corpo": "Muralha", "forca": "medio"}}}
```

- `corpo`: como o corpo da arte se lê — `Bruto` (forte e resistente), `Muralha` (tanque), `Lamina` (rápido de ataque
  físico), `Artilharia` (ataque mágico à distância), `Enxame` (equilibrado), `Anomalo` (mágico e estranho). Escolha pelo
  desenho e pelo conceito.
- `forca` (`fraco`/`medio`/`forte`/`muito_forte`): posição dentro do tier. **Sugestão** — é balanceamento, o dono
  confirma. Varie dentro do lote (nem todos fortes).

## Personagens / NPCs

```
<lote>/
├── fichas.json          uma por pessoa: nome, gênero, idade, papel, etnia/tema, descricao (lore curta), visual
├── paginas/             pagina_NNN.png (original) — histórico
├── recortes/            pagina_NNN_colC_rosto.png (512×512) e pagina_NNN_colC_corpo.png (512×1024)
└── ENTREGA.md
```

- Cada ficha aponta os dois arquivos (`rosto`, `corpo`). Nome escrito à mão e conferido (regras/npc-personagens.md).

## Itens

```
<lote>/
├── itens.json           um por item: nome, tipagem, faixa, descricao ("o que é"), arquivo, cartela/posição
├── cartelas/            pagina_NN_original.png
├── <tipagem>/           faixa_NN_<descricao>.png — 320×320 RGBA
└── ENTREGA.md
```

## Cenários, mapas, capas, ícones

```
<lote>/
├── entregas.json        um por imagem: id/nome do Local ou evento, arquivo, medida, prompt usado
├── finais/              no tamanho de regras/formatos.md (JPG/PNG/WebP conforme o tipo)
├── brutos/              o que a IA entregou, antes de ajustar
└── ENTREGA.md
```

## Antes de dizer "pronto"

- Toda ficha tem descrição validada (regras/fichas-nomes-descricoes.md) e todo arquivo citado existe.
- Recortes conferidos: 1 criatura inteira por arquivo, fundo transparente, sem pedaço do vizinho.
- `ENTREGA.md` lista o que ficou pendente (célula reprovada sem conserto, arte que precisa de olho humano).
