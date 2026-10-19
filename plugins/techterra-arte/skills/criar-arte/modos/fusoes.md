# Modo: Fusões

Fusões usam o mesmo fluxo do [modo monstros](monstros.md) (entrada → fichas → fila → sessão de imagem → recorte →
entrega). Aqui está só o que muda.

## Blocos

| Bloco | O que é | Pais |
|---|---|---|
| `X` | fusão base + sacrifício (inclui crossover de pacote temático e Derivada) | exatamente 2: `BASE` e `SACRIFICIO` |
| `A` | ápice: fusão base + sacrifício de míticos | exatamente 2: `BASE` e `SACRIFICIO` |
| `F` | fusão de fusões: os pais já são fusões, criatura totalmente nova | 2–3, papel `PAI`, todos do mesmo tamanho |

## Plano

1. Pares: o criador dá os pares, ou a regra para montá-los. Fusões de um **pacote temático** (ex.: crossover dos monstros
   de Halloween, anéis por estágio, ápice com os míticos): [../regras/lotes-tematicos.md](../regras/lotes-tematicos.md) §3.
2. Para cada par, escreva a **leitura** de 1 linha (o conceito do crossover) no `plano.json` — os agentes de ficha seguem.
3. Tier = maior pai + 1 (teto 10); tipo 1 da base, tipo 2 do sacrifício; par de tipos não repete no lote; base humanoide
   → fusão humanoide (o `montar_entrada.py` avisa).
4. As **artes dos pais o usuário fornece** em `<lote>/artes/`, com os dados de cada pai (nome exato, tier, tipos,
   descrição, humanoide, linhagem = outros nomes da linha dele). O `montar_entrada.py` monta a prancha de cada cartela:
   base grande à esquerda, sacrifício pequeno à direita (F: todos do mesmo tamanho).

## Fichas

Campos extras de fusão: `herda` (`{nome exato de cada pai: o que veio dele}` — base: silhueta, cabeça, rosto, traço
marcante; sacrifício: material, acento, 1–2 traços e o domínio como aura/arma) e `ascensao` (por que é um degrau acima).
Nome sem 4 letras seguidas de nenhum pai nem da linhagem (o validador confere). Descrição de fusão: domínio → tamanho →
o que faz → gosta/abomina → vigília, com 1 capacidade real.

## Cartela de opções (4 visões)

Quando o criador quer escolher a arte de uma fusão: uma cartela 2x2 com **4 visões diferentes** da mesma criatura (cor,
com/sem objeto, leitura fora da caixa), não 4 poses. Monte como lote de 1 cartela com as 4 células apontando para os
mesmos pais, cada uma com uma leitura diferente.

## Entrega

`monstros.json` sai com `ingredientes` `[{papel, nome}]` (sempre pelo nome — id muda entre ambientes) — ver
[../regras/entrega.md](../regras/entrega.md).

## Regras

[../regras/fusoes.md](../regras/fusoes.md) (dono das regras de fusão, evolução, variação e revitalização) e as demais do
[modo monstros](monstros.md). Centrais: ascensão (bem mais forte que os pais), nunca "a base com enfeite", metade-metade
ou os dois lado a lado; ~65% de base é guia, a leitura do dono manda; nada ligado aos 20 primordiais.
