# Formatos por tipo de arte

Decisão do dono (19/10/2026): **manter os tamanhos já usados, por tipo** — não unificar. A coluna "Sai" é o arquivo que o
jogo consome; a "Gera" é o que a IA de imagem entrega.

| Tipo | Gera (IA de imagem) | Sai (depois do recorte/ajuste) | Observações |
|---|---|---|---|
| Monstro | cartela **1254×1254** PNG com alfa, grade 2x2, exatamente 4 criaturas | recorte **512×512** PNG RGBA por criatura | recorte por contorno (componentes conexos); cartela original nunca é redimensionada |
| Fusão | idem monstro + prancha dos pais (1254², base grande à esquerda, sacrifício pequeno à direita) como anexo | **512×512** RGBA | — |
| Personagem / NPC | página **1254×1254** com 3 colunas (2 mulheres + 1 homem), rosto no topo + corpo inteiro embaixo, fundo transparente | rosto **512×512** + corpo **512×1024** RGBA | linha vazia entre rosto e corpo; nenhum número além da idade no texto de cada pessoa (o preâmbulo mantém as coordenadas aprovadas) |
| Item / equipamento | cartela **1254×1254** com alfa, grade **5x5** (o que é linha e coluna: ver [itens.md](itens.md) §4) | **320×320** RGBA, margem de 16 px (mínimo 8) | o item é menor que o monstro no arquivo final; a cartela é que tem 25 objetos |
| Livro de Habilidade | igual a item | **320×320** RGBA | medalhão vazio e paleta neutra (o jogo pinta a cor) |
| Essência | igual a item | **320×320** RGBA | — |
| Pedra ritual | igual a item | **512×512** RGBA | — |
| Ícone de mapa | cartela **1254² 4x4**, medalhões ~270 px | **300×300** RGBA (medalhão redondo, borda branca, máscara circular) | mostrado a 80×80 |
| Ícone de tipo | — | 512×512 RGBA | — |
| Fundo de Local (Narraris, Jornada, expansões) | 16:9 | **1672×941** JPG | aplicado com `cover` + véu escuro; horizonte no terço de cima, chão aberto, luminância 70–200 |
| Fundo dos lados (TechTerra/Mascris) | 16:9 | **1536×864** JPG | — |
| Portão da Jornada | 16:9 | **1600×900** JPG | faixas livres fixas: a interface escreve por cima |
| Sub-mapa de Região / lados / mundi | paisagem 3:2 | **1536×1024** PNG | pinos são pixels sobre a arte: redimensionar, nunca recortar |
| Mapa de Narraris | prompt pede 1600×1000 | 1586×992 | idem |
| Capa de evento/expedição/raid | cartela **1536×2048** com 2x2 cenas 3:4 separadas por faixa branca de 40 px | **510×680** WebP por cena (é o que cada cena da cartela rende) | o cartão do jogo recorta 146×188 pelo centro: palco no meio |
| Wallpaper de passe / moldura de invasão | — | **1672×941** | moldura segue o encaixe de `referencias/capas/template_monstros_invasao.png` |
