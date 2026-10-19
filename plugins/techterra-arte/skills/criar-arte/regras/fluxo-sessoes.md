Para que serve: como dividir o trabalho entre a sessão do Claude e a sessão da IA de imagem, onde salvar, e como orquestrar agentes num lote grande.

# Fluxo das sessões

## As duas sessões

| Sessão Claude (prepara) | Sessão da IA de imagem (só gera) |
|---|---|
| escreve fichas, nomes, descrições, visual e o **texto final** de cada prompt | anexa as imagens que a fila manda, na ordem |
| monta a **fila** (prompt pronto + anexos + onde salvar) | cola o prompt **exatamente** como está no arquivo |
| escreve o prompt da sessão de imagem (modos abaixo) | gera, confere, salva no caminho mandado, registra |
| confere o que chegou, recorta, aplica as avulsas | **não** escreve ficha, nome, descrição, visual nem prompt |
| **nunca** gera imagem nem pede ao usuário para colar prompt no meio | não cria script que escreva ficha ou prompt |

- O prompt da sessão de imagem **proíbe** criar ou alterar ficha, nome, descrição, prompt, fila ou referências.
  — a IA de imagem que inventa ficha foge do que foi decidido aqui.
- Única edição de texto permitida à sessão de imagem: acrescentar a frase de correção no fim do prompt numa 2ª
  tentativa, salvando como `_v2` (ver [cartela-e-enquadramento.md](cartela-e-enquadramento.md)).
- Cartela fora da fila ou sem arquivo de prompt: **pula e anota**, não improvisa.
- Para refazer depois: o Claude escreve um `_v2` do prompt e renomeia a imagem ruim para `_ruimN`; ela volta para a
  fila sozinha.
- **Todo lote com imagem nasce em par de documentos:** o **PROMPT da sessão de imagem** (`PROMPT_<LOTE>.md` ou
  `PROMPT_IMAGEM_*.md`: a fila de prompts prontos, gera sem parar) + o **EXECUTAR** do Claude (escreve, confere,
  recorta; nunca gera imagem nem pede para colar prompt no meio).

## Fila cheia antes de gerar

- A sessão de imagem só começa quando **todos** os prompts do lote estão escritos e validados (`fila.json` ou
  `prompts/pagina_NNN.txt`). — com a fila pela metade a sessão para e espera.
