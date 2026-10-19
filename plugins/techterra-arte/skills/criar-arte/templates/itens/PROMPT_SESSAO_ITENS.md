# Sessão de imagem — itens: {LOTE} ({TOTAL_PAGINAS} cartela(s) 5x5)

> Arquivo **gerado** por `itens_montar_prompts.py`. Nomes, fichas e o texto de cada cartela já estão decididos.
> Você **só gera**: anexa, cola, gera, confere, salva onde está mandado e registra. **Proibido** criar ou alterar
> ficha, nome, descrição, prompt, `fila.json`, `itens.json` ou as referências, e proibido criar script que escreva
> qualquer um deles. Cartela fora da fila ou sem arquivo de prompt: pule e anote.
>
> Siga este roteiro nesta conversa ou numa nova (ChatGPT ou Codex, com ferramenta de imagem). Se esta mesma conversa
> preparou o lote, a partir daqui ela está na etapa de geração. Lote levado para outro ambiente (ex.: `.zip` extraído
> em `/mnt/data/<lote>` numa conversa nova do ChatGPT): use a pasta onde ele foi extraído no lugar da pasta abaixo e a
> pasta desta skill no seu ambiente nos comandos — a fila usa caminhos relativos.

## ONDE SALVAR (obrigatório)

Pasta do lote (trabalhe de dentro dela; os caminhos da fila são relativos a ela):

```text
{PASTA_LOTE}
```

| Arquivo (em `cartelas/`) | O que é |
|---|---|
| `pagina_NN_vK.png` + `pagina_NN_vK.prompt.txt` | cada tentativa (K = 1, 2, 3), inclusive as descartadas, com o prompt exato usado |
| `pagina_NN_original.png` | a tentativa escolhida, **cópia exata, sem nenhuma edição** |
| `pagina_NN.prompt.txt` | o prompt exato da tentativa escolhida |

Registros (em `validacao/`): `geracoes.json` (ou `geracoes_<x>-<y>.json` no modo FAIXA) — lista com
`{"pagina", "tentativa", "arquivo", "prompt", "escolhida", "simulacao": "OK|ATENCAO|REPROVADA", "problemas": [...]}`.
No fim, acrescente uma linha em `ENTREGAS.md` da pasta de trabalho (data, lote, pasta, cartelas geradas, pendências).

Nomes em minúsculas, sem acento, `_` entre palavras, números com dois dígitos. A cópia que fica no cache do gerador
**não é entrega**: copie sempre para o caminho acima. Texto em UTF-8 sem BOM.

## Como executar (cada cartela da fila, em ordem, sem parar entre elas)

1. Leia `fila.json`. Pule a cartela que já tem `cartelas/pagina_NN_original.png` (se a sessão cair, basta mandar a
   mesma frase de novo).
2. **Anexe as imagens de `anexos`, nesta ordem** (1ª estilo, 2ª diagrama da grade) e cole o conteúdo do arquivo de
   `prompt` **exatamente** como está, sem resumir nem traduzir. Se a ferramenta de imagem não alcançar um anexo, mostre
   ao usuário a lista, na ordem, e peça para ele anexar as imagens na conversa.
3. Gere em **1254 × 1254**, PNG com **fundo transparente de verdade**. Salve como `pagina_NN_vK.png` + `.prompt.txt`.
   Se o ambiente de código não enxergar a imagem gerada, peça ao usuário para baixá-la e reenviá-la por upload.
4. **Confira no olho:** 25 objetos em 5×5; ordem igual à lista do prompt (a ordem dá o nome de cada recorte; a tabela
   de conferência abaixo diz o que é cada célula); nenhum texto; fundo sem xadrez pintado; o diagrama não aparece
   desenhado; nenhuma peça com cabo, formato de gente ou criatura dentro; faixa alta mais elaborada, não maior.
5. **Simule o recorte** (não grava nada):

   ```text
   python "{SKILL}/scripts/recortar_grade.py" "{PASTA_LOTE}" --pagina N --simular
   ```

   Para simular uma tentativa antes de escolhê-la: `python "{SKILL}/scripts/recortar_grade.py" "cartelas/pagina_NN_vK.png" --simular`.
   OK ou ATENÇÃO servem. Objeto um pouco grande que não encosta no vizinho está aprovado.
6. **Refazer só por erro real:** quantidade errada (célula vazia ou objeto a mais), fundo opaco ou xadrez pintado
   (REPROVADA na página), texto na imagem, objeto de gente (cabo, luva, torso), diagrama desenhado, objeto cortado na
   borda. Refaça **do zero** com o mesmo prompt — a única edição permitida é acrescentar no fim uma frase de correção
   (ex.: `Previous attempt failed: the layout diagram was drawn into the image. The background must be fully
   transparent; never draw the grey squares or the pink lines.`), salvando como `_v2`. **Nunca edite a imagem.**
   No máximo 3 imagens por cartela; se uma ou duas células ainda falharem, registre quais e siga (viram avulsa depois).
7. Copie a tentativa escolhida para `pagina_NN_original.png` e o prompt para `pagina_NN.prompt.txt`; registre.
8. Ao terminar a fila: **pare** e responda com a pasta do lote num bloco de código e a lista de pendências.
   Não recorte, não aprove arte (quem aprova é o dono) e não suba nada.

## Modos

- **Piloto:** só as cartelas que a mensagem mandar; pare e espere o dono julgar.
- **FAIXA** (normal): "faça as cartelas X–Y" — só elas, em ordem, pulando as que já têm original; registro com sufixo `_<x>-<y>`.
- **TODOS:** uma sessão coordena as faixas (se houver subagentes, abre um trabalhador por faixa, mandando ler este
  mesmo arquivo; sem subagentes — o normal no ChatGPT —, faz as faixas em sequência, ela mesma); só ela junta os
  registros no fim.

## Mapa das cartelas

{MAPA}

## Tabela de conferência (o que cada célula é — não vai no prompt)

{CONFERENCIA}
