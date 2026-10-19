Para que serve: como pedir, conferir, consertar e recortar uma cartela sem perder criatura nem objeto.

# Cartela e enquadramento

Medidas de cada tipo: [formatos.md](formatos.md). Diagramas a anexar: [../referencias/REFERENCIAS.md](../referencias/REFERENCIAS.md).

> **Scripts:** o verificador de enquadramento e os recortadores citados aqui estão em `scripts/` (lista em
> [../scripts/LEIA-ME.md](../scripts/LEIA-ME.md)). Não improvise script.

## A cartela 2x2 de monstros

- **Exatamente 4 criaturas**, em grade 2x2 invisível, ordem de leitura (L1C1, L1C2, L2C1, L2C2). Nunca 2 ou 3.
  — o dono reprovou cartelas com 2 e com 3.
- A IA de imagem entrega **1254×1254 PNG com alfa**: esse é o tamanho certo.
- **O prompt da cartela 2x2 de monstros nunca cita pixel** nem medida. (NPC, itens, capas e ícones citam medida de
  propósito: siga o molde de cada um.)
- **Nunca editar a cartela com código**: nada de redimensionar, cortar, completar borda, recentralizar, remontar a
  grade ou desenhar por script. Salvar exatamente como veio. O recorte é outra etapa.
- Fundo transparente: os 4 cantos com alfa até 8 contam como transparentes (alfa 1, 2, 3 é invisível).
- Uma criatura por célula: sem segunda criatura, montaria, moldura, chão, sombra ou elemento de interface.

## Enquadramento: o que funciona

- **Percentual não funciona.** Pedir 90%, 75% e 68% de ocupação deu, na mesma cartela, 99%, 93% e 91%.
  — o gerador sempre desenha maior do que o pedido.
- **Pedir "borda vazia" piora**: o gerador puxa as 4 criaturas para o meio e elas invadem a vizinha.
- O controle que funciona tem três partes:
  1. **Diagrama anexado** (`guia_enquadramento_2x2.png`): 4 quadrados cinza deslocados para os cantos = onde cada
     criatura pode estar; cruz rosa listrada no meio = proibido. O prompt diz que o diagrama **só guia a posição e
     nunca é desenhado**, e que o fundo final é totalmente transparente.
  2. **Cada criatura inclinada para o próprio canto**: o espaço entre a criatura e o meio da imagem é sempre maior que
     o espaço entre ela e a borda de fora. "Quatro adesivos separados numa folha transparente, não uma cena."
  3. **Conserto por célula** (avulsa, abaixo) em vez de jogar fora a cartela.
- Tudo o que se projeta (asa, cauda, coroa, arma, cabelo, fita, aura, partícula) cabe no quadrado cinza. Asas meio
  dobradas ou erguidas junto ao corpo; armas na vertical, junto ao corpo; criaturas compridas se enrolam dentro do
  quadrado em vez de esticar para o meio. Nunca achatar a criatura.
- **Humanoides e criaturas em pé são os que mais passam do quadrado**: o prompt pede que sejam desenhados menores,
  com o topo da cabeça e os pés bem dentro do quadrado.
- **Invadir a linha do meio sem encostar não perde nada**: o recorte separa as criaturas pelo contorno (manchas
  conectadas), não pela linha. Isso é só "atenção", nunca motivo para refazer.

## O que o verificador reprova

O verificador de enquadramento mede a cartela pelo alfa e responde OK, ATENÇÃO ou REPROVADA, dizendo quais células
falharam. Ele reprova **só perda real de arte**:

- criaturas **encostadas** (o recorte corta as duas);
- criatura **cortada na borda** da imagem;
- **pedaço solto** no quadrado da vizinha;
- quantidade **diferente de 4**;
- **fundo vazado** (não transparente, ou o diagrama apareceu desenhado).

ATENÇÃO é aceitável e **nunca gera tentativa nova**.

