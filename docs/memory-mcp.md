# Memory MCP — memória cross-agent

A skill orchestrator inclui um **MCP server opcional** (`tools/skill-memory/`) que permite **memória compartilhada entre os 3 agents** (OpenClaw, Hermes, Claude Code) rodando na mesma máquina.

## Por que vale

Cada agente tem sua própria memória interna. Se você roda 2-3 em paralelo, cada um sabe coisas diferentes. Esse MCP unifica: SQLite local único em `~/.skill-orchestrator/memory.db`, 4 tools simples, todos os agents que conectam veem o mesmo state.

**Zero rede. Privacidade total.**

## Status: opcional, complementar

A skill **não exige** este MCP. As features principais (matriz, slashes, modos, swarm) funcionam sem ele. Quando o MCP está disponível, a skill **prefere** usar `remember`/`recall` ao invés de `~/.skill-orchestrator/stats.json` pra contexto persistente — porque vira cross-agent.

## Setup

Veja [`tools/skill-memory/README.md`](../tools/skill-memory/README.md) pra:
- Install (`npm install`)
- Conectar no Claude Code (`~/.claude/config.json`)
- Conectar no Hermes (config YAML)
- Conectar no OpenClaw (plugin MCP)

## Comportamento esperado dentro da orchestrator

Quando o agent percebe `skill-memory` disponível:

1. **Antes de perguntar preferência ao user**, sempre `recall(key: "<preferencia>")` primeiro.
2. **Após decisão importante**, `remember` com tag relevante.
3. **Em modo persistente** (`/claw --mode dev fixa`), gravar via `remember(key: "mode_default", value: "dev")` ao invés de arquivo local.
4. **Brand kit, perfil do user, decisões arquiteturais** — tudo passa por aqui.

Quando o MCP **não** está disponível → fallback graceful pro arquivo local `~/.skill-orchestrator/stats.json`. Nunca trava.

## Como saber se está disponível

No início da sessão, tente `recall(key: "__health__")`. Se a tool existir → MCP ativo. Se erro "tool not found" → fallback local.

## Anti-padrões

- ❌ Gravar dados sensíveis (tokens, senhas, números de cartão) no memory MCP. Use secrets manager dedicado.
- ❌ Tornar a skill dependente do MCP. Funcionalidade core sempre funciona sem ele.
- ❌ Memory poison: se um agent escreve lixo, todos veem. Combine com auditoria via `/claw audit`.
