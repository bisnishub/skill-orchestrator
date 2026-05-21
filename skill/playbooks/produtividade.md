# Playbook — Produtividade

Encadeamentos comuns envolvendo Gmail, Calendar, Drive, Notion.

## 1. Inbox triage diária
**Gatilho:** "limpa inbox", "triagem", "o que tem de importante hoje".

1. `Gmail.search_threads` com `is:unread newer_than:1d` (limit 30).
2. Para cada thread: classifique em **AÇÃO / FYI / LIXO** baseado em remetente + assunto.
3. AÇÃO → criar evento Calendar com `Calendar.create_event` (block 15min, mesmo dia) **OU** draft de resposta com `Gmail.create_draft`.
4. FYI → label "FYI" com `Gmail.label_thread`.
5. LIXO → label "Archive-Bot" (não deletar — auditável).
6. Reportar: `{ação: N, fyi: N, lixo: N}` + top 3 ações.

## 2. Agenda da semana
**Gatilho:** "minha semana", "agenda da semana", "o que tenho".

1. `Calendar.list_events` próximos 7 dias.
2. Agrupar por dia, marcar conflitos.
3. Sugerir 3 blocos de foco profundo (2h cada) em horários sem reunião usando `Calendar.suggest_time`.
4. Se user aprovar → criar com `Calendar.create_event` título "🧠 Foco".

## 3. Doc → Notion
**Gatilho:** "joga isso no Notion", "salva como página".

1. Se origem é Drive: `Drive.read_file_content` → markdown.
2. Se origem é arquivo local: ler direto.
3. Autenticar Notion se necessário (`Notion.authenticate`).
4. Criar página na database default da CCB (perguntar workspace se múltiplos).
5. Devolver link.

## 4. Reunião → Follow-up
**Gatilho:** "depois da call", "follow-up", "next steps daquela reunião".

1. Pegar última transcrição (Zoom MCP / Google Meet plugin).
2. Extrair: decisões, action items, donos, prazos.
3. Para cada action item com dono ≠ user: draft email via `Gmail.create_draft`.
4. Para cada action item do user: criar evento Calendar OU página Notion (perguntar).
