# Playbook — Dados

Supabase, Eletroposto MCP, cross-source reports.

## 1. Supabase exploration
**Gatilho:** "ver o banco", "quais tabelas", "estrutura do schema".

1. `Supabase.list_projects` → confirmar projeto (perguntar se >1).
2. `Supabase.list_tables` → mapa.
3. Se user pediu query específica: `Supabase.execute_sql` (read-only por default).
4. Schema change? **Sempre** `Supabase.get_advisors` antes de `apply_migration`.
5. Migration aplicada → `Supabase.get_logs` pra confirmar sem erro.

## 2. Eletroposto health check
**Gatilho:** "como tá o eletroposto", "estações", "transações de hoje".

1. `spark_dashboard_summary` → visão geral.
2. `spark_station_status` → estações offline/erro.
3. Se houver offline: `whatsapp_notify_admin` com lista.
4. `spark_list_transactions` last 24h → outliers (valor zero, duração > 8h).
5. Reportar em bloco resumido + 1 ação recomendada.

## 3. Lead lookup
**Gatilho:** "quem é o CPF X", "esse lead", "histórico do cliente".

1. `spark_get_user_by_cpf` → perfil.
2. `spark_list_transactions` filtrado por user.
3. Se silêncio > 30 dias → propor follow-up via `whatsapp_send_text` (perguntar antes de enviar).

## 4. Cross-source report (Supabase + Eletroposto)
**Gatilho:** "relatório", "consolidar dados", "comparar fontes".

1. Listar fontes necessárias.
2. Para cada fonte: query mínima → JSON.
3. Mesclar em memória (não criar tabela intermediária sem permissão).
4. Entregar como markdown com tabelas + 3 insights no topo.
