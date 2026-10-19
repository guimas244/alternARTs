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

## Estrutura

```
.claude-plugin/marketplace.json          catálogo (1 plugin)
plugins/techterra-arte/
  .claude-plugin/plugin.json
  skills/criar-arte/
    SKILL.md                             entrada: escolhe o modo
    modos/                               um arquivo por tipo de arte
    regras/                              regras do jogo (estilo, fichas, formatos…)
    referencias/                         imagens aprovadas que vão anexadas (ver REFERENCIAS.md)
    templates/                           modelos de prompt e de contrato
    scripts/                             ferramentas (Python + Pillow)
    dados/                               dados de apoio (nomes já usados…)
```

## Testar localmente (dono)

```
claude --plugin-dir ./plugins/techterra-arte
claude plugin validate ./plugins/techterra-arte
```
