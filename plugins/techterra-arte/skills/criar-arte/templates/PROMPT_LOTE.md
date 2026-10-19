# Prompt — {TITULO}: {MONSTROS} monstros ({TOTAL} cartelas 2x2) — SÓ IMAGENS

<!-- Modelo: templates/PROMPT_LOTE.md da skill criar-arte. Preenchido por scripts/preparar_fila.py; não edite à mão o
     PROMPT_<LOTE>.md gerado (rode o script de novo). -->

| Cartelas | Bloco | Monstros |
|---|---|---:|
{TABELA}

Cole na IA que gera as imagens. Uma sessão por faixa de 4 cartelas, todas ao mesmo tempo:

{FAIXAS}

**Ou tudo num prompt só** (a sessão abre um trabalhador por faixa, se a ferramenta tiver subagentes):

> Leia e execute `{ARQUIVO_PROMPT}` — TODOS

Para refazer só células trocadas depois da geração (lista em `trocas.json`, escrita pelo Claude):

> Leia e execute `{ARQUIVO_PROMPT}` — TROCAS

Se a sessão cair, mande a mesma frase de novo: ela pula as cartelas que já têm imagem. As fichas, os nomes e o texto de
cada prompt foram escritos pelo Claude e estão prontos em `fila.json`.

---

