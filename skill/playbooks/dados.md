# Playbook — Dados

Exploração e relatórios envolvendo bancos de dados (Supabase) e MCPs custom de dados que o agente tiver autenticados.

## 1. Supabase exploration
**Gatilho:** "ver o banco", "quais tabelas", "estrutura do schema".

1. `Supabase.list_projects` → confirmar projeto (perguntar se >1).
2. `Supabase.list_tables` → mapa de tabelas.
3. Se user pediu query específica: `Supabase.execute_sql` (read-only por default).
4. Schema change? **Sempre** `Supabase.get_advisors` antes de `apply_migration`.
5. Migration aplicada → `Supabase.get_logs` pra confirmar sem erro.

## 2. Análise rápida de tabela
**Gatilho:** "quantos registros tem", "top N de X", "agrupa por Y".

1. `Supabase.list_tables` se nome da tabela não foi dado.
2. Montar SQL **read-only** (SELECT, sem INSERT/UPDATE/DELETE).
3. `Supabase.execute_sql` com `LIMIT` apropriado (default 100 se user não disse).
4. Devolver markdown com tabela + 1 observação relevante (outlier, padrão, gap).

## 3. Cross-source report
**Gatilho:** "relatório", "consolidar dados", "comparar fontes".

1. Listar fontes necessárias (Supabase + MCPs custom autenticados).
2. Para cada fonte: query mínima → JSON.
3. Mesclar em memória (**não** criar tabela intermediária sem permissão explícita).
4. Entregar como markdown com tabelas + 3 insights no topo.

## 4. Lead/cliente lookup (qualquer CRM/MCP)
**Gatilho:** "histórico desse cliente", "esse lead", "quem é o user X".

1. Identificar o MCP de CRM disponível (HubSpot, custom, Supabase com tabela de users…).
2. Buscar perfil + últimos N eventos/transações.
3. Se silêncio prolongado, sugerir follow-up — **nunca enviar mensagem sem confirmação explícita**.

## 5. Health check de serviço externo
**Gatilho:** "como tá o sistema", "tá tudo no ar", "monitorar X".

1. Endpoint de status / dashboard summary do MCP correspondente.
2. Listar anomalias (erro, offline, queda de volume).
3. Sugerir 1 ação concreta — não 5. Foco no maior risco.
