# Modo: Personagens e NPCs (rosto + corpo)

- **Entra:** o tema do lote (povo, região ou mistura de etnias) e quantas pessoas; ou o personagem a atualizar.
- **Sai:** `recortes/pagina_NNN_colC_rosto.png` (512²) + `..._corpo.png` (512×1024) + `fichas.json` (regras/entrega.md).
- **A regra é** [../regras/npc-personagens.md](../regras/npc-personagens.md) (método Lote 09, aprovado em 09/10/2026).
  Este arquivo só diz **como produzir**; leia a regra antes de escrever o roster.
- Tamanhos: [../regras/formatos.md](../regras/formatos.md). Anexos: [../referencias/REFERENCIAS.md](../referencias/REFERENCIAS.md).
  Sessões e onde salvar: [../regras/fluxo-sessoes.md](../regras/fluxo-sessoes.md).

Scripts (Python 3 + Pillow; confira `python -c "import PIL"`), sempre com a pasta do lote como argumento:

```
python "${CLAUDE_SKILL_DIR}/scripts/npc_montar_prompts.py" <lote> [--gravar | --parte visual/parte_A.json | --contrato]
python "${CLAUDE_SKILL_DIR}/scripts/npc_recortar.py" <lote> [--paginas 1,3]
```

## Pasta do lote (dentro da pasta de trabalho do usuário, nunca na skill)

```
<lote>/
├── tema.json                 traço e moda do preâmbulo (você escreve)
├── roster.json               páginas e pessoas (você escreve)
├── nomes_npc_existentes.json lista de nomes de NPC do jogo (o USUÁRIO fornece; opcional, mas avise se faltar)
├── CONTRATO-VISUAL.md        contrato dos agentes (gerado por --contrato)
├── visual/parte_<L>.json     linhas escritas pelos agentes [{"nome", "visual"}]
├── prompts/pagina_NNN.txt    preâmbulo + cabeçalho + 3 colunas (gerado; _vK quando refeito)
├── referencias/              os 4 anexos fixos copiados da skill (gerado)
├── fila.json                 fila da sessão de imagem (gerado)
├── PROMPT_IMAGEM_<LOTE>.md   prompt da sessão de imagem (gerado de templates/npc/PROMPT_IMAGEM_NPC.md)
├── paginas/pagina_NNN.png    páginas 1254² (sessão de imagem; _v1 = 1ª tentativa, _ruimN = reprovada)
├── validacao/                geracoes_<x>-<y>.json (sessão de imagem), recortes.json (recortador)
├── recortes/                 rosto + corpo por coluna (gerado por npc_recortar.py)
├── fichas.json               uma ficha por pessoa, com rosto/corpo (gerado/atualizado pelo recortador)
└── ENTREGA.md                resumo (você escreve)
```

### `tema.json`

```json
{"lote": "nordicos_eslavos", "titulo": "Nórdicos e Eslavos", "variante": "tema",
 "traco": "<TEMA-TRAÇO em inglês>", "moda": "<TEMA-MODA em inglês>", "traco_curto": "traço nórdico e eslavo",
 "tirar_snow": false}
```

- `variante`: `tema` (um povo/região: `traco`, `moda` e `traco_curto` obrigatórios) ou `multietnico` (cada pessoa com o
  traço do próprio subtipo; os três textos têm padrão e podem ser sobrescritos).
- O exemplo aprovado, o molde dos dois trechos e a variante multiétnica estão em
  [../templates/npc/PREAMBULO_NPC.md](../templates/npc/PREAMBULO_NPC.md). O resto do preâmbulo **não muda**.

### `roster.json`

```json
{"lote": "nordicos_eslavos",
 "paginas": [
  {"pagina": 1, "pessoas": [
   {"nome": "Zlata Korvenka", "genero": "F", "idade": 25, "papel": "cantora de uma taverna de inverno",
    "subtipo": "eslava", "descricao": "lore curta, sem país da Terra",
    "pele": "clara de porcelana", "cabelo": "loiro-platinado", "cabelo_corte": "muito longo em ondas soltas",
    "olho": "azul-gelo quase branco", "corpo": "esbelta, cintura fina", "temperamento": "meiga e sedutora",
    "estilo_roupa": "veludo de salão de inverno", "peca_chave": "vestido midi de veludo de ombros à mostra",
    "paleta": ["azul-noite", "creme"], "prisions": {"n": 3, "cor": "azul-claras"}},
   {"…": "mais 2 pessoas, na ordem das colunas"}]}
 ]}
```

| Campo | |
|---|---|
| `pagina` | inteiro único (vira `pagina_NNN`); páginas 1–4 = piloto |
| `pessoas` | exatamente 3, na ordem das colunas, **2 mulheres + 1 homem** |
| obrigatórios | `nome` (escrito à mão, regra §10), `genero` (`F`/`M`), `idade` (≥ 18 neste método), `papel` (sem número nem "Tier"), `subtipo` (no gênero da pessoa: "eslava", "ucraniano") |
| validados se vierem | `olho`, `cabelo` (a cor tem de aparecer igual na linha), `prisions` `{n: 2–4, cor}`, `estilo_roupa` e `olho` sem repetir na página, `arma: true` (só soldado/bandido/mercenário: libera a palavra arma) |
| livres (o sorteio que o agente usa) | `pele`, `cabelo_corte`, `corpo`, `barba` (homem), `temperamento`, `peca_chave`, `paleta`, `estilo_roupa` |
| `descricao` | lore curta da pessoa; vai para a `fichas.json` (obrigatória na entrega) |
| `visual` | a linha da imagem; pode vir aqui ou (com agentes) em `visual/parte_<L>.json` |
| página: `rosto_ref` | refação fiel: `{"coluna", "arquivo", "dna"}` (ver Refação fiel) |
| página: `tipo: "atualizar"` | atualizar personagem existente (ver abaixo) |

