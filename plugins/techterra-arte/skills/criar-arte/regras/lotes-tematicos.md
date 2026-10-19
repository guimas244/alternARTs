# Lote temático — quando o criador dá uma tipagem, um tema ou uma referência

Para que serve: o ponto de partida de um lote muda o desenho do lote. Este arquivo diz como montar o plano em cada caso
antes de escrever qualquer ficha. O plano (quantas, quais tipos, quais tiers, quais linhas) é mostrado ao criador numa
tabela curta e só depois as fichas começam.

## 1. O criador dá uma TIPAGEM ("um lote de Gelo")

Molde do pacote por tipagem: **32 monstros, 8 cartelas de 4**.

- **Tipo 1 = a tipagem pedida** em todos; o tipo 2 varia: **no mínimo 15 tipos 2 diferentes** no lote. O mesmo par de
  tipos só se repete dentro de uma linha evolutiva.
- **Tiers:** 3 monstros por tier do T1 ao T8 e 4 no T9 e no T10. Distribuição nas cartelas (ordem de leitura):

  | Cartela | Tiers |
  |---|---|
  | 01 | 1, 1, 2, 2 |
  | 02 | 3, 3, 4, 4 |
  | 03 | 5, 5, 6, 6 |
  | 04 | 7, 7, 8, 8 |
  | 05 | 9, 9, 10, 10 |
  | 06 | 1, 2, 3, 4 (o terceiro de cada tier) |
  | 07 | 5, 6, 7, 8 (o terceiro de cada tier) |
  | 08 | 9, 9, 10, 10 (terceiro e quarto) |

- **Linhas evolutivas** entre monstros do lote; um estágio nunca fica numa cartela anterior à do antecessor (ou, como
  no molde mais novo, a linha inteira fica dentro da mesma cartela, para nenhuma cartela depender de outra).
- **A tipagem tem que se ver:** o tipo 1 dá o conceito e a anatomia; o tipo 2 dá material, cor e comportamento. A cor
  NÃO é a estereotipada do tipo (Planta não precisa ser verde).
- **Não repetir o que a tipagem já tem:** peça ao usuário a lista de monstros que a tipagem já possui (nome + ideia) e
  não repita arquétipo, silhueta nem ideia central. Sem a lista, use pelo menos `dados/nomes_existentes.json` para nomes.
- 1–2 humanoides por cartela (regras/humanoides.md).

## 2. O criador dá um TEMA ou uma REFERÊNCIA EXTERNA ("filmes de terror", "Halloween", "circo", "mitologia nórdica")

O tema vira **arquétipos**, nunca personagens. Passo a passo:

1. **Liste os arquétipos** do tema (ex.: terror → palhaço do bueiro, predador nascido de ovo, matador mascarado do lago,
   grande tubarão, assombração dos sonhos, múmia, fantasma da tela, conde vampiro, lobisomem, gigante costurado,
   cavaleiro sem cabeça, sacerdote da caixa-enigma). Mostre a lista ao criador antes de seguir.
