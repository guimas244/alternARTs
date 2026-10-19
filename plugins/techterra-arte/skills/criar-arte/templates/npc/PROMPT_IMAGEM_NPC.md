# Sessão de IMAGEM — {TITULO} (personagens/NPC)

<!-- Template: o scripts/npc_montar_prompts.py --gravar troca os marcadores entre chaves (PASTA_LOTE, SKILL, LOTE,
     TITULO, TOTAL, PRIMEIRA, ULTIMA) e grava como <lote>/PROMPT_IMAGEM_<LOTE>.md. Regras: regras/npc-personagens.md
     e regras/fluxo-sessoes.md. Não edite o arquivo gerado à mão: mude o template ou o roster e rode de novo. -->

Siga este roteiro nesta conversa ou numa nova (ChatGPT ou Codex, com ferramenta de imagem), com **uma** destas
frases:

| Modo | Frase |
|---|---|
| Piloto | `Leia {PASTA_LOTE}/PROMPT_IMAGEM_{LOTE}.md e faça o PILOTO.` |
| Faixa (normal) | `Leia {PASTA_LOTE}/PROMPT_IMAGEM_{LOTE}.md e faça a FAIXA 005-016.` |
| Todos | `Leia {PASTA_LOTE}/PROMPT_IMAGEM_{LOTE}.md e faça TODOS.` |

Várias sessões de FAIXA podem rodar ao mesmo tempo, cada uma com um intervalo diferente. Caiu? Mande a mesma frase de
novo: ela pula as páginas que já têm imagem. No ChatGPT, o normal é a própria conversa que preparou o lote fazer o
PILOTO e depois TODOS, com as faixas em sequência.

Lote levado para outro ambiente (ex.: `.zip` extraído em `/mnt/data/<lote>` numa conversa nova do ChatGPT): use a pasta
onde ele foi extraído no lugar da pasta do lote abaixo e a pasta desta skill no seu ambiente — a fila usa caminhos
relativos.

---

Você é uma sessão de IMAGEM do lote de personagens **{TITULO}** do TechTerra ({TOTAL} páginas, {PRIMEIRA} a {ULTIMA}).
Seu ÚNICO trabalho é gerar a imagem de cada página da sua faixa e salvá-la na pasta do lote.

**Proibido:** criar ou alterar ficha, nome, descrição, roster, prompt, `fila.json`, referências ou qualquer arquivo fora
de `paginas/` e `validacao/`; escrever script que escreva ficha ou prompt; recortar; cadastrar; mexer em banco, API ou
git. A sessão de imagem só anexa, cola, gera, confere, salva e registra. Se esta mesma conversa preparou o lote, a
partir daqui ela está na etapa de geração: roster e linhas estão fechados.

## PASTA DO LOTE

```
{PASTA_LOTE}
```

Todos os caminhos abaixo são relativos a essa pasta.

## MODOS

- **PILOTO:** gere só as páginas 001 a 004 e pare. O dono julga o traço antes de liberar o resto.
- **FAIXA x-y:** gere só as páginas de x a y, em ordem crescente. Nunca gere página fora da faixa: outra sessão cuida
  dela. Enquanto **não existir** `prompts/PILOTO_APROVADO.txt`, só as páginas 001 a 004 podem ser geradas: o resto da
  faixa espera, e você para avisando isso.
- **TODOS:** você coordena. Divida {PRIMEIRA}–{ULTIMA} em faixas de 12 páginas; se puder abrir trabalhadores, abra um por
  faixa mandando ler ESTE arquivo inteiro (sem resumir as regras) com a frase "faça a FAIXA x-y", reabra quem parar
  no meio, e só você junta os registros no fim. Sem trabalhadores, faça as faixas em sequência.

## FILA

- `fila.json` lista cada página: `prompt` (o arquivo do texto), `anexos` na ordem e onde salvar (`salvar`).
- O texto de cada página é o do campo `prompt` (normalmente `prompts/pagina_NNN.txt`; `prompts/atualizar_NNN.txt` em
  página de atualizar personagem). Se existir `pagina_NNN_v2.txt`, `_v3.txt`…, use o de número **maior**.
- **Pendente** = página da sua faixa que está na fila, tem o arquivo de prompt e **não** tem `paginas/pagina_NNN.png`.
- Página sem arquivo de prompt ou fora da fila: **pule e anote**, não improvise.
- Gere as pendentes em ordem crescente, direto até a última, sem parar entre elas e sem pedir confirmação.

## COMO GERAR CADA PÁGINA

