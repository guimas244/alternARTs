# alternARTs — regras para quem edita este repositório

Este repo é o plugin `techterra-arte` (skill `criar-arte`), a fábrica de arte do Techterra. Estudo de origem:
`techterra-online-backend/docs/estudo-artes-techterra.md` (repo do jogo).

## Decisões do dono (19/10/2026)

- **Repositório público (19/10/2026).** Nada de segredo, caminho pessoal ou dado de jogador aqui.
- **Só o dono (guimas244) e o Claude fazem commit.** Commit e push só com ordem explícita do dono na mensagem atual.
  Mensagens curtas, em português, sem `Co-Authored-By` de IA.
- **Arte gerada não entra aqui.** Só referências aprovadas (`skills/criar-arte/referencias/`). Uma arte gerada vira
  referência nova apenas quando o dono escolher — e ganha uma linha em `referencias/REFERENCIAS.md` com motivo e data.
- **Sem banco e sem produção.** A skill termina nas cartelas recortadas e nas fichas. Nada de credencial, DSN, alias ssh,
  URL de prod, UID ou caminho pessoal (`D:\…`, `C:\Users\…`) em arquivo deste repo.
- **Tamanhos por tipo** conforme `regras/formatos.md` (manter os já usados, sem unificar).
- **Claude Code:** sem `version` no `.claude-plugin/plugin.json` (cada commit é uma versão).
- **ChatGPT/Codex (alvo principal):** a cada mudança na skill, **subir o `version`** de
  `plugins/techterra-arte/.codex-plugin/plugin.json` (1.2.0 → 1.2.1 correção, 1.3.0 novidade) e a mesma versão na frase do menu de ajuda (SKILL.md §0), no mesmo commit, e dar
  push. Quem instalou pelo marketplace do GitHub atualiza com o ↻ da tela Plugins (ou reabrindo o app). O zip
  (`python empacotar_chatgpt.py`) é só para quem instalou por arquivo.

## Ao editar

- Scripts recebem a pasta de trabalho por argumento e nunca gravam dentro do plugin. Caminhos de referência no SKILL.md
  usam `${CLAUDE_SKILL_DIR}`.
- `SKILL.md` curto (roteador); o detalhe vai em `modos/` e `regras/`.
- Regra nova vale para todos os modos? `regras/`. Só para um tipo? `modos/<tipo>.md`.
- Imagem nova em `referencias/` só se o dono pedir; manter cada uma pequena (até ~2 MB).