2. **Escolha a estrutura** do lote e mostre ao criador. O molde aprovado do Halloween:
   - **10 linhas evolutivas de 3 estágios = 30 monstros + 2 míticos T10 = 32** (8 cartelas);
   - estágio 1 = algo **simples e quase inofensivo** (um objeto ou bichinho: o balão, o travesseiro, a fita, o ovo);
     estágio 2 = a **forma real** (o monstro reconhecível); estágio 3 = a **forma ultimate**;
   - as linhas têm **escadas de tier diferentes** (da mais fraca, T1→T3→T6, à mais forte, T3→T7→T10) — vale o tier de
     cada criatura, não o estágio;
   - evolução com **corpo novo** a cada estágio (mesmas 2 cores, mesmos olhos, mesmo traço marcante; nunca "o mesmo
     desenho maior").
3. **Distribua as tipagens.** No Halloween, cada linha usou 3 tipagens: o tipo 1 fixo na linha toda, e o estágio final
   troca o tipo 2 — assim as **30 tipagens aparecem uma vez cada**. Use esse molde quando o criador quiser o lote
   cobrindo todas as tipagens; senão, combine com ele.
4. **Escreva o bloco de clima do tema** que vai em todo prompt do lote (como o "HALLOWEEN PACK"): o que o tema é, o tom,
   o que é proibido. Ex. de terror: *assustador e divertido como noite de Halloween; o medo vem da silhueta, da expressão
   e do clima; sem sangue, sem ferida aberta, sem parte decepada; nunca reproduzir personagem, ator, figurino ou logo de
   filme — siga só a descrição de cada criatura.*
5. **Originalidade:** o nome do filme/obra/personagem **nunca** aparece no prompt, no nome nem na descrição. Pode ficar só
   num campo interno `inspiracao` da ficha, para o criador saber de onde veio. A descrição evoca o arquétipo sem citar
   (ex.: "o ciclo que volta a cada vinte e sete anos", não o nome do palhaço). Exceção: tipagem Nostálgico, onde a
   referência reconhecível é a definição do tipo (regras/restricoes.md).
6. **Obtenção e evolução no jogo** (chance, level, evento, quantos por jogador) são decisão do criador: pergunte e
   registre no `monstros.json` como ele disse (regras/entrega.md). No Halloween: estágio 1→2 por chance, 2→3 por level.

## 3. O criador pede FUSÕES de um pacote temático ("fusões com os de Halloween")

Molde aprovado (fusões de Halloween, 19/10/2026):

- **Os dois pais saem do pacote temático.** O espaço novo é o **crossover**: arquétipo × arquétipo (filme × filme),
  sempre do **mesmo estágio** (simples × simples, forma real × forma real, ultimate × ultimate).
- **Anéis:** com N linhas, cada estágio é um anel de N fusões — cada linha entra **1× como base e 1× como sacrifício**
  por estágio, e nenhuma dupla de arquétipos se repete entre os estágios. Com 10 linhas: 3 anéis = 30 fusões.
- **Ápice** com os míticos do pacote. Dois míticos → as duas direções (A base + B sacrifício, e B base + A sacrifício):
  dois seres completamente diferentes, cada um mandado pela sua base.
- **Tipos:** tipo 1 da base, tipo 2 do sacrifício; nenhum par de tipos repete dentro do lote nem com fusões que o
  pacote já tenha (peça a lista ao usuário).
- Escolha os pares pelos **crossovers que fazem sentido** (o vampiro e o lobisomem, o mascarado e o dos sonhos, o gigante
  costurado reanimado por raio…) e escreva para cada par uma **leitura** de 1 linha antes das fichas.
- Base humanoide → fusão humanoide; 1–2 humanoides por cartela (arrume a ordem das cartelas para caber).
- Total múltiplo de 4 (cartelas cheias): se sobrar vaga, complete com um ápice ou uma fusão a mais combinada com o criador.
- Demais regras: regras/fusoes.md.

## 4. O criador anexa uma IMAGEM de referência

- Pergunte para quê: **estilo** (traço, luz, acabamento), **conteúdo** (a criatura/objeto a seguir) ou **encaixe**
  (onde fica a arte e onde fica vazio). Isso muda o texto do anexo no prompt.
- Ela entra como **anexo do lote** (na pasta de trabalho), dentro do limite de 5 anexos por geração.
- Só vira referência da skill (`referencias/`) se o dono do repositório escolher.
- Nunca copiar a imagem como figura: o prompt diz o que tirar dela ("só o traço", "só a silhueta", "só o encaixe").

## 5. Sempre

- Plano aprovado antes das fichas; fichas validadas antes da fila; fila cheia antes da sessão de imagem
  (regras/fluxo-sessoes.md).
- O lote termina no pacote de entrega com recortes e descrições (regras/entrega.md).