```text
Você GERA AS IMAGENS do lote {TITULO} ({LOTE}) do Techterra: {MONSTROS} monstros em {TOTAL} cartelas 2x2.
Trabalhe dentro de {PASTA_LOTE}
Todos os caminhos citados aqui e na fila são relativos a essa pasta. Outros agentes podem trabalhar ao lado (outras
faixas deste lote): só crie arquivos em cartelas/ e validacao/.

═══ SEU PAPEL ═══
Você NÃO escreve fichas, nomes, descrições nem prompts. Tudo chega PRONTO na fila. O seu trabalho é só: anexar as
imagens que a fila manda, colar o texto do prompt EXATAMENTE como está no arquivo, gerar, conferir, salvar no caminho
indicado e registrar.
PROIBIDO, sem exceção:
- criar ou alterar ficha (monstros.json, fichas_claude/), nome, descrição ou "visual";
- criar, reescrever, resumir, traduzir ou "melhorar" arquivo em prompts/;
- criar scripts que escrevem fichas ou prompts;
- alterar plano.json, entrada.json, fila.json e trocas.json (fora do campo "estado"), referencias/, pais/, artes/;
- mexer em qualquer pasta fora desta (outros lotes e a pasta da skill são SÓ LEITURA).
Se uma cartela não está na fila, ou falta o arquivo de prompt dela, NÃO improvise: pule e anote.
ÚNICA edição de texto permitida: acrescentar ao FIM do prompt a FRASE DE CORREÇÃO numa 2ª tentativa (ver CONSERTO),
salvando a variação como prompts/cartela_NNN_v2.txt (o original fica intacto).

═══ O QUE É ESTE LOTE (para você CONFERIR a imagem; não para escrever nada) ═══
{DESCRICAO_LEVA}

═══ A FILA ═══
fila.json é uma lista. Cada item (uma cartela):
  "cartela": número (1–{TOTAL}); "leva": {LEVAS};
  "estado": "pronta" | "gerada" | "pendente de conserto"; "prompt": arquivo com o texto FINAL;
  "anexos": as imagens a anexar, NESTA ORDEM (no máximo 5); "salvar": onde gravar a cartela aprovada;
  "monstros": os 4 nomes (L1C1, L1C2, L2C1, L2C2); "depende_de": cartelas que precisam ter imagem antes desta
  (um anexo dela é a cartela de lá); "avulsas": para cada célula, prompt, anexos e caminho de uma AVULSA (conserto de
  1 criatura).

═══ MODO FAIXA (sessão que recebe "— FAIXA x–y") — o modo normal ═══
Você é TRABALHADOR daquela faixa. Faça, só nas cartelas dela e em ordem crescente, SEM parar entre elas: anexar,
colar o prompt, gerar, medir o enquadramento, consertar por avulsa e salvar.
- PULE toda cartela da faixa que já tem cartelas/cartela_NNN_original.png (assim, se cair, basta mandar a mesma frase
  de novo).
- Cartela com "depende_de" cuja cartela de lá ainda não tem _original: deixe para o fim da faixa; se continuar
  faltando, pule e anote.
- Escreva SOMENTE: as imagens das suas cartelas em cartelas/ ; validacao/geracoes_<x>-<y>.json,
  validacao/cartelas_<x>-<y>.json e validacao/avulsas_<x>-<y>.json (x e y com 3 dígitos, ex.: geracoes_001-004.json).
- NUNCA edite fila.json nem arquivo de outra faixa.
- Ao terminar, responda com: cartelas geradas, imagens gastas, cartelas "pendente de conserto" e as que precisam de
  olho humano.

═══ MODO TODOS (sessão que recebe "— TODOS", ou nenhuma faixa) ═══
Você é o COORDENADOR das {TOTAL} cartelas e NÃO gera imagem nenhuma você mesmo enquanto houver subagentes.
1. Abra AGORA, em paralelo, {NUM_FAIXAS} subagente(s) TRABALHADOR(ES), um por faixa: {LISTA_FAIXAS}.
   A instrução de cada um é exatamente esta frase, trocando a faixa:
   "Leia e execute {ARQUIVO_PROMPT} — FAIXA {PRIMEIRA_FAIXA}"
   Não resuma as regras para eles: cada trabalhador lê este arquivo inteiro e segue o MODO FAIXA.
2. Se a ferramenta limitar os subagentes simultâneos, abra o máximo permitido e, assim que um terminar, abra o da
   próxima faixa. Se o gerador recusar por limite de uso, reduza para 2–4 ao mesmo tempo.
3. Trabalhador que parar no meio, ou voltar com cartelas faltando: abra outro com a MESMA faixa (ele pula o que já tem
   imagem). Repita até toda cartela ter cartelas/cartela_NNN_original.png.
4. Só o coordenador edita o campo "estado" em fila.json. No fim, junte os registros por faixa em
   validacao/geracoes.json, validacao/cartelas.json e validacao/avulsas.json, e responda com: N de {TOTAL} cartelas com
   imagem, a lista das "pendente de conserto" e das que precisam de olho humano.
Sem subagentes disponíveis: faça as faixas em sequência, você mesmo, sem parar entre elas.

═══ MODO TROCAS (sessão que recebe "— TROCAS") ═══
Lista em trocas.json: cada item é UMA célula ("cartela", "linha", "coluna", "nome", "prompt", "anexos", "salvar",
"estado"). Para cada item com "estado": "pronta": gere SÓ aquela criatura, sozinha (grade 1), anexando "anexos" na
ordem e colando o texto do arquivo "prompt" sem mexer. NÃO anexe a cartela antiga. Salve em "salvar" (_v1; _v2 só se
a _v1 for REPROVADA) e meça com o verificador no modo --avulsa (abaixo). Registre em validacao/avulsas_trocas.json:
    {"cartela": N, "linha": L, "coluna": C, "nome": "...", "arquivo": "cartelas/avulsa_NNN_LxCy_troca_vk.png"}
e troque o "estado" do item em trocas.json para "gerada". Orçamento: até 2 imagens por item.

═══ ANTES DE COMEÇAR (toda vez, inclusive ao retomar) ═══
1. Leia fila.json (só os itens da sua faixa).
2. Veja cartelas/ e validacao/enquadramento/ (um arquivo por imagem já medida), se existirem.
Não precisa ler plano.json, entrada.json nem fichas: não há texto para escrever.

═══ GERAÇÃO DE CADA CARTELA ═══
- Ferramenta de imagem integrada (image_gen). Ela entrega 1254 x 1254 PNG com alfa: ESSE é o tamanho certo.
- Anexe as imagens de "anexos" NA ORDEM (o texto do prompt as chama de Image 1, 2, 3…). Vale o que está na fila.
- O texto enviado ao gerador é o CONTEÚDO INTEIRO do arquivo "prompt", sem cortar, resumir nem acrescentar.
- UMA geração por cartela, e siga direto para a próxima. Quem julga a qualidade é o criador, depois.
- Salve EXATAMENTE como veio (tentativas: cartela_NNN_v1.png, _v2.png; a aprovada também como
  cartela_NNN_original.png). PROIBIDO redimensionar, cortar, completar borda, recentralizar ou editar com código.
- ENQUADRAMENTO — rode SEMPRE, logo depois de salvar cada tentativa (de dentro da pasta do lote):
      python "{SKILL}/scripts/checa_enquadramento.py" cartelas/cartela_NNN_<tentativa>.png
  Responde OK, ATENÇÃO ou REPROVADA e diz QUAIS células falharam. Só reprova perda real de arte: criaturas
  ENCOSTADAS, criatura CORTADA na borda, PEDAÇO SOLTO no quadrado do vizinho, número de criaturas diferente de 4, ou
  fundo não transparente (ou o diagrama desenhado). ATENÇÃO é aceitável. NUNCA conserte a imagem com código.
- ORÇAMENTO: por cartela, no máximo 3 imagens no total, contando a cartela e as avulsas.
  · ATENÇÃO nunca gera tentativa nova. Só REPROVADA gera conserto.
  · Defeito de olho PEQUENO (um brilho fora da paleta, um detalhe fraco, um olho a mais/a menos) NÃO gera tentativa:
    anote e siga. Só refaça por olho se a criatura estiver ERRADA: outra criatura, texto na imagem, dois bichos
    costurados (metade-metade), variação irreconhecível, fusão igual a um pai, os dois pais lado a lado, dois rostos
    iguais na cartela, tier lido errado, ou algo que o bloco de clima do lote proíbe.
  · Estourou o orçamento: salve a melhor como _original, anote "pendente de conserto" no seu registro e siga.
- CONSERTO (não jogue fora 3 criaturas boas por causa de 1):
  · Fundo não transparente, ou 3–4 células reprovadas: gere a cartela INTEIRA de novo, UMA vez, com a FRASE DE
    CORREÇÃO no fim do prompt (uma por criatura citada pelo verificador, trocando R e C), salvando o texto como
    prompts/cartela_NNN_v2.txt:
    "Previous attempt failed: the creature at row R, column C touched its neighbor / was cut by the image edge / left
    a loose piece in another cell. Draw it noticeably smaller and keep it inside its gray square."
    Fundo vazado: "Previous attempt failed: the layout diagram was drawn into the image. The background must be fully
    transparent; never draw the gray squares or the pink cross."
  · 1 ou 2 células reprovadas: GUARDE a cartela (ela é a _original) e gere SÓ a criatura de cada célula reprovada
    como AVULSA, com o item de "avulsas" daquela linha/coluna (os anexos na ordem — um deles é a própria cartela salva
    — e o texto do "prompt" dele, sem mexer). Em "encostadas", gere AVULSA as DUAS do par. Salve no "salvar" da avulsa
    (_v1; _v2 só se a _v1 for REPROVADA e couber no orçamento) e meça:
        python "{SKILL}/scripts/checa_enquadramento.py" cartelas/avulsa_NNN_L1C2_v1.png --avulsa
    Avulsa OK ou ATENÇÃO serve. Registre no seu avulsas_<faixa>.json:
    {"cartela": N, "linha": L, "coluna": C, "nome": "...", "arquivo": "cartelas/avulsa_NNN_LxCy_vk.png"}.
  · Criatura ERRADA no olho numa célula só: mesma AVULSA. Em 3–4 células: cartela inteira de novo, uma vez.
  · Quando há prancha (pais, original ou antecessor), a avulsa parte do quadrante da prancha (vai no anexo), nunca de
    uma tentativa anterior.
- Confira no olho, sem refazer por pouco:
  TODAS: (a) nenhum texto; (b) exatamente 4 criaturas, sem 2 rostos iguais na cartela; (c) o tier lido bate com a
  POWER LADDER; (d) humanoide marcado como HUMANOID tem proporção humana.
{CONFERENCIA_BLOCOS}
- Registre as tentativas no seu geracoes_<faixa>.json (cartela, leva, tentativa, arquivo, veredito do verificador,
  células reprovadas, observação curta) e a conferência no seu cartelas_<faixa>.json.

═══ ONDE SALVAR (obrigatório — fixo, sem exceção) ═══
Raiz: {PASTA_LOTE}
- cartelas/cartela_NNN_original.png (a aprovada; NNN com 3 dígitos, 001 a {ULTIMA});
- cartelas/cartela_NNN_v1.png / _v2.png (tentativas);
- cartelas/avulsa_NNN_L<linha>C<coluna>_v<k>.png (consertos de célula);
- validacao/geracoes_<faixa>.json, cartelas_<faixa>.json, avulsas_<faixa>.json
  e validacao/enquadramento/<imagem>.json (gravado pelo verificador).
A cópia no cache do gerador NÃO é entrega: copie sempre para o caminho acima. Nomes de arquivo em minúsculas, sem
acento, "_" entre palavras. Texto em UTF-8 sem BOM (Python: open(caminho, "w", encoding="utf-8")). Nunca
Set-Content/Out-File sem -Encoding utf8.

═══ NO FIM ═══
Responda com a pasta absoluta das cartelas num bloco de código ({PASTA_CARTELAS}), a lista das cartelas geradas,
as "pendente de conserto" e as que precisam de olho humano.

NÃO FAÇA: escrever ou trocar fichas, nomes, prompts, tipos, tiers, pais ou originais; recorte; cadastro no jogo;
habilidades; atributos; commit ou push. Fora desta pasta, tudo é SÓ LEITURA.
```
