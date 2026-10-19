# templates/

Modelos usados pelos scripts e pelo Claude. **Não edite um modelo para um lote só**: copie para a pasta do lote (ou
deixe o script preencher). Placeholders entre chaves (`{TITULO}`, `{LOTE}`, `{SKILL}`…).

## Monstros e fusões (cartela 2x2)

| Modelo | Para quê | Quem usa |
|---|---|---|
| `CABECALHO_CARTELA.txt` | cabeçalho aprovado de todo prompt de cartela (técnica, rostos, tipagem dupla, POWER LADDER). Cópia fiel; o parágrafo FILL THE CELL é trocado pelo LAYOUT do diagrama | `scripts/preparar_fila.py` (lê; não copia) |
| `PROMPT_LOTE.md` | prompt da sessão de imagem: papel (só gera), fila, modos FAIXA/TODOS/TROCAS, geração, verificador, orçamento, conserto por avulsa, conferência, ONDE SALVAR | `scripts/preparar_fila.py` grava `PROMPT_<LOTE>.md` preenchido na pasta do lote |
| `CONTRATO-FICHAS.md` | contrato do agente de fichas para os 6 blocos (N, V, F, L, X, A); aponta para `regras/` em vez de repetir | o Claude copia para a pasta do lote (troca `{TITULO}`, `{LOTE}`, `{SKILL}`; apaga os blocos que o lote não tem) |
| `INSTRUCOES-AGENTE-FICHAS.md` | instruções curtas de cada agente de fichas (ler, não repetir, escrever só a sua parte, fechar, responder curto) | o Claude copia para a pasta do lote (troca `{TITULO}`, `{SKILL}`) |

Placeholders de `PROMPT_LOTE.md` (preenchidos por `preparar_fila.py`): `{TITULO}`, `{LOTE}`, `{TOTAL}` (cartelas),
`{MONSTROS}`, `{ULTIMA}`, `{PASTA_LOTE}` e `{PASTA_CARTELAS}` (absolutas), `{ARQUIVO_PROMPT}`, `{SKILL}`, `{TABELA}`,
`{FAIXAS}` (faixas de 4 cartelas), `{LISTA_FAIXAS}`, `{NUM_FAIXAS}`, `{PRIMEIRA_FAIXA}`, `{LEVAS}`, `{DESCRICAO_LEVA}`,
`{CONFERENCIA_BLOCOS}`.

Os outros modos (personagens, itens, cenários, mapas, capas, ícones) ganham modelos nas etapas seguintes.
