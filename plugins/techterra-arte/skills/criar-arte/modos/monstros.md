# Modo: Monstros (lote novo, evolução, variação, prodígio, humanoide, revitalização)

Fluxo completo de um lote de monstros, do pedido ao pacote de entrega. Fusões usam o mesmo fluxo com o
[modo fusões](fusoes.md). `{SKILL}` = a pasta desta skill (onde está o SKILL.md); `<lote>` = a pasta de trabalho do
lote (fora da skill; no ChatGPT web, `/mnt/data/<lote>`; no ChatGPT desktop, a pasta local). Ambiente (ChatGPT, Codex, Claude Code):
[../regras/ambiente.md](../regras/ambiente.md).

## 0. Plano do lote

1. Entenda o pedido. Se o criador deu uma **tipagem**, um **tema/referência** (ex.: filmes de terror) ou uma **imagem de
   referência**, monte o plano por [../regras/lotes-tematicos.md](../regras/lotes-tematicos.md).
2. Mostre ao criador uma tabela curta: cartelas × células (bloco, tier, tipos, humanoide, leitura de 1 linha). Ajuste até
   ele aprovar. Múltiplo de 4 (cartela sempre cheia).
3. Crie `<lote>/` e escreva `<lote>/plano.json` (formato em [../scripts/CONTRATO-INTERNO.md](../scripts/CONTRATO-INTERNO.md)).
   Variação/evolução de monstro existente: peça ao usuário as artes de origem (no ChatGPT, por upload) e salve em
   `<lote>/artes/`.

Blocos: `N` novo · `V` variação (mesma criatura em outro elemento) · `F` fusão de fusões · `L` prodígio (tema por cartela)
· `X`/`A` fusões (ver [fusoes.md](fusoes.md)).

### Personagens nomeados: releitura (padrão) ou homenagem

Pedido com personagens/figuras **nomeados** — ex.: *"Quero lotes criando humanoides: 1. Ghostface — do filme Pânico,
tipo fantasma; 2. Chucky — Brinquedo Assassino, docrates; …"* — é **`"fidelidade": "releitura"`** no plano: criatura
do Techterra (~25% referência / ~75% Techterra) em que só **1–2 âncoras de FORMA** (contorno do rosto/máscara,
silhueta, gesto ou objeto), traduzidas pelos tipos, deixam ver a referência numa segunda olhada; os dois tipos fazem o
resto (camada Techterra obrigatória e `classe` própria — regras/lotes-tematicos.md). Com "humanoides": 1 humanoide por item na forma real (sem estágio de objeto/bichinho), `tipo1` = o
tipo dado pelo usuário, `referencia_conteudo: {"descricao": ...}` na célula (o único lugar com o nome). O plano mostra,
por item, **"Criatura do Techterra"**, **"Âncoras de forma"** e **"Reinvenção pelos tipos"** e pergunta se o
equilíbrio está bom. **Sem imagem
do personagem por padrão** ("anexe só se as âncoras não bastarem"; se vier, `referencia_conteudo.arte` +
`"usar_imagem": true`). A ficha ganha `ancoras` e `reinvencao`; o prompt, o bloco `REIMAGINED CELLS`.

Só quando o usuário disser **"igual", "fiel", "idêntico"** aos personagens é `"fidelidade": "homenagem"`: traços
icônicos reconhecíveis à primeira vista (`tracos_iconicos`, bloco `HOMAGE CELLS`), imagem de cada personagem opcional em
`referencia_conteudo.arte`. Tema aberto sem nomes ("filmes de terror") continua `arquetipo`. Nunca o nome da figura em
ficha ou prompt; o plano traz o aviso de direito autoral. Detalhe: [../regras/lotes-tematicos.md](../regras/lotes-tematicos.md)
§Nível de fidelidade e §2.0.

### Linhas evolutivas

Toda evolução é célula `N` (regras em [../regras/fusoes.md](../regras/fusoes.md) §Evolução). Dois casos:

- **Linha nova dentro do lote** — o estágio aponta para a célula antecessora com `evolui_de: [cartela, linha, coluna]`
  (mesma cartela ou anterior). Ex.: *"lote com 4 linhas de 3 estágios de Gelo"*.
