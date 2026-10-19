# Modo: Monstros (lote novo, evolução, variação, prodígio, humanoide, revitalização)

Fluxo completo de um lote de monstros, do pedido ao pacote de entrega. Fusões usam o mesmo fluxo com o
[modo fusões](fusoes.md). `{SKILL}` = `${CLAUDE_SKILL_DIR}`; `<lote>` = a pasta de trabalho do lote (fora da skill).

## 0. Plano do lote

1. Entenda o pedido. Se o criador deu uma **tipagem**, um **tema/referência** (ex.: filmes de terror) ou uma **imagem de
   referência**, monte o plano por [../regras/lotes-tematicos.md](../regras/lotes-tematicos.md).
2. Mostre ao criador uma tabela curta: cartelas × células (bloco, tier, tipos, humanoide, leitura de 1 linha). Ajuste até
   ele aprovar. Múltiplo de 4 (cartela sempre cheia).
3. Crie `<lote>/` e escreva `<lote>/plano.json` (formato em [../scripts/CONTRATO-INTERNO.md](../scripts/CONTRATO-INTERNO.md)).
   Variação/evolução de monstro existente: peça ao usuário as artes de origem e salve em `<lote>/artes/`.

Blocos: `N` novo · `V` variação (mesma criatura em outro elemento) · `F` fusão de fusões · `L` prodígio (tema por cartela)
· `X`/`A` fusões (ver [fusoes.md](fusoes.md)).

## 1. Entrada

```
python "{SKILL}/scripts/montar_entrada.py" <lote>
```

Gera `entrada.json` (células numeradas), `pais/`, as pranchas `referencias/cartela_NNN_pais.png` (V/F/X/A) e copia as
referências da skill para `<lote>/referencias/`. Corrija o plano até sair sem erro.

## 2. Fichas (agentes em paralelo)

1. Copie para `<lote>/` os modelos `{SKILL}/templates/CONTRATO-FICHAS.md` e `INSTRUCOES-AGENTE-FICHAS.md`, trocando
   `{TITULO}`, `{LOTE}` e `{SKILL}`.
2. Divida as cartelas em partes (ex.: 2 cartelas por agente, letras A, B, C…). Cada agente escreve só
   `fichas_claude/parte_<L>.json`, olhando `python "{SKILL}/scripts/ver_celulas.py" <lote> <cartelas>` e as pranchas, e
   fecha com:
   ```
   python "{SKILL}/scripts/compor_fichas.py" <lote> fichas_claude/parte_<L>.json
   ```
   (completa os campos fixos, monta o `visual` e valida; repetir até **OK**).
3. Revisão cruzada no fim, com todas as partes: `python "{SKILL}/scripts/valida_fichas.py" <lote>`. Em lote grande, um
   agente revisor lê as fichas contra as pranchas (membros, olhos, "base com enfeite", ideias repetidas).
4. Toda ficha tem **descrição de jogo** ([../regras/fichas-nomes-descricoes.md](../regras/fichas-nomes-descricoes.md)).

## 3. Fila e prompt da sessão de imagem

```
python "{SKILL}/scripts/preparar_fila.py" <lote>            # ensaio
python "{SKILL}/scripts/preparar_fila.py" <lote> --gravar
```

Gera `monstros.json` (fichas integradas), `prompts/`, `fila.json` e `PROMPT_<LOTE>.md`. Entregue ao usuário a frase para
colar na IA de imagem (aberta **dentro de `<lote>`**):

```
Leia e execute <lote>/PROMPT_<LOTE>.md — TODOS
```

(ou `— FAIXA 001–004`, uma sessão por faixa). A sessão só gera, mede o enquadramento, conserta por avulsa e registra.

## 4. Depois da geração

1. Confira `cartelas/` e `validacao/` (cartelas "pendente de conserto", avulsas). Para refazer uma cartela já gerada:
   `preparar_fila.py <lote> --gravar --conserto N` e a sessão de imagem no modo TROCAS ou avulsa.
2. Recorte:
   ```
   python "{SKILL}/scripts/recortar_cartela.py" <lote>
   ```
   Gera `recortes/NN_tTT_<slug>.png` (512² RGBA), aplica as avulsas por cima e monta `recortes/_visao_geral.png` — abra
   a visão geral e confira.
3. Entrega:
   ```
   python "{SKILL}/scripts/montar_entrega.py" <lote>
   ```
   Valida (descrição em toda ficha, recorte de toda célula) e escreve `cadastro.json` (corpo sugerido) e `ENTREGA.md`.
   Pacote: [../regras/entrega.md](../regras/entrega.md).

## Regras deste modo

[../regras/estilo.md](../regras/estilo.md) · [../regras/tipagens.md](../regras/tipagens.md) ·
[../regras/fichas-nomes-descricoes.md](../regras/fichas-nomes-descricoes.md) ·
[../regras/cartela-e-enquadramento.md](../regras/cartela-e-enquadramento.md) ·
[../regras/humanoides.md](../regras/humanoides.md) · [../regras/fusoes.md](../regras/fusoes.md) (evolução, variação,
revitalização) · [../regras/restricoes.md](../regras/restricoes.md) · [../regras/fluxo-sessoes.md](../regras/fluxo-sessoes.md).

Centrais: exatamente 4 por cartela; 1–2 humanoides por cartela de lote inédito; cor da mistura dos 2 tipos (ciano só
elétrico); rosto único; escada de poder (ameaça, não tamanho); tamanho vem da lore; descrição sem aparência; orçamento de
3 imagens por cartela.

**Revitalização** (redesenhar arte existente mantendo o estilo dela): não usa as referências de estilo da skill — só a
folha base com as originais (no máximo 2 anexos). Monte a folha à mão e escreva o prompt a partir de
`templates/PROMPT_LOTE.md`, tirando os anexos de estilo.

Tamanhos: [../regras/formatos.md](../regras/formatos.md). Anexos: [../referencias/REFERENCIAS.md](../referencias/REFERENCIAS.md).
