# Modo: Mapas (sub-mapa de Região, mapa-múndi, mapa-modelo dos lados, mapa de Narraris)

Regras: [../regras/cenarios-mapas-capas.md](../regras/cenarios-mapas-capas.md) §2 (sub-mapa) e §3 (mundi e
mapa-modelo). Tamanhos: [../regras/formatos.md](../regras/formatos.md). Anexos:
[../referencias/REFERENCIAS.md](../referencias/REFERENCIAS.md). Sessões e ONDE SALVAR:
[../regras/fluxo-sessoes.md](../regras/fluxo-sessoes.md).

- **Entra:** sub-mapa — a Região (bioma, conceito, tipo: comum, reino, bastião ou porto), a lista de lugares (com marco
  e posição no quadro), as ligações entre eles e o ponto da Região no mundi; mundi — as terras, cada uma com posição,
  proporção, silhueta e paleta. Quem fornece é o usuário (a skill não tem banco).
- **Sai:** `finais/mapa_<id>.png` **1536×1024** (sub-mapa, lados, mundi) ou **1586×992** (mapa de Narraris), mais
  `entregas.json` e `ENTREGA.md`.
- **Pinos e coordenadas não são da skill.** A skill entrega a arte com os lugares **visíveis, separados e fáceis de
  apontar** e as trilhas pintadas; marcar os pinos, gravar coordenadas e conexões é do processo de cadastro, que roda
  por cima desta arte. Por isso a arte **nunca é recortada** depois de gerada (pino é pixel).

## Pasta do lote

```
<lote>/
├── plano.md                       lugares (marco + posição), ligações, tipo de Região; fundos dos Locais (se houver)
├── referencias/mundi_recorte_<id>.jpg   recorte do mundi em volta do ponto (sub-mapa)
├── prompts/  mapa_<id>.txt | mundi_<id>.txt  (+ <id>.txt dos fundos)
├── PROMPT_<LOTE>.md               sessão de imagem (templates/mapas/PROMPT_SUBMAPA.md ou PROMPT_MUNDI.md)
├── brutos/mapa/ (sub-mapa)   brutos/ (fundos)   finais/   conferencia/   validacao/
├── entregas.json
└── ENTREGA.md
```

## Sub-mapa — fluxo (o mapa inteiro, sem parar entre fases)

1. **Plano** (`plano.md`): N lugares distintos, cada um com UM marco visual e uma posição no quadro, com folga entre
   eles e da borda; ligações (trilha, estrada, escadaria, ponte sobre rio — nunca sobre o mar); o lugar mais perigoso
   no ponto mais alto e mais distante; acréscimo do tipo de Região (§2). Se o mapa também ganha fundos de Local, faça
   já o plano de fundos do [modo cenários](cenarios.md) (passo 1 de lá).
2. **Recorte do mundi** em volta do ponto da Região, a partir de `${CLAUDE_SKILL_DIR}/referencias/mapas/mundi-mascris-completo.jpg`
   (ou do mundi que o usuário fornecer): uma janela de cerca de 1/3 da largura e 1/3 da altura do mundi, centrada no
   ponto (na arte de 1536×1024, 480×320 px), ampliada para 1536×1024 e salva em
   `<lote>/referencias/mundi_recorte_<id>.jpg` — nunca na skill. Ainda não há script para isso: use um editor de
   imagem. O recorte dá bioma, relevo e contorno; o sub-mapa copia só a geografia, nunca o traço de pergaminho.
3. **Prompt** em `prompts/mapa_<id>.txt` com o texto fixo de
   [`templates/mapas/PROMPT_SUBMAPA.md`](../templates/mapas/PROMPT_SUBMAPA.md) (frase dos anexos + molde + acréscimo do
   tipo). Prompts dos fundos, se houver: [modo cenários](cenarios.md) passo 2.
4. **PROMPT da sessão:** copie o template para `<lote>/PROMPT_<LOTE>.md`, troque `{PASTA_LOTE}`, `{SKILL}`, `{LOTE}`,
   `{id}`, `{N}`; anexos na ordem: `submapa-kaiangue.jpg` (sempre) + `submapa-aita.jpg` (cidade grande) ou
   `submapa-ossario.jpg` (bioma sem mar) + o recorte do mundi. Na "Fase 2", cole a FILA de fundos de
   `templates/cenarios/PROMPT_FUNDOS.md`. Fila cheia antes de gerar.
5. **Sessão de imagem:** gera o sub-mapa e, em seguida, os fundos, sem parar.
6. **Ajustar e medir:**

   ```
   python "${CLAUDE_SKILL_DIR}/scripts/fundos_normalizar.py" <lote> --destino submapa --entrada brutos/mapa
   python "${CLAUDE_SKILL_DIR}/scripts/fundos_normalizar.py" <lote> --destino local
   ```

   O sub-mapa fica em `brutos/mapa/` e os fundos na raiz de `brutos/` (o script não desce em subpastas). Mapa: **só redimensiona**, PNG; proporção longe de 3:2 vira
   aviso de distorção (gere de novo na proporção certa se aparecer). Luminância e bordas são só aviso no mapa.
7. **Conferir no olho:** os N lugares aparecem e dá para apontar cada um; as trilhas estão pintadas; nada escrito,
   sem moldura, sem criatura; a geografia lembra o recorte; nenhuma ponte sobre o mar; a muralha (se houver) é a de
   sempre (§2).
8. **Entrega:** em `entregas.json`, acrescente ao registro do mapa a lista `lugares` (nome + onde está no quadro, como
   foi pedido) para o cadastrador achar cada um; `ENTREGA.md` com o que precisa de olho humano; linha no `ENTREGAS.md`.

## Mapa-múndi e mapa-modelo dos lados

1. Posições e proporções de cada terra **escritas** em porcentagem do quadro (o esquema de posições é só para o dono
   conferir; nunca vai anexado).
2. Prompt em `prompts/mundi_<id>.txt` com o texto fixo de
   [`templates/mapas/PROMPT_MUNDI.md`](../templates/mapas/PROMPT_MUNDI.md); PROMPT da sessão a partir do mesmo
   template. Só texto + no máximo uma imagem de traço; **conversa nova**; tentativa nova = `_v2`, `_v3`.
3. Ajustar: `fundos_normalizar.py <lote> --destino mundi` (1536×1024, só redimensiona; a moldura do mundi é proposital,
   então a borda não é medida). Mapa de Narraris (prompt pede 1600×1000): `--destino narraris_mapa` (1586×992).
4. Conferir no olho pelos critérios do §3 (terras separadas e reconhecíveis, cores só dentro das terras, sem letra na
   rosa dos ventos) e entregar como no sub-mapa.
