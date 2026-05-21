# Playbook — Pesquisa / Análise

Pesquisa estruturada com web search + scraping + síntese. Destino padrão: Notion (relatório navegável) ou Markdown local.

## 1. Pesquisa estruturada (`/claw research <tópico>`)
**Gatilho:** "/claw research", "pesquisa sobre X", "estudo de mercado de Y".

Pipeline em 4 fases:

### Fase 1 — Escopo (1 pergunta máx)

Antes de gastar tempo, confirme:
- **Profundidade**: overview (30min de leitura), análise (relatório de 5-10 páginas), ou deep-dive (relatório completo com fontes)?
- Se user já disse, pule essa pergunta.

### Fase 2 — Coleta

1. Web search inicial: 5-10 fontes primárias (sites oficiais, papers, estudos, reportagens reputadas).
2. Para cada fonte: `WebFetch` ou `ctx_fetch_and_index` (preserva contexto longo no sandbox).
3. Priorizar: fontes **2024-2026**, autores reconhecidos no campo, dados quantitativos.
4. **Não** usar blogs com paywall ou sites com conteúdo gerado por IA óbvio.

### Fase 3 — Síntese

Estrutura padrão do relatório:

1. **TL;DR** (3-5 bullets — o que importa)
2. **Contexto** (1 parágrafo — por que esse tema agora)
3. **Achados principais** (5-8 seções, cada uma com fonte citada)
4. **Tensões / discordâncias** (onde as fontes discordam — IMPORTANTE, não esconder)
5. **Implicações** (e daí? — 3 ações ou decisões que decorrem)
6. **Fontes** (lista numerada, com URL e data de acesso)

### Fase 4 — Destino

Perguntar **uma** vez (se não foi dito):
- Notion (cria página com toggle headers)
- Markdown local (entrega arquivo)
- Google Doc (`Drive.create_file`)

## 2. Comparativo de empresas/produtos
**Gatilho:** "compare X vs Y", "qual ferramenta melhor pra Z", "matriz de comparação".

1. Definir **critérios** explícitos (preço, features, suporte, integrações, etc) — perguntar se não foi dado.
2. Para cada opção, buscar:
   - Site oficial (feature list, pricing)
   - 2-3 reviews independentes (G2, Capterra, threads de Reddit/HN com substância)
3. Tabela markdown comparativa: linhas = critérios, colunas = opções.
4. **Veredito honesto**: melhor pra cada perfil (ex: "Opção A pra time pequeno; Opção B pra escala enterprise").
5. Citar fontes sempre.

## 3. Scraping de dados públicos
**Gatilho:** "extrai dados de X", "lista de Y do site Z", "scraping legal".

**Antes de scrappear, verificar:**

- O site tem API? Use a API primeiro.
- `robots.txt` permite? Se proibido, **NÃO** scrapeie.
- Dados são públicos? Login required = não público = não scrapeie sem autorização.

Se OK:

1. `WebFetch` ou `ctx_fetch_and_index` numa página representativa.
2. Identificar padrão (HTML/seletor).
3. Iterar com paginação respeitando rate limit (1 req/s default — não martelar).
4. Salvar como CSV/JSON.
5. **Não republicar** dados sem atribuição à fonte.

## 4. Monitoramento de tópico
**Gatilho:** "fica de olho em X", "me avisa quando sair algo sobre Y".

1. Não tente fazer streaming/polling no agente — peso desnecessário.
2. Propor: cron diário/semanal que faz a busca e envia resumo via canal (Telegram, email).
3. Setup do cron varia por agente (`openclaw schedule create`, Hermes cron, Claude Code cron via skill `/loop`).
4. Entregar comando exato pro agente do user.

## 5. Verificação de fato (fact-check)
**Gatilho:** "isso é verdade?", "vi alguém falando X, procede?", "checar essa estatística".

1. Localizar a **fonte original** (não acreditar em terceiro que cita).
2. Verificar **data** (estatísticas de 2018 podem estar desatualizadas).
3. Conferir contexto (números fora de contexto enganam).
4. Conclusão em 3 níveis: **confirmado**, **parcialmente verdadeiro** (com nuance), **falso**.
5. Sempre linkar a fonte definitiva.

---

**Princípios:**

- **Fontes > opiniões.** Toda afirmação importante precisa de origem rastreável.
- **Discordância > consenso forçado.** Quando fontes divergem, exponha — não esconda pra parecer mais "limpo".
- **Recente > antigo.** Especialmente em tech/mercado, preferir últimos 18 meses.
- **Não invente números.** Se não achou dado, diga "não encontrei". Pior que dado faltando é dado inventado.
- **Respeite robots.txt e termos de uso.** Pesquisa ética > atalho.
