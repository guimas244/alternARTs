# Instruções do agente de fichas — {TITULO}

<!-- Modelo: templates/INSTRUCOES-AGENTE-FICHAS.md da skill criar-arte. O Claude copia para a pasta do lote trocando
     {TITULO} e {SKILL} (pasta da skill, com barras "/"). -->

Você escreve fichas de monstros para o jogo Techterra, em português do Brasil, seguindo um contrato. A mensagem que te
chamou diz a **pasta do lote**, a sua **LETRA** e as suas **CARTELAS**. Rode tudo de dentro da pasta do lote.

## 1. Leia

1. `CONTRATO-FICHAS.md` inteiro, e as regras da skill que ele aponta (`{SKILL}/regras/*.md`).
2. As suas células: `python "{SKILL}/scripts/ver_celulas.py" . <suas cartelas>`.
3. A prancha `referencias/cartela_NNN_pais.png` de cada cartela sua que tiver uma, com Read (e `pais/<slug>.png` se
   precisar de detalhe). Ficha escrita sem olhar a arte de origem sai errada.

## 2. Não repita ideias de outras partes

Antes de escolher nomes e conceitos, liste com um script curto o `nome` + `arquetipo` (ou `epiteto`, ou o começo da
`anatomia`) de todas as `fichas_claude/parte_*.json` já escritas. Não repita a **raiz do nome** (as 5 primeiras letras),
a **ideia central** nem a **classe de humanoide** de outra parte.

## 3. Escreva

- Só em `fichas_claude/parte_<LETRA>.json`, em UTF-8 sem BOM. Outros agentes escrevem outras partes ao mesmo tempo: não
  toque em mais nada da pasta. Scripts auxiliares seus ficam fora da pasta do lote.
- Pense na cartela inteira antes: as 4 criaturas bem diferentes em silhueta, rosto, cor e material.

## 4. Feche

`python "{SKILL}/scripts/compor_fichas.py" . fichas_claude/parte_<LETRA>.json`. Repita até **OK** e rode mais uma vez no
fim.

## 5. Responda (curto)

- As últimas linhas do validador.
- A lista `n — nome — uma linha do conceito`.
- Ambiguidades do contrato ou problemas na arte de origem (letreiro, traço diferente), se houver.
