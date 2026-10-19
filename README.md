# alternARTs

Fábrica de arte do jogo **Techterra**. A skill `criar-arte` (formato aberto de skills: pasta com `SKILL.md`) planeja
lotes, escreve fichas e prompts, **gera as cartelas** e confere e recorta: monstros, fusões, personagens/NPCs (rosto e
corpo), itens, cenários, mapas, capas e ícones.

**Alvo principal: ChatGPT** — é onde as imagens são geradas. Também funciona no Codex e no Claude Code (este só prepara;
não gera imagem). Detalhe de cada ambiente: `plugins/techterra-arte/skills/criar-arte/regras/ambiente.md`.

Repositório público. Só o dono (guimas244) e o Claude fazem commit; quem usa a skill só instala.

## Instalar no ChatGPT (app desktop) — recomendado

1. Na tela **Plugins** do app: **Adicionar → Adicionar marketplace**.
2. **Origem:** `guimas244/alternARTs` · **Referência do Git:** `main` · **Caminhos esparsos:** vazio → **Adicionar
   marketplace**.
3. Em **Explorar diretório** (ou na aba **Pessoais**), escolha o catálogo **"alternARTs — arte do Techterra"** e instale
   o plugin **Arte Techterra**.
4. Confira em **Habilidades** se apareceu `criar-arte`. Teste: "criar-arte: ajuda" ou "quero um lote piloto de 1
   cartela de monstros novos de gelo" (roteiro em "Primeiro lote", abaixo).

**Atualizar:** não precisa reinstalar. Quando a skill mudar no GitHub, clique no **↻** da tela Plugins (ou reabra o
app). A versão do plugin aparece em `plugins/techterra-arte/.codex-plugin/plugin.json`.

**Alternativa por arquivo** (se o marketplace não estiver disponível no seu ChatGPT): gere o zip com
`python empacotar_chatgpt.py` (sai em `dist/criar-arte.zip`) e envie em Skills/Habilidades → Upload. Nesse caso, cada
atualização exige enviar o zip de novo.

## Instalar no Codex (linha de comando)

```
codex plugin marketplace add guimas244/alternARTs
```

Atualizar: `codex plugin marketplace upgrade alternarts`.

## Instalar no Claude Code

```
/plugin marketplace add guimas244/alternARTs
/plugin install techterra-arte@alternarts
```

Atualizar: ligue a atualização automática em `/plugin` → **Marketplaces** → `alternarts`, ou rode
`/plugin marketplace update alternarts`. O Claude Code só prepara (não gera imagem).

Para os scripts de conferência e recorte, em qualquer ambiente com Python local: `pip install pillow`.

## Usar

Peça normalmente ("quero um lote de 8 cartelas de monstros de gelo", "faz fusões entre estes pares", "um lote de NPCs
nórdicos", "ícones de mapa para estes Locais"). A skill escolhe o modo, lê as regras e trabalha **na sua pasta de
trabalho** — nada é gravado dentro do plugin.

No ChatGPT e no Codex, a própria conversa gera as imagens seguindo o `PROMPT_<LOTE>.md`. No Claude Code, a skill entrega
o `PROMPT_<LOTE>.md` e a frase para colar no ChatGPT/Codex.

## Primeiro lote (para quem está começando)

Comece pequeno: **1 cartela de 4 monstros novos (bloco N)**, sem artes de origem. Cada passo é feito pelo Claude com a
skill; você só aprova o plano, abre a sessão de imagem e julga o resultado. `<lote>` é uma pasta sua, fora do plugin.

1. **Pedido:** "quero um lote piloto de 1 cartela de monstros novos de gelo".
2. **Plano:** o Claude mostra a tabela das 4 células (tier, tipos, leitura); você aprova; ele grava `<lote>/plano.json`.
3. **Entrada:** `montar_entrada.py <lote>` → `entrada.json` e as referências copiadas para o lote.
4. **Fichas (1 parte):** o Claude escreve `fichas_claude/parte_A.json` e fecha com
   `compor_fichas.py <lote> fichas_claude/parte_A.json` até sair **OK**.
5. **Fila:** `preparar_fila.py <lote>` (ensaio) e `preparar_fila.py <lote> --gravar` → `prompts/`, `fila.json` e
   `PROMPT_<LOTE>.md`.
6. **Sessão de imagem:** numa sessão nova, aberta dentro de `<lote>`, cole a frase que a skill entregar
   (`Leia e execute <lote>/PROMPT_<LOTE>.md — TODOS`). Ela gera a cartela e a confere com `checa_enquadramento.py`.
7. **Recortar:** `recortar_cartela.py <lote>` → `recortes/` (512×512) e `recortes/_visao_geral.png` para olhar.
8. **Entregar:** `montar_entrega.py <lote>` → `cadastro.json` e `ENTREGA.md` com as pendências.

Os scripts ficam em `skills/criar-arte/scripts/` (lista e comandos completos em
[scripts/LEIA-ME.md](plugins/techterra-arte/skills/criar-arte/scripts/LEIA-ME.md)); o Claude chama cada um com o
caminho da skill.

**O que você precisa fornecer** (a skill não tem banco nem acervo do jogo):

- **artes de origem** em `<lote>/artes/` — pais de fusão, monstro original de uma variação, antecessor de uma evolução,
  personagem a atualizar (PNG, de preferência com fundo transparente);
- **listas de nomes de NPC** (quem são as pessoas do lote);
- **2 ou 3 artes do próprio jogo** como referência de estilo para capas de evento/expedição/raid;
- para cenários e mapas, a descrição do mapa e dos Locais (nome, marco, vizinhos).

## Estrutura

```
.claude-plugin/marketplace.json          catálogo (1 plugin)
plugins/techterra-arte/
  .claude-plugin/plugin.json
  skills/criar-arte/
    SKILL.md                             entrada: escolhe o modo
    modos/                               um arquivo por tipo de arte (monstros, fusoes, personagens, itens,
                                         cenarios, mapas, capas, icones)
    regras/                              regras do jogo (estilo, fichas, formatos…)
    referencias/                         imagens aprovadas que vão anexadas (ver REFERENCIAS.md)
    templates/                           modelos de prompt e de contrato
      (raiz)                             monstros/fusões: cabeçalho da cartela, PROMPT_LOTE, contrato das fichas
      npc/  itens/  cenarios/  mapas/  capas/  icones/
    scripts/                             ferramentas (Python + Pillow) — ver scripts/LEIA-ME.md
      monstros/fusões                    montar_entrada, ver_celulas, compor_fichas, valida_fichas, preparar_fila,
                                         checa_enquadramento, recortar_cartela, montar_entrega
      personagens/NPC                    npc_montar_prompts, npc_recortar
      itens e ícones                     itens_montar_prompts, recortar_grade
      cenários, mapas, capas             fundos_normalizar, capas_converter
      apoio                              comum.py, CONTRATO-INTERNO.md, test_recortar_grade.py
    dados/                               dados de apoio (nomes já usados…)
```

## Testar localmente (dono)

```
claude --plugin-dir ./plugins/techterra-arte
claude plugin validate ./plugins/techterra-arte
```
