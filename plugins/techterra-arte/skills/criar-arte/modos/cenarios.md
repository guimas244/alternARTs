# Modo: Cenários (fundo de batalha do Local, fundo dos lados, portão da Jornada)

Regras de composição (o porquê de cada exigência): [../regras/cenarios-mapas-capas.md](../regras/cenarios-mapas-capas.md)
§1 (fundo de Local) e §4 (portão). Tamanhos: [../regras/formatos.md](../regras/formatos.md). Anexos:
[../referencias/REFERENCIAS.md](../referencias/REFERENCIAS.md). Sessões e ONDE SALVAR:
[../regras/fluxo-sessoes.md](../regras/fluxo-sessoes.md). Ambiente (ChatGPT, Codex, Claude Code):
[../regras/ambiente.md](../regras/ambiente.md). `{SKILL}` = a pasta desta skill (onde está o SKILL.md); `<lote>` = a
pasta do lote (no ChatGPT web, `/mnt/data/<lote>`; no ChatGPT desktop, a pasta local).

- **Entra:** o mapa (nome, identidade em 1 frase, paleta por nome, luz/atmosfera) e a lista de Locais (nome, descrição
  em 2 frases, marco, vizinhos). Quem fornece é o usuário (a skill não tem banco).
- **Sai:** `finais/<id>.jpg` — fundo de Local **1672×941**, fundo dos lados **1536×864**, portão **1600×900** — mais
  `entregas.json` e `ENTREGA.md`.
- **Capa de Jornada:** sem regra própria ainda — pergunte ao usuário antes de gerar.

## Pasta do lote

```
<lote>/
├── plano.md             tabela Local → marco → "próprio" / "usa o fundo de <Local>" (+ motivo de cada próprio)
├── prompts/<id>.txt     um por fundo próprio (texto fixo do template + o {} preenchido)
├── PROMPT_<LOTE>.md     sessão de imagem (de templates/cenarios/PROMPT_FUNDOS.md)
├── brutos/              o que a IA entregou (<id>.png, <id>_v2.png…, <arquivo>.prompt.txt ao lado; portões em brutos/portao/)
├── finais/              <id>.jpg no tamanho do destino (+ <id>.jpg.prompt.txt)
├── conferencia/         prancha_<destino>.jpg; <id>_grade.jpg nos portões
├── validacao/           geracoes_fundos.json (sessão de imagem)
├── entregas.json        um registro por imagem (gerado/atualizado pelo script)
└── ENTREGA.md           resumo e pendências
```

`id` = `NN_<slug_do_local>` (NN = ordem no mapa, 2 dígitos; minúsculas, sem acento, `_`). Portão: `portao_<tema>`.

## Fluxo

1. **Plano dos fundos** (`plano.md`), antes de qualquer prompt — regra "Fundo próprio × reaproveitado" do §1:
   próprio só para cidade(s), Local final e marco único; Locais genéricos do mesmo bioma e luz dividem fundo (2 a 4
   por fundo, nunca dois vizinhos); fundos novos ≤ metade dos Locais; outro mapa só como plano B. Cada Local diz
   "próprio" ou "usa o fundo de <Local>". Plano fora disso: refaça antes de escrever prompt.
2. **Um prompt por fundo próprio** em `prompts/<id>.txt`, com o texto fixo de
   [`templates/cenarios/PROMPT_FUNDOS.md`](../templates/cenarios/PROMPT_FUNDOS.md) (Local, lados ou portão), trocando
   só o `{}`. Paleta por nome, nunca hex; suporte liso nomeado (lombadas, placas, estandartes) quando houver.
   Escolha a referência de `referencias/cenarios/` que mais combina com cada Local (tabela em REFERENCIAS.md). Portão:
   sem anexo; tema novo repete a planta trocando só material, luz e paleta.
3. **PROMPT da sessão:** copie o template para `<lote>/PROMPT_<LOTE>.md`, troque `{PASTA_LOTE}` (pasta absoluta do
   lote), `{SKILL}` (caminho absoluto da pasta da skill) e `{LOTE}`, preencha a FILA (todos os fundos próprios, com o
   anexo de cada um) e apague a caixa do topo e o "Texto fixo". Fila cheia antes de gerar.
4. **Geração das imagens:** no ChatGPT/Codex, a própria conversa segue o `PROMPT_<LOTE>.md` e gera; no Claude Code,
   entregue a frase para colar no ChatGPT/Codex. Gera a fila inteira em `brutos/`, uma vez cada; refaz do zero só por
   erro real, no máximo 3 imagens.
5. **Normalizar e medir:**

   ```
   python "{SKILL}/scripts/fundos_normalizar.py" <lote> --destino local     # ou --destino lados
   python "{SKILL}/scripts/fundos_normalizar.py" <lote> --destino portao --entrada brutos/portao
   ```

   Fundos: recorte 16:9 pelo centro + redução; portão: **só redimensiona** (a interface é posicionada em % da arte).
   Mede luminância (70–200), desvio do terço central (≥ 25) e bordas (moldura). Fundo de Local/lados fora da medida
   **não é gravado** (REPROVADA): gere de novo do zero com a frase da tabela "O que costuma voltar errado". `--aceitar`
   só quando o dono decidir manter. Portão: as medidas viram aviso; confira em `conferencia/<id>_grade.jpg` (portões,
   pilar e as três faixas livres no lugar). O script lê só os arquivos da pasta de entrada (não desce em
   subpastas): por isso o portão fica em `brutos/portao/`.
6. **Conferir no olho** (a medida não vê) pela `conferencia/prancha_<destino>.jpg`: câmera na altura do olho;
   horizonte no terço de cima; cobrindo as laterais, o centro ainda diz qual é o lugar; chão do centro aberto; nenhuma
   letra ou glifo; nenhum bicho ou pessoa em primeiro ou meio plano.
7. **Entrega:** complete em `entregas.json` o `nome` de cada Local e, nos fundos compartilhados, `locais` (quem usa
   aquele fundo) — o script preserva esses campos. Escreva `ENTREGA.md` (próprios × reaproveitados, luminância mínima,
   pendências e o que precisa de olho humano) e acrescente a linha no `ENTREGAS.md` da pasta de trabalho. No ChatGPT web,
   entregue o lote como `.zip` (no desktop, a própria pasta).

Ligar o fundo aos Locais no jogo (subir imagem, preencher o Local) é do processo de cadastro, fora da skill.
