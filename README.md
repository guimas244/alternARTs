# alternARTs

Fábrica de arte do jogo **Techterra**, empacotada como plugin do Claude Code. A skill `criar-arte` planeja lotes,
escreve fichas e prompts, monta a fila para a IA de imagem e confere e recorta as cartelas: monstros, fusões,
personagens/NPCs (rosto e corpo), itens, cenários, mapas, capas e ícones.

Repositório privado. Só o dono (guimas244) e o Claude fazem commit; quem usa a skill só instala.

## Instalar (Claude Code)

1. Tenha acesso de leitura a este repositório no GitHub e credencial git funcionando na máquina:
   - HTTPS: `gh auth login` e depois `gh auth setup-git`; ou
   - SSH: chave carregada no `ssh-agent`, sem pedir senha.
2. No Claude Code:
   ```
   /plugin marketplace add guimas244/alternARTs
   /plugin install techterra-arte@alternarts
   ```
3. Python 3 com Pillow (`pip install pillow`) para os scripts de conferência e recorte.

## Atualizar

- Ligue a atualização automática em `/plugin` → **Marketplaces** → `alternarts` → **Enable auto-update**; ou
- manualmente: `/plugin marketplace update alternarts`.

O plugin não tem número de versão: cada commit no `main` é uma versão nova.

## Usar

Peça normalmente ("quero um lote de 8 cartelas de monstros de gelo", "faz fusões entre estes pares", "um lote de NPCs
nórdicos", "ícones de mapa para estes Locais"). A skill escolhe o modo, lê as regras e trabalha **na sua pasta de
trabalho** — nada é gravado dentro do plugin.

A geração das imagens acontece numa sessão separada da IA de imagem: a skill entrega o `PROMPT_<LOTE>.md` e a frase para
colar lá.

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
