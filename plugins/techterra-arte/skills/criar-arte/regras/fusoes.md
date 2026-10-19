Regras de conteúdo de fusões, fusões de fusões, evoluções, variações e revitalizações (o que a ficha e o prompt precisam cumprir).

# Fusões, evoluções e variações

Os campos comuns da ficha estão em [fichas-nomes-descricoes.md](fichas-nomes-descricoes.md); aqui vai só o que muda.
Nada disto pode envolver os 20 primordiais — nem como pai, original, antecessor ou referência (ver
[restricoes.md](restricoes.md)).

## Montar os pares

- **Exatamente 2 pais:** BASE (dá o corpo) + SACRIFÍCIO (dá material, cor de acento, 1–2 traços e o domínio como aura,
  arma ou emanação).
- **Use todos os pais possíveis.** Se um grupo precisar repetir, **todos do grupo repetem o mesmo número de vezes** —
  nunca repetir só um.
- **Ápice:** a classe mais nobre de pais (os mais importantes da leva) fica com o lugar de ápice do lote.
  Se o ápice usa os mesmos pais nos dois sentidos (A base + B sacrifício, e B base + A sacrifício), têm que sair **dois
  seres completamente diferentes**, cada um mandado pela sua base.
- **Tier = maior pai + 1**, teto 10.
- **Tipo 1 = da base, tipo 2 = do sacrifício.** O mesmo par de tipos não se repete na leva.
- **Base humanoide → fusão humanoide.**

## O que a arte tem que mostrar

- **Ascensão:** bem mais forte que os dois pais no tier dela. Nunca "a base com enfeite", nunca metade-metade, nunca os
  dois lado a lado, nunca o sacrifício como bicho separado, montaria ou pet.
- **Base reconhecível (~65%)** na silhueta, na cabeça, no rosto e no traço marcante. **~65% é guia; nunca justifica
  "base com enfeite"** — a ascensão e a leitura do dono mandam.
