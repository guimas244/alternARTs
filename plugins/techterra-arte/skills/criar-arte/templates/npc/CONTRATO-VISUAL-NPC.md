# Contrato — texto de imagem das pessoas ({TITULO})

<!-- Template: `npc_montar_prompts.py <lote> --contrato` grava este arquivo como <lote>/CONTRATO-VISUAL.md, com os
     caminhos trocados. A sessão do Claude diz a cada agente a LETRA e as páginas dele. -->

Você escreve o `visual` (a linha da imagem) de cada pessoa das **suas páginas** do roster. Você é dono **só** do
arquivo `visual/parte_<LETRA>.json`. Não mexa em mais nada: nem roster, nem prompts, nem imagens, nem arquivos de
outro agente, nem git. UTF-8 sem BOM, pt-BR.

- Pasta do lote: `{PASTA_LOTE}`
- Entrada: `roster.json` (as pessoas das suas páginas: nome, gênero, idade, papel, subtipo e o que foi sorteado) e
  `tema.json`.
- **Leia antes (obrigatório):** `{SKILL}/regras/npc-personagens.md` §6 a §10 — é a regra; este contrato só resume o que
  o validador cobra. Se houver piloto aprovado em `prompts/pagina_001.txt`…`pagina_004.txt`, leia também: é o tom e o
  nível de detalhe (não copie frases dele).
- **Leia as outras partes** já escritas em `visual/` antes de escrever a sua (agentes em paralelo repetem a mesma ideia).

## Saída

`visual/parte_<LETRA>.json`: lista JSON, na ordem do roster, `{"nome": "<nome exato do roster>", "visual": "<uma linha>"}`.

## A linha (fórmula da regra §6; uma linha só, **750 a 980 caracteres**)

```text
cria a|o <Nome>, <idade> anos, <papel>. Beleza de top model <subtipo>, <2 adjetivos do temperamento>: pele <pele>,
cabelo <cor> <corte>, olhos <cor> <forma> e vivos (só a cor da íris, sem brilho) <maquiagem dos olhos>, <2–3 traços
do rosto>; <marca de estilo 1 com LADO>, <marca de estilo 2 com LADO>. <corpo e postura>. <roupa: 3–5 peças com tecido,
corte e cor>; <N por extenso> prisions <cor> <onde ficam>. Expressão <concreta, ligada ao temperamento>.
```

- Homem: `Beleza de modelo masculino <subtipo>`, com a barba escrita.
- Nome, idade, papel e subtipo **exatamente** como no roster. Se o roster trouxer `olho`, `cabelo` e `prisions`,
  escreva a cor igual, letra por letra.

## O que o validador recusa (`npc_montar_prompts.py`)

| Cobra | Regra |
|---|---|
| abertura | começa com `cria a <Nome>, <idade> anos, ` (mulher) ou `cria o …` (homem) |
| tamanho | 750–980 caracteres, sem quebra de linha |
| números | **nenhum algarismo além da idade** (nada de "Tier N", medidas, quantidades em algarismo) |
| olhos | a frase literal `vivos (só a cor da íris, sem brilho)` |
| subtipo | `Beleza de top model <subtipo>` / `Beleza de modelo masculino <subtipo>` |
| LADO | pelo menos duas marcas com ESQUERDO/ESQUERDA/DIREITO/DIREITA em MAIÚSCULAS |
| prisions | `<duas\|três\|quatro> prisions <cor>` (a do roster, se houver) |
| expressão | a palavra "Expressão" com algo concreto depois |
| mulher | tom meigo/sensual (meiga, doce, delicada, romântica, sensual ou feminina) |
| texto em objeto | "escrito" só como "sem nada escrito" |
| palavras proibidas (fora do nome e do papel) | cicatriz, olheira, ruga, cansado, desgrenhado; brilhante, luminoso, neon, reluzente, refletivo; magia, mago, aura, runa, cibernética; arma, espada, machado, adaga, faca, armadura (salvo `"arma": true` na pessoa); pele de animal; monstro, bicho, criatura; viking, camponês; nudez, lingerie, transparência; Narraris; "Tier" |

E na página/lote: 2 mulheres + 1 homem, nomes únicos, sem diacrítico estrangeiro, cor de olho e estilo de roupa sem
repetir na página; aviso para expressões que começam com as mesmas três palavras.

## Sem molde (o validador não pega; o revisor cruzado pega)

- Na mesma página: silhueta, comprimento de roupa e penteado diferentes; nenhuma página monocromática.
- A mesma marca de estilo no máximo 4 vezes a cada 36 pessoas; varie calçado, acessório e lugar da prision.
- Lote por tipagem ou faixa: objeto-assinatura da tipagem nunca repetido nas pessoas dela (regra §10).
- Não copie peças marcantes de personagens existentes nem frases do piloto.
- A peça-chave do roster é a roupa principal e tem de aparecer; a paleta dá as duas cores dominantes.
- Mulheres: regra §6 "Mulheres" (rosto delicado, postura graciosa, roupa feminina, expressão doce/quente; nunca
  "machona", nunca terno quadrado, jaqueta técnica, calça cargo ou coturno).

## Conferência

Rode até dar **0 erros** (os erros das pessoas de outras partes não aparecem):

```
python "{SKILL}/scripts/npc_montar_prompts.py" "{PASTA_LOTE}" --parte visual/parte_<LETRA>.json
```

Não rode sem `--parte` nem com `--gravar`. Responda no fim só: quantos visuais, quantos erros restantes e qualquer
linha do roster que achou incoerente (papel × roupa que brigam, nome que não casa com o subtipo).