- **Evoluir monstro que já existe no jogo** — o usuário envia a arte do antecessor (salve em `<lote>/artes/`) e a
  célula leva `antecessor_externo: {nome, tier, tipo1, tipo2, descricao, arte, humanoide}`; ele aparece grande no
  quadrante da célula na prancha. Ex.: *"crie a evolução destes 3 monstros"* + as 3 artes.

Os dois são exclusivos na mesma célula; `evolucao_modo`/`level_requerido` são opcionais em qualquer um. O tier da
evolução nunca é menor que o do antecessor.

## 1. Entrada

```
python "{SKILL}/scripts/montar_entrada.py" <lote>
```

Gera `entrada.json` (células numeradas), `pais/`, as pranchas `referencias/cartela_NNN_pais.png` (V/F/X/A e N com
antecessor externo) e copia as
referências da skill para `<lote>/referencias/`. Corrija o plano até sair sem erro.

## 2. Fichas (por partes; em paralelo se houver subagentes)

1. Copie para `<lote>/` os modelos `{SKILL}/templates/CONTRATO-FICHAS.md` e `INSTRUCOES-AGENTE-FICHAS.md`, trocando
   `{TITULO}`, `{LOTE}` e `{SKILL}`.
2. Divida as cartelas em partes (ex.: 2 cartelas por parte, letras A, B, C…). Se o ambiente tiver subagentes, um agente
   por parte, em paralelo; senão (ChatGPT), escreva as partes em sequência, uma por vez. Cada parte vai só em
   `fichas_claude/parte_<L>.json` (`fichas_claude/` é o nome fixo da pasta das fichas, que os scripts leem), olhando
   `python "{SKILL}/scripts/ver_celulas.py" <lote> <cartelas>` e as pranchas, e fecha com:
   ```
   python "{SKILL}/scripts/compor_fichas.py" <lote> fichas_claude/parte_<L>.json
   ```
   (completa os campos fixos, monta o `visual` e valida; repetir até **OK**).
3. Revisão cruzada no fim, com todas as partes: `python "{SKILL}/scripts/valida_fichas.py" <lote>`. Em lote grande,
   releia as fichas contra as pranchas (membros, olhos, "base com enfeite", ideias repetidas) — com um agente revisor,
   se houver subagentes, ou você mesmo, numa passada só no fim.
4. Toda ficha tem **descrição de jogo** ([../regras/fichas-nomes-descricoes.md](../regras/fichas-nomes-descricoes.md)).

## 3. Fila, prompt e geração das imagens

```
python "{SKILL}/scripts/preparar_fila.py" <lote>            # ensaio
python "{SKILL}/scripts/preparar_fila.py" <lote> --gravar
```

Gera `monstros.json` (fichas integradas), `prompts/`, `fila.json` e `PROMPT_<LOTE>.md`. Depois:

- **No ChatGPT/Codex:** a própria conversa segue o `PROMPT_<LOTE>.md` (modo TODOS, faixas em sequência) e gera as
  cartelas. Daqui em diante as fichas e os prompts estão fechados: só gerar, medir o enquadramento, consertar por
  avulsa e registrar.
- **No Claude Code:** entregue ao usuário só a frase abaixo, com o caminho absoluto do `PROMPT_<LOTE>.md`, para colar
  numa conversa nova do **ChatGPT desktop** ou do Codex (os dois enxergam o disco: sem `.zip`, sem instruções extras —
  o roteiro já diz a pasta, os anexos, a conferência e onde salvar):

```
criar-arte: leia e execute <lote>/PROMPT_<LOTE>.md — TODOS
```

(ou `— FAIXA 001–004`, uma sessão por faixa). Só no **ChatGPT web** (sem acesso ao disco) o lote vai como `.zip`
anexado à conversa, extraído em `/mnt/data/<lote>`. Detalhe por ambiente: [../regras/ambiente.md](../regras/ambiente.md).

## 4. Depois da geração

1. Confira `cartelas/` e `validacao/` (cartelas "pendente de conserto", avulsas). Para refazer uma cartela já gerada:
   `preparar_fila.py <lote> --gravar --conserto N` e a geração no modo TROCAS ou avulsa.
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
   Pacote: [../regras/entrega.md](../regras/entrega.md). No ChatGPT web, entregue o lote como `.zip` (no desktop, a própria pasta)
   (`shutil.make_archive`).

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
