# alternARTs — regras para quem edita este repositório

Este repo é o plugin `techterra-arte` (skill `criar-arte`), a fábrica de arte do Techterra. Estudo de origem:
`techterra-online-backend/docs/estudo-artes-techterra.md` (repo do jogo).

## Decisões do dono (19/10/2026)

- **Só o dono (guimas244) e o Claude fazem commit.** Commit e push só com ordem explícita do dono na mensagem atual.
  Mensagens curtas, em português, sem `Co-Authored-By` de IA.
- **Arte gerada não entra aqui.** Só referências aprovadas (`skills/criar-arte/referencias/`). Uma arte gerada vira
  referência nova apenas quando o dono escolher — e ganha uma linha em `referencias/REFERENCIAS.md` com motivo e data.
- **Sem banco e sem produção.** A skill termina nas cartelas recortadas e nas fichas. Nada de credencial, DSN, alias ssh,
  URL de prod, UID ou caminho pessoal (`D:\…`, `C:\Users\…`) em arquivo deste repo.
- **Tamanhos por tipo** conforme `regras/formatos.md` (manter os já usados, sem unificar).
- **Sem `version`** no `plugin.json`: cada commit é uma versão.

## Ao editar

- Scripts recebem a pasta de trabalho por argumento e nunca gravam dentro do plugin. Caminhos de referência no SKILL.md
  usam `${CLAUDE_SKILL_DIR}`.
- `SKILL.md` curto (roteador); o detalhe vai em `modos/` e `regras/`.
- Regra nova vale para todos os modos? `regras/`. Só para um tipo? `modos/<tipo>.md`.
- Imagem nova em `referencias/` só se o dono pedir; manter cada uma pequena (até ~2 MB).
