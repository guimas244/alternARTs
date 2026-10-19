Regras dos humanoides dentro das cartelas de monstros (não confundir com personagens/NPCs, que são pessoas em foto realista).

# Humanoides nas cartelas de monstros

Humanoide aqui é **monstro** em forma humana — feito no mesmo traço de ilustração das outras criaturas. Personagem e
NPC (gente do mundo, foto realista) é outro modo.

## Quantos

- **Toda cartela 2x2 de monstros inéditos (lote misto) tem 1 ou 2 humanoides.** Nunca 0, nunca 3 ou 4.
  *Por quê: um lote que limitou humanoides por pacote saiu com só 2 em 192; o dono sentiu falta.*
- **Lote "de humanoides"** (o pedido diz "humanoides", ex.: *"Quero lotes criando humanoides: 1. … 2. …"*): **todas** as
  células são humanoides — no plano, as 4 de cada cartela com `humanoide_previsto: true` (os scripts aceitam a cartela
  4/4 só assim). Com evolução, os 3 estágios também são humanoides (jovem → adulto → ultimate), nunca objeto/bichinho.
  A regra de 1–2 por cartela vale para o lote misto.
- **Fusão e variação:** a quantidade sai das bases/originais — base humanoide → fusão humanoide; original humanoide →
  variação humanoide. Pode dar 0 numa cartela. *Inferência (confirmar com o dono):* se passar de 2 numa cartela,
  redistribua entre cartelas.

## Classe

- **Classe livre e variada**: mago, samurai, rei caído, ferreira, astróloga, carteiro, dançarina, pirata, sacerdote…
- Anjo, demônio e cavaleiro são **exemplos, não cota**. *Por quê: quando virou cota fixa de cavaleiro + anjo + demônio,
  o dono corrigiu — "isso foram exemplos".*
- *Recomendação (não é regra do dono):* evite repetir classe entre células do mesmo lote sem motivo; prefira classes
  que nasçam da mistura dos dois tipos.
- Na ficha: `humanoide: true` e `classe: "<classe>"`.

## Traço e corpo

- **Mesmo traço** dos monstros da cartela (contorno, cel-shading, luz), épico.
- **Proporção humana**: cabeça, tronco, 2 braços, 2 pernas, ereto. Pode ter material, cor e elementos do tipo (armadura
  de cristal, manto de névoa), mas o corpo lê como gente.
- **Tier pela escada de poder** de [estilo.md](estilo.md), como qualquer monstro: T1–2 figura jovem e quase inofensiva,
  T3–4 jovem com as primeiras defesas, T5–6 adulto armado, T7–8 guerreiro de topo com armadura e marca de batalha,
  T9–10 figura de chefe final (coroa, auréola, arsenal). O tamanho continua vindo da lore, não do tier.
- Rosto único, como em toda ficha (nunca igual ao de outra criatura da cartela).

## Anexo

- Nas cartelas com humanoide, anexe `referencias/monstros/referencia-humanoides.png` (proporção e leitura de figurino),
  na posição indicada em `referencias/REFERENCIAS.md`.
- Humanoide em pé é o que mais passa do quadrado da célula: incline-o para o próprio canto, como as outras criaturas.
