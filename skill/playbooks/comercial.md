# Playbook — Comercial / Vendas

Pipeline lead → qualificação → proposta → follow-up. Funciona com qualquer CRM via MCP autenticado (HubSpot, Pipedrive, Salesforce, ou tabela Supabase custom).

## 1. Triagem de leads novos
**Gatilho:** "leads novos", "quem entrou hoje", "novos cadastros".

1. Listar leads criados nas últimas 24-48h via MCP do CRM.
2. Classificar por **fit** (regras combinadas com o user, ex: porte da empresa + cargo + setor):
   - **HOT** → fit alto + sinal de intenção (preencheu form completo, baixou material premium)
   - **WARM** → fit alto sem sinal forte
   - **COLD** → fit baixo
3. Para HOT: propor outreach personalizado **hoje** (template + perguntar antes de enviar).
4. Para WARM: agendar follow-up em 2-3 dias.
5. Para COLD: nurture sequence (newsletter, conteúdo) — não outreach 1:1.

## 2. Qualificação (BANT ou MEDDIC light)
**Gatilho:** "qualificar lead X", "vale a pena esse lead", "esse cara é cliente?".

Estrutura mínima de qualificação (BANT light):

- **Budget** — tem verba pra isso ou seria gasto novo?
- **Authority** — fala com quem decide?
- **Need** — dor está clara ou ainda explorando?
- **Timeline** — quando precisaria?

1. Buscar histórico no CRM (todas interações).
2. Se faltam respostas → sugerir email de discovery (5 perguntas curtas, **não** questionário de 20 itens).
3. Se qualificado → mover stage no CRM + criar evento de discovery call.
4. Se não-qualificado → mover pra nurture com motivo registrado (não deletar — pode voltar).

## 3. Follow-up de leads silenciosos (`/claw followup`)
**Gatilho:** "/claw followup", "quem tá parado", "leads sem resposta".

1. Buscar no CRM leads com **última interação > 7 dias** + status "em conversa".
2. Para cada um, identificar **a última coisa que ficou pendente** (resposta de proposta, agendamento, dúvida).
3. Gerar draft de follow-up com:
   - Referência ao último contato ("conforme conversamos sobre X")
   - Valor novo (insight, estudo, case) — nunca "só passando pra ver se viu meu último email"
   - CTA simples (1 pergunta sim/não OU link pra agendamento)
4. Listar tudo em batch — user aprova quais enviar (**nunca** mandar sem confirmação).

## 4. Proposta / orçamento
**Gatilho:** "preparar proposta pra X", "orçamento", "comercial pra fechar".

1. Levantar contexto da oportunidade: dor, escopo, prazo, budget indicado.
2. Estrutura de proposta:
   - **Contexto** (1 parágrafo — o que ouvi)
   - **Solução proposta** (escopo claro, o que entra e **o que NÃO entra**)
   - **Timeline** (marcos, não datas exatas se não houver compromisso)
   - **Investimento** (3 opções quando faz sentido: lean / standard / premium)
   - **Próximos passos** (1-2 ações concretas, com prazo)
3. Saída: Google Docs ou PDF (perguntar formato).
4. Se for orçamento simples (1 página), gerar markdown convertível.

## 5. Discovery call — prep e pós
**Gatilho:** "tenho call com X amanhã", "preparar reunião comercial", "depois daquela call".

**Pré-call** (24h antes):
1. Pesquisa rápida: LinkedIn da pessoa, site da empresa, últimas notícias (via WebFetch).
2. Briefing 1-página: contexto + 5 perguntas-chave + objetivos da call.
3. Salvar em Notion ou Drive ligado ao card do CRM.

**Pós-call** (mesmo dia):
1. Anotações estruturadas: dor identificada, próximos passos, prazos, objeções.
2. Atualizar card do CRM.
3. Draft de follow-up email com **action items concretos** (não "foi um prazer conversar").
4. Agendar próximo touchpoint.

## 6. Pipeline review semanal
**Gatilho:** "como tá meu pipeline", "review semanal", "forecast".

1. Listar oportunidades por stage com **valor previsto × probabilidade**.
2. Identificar:
   - **Risco** — oportunidades sem movimento há >14 dias
   - **Quick wins** — late-stage prováveis de fechar em 30d
   - **Forecast realista** (não otimista) pro mês
3. Sugerir foco da semana: top 3 ações que movem mais agulha.

---

**Princípios:**

- **Não automatize outreach 1:1.** Pode dar draft, **nunca** envia sem aprovação.
- **CRM é fonte de verdade.** Antes de inventar contexto, busque histórico.
- **Valor antes de pedido.** Todo follow-up traz algo novo, não só lembrete.
- **Honestidade > pressão.** Lead não-qualificado é nurture, não força-venda.
- **Privacidade.** Não logue dados de leads na telemetria local (use só categoria, não nomes).