Defeito pequeno de olho (um brilho fora da paleta, um detalhe fraco, um olho a mais) também não gera tentativa:
anote e siga. Refazer por olho só quando a criatura está **errada**: outra criatura, texto na imagem, dois bichos
costurados, variação irreconhecível, fusão igual a um pai, dois rostos iguais na cartela, tier lido errado.

## Conserto: avulsa (grade 1)

- **1 ou 2 células reprovadas:** guardar a cartela (ela continua sendo a original) e gerar **só a criatura daquela
  célula, sozinha** (grade 1), como **avulsa**. Em "encostadas", gerar avulsa das **duas** do par.
  — não se joga fora uma cartela com 3 criaturas boas.
- **3 ou 4 células reprovadas, ou fundo vazado:** gerar a cartela inteira de novo, **uma vez**, com uma frase de
  correção no fim do prompt (uma por célula citada), salvando o prompt como `_v2` (o original fica intacto):
  - "Previous attempt failed: the creature at row R, column C touched its neighbor / was cut by the image edge / left
    a loose piece in another cell. Draw it noticeably smaller and keep it inside its gray square."
  - Fundo vazado: "Previous attempt failed: the layout diagram was drawn into the image. The background must be
    fully transparent; never draw the gray squares or the pink cross."
- A avulsa passa pelo mesmo verificador (modo avulsa); OK ou ATENÇÃO serve.
- **Registrar** cada avulsa em `validacao/avulsas.json` da pasta do lote, uma entrada por célula:
  `{"cartela": N, "linha": L, "coluna": C, "nome": "...", "arquivo": "cartelas/avulsa_NNN_LxCy_vk.png"}`.
  Nome do arquivo: `avulsa_<cartela com 3 dígitos>_L<linha>C<coluna>_v<k>.png`.
- **O refeito é aplicado depois do recortador geral**: primeiro recorta todas as cartelas, depois encaixa as avulsas
  por cima, no lugar da célula. — se rodar antes, o recortador geral desfaz o conserto.

## Refazer parte dos pais ou da prancha

- Variação e fusão: a avulsa (ou a cartela refeita) parte **do quadrante da prancha** (os pais ou o original), que vai
  anexado — **nunca de uma tentativa anterior**. — partir da tentativa ruim herda o erro.
- Antes de usar o recorte de um pai como anexo, conferir: pode vir com silhueta, letreiro ou número junto. Pai com
  letra no recorte → nenhuma letra na criatura nova.

## Orçamento

- **No máximo 3 imagens por cartela de monstros**, contando a cartela e as avulsas.
- Estourou: salvar a melhor como original, anotar **"pendente de conserto"** no registro e seguir para a próxima.
  Nunca ficar preso numa cartela.

## Cartela 5x5 de itens

Grade, organização (linha × coluna), enquadramento e recorte da cartela de itens: [itens.md](itens.md) §4 e §6.

## Recorte de personagem (página de 3 colunas)

- Entre o rosto (em cima) e o corpo (embaixo) tem uma **linha vazia**: é ela que separa os dois.
- **Corpo = só a mancha ligada aos pés.** Colunas que se tocam são separadas por crescimento simultâneo a partir dos
  pés das 3 colunas.
- No rosto, fiapos menores que 3% da área saem.
- Rosto e corpo que se tocam: corte na borda brusca do busto (onde a largura cai mais da metade); em último caso,
  máscara à mão.

## Nenhum texto na arte

- A regra geral está em [restricoes.md](restricoes.md). Aqui fica só a técnica de prompt:
- Personagem: nada de "Tier N" nem outro número além da idade no texto da pessoa. Item: sem nome em português na
  célula. — o gerador escreve na imagem o que lê solto no prompt.
- O prompt de cartela sempre traz a proibição explícita de texto e avisa que nomes e descrições são só metadados.
- Revisor visual: ficha que vira letra na imagem é erro de célula.
