# Exemplos práticos

Conversas reais que a `orchestrator` resolve sozinha.

---

### Triage matinal

> **Você:** bom dia, dá uma olhada no inbox e me fala o que importa hoje

**Orchestrator:**

```
Vou usar Gmail.search_threads (filtro is:unread newer_than:1d, limit 30)
porque o pedido é triagem de inbox recente — playbook produtividade #1.
```

→ classifica em AÇÃO / FYI / LIXO, sugere 3 ações, label e arquiva o resto.

---

### Live na quinta

> **Você:** vou fazer live na quinta sobre Supabase RLS. me ajuda?

**Orchestrator:**

```
Pedido combina "conteúdo OpenClaw Brasil" + "mídia". Vou seguir
playbooks/conteudo-openclaw.md #1 (Live CCB do zero).
```

→ gera roteiro teleprompter, adapta slides, prepara thumbnail via Higgsfield, monta checklist de live.

---

### Cross-source report

> **Você:** preciso cruzar usuários do supabase com leads do nosso CRM

**Orchestrator:**

```
Pedido cruza duas fontes (Supabase + CRM via MCP). Playbook dados.md #3
(cross-source report). Vou puxar JSON de cada fonte e mesclar.
```

→ `Supabase.execute_sql` + MCP do CRM autenticado, merge em memória, devolve markdown com tabela e 3 insights.

---

### Onboarding de membro novo

> **Você:** /claw o joão acabou de entrar na CCB e nunca usou OpenClaw

**Orchestrator:**

```
Setup/onboarding → playbooks/setup-openclaw.md. Pulando direto pro
despacho porque você usou /claw.
```

→ devolve sequência de passos personalizada (Mac vs Linux, VPS ou local, canais a conectar, skills CCB pra instalar).

---

### Pedido ambíguo (ela pergunta UMA coisa)

> **Você:** quero automatizar aquilo

**Orchestrator:**

```
Pedido ambíguo. Uma pergunta: "aquilo" é (a) inbox / agenda,
(b) algo no banco / CRM, ou (c) outra coisa?
```

→ sem inventar, sem listar 10 opções. Uma pergunta, despacha na resposta.