- Cada item da fila diz: número, estado (`pronta` / `gerada` / `pendente de conserto`), arquivo do prompt, anexos na
  ordem (o prompt os chama pela ordem, com o rótulo do molde de cada modo: "Image N", "Reference N" ou "first/second
  supplied image"), onde salvar, e o item de avulsa de cada célula.
- **Não liberar a geração antes da revisão cruzada das fichas.** — célula gerada com ficha velha vira troca depois.

## Uma geração por página

- Gerar cada cartela/página **uma vez**, salvar e seguir direto até a última, sem parar entre elas.
- Quem julga a qualidade é o **dono, depois**. A sessão não reprova por detalhe.
  — "refaça até ficar bonito" fez uma sessão passar horas e aprovar uma página.
- Refazer só por erro real, definido por modo (este arquivo é a referência; os modos detalham):
  - monstros: o verificador de enquadramento reprovou, ou a criatura está errada (lista em
    [cartela-e-enquadramento.md](cartela-e-enquadramento.md)); orçamento de **3 imagens por cartela** contando as
    avulsas;
  - personagens: **no máximo 1 refação**, só por erro grave (não saíram 3 pessoas, fundo todo opaco, nudez);
  - itens: ver [itens.md](itens.md) §6;
  - cenários, mapas, capas e ícones: ver [cenarios-mapas-capas.md](cenarios-mapas-capas.md) (Regras comuns).
- O verificador e os recortadores estão em `scripts/` (lista em [../scripts/LEIA-ME.md](../scripts/LEIA-ME.md)).

## Limite de anexos

- A ferramenta de imagem aceita **no máximo 5 anexos** por geração (recusa acima disso).
- Cartela nova de monstros usa até 5: estilo, variedade, prancha, diagrama, humanoides.
- **Revitalização** (refazer arte existente mantendo-a): **no máximo 2, só folha(s) base**, nunca referência de estilo
  de outra coleção — regra completa em [fusoes.md](fusoes.md#revitalização).
- Muitas artes de origem numa cartela: pré-montar **uma folha** com elas em vez de anexar uma a uma.

## ONDE SALVAR (obrigatório em todo prompt de imagem)

Todo prompt de sessão de imagem tem uma seção **"ONDE SALVAR (obrigatório)"** com:

- a **pasta absoluta** de saída, **dentro da pasta de trabalho do usuário** (o diretório da sessão ou o que ele
  indicar) — nunca dentro da pasta da skill, que é trocada a cada atualização;
- as subpastas (ex.: `cartelas/`, `validacao/`, `recortes/`);
- a regra de nome (**esta é a referência única**): **minúsculas, sem acento, `_` entre palavras, `_vN` para
  tentativas**, números com zeros à esquerda (`cartela_007_original.png`, `cartela_007_v1.png`,
  `avulsa_007_L1C2_v1.png`);
- os registros esperados (registro de gerações, de conferência, de avulsas; índice/`index` do lote; manifesto ou
  LEIA-ME com o que faltou).

Regras junto:

- A cópia que fica no cache do gerador **não é entrega**: copiar sempre para o caminho mandado.
  — sem pasta no prompt, a imagem cai num lugar que só o gerador conhece e ninguém acha depois.
- Texto em UTF-8 sem BOM.
- No fim, a sessão responde com a pasta absoluta num bloco de código.

## Índice de entregas

- Ao terminar um lote, acrescentar uma linha no **`ENTREGAS.md`** da pasta de trabalho: data, lote, pasta absoluta das
  cartelas/recortes, quantidade, pendências.
- Quando o usuário disser "a arte ficou pronta", **ler o `ENTREGAS.md` primeiro**, depois a pasta indicada.

## Pedido de "proposta" de pacote

- "Proposta" de pacote de monstros = **já montar no padrão de fabricação**: pasta do lote, contrato das fichas,
  fichas escritas por agentes em paralelo, validador (`valida_fichas.py`/`compor_fichas.py`), prompts por cartela, `fila.json` e o prompt da sessão de imagem.
  **Não** fazer HTML de proposta nem formulário. — o dono avalia olhando as fichas e as cartelas.
- Decisões abertas: tomar com o padrão recomendado e listar na resposta.

## Modos do prompt da sessão de imagem

1. **Piloto**: poucas cartelas/páginas (ex.: 4) para o dono julgar o traço. Só depois escala.
2. **FAIXA** (modo normal): a sessão recebe um intervalo de cartelas (ex.: 001–012), faz só elas, em ordem, sem parar,
   e **pula as que já têm imagem** (se cair, basta mandar a mesma frase de novo). Grava só os arquivos da sua faixa
   (registros com sufixo `_<x>-<y>`). Várias sessões de FAIXA rodam ao mesmo tempo.
3. **TODOS**: uma sessão coordena — abre um trabalhador por faixa (mandando ler o mesmo prompt, sem resumir as
   regras), reabre quem parar no meio, e só ela edita o estado da fila e o progresso; junta os registros no fim. Sem
   subagentes, faz as faixas em sequência.
4. **TROCAS**: refaz só as células trocadas depois da geração (lista em `trocas.json`): cada uma como avulsa, sem
   anexar a cartela antiga.

## Orquestração com vários agentes

- **"Leia as outras partes" desde o início**: cada agente de ficha lê o que os outros já escreveram antes de
  escrever o seu. — agentes em paralelo repetem a mesma ideia e a mesma raiz de nome (pipa ×5, sino ×5).
- **Revisor cruzado no fim**, lendo todas as partes juntas: raiz de nome, conceito, esqueleto de descrição e frase de
  tamanho repetidos ("tem a altura de um…").
- **Revisor visual contra a prancha**: compara cada ficha com a imagem dos pais/original. — numa leva pegou 54 fichas
  erradas em 208 (membros e olhos errados, fusão que era só o pai com enfeite, texto que viraria letra).
- **Medidor de variedade escrito ANTES** de soltar os agentes, com **alocação nominal** (dizer qual parte fica com
  qual forma/ideia) e **faixa em vez de piso** (ex.: "nenhuma forma em mais de N"). — com o mesmo contrato, vários
  agentes convergem para a mesma fôrma; cota de piso cria o efeito pêndulo.
- Posse exclusiva de arquivo por agente; os registros por faixa/parte são juntados por um só no fim.
- **Ensaio nunca grava na pasta de outro agente**: teste vai numa subpasta própria. — ensaio que escreve no arquivo
  alheio já é trabalho, e pode destruir o dele.