## Passo a passo

1. **Tema.** Combine com o usuário o povo/região (ou multiétnico), quantas páginas e a proporção de olhos
   (padrão 70% fantasia / 30% natural, regra §9). Peça a lista de nomes de NPC existentes. Escreva `tema.json`.
2. **Roster.** Escreva `roster.json` seguindo a regra §9–§10: peça-chave sorteada **dentro do papel**, papéis que
   combinam com mulheres meigas, nomes à mão por subtipo, 3 estilos e 3 cores de olho diferentes por página, nada de
   molde de etnia. Rode `npc_montar_prompts.py <lote>` para pegar erro de roster cedo (as linhas ainda faltam).
3. **Piloto (4 páginas).** Escreva você mesmo as 12 linhas das páginas 1–4 (no `visual` do roster), valide, rode com
   `--gravar` e mande o usuário abrir a sessão de imagem com a frase **PILOTO** do `PROMPT_IMAGEM_<LOTE>.md`. O dono
   julga o traço; aprovado, crie `prompts/PILOTO_APROVADO.txt` (sem ele a sessão não passa da página 4).
4. **Texto visual por agentes** (lote grande). Rode `--contrato`. Divida as páginas restantes em partes de até 12
   páginas, uma LETRA por agente; cada agente lê `CONTRATO-VISUAL.md` + a regra, escreve só `visual/parte_<L>.json` e
   roda `--parte visual/parte_<L>.json` até 0 erros. Depois, um **revisor cruzado** lê todas as linhas juntas (marca de
   estilo repetida, expressões iguais, objeto-assinatura repetido, papel × roupa) antes de liberar.
5. **Montar a fila.** `npc_montar_prompts.py <lote> --gravar`: valida tudo (linha 750–980 caracteres, nenhum número
   além da idade, frase literal dos olhos, LADO, prisions, palavras proibidas, 2F+1M, nomes únicos) e só grava sem
   erro: `prompts/`, `referencias/`, `fila.json`, `PROMPT_IMAGEM_<LOTE>.md`. **A fila tem de estar cheia antes de
   mandar gerar.** Página que já tem imagem nunca é sobrescrita.
6. **Sessão de imagem.** O usuário abre uma ou mais sessões com as frases do `PROMPT_IMAGEM_<LOTE>.md` (FAIXA x-y em
   paralelo, ou TODOS). Uma geração por página; no máximo 1 refação, só por erro grave. Você **não** gera imagem.
7. **Conferir.** Abra as páginas (Read) com a conferência da regra §10. Página que precisa voltar: renomeie para
   `paginas/pagina_NNN_ruimN.png`, ajuste a linha no roster/parte e rode `--gravar` — sai `prompts/pagina_NNN_vK.txt`
   e a página volta para a fila sozinha. Beleza "menor" ou detalhe: anote para o dono, não refaça.
8. **Recortar.** `npc_recortar.py <lote>` (ou `--paginas 1,3`): rosto 512² + corpo 512×1024 por coluna, separados pela
   linha vazia entre busto e corpo; corpo = só a mancha ligada aos pés (colunas que se tocam são separadas); fiapos
   < 3% saem do rosto. Leia os avisos (`validacao/recortes.json`): página opaca, corte sem vão, corpo passando da
   coluna, pés altos. Abra os recortes avisados antes de entregar.
9. **Entrega.** `fichas.json` sai do roster com `rosto`/`corpo` preenchidos; complete as `descricao` que faltarem e
   rode o recortador de novo (ele preserva o que já está na ficha). Escreva `ENTREGA.md` (quantas, quais, pendências,
   o que precisa de olho humano) e acrescente a linha no `ENTREGAS.md` da pasta de trabalho.

## Atualizar personagem que já existe

Fluxo próprio, com a arte atual como referência (não embeleza): [../templates/npc/ATUALIZAR_PERSONAGEM.md](../templates/npc/ATUALIZAR_PERSONAGEM.md).
O rosto e o corpo atuais **o usuário fornece**. A página entra no roster com `"tipo": "atualizar"` e `"anexos"`; o
prompt `prompts/atualizar_NNN.txt` é escrito à mão; a fila, o recorte e a ficha seguem os mesmos scripts.

## Refação fiel (mesma pessoa do lote, de novo)

Na página do roster, `"rosto_ref": {"coluna": N, "arquivo": "referencias/rosto_<slug>.png", "dna": "<DNA do rosto em
inglês>"}`: o tile do rosto aprovado vira o 5º anexo e a página ganha `Column N: same person as reference image 5.
Face DNA: …`. As outras colunas pegam os próximos pendentes. Detalhe em `ATUALIZAR_PERSONAGEM.md` e na regra §11.

## Limites

- O validador não pega molde (marca repetida a cada 36, objeto-assinatura por tipagem, silhueta igual na página): é o
  revisor cruzado. Também não confere país da Terra fora do `subtipo` nem nome "quase igual" (só primeiro nome igual).
- Nome existente só é checado com `nomes_npc_existentes.json`; sem ele, só dentro do lote.
- Lotes de faixa baixa (crianças) estão **fora** deste método (regra §8): não use o preâmbulo de beleza.