- **Leitura do dono vale mais que os 65%.** Se o dono definiu a leitura de uma criatura ("castelo com braços
  flutuantes", "cobra saindo do corpo", "fruto marinho"), o prompt segue isso e a conferência cobra exatamente isso.
- **Tier baixo continua jovem.** Fusão T4–T6 segue a escada de poder; ascensão não é virar titã.
- **Selvagem** (quando pedido) = nada crescendo do corpo (galho, raiz, folha); materiais só na roupa e na arma.
- **Pai sem corpo próprio** (tornado, nuvem, energia): a fusão falha quando vira "o tornado recolorido com o outro pai de
  enfeite". Funciona quando o outro pai dá o corpo e o pai sem corpo entra como matéria ou detalhe.
- **Pai com letreiro, moldura ou número no recorte:** nada de letra na criatura nova. Confira o recorte do pai antes de
  usar (já veio recorte com silhueta e letreiro grudados).

### Anexos e prancha

- Referência de estilo = só o traço; referência de variedade pesa **mais** (detalhe, material, brilho, presença).
- **Prancha dos pais** por cartela: em cada quadrante, a BASE grande à esquerda e o SACRIFÍCIO pequeno à direita.
  **Olhe a prancha antes de escrever a ficha.** As artes dos pais (e do original/antecessor) **o usuário fornece** — a
  skill não tem banco nem acervo; a prancha é montada por `scripts/montar_entrada.py` a partir delas.
- Para refazer uma arte, parta **sempre dos pais** (prancha/quadrante), nunca de uma tentativa anterior. *Por quê: cada
  refação a partir da anterior acumula o erro.*

### Cartela de opções (visões)

Quando o pedido é ver alternativas de uma fusão: **4 VISÕES diferentes** da mesma criatura na mesma imagem 2x2 — outra
cor, com/sem objeto, uma leitura "fora da caixa" — e **não 4 poses** do mesmo desenho.

## Campos próprios da fusão

| Campo | Regra |
|---|---|
| `herda` | `{nome exato da base: o que fica dela, nome exato do sacrifício: o que vem dele}` |
| `ascensao` | 1–2 frases: o que a torna um degrau acima dos dois (o traço virou domínio, a arma virou corpo…) |
| `paleta` | corpo segue a base; acento vem do sacrifício |
| `rosto` | parte do rosto da base, mas nunca dois rostos iguais na cartela |
| `marcas_poder` | **fusão: +1 marca** sobre a escada de [estilo.md](estilo.md) (seção Escada de poder) |
| `marca_da_habilidade` | um poder que nenhum pai tinha sozinho, nascido da soma dos dois |

## Nome da fusão

- **Fusão comum (nome próprio):** palavra inventada, sonora, que evoca o domínio dela (não uma junção dos pais). Modelo
  de nome próprio e de descrição: o estilo "Abdicrégio" (palavra inventada que evoca o domínio). **Nenhuma sequência de 4+
  letras em comum** com nenhum pai **nem com a linhagem** deles (de quem os pais nasceram).
- **Fusão Derivada** (mantém uma criatura de referência e acrescenta o outro ingrediente): nome = **nome inteiro da
  referência + epíteto** (como na variação).
- Único (fora de `dados/nomes_existentes.json` e do lote), sem número, sem nome de filme, personagem ou ator.

## Descrição da fusão

~440 caracteres, **4–5 frases curtas, nesta ordem**:

1. **domínio** (o que ela governa ou encarna);
2. **tamanho por comparação** (decidido pela lore; nunca "maior que o pai");
3. **o que faz** no mundo;
4. **o que gosta / o que abomina**;
5. **vigília** (o que faz quando ninguém está olhando, as folgas).

- Cite **1 capacidade real** da criatura, para a força ficar clara.
- Que dê para sentir os dois pais misturados — sem citar o nome de nenhum deles.
- Todas as proibições da descrição comum valem (sem físico, sem algarismo, sem "fusão/sacrifício/mítico", sem nome de
  monstro nem palavra que é nome de monstro).

## Fusão de fusões

Os pais **já são fusões**. O resultado é o próximo degrau da cadeia: criatura **totalmente nova**, que não lembra nenhum
pai sozinho.

- Formatos: **dupla** (2 fusões, T4–T10), **tríade** (3 fusões, T9–T10), **terceira geração** (um pai que já nasceu de
  fusão + uma fusão, T10).
- `herda` com **todos** os pais; de cada um, 1 ou 2 elementos (material, cor, motivo, arma, formato de olho).
- `ascensao`: na terceira geração, a ideia de "linhagem antiga que chegou ao fim" é bem-vinda.
- `marcas_poder`: +1, como em toda fusão.
- Nome sem 4+ letras de nenhum pai **nem avô**.

## Evolução

- Muda de **forma** a cada estágio: corpo novo, postura nova, armas novas pela escada de poder.
- Mantém **só**: as 2 cores, os olhos (formato e cor) e **um** traço marcante. Se os dois estágios parecem o mesmo
  desenho, a ficha está errada.
- Linha de 2 ou 3 estágios, sempre subindo de tier, mantendo os dois tipos.
- A `anatomia` (ou o `visual`) do estágio novo começa com "Evolução do <nome>." / "Evolução da <nome>.".
- Anexe a cartela (ou o recorte) do antecessor. Um estágio nunca fica numa cartela anterior à do antecessor; quando o
  lote pede, os dois estágios ficam na mesma cartela.
- Nome próprio, sem prefixo obrigatório em comum com o antecessor.

## Variação

A **mesma criatura** do original, nascida em outro elemento (sai um tipo, entra outro).

- **~70% reconhecível**: silhueta, anatomia, rosto/olhos (mesmo layout, cor nova), pose e ideia ficam (`mantem`).
- **~30% muda**: material, superfície, paleta e detalhes do elemento novo (`muda`).
- **Mesmo porte, idade e tier**: não cresce, não envelhece, não ganha arma nova.
- **Nome = nome do original + epíteto** de 1 a 3 palavras em português que evoca o tipo novo ("Boreal", "de Cinza",
  "de Maré Baixa", "Sem Sombra"). Varie os epítetos e prefira um que diga algo do original no elemento novo; o epíteto
  não pode ser nome de monstro.
- Original humanoide continua humanoide (mesma classe ou uma vizinha).
- Original em outro traço (foto, rascunho, anime, chibi): escreva "no traço de ilustração das outras criaturas". Se o
  recorte tem letreiro, moldura, número ou figura extra, diga o que **não** entra.

## Revitalização

Refazer uma arte antiga que já existe, **preservando o estilo dela** (nanquim, pintura…).

- Anexos: **no máximo 2, só folha(s) base** (as originais coladas no guia). **Nunca** referência de estilo de outra
  coleção. — anexo demais dilui a base e troca o estilo que era para preservar.
- Forma **nova** (evolução, fusão, forma suprema) não é revitalização: segue o estilo padrão do jogo, com a referência de
  estilo anexada.

## Estágios por recorte progressivo

Quando uma criatura tem várias idades ou estágios (ex.: um dragão que envelhece e cresce), é aceito gerar **uma única
arte** com os estágios e recortar cada estágio dela. Precedente aceito pelo dono (estágios etários do Superatos).