1. Anexe os arquivos do campo `anexos` da página, **na ordem da fila** (o texto os chama de Reference 1, 2…).
   Na página normal são estes quatro:
   1. `referencias/estilo_pagina_1.png` (layout e técnica; nunca as pessoas dela)
   2. `referencias/prisions.png` (as prisions)
   3. `referencias/beleza_marta.png` (nível de beleza e acabamento, não o rosto)
   4. `referencias/beleza_elira.png` (idem)
   5. só quando a fila listar um 5º anexo (tile de rosto de uma refação fiel): ele, por último.
   Página de atualizar personagem traz outros anexos (rosto e corpo atuais primeiro): siga a fila.
   Se faltar um anexo em `referencias/`, pare e avise (quem copia é o preparo, a partir de
   `{SKILL}/referencias/personagens/`). Se o arquivo existe mas a ferramenta de imagem não o alcança, mostre ao
   usuário a lista dos anexos, na ordem, e peça para ele anexar as imagens na conversa.
2. Cole **exatamente** o texto do arquivo de prompt, inteiro, sem resumir, traduzir nem "melhorar".
3. Saída esperada: PNG **1254 × 1254** com fundo transparente de verdade (alfa real), 3 colunas, busto em cima e corpo
   inteiro embaixo.
4. Salve em `paginas/pagina_NNN.png`. A cópia que fica no cache do gerador **não é entrega**. Se o ambiente de código
   não enxergar a imagem gerada, peça ao usuário para baixá-la e reenviá-la por upload, e copie para esse caminho.

## UMA GERAÇÃO POR PÁGINA

- Gere a página **uma vez**, salve e vá para a próxima. Quem julga a beleza e o acabamento é o dono, depois.
- Refaça **no máximo 1 vez**, só por erro grave:
  a. não saíram 3 pessoas (em página de atualizar: a pessoa pedida), ou alguma ficou sem o busto em cima ou sem o
     corpo inteiro embaixo;
  b. o fundo veio todo opaco (cenário, cor chapada ou xadrez pintado na folha toda);
  c. há nudez ou lingerie.
- **Não é motivo para refazer:** rosto "menos bonito" que a referência, expressão, cor exata do olho ou do cabelo,
  peça de roupa diferente, marca do lado trocado, prision a mais ou a menos, vão pequeno entre busto e corpo, pé
  levemente cortado, sombra leve, algo encostando na linha da coluna. Anote e siga.
- Se refez: a primeira fica como `paginas/pagina_NNN_v1.png` e a segunda como `paginas/pagina_NNN.png`, do jeito que
  vier. Nunca faça uma terceira.
- A ferramenta recusou a página? Pule para a próxima e anote.
- Imagens `pagina_NNN_ruimN.png` foram reprovadas na conferência do preparo: não mexa nelas. Se a página ficou sem
  `pagina_NNN.png` por causa disso, ela está pendente de novo (com um prompt `_vK` novo): gere.

## CONFERÊNCIA RÁPIDA (anote; só os erros graves acima fazem refazer)

1. As três são bonitas de verdade, no nível das referências 3 e 4, cada uma de um subtipo.
2. Mulheres meigas, femininas e sensuais (nunca "machonas"); homem bonito e masculino.
3. Olhos na cor pedida, visíveis no busto e sem brilho.
4. Fundo transparente; vão vazio entre busto e corpo; nada cruza a coluna; os dois pés aparecem.
5. Mesma pessoa em cima e embaixo (rosto, cabelo, maquiagem, roupa, marcas do lado certo).
6. Roupa de moda como descrita, sem fantasia histórica nem roupa de camponês.
7. Só as prisions brilham. Nenhum texto, número, logo, monstro ou bicho.
8. Sensual sem ser vulgar: sem nudez, lingerie, transparência ou pose vulgar.

## ONDE SALVAR (obrigatório)

- Pasta absoluta: `{PASTA_LOTE}`
- Imagens: `paginas/pagina_NNN.png` (final) e `paginas/pagina_NNN_v1.png` (1ª tentativa, só se refez).
- Nomes: minúsculas, sem acento, `_` entre palavras, número com 3 dígitos.
- Registro da sua faixa: `validacao/geracoes_<x>-<y>.json` (PILOTO: `geracoes_piloto.json`; TODOS: um por faixa),
  lista de `{"pagina": N, "arquivo": "paginas/pagina_NNN.png", "geracoes": 1|2, "observacao": "ok" | "<o que anotou>"}`.
  Inclua as páginas puladas (`"arquivo": null`, com o motivo).
- Texto em UTF-8 sem BOM.

## NÃO FAÇA

- Não edite nada em `prompts/`, `referencias/`, `fila.json` nem fora de `paginas/` e `validacao/`.
- Não apague nenhuma imagem.
- Não reescreva o texto de uma página para ela passar: anote o problema.
- Não gere a mesma página 3 ou mais vezes atrás de perfeição.

## AO FINAL

Responda com uma tabela curta `página | gerações (1 ou 2) | observação` e a pasta absoluta num bloco de código.
