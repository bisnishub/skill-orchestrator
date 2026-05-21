# Playbook — Multi-Agent Swarm

`/claw swarm <objetivo>` dispara N subagents em paralelo, cada um com playbook próprio. A Orchestrator vira **maestro**: decompõe, distribui, coordena hand-offs, agrega resultados.

## Quando usar swarm vs. despacho normal

| Cenário | Use |
| --- | --- |
| 1 tool, 1 ação | Despacho normal (`/claw triage`) |
| Pipeline sequencial de 2-3 passos | Playbook composto (carrega `playbooks/X.md`) |
| 4+ tarefas **paralelizáveis** com hand-offs | **Swarm** (`/claw swarm`) |

Regra prática: se o objetivo tem 4+ subobjetivos **independentes** (não esperam um pelo outro), vale swarm.

## Fluxo

### 1. Decomposição

Ao receber `/claw swarm <objetivo>`:

1. Identificar **3-7 papéis** necessários. Exemplos:
   - "Campanha de lançamento" → designer, copywriter, analista, scheduler, monitor
   - "Migração de schema" → arquiteto, dev backend, dev frontend, QA, doc writer
   - "Análise de concorrente" → pesquisador, analista financeiro, analista de produto, sintetizador
2. Para cada papel, mapear o **playbook** ou **prompt-base** correspondente.
3. **Mostrar o plano** ao user antes de disparar — ele aprova ou ajusta.

### 2. Fan-out — disparar subagents

Forma de dispatch varia por host agent:

**Claude Code:** usa `Agent` tool com `subagent_type` e prompts dedicados:

```
Agent({
  description: "Copy hooks for campaign",
  subagent_type: "general-purpose",
  prompt: "Write 3 hook variations for [contexto]. Output as JSON array..."
})
```

**OpenClaw / Hermes:** usa o equivalente do agent (consultar docs do host).

Disparar **em paralelo** quando independentes (UM tool call com múltiplos `Agent`). Sequencial quando há dependência.

### 3. Protocolo de hand-off (JSON estruturado)

Cada subagent retorna no formato:

```json
{
  "role": "copywriter",
  "status": "done",
  "outputs": {
    "hooks": ["...", "...", "..."],
    "main_copy": "..."
  },
  "needs_from_others": [],
  "blockers": [],
  "next_step_suggestion": "designer pode começar agora com os hooks"
}
```

Se `status: "blocked"` ou `needs_from_others` não vazio:
- Não declarar terminado.
- Coordenador resolve a dependência ou redespacha.

### 4. Agregação

Quando todos os subagents retornam `done`:

1. Coletar todos os `outputs`.
2. Validar consistência (datas batem? brand kit foi respeitado em todos os assets?).
3. Compor entregável único — geralmente um documento (Notion page, Google Doc, ou pasta com tudo).
4. Resumo executivo no topo: o quê foi entregue, quem fez, próximos passos.

## Exemplos

### Exemplo 1 — Campanha de lançamento

```
/claw swarm lançar feature X com campanha em 5 dias
```

**Plano proposto:**

| Papel | Playbook | Output esperado |
| --- | --- | --- |
| Copywriter | `criador-conteudo.md` §2 | 3 variações de hook + main copy + thread Twitter |
| Designer | `criador-conteudo.md` §1.5 (thumb) | Thumb hero + 3 social cards + favicon |
| Analista | `pesquisa.md` §2 | Benchmark vs. competidores |
| Scheduler | `produtividade.md` §2 | Cronograma 5 dias com posts agendados |
| Monitor | `dados.md` §5 (health check) | Dashboard de métricas pós-lançamento |

Após plano aprovado → dispara 5 subagents em paralelo → coleta → entrega pasta `/campanha-X-{date}/`.

### Exemplo 2 — Briefing 360° de cliente

```
/claw swarm briefing completo do cliente Acme
```

Subagents:
- **CRM lookup** → histórico do account, deals, contatos (via `comercial.md` §5 pré-call)
- **News scan** → últimas 90d de notícias da empresa (via `pesquisa.md`)
- **LinkedIn snapshot** → mudanças de chave (saídas, hires) — só dados públicos
- **Internal notes** → email/Notion/Drive references ao cliente

Coordenador agrega → 1 pager com tudo.

### Exemplo 3 — Code review massivo

```
/claw swarm review todos os PRs abertos
```

Cada PR vira um subagent paralelo (até 5 em paralelo pra não saturar):
- Cada um roda `engenheiro-solo.md` §2 no PR designado
- Retorna `{pr_id, summary, blockers, risk}`
- Coordenador prioriza: ready → quick wins → bloqueados

## Limites e safety

- **Cap em 7 subagents simultâneos.** Mais que isso vira ruído + custo.
- **Token budget total visível.** Pra cada swarm, estimar custo agregado antes de disparar. Se > limit aceito, perguntar.
- **Nenhum subagent toma ação destrutiva sozinho.** Operações tipo `merge PR`, `apply migration`, `send email` voltam pro coordenador, que pede confirmação humana.
- **Timeout por subagent: 5 minutos default.** Se travou, marcar como blocked, seguir sem ele, reportar gap.
- **Logging obrigatório.** Cada subagent loga no `~/.skill-orchestrator/log.jsonl` com `tool: "swarm-<role>"` pra auditoria depois.

## Padrão de prompt pro subagent

Quando você delega via `Agent` tool, o prompt deve ter:

```
ROLE: <papel exato>
GOAL: <o que entregar — 1-2 linhas concretas>
INPUTS: <o que ele recebe — context, dados prévios, brand kit, etc>
OUTPUTS: <formato esperado — JSON com chaves específicas>
CONSTRAINTS:
  - Não tome ações destrutivas. Retorne propostas, não execute.
  - Limite: <budget tokens / tempo>
  - Idioma: pt-BR
HAND-OFF: ao terminar, retorne JSON no protocolo (role, status, outputs, blockers, next_step).
```

Quanto mais específico, melhor o output. Vago = ruim.

---

## Comparação rápida — quando NÃO usar swarm

- Tarefa simples (1-2 tools) → despacho normal é mais barato
- Coisa que precisa decisões humanas no meio → não automatize com swarm
- Dados sensíveis multi-stage → menor superfície de erro com pipeline sequencial humano-no-meio
- Custo: cada subagent é uma chamada API. Faz a conta antes.
