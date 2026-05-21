# Swarm Protocol — spec formal

Protocolo JSON pra hand-off entre subagents num `/claw swarm`. Estável a partir de v0.5.

## Mensagem do subagent (return)

```json
{
  "protocol_version": "1.0",
  "role": "string (required, kebab-case)",
  "status": "done | blocked | partial | error",
  "outputs": {
    "<key>": "<any>",
    "..."
  },
  "needs_from_others": [
    {
      "from_role": "string",
      "what": "string (what's needed)",
      "deadline": "iso8601 | null"
    }
  ],
  "blockers": [
    {
      "type": "auth | permission | data | external | unknown",
      "description": "string",
      "suggested_action": "string"
    }
  ],
  "next_step_suggestion": "string | null",
  "tokens_used": "int (optional, for budget tracking)",
  "elapsed_ms": "int (optional)"
}
```

## Mensagem do coordenador (dispatch)

```json
{
  "protocol_version": "1.0",
  "swarm_id": "uuid",
  "role": "string (kebab-case)",
  "goal": "string (1-2 sentences)",
  "inputs": {
    "<key>": "<any>"
  },
  "expected_outputs": ["key1", "key2"],
  "constraints": {
    "token_budget": "int | null",
    "time_budget_ms": "int | null",
    "destructive_actions_allowed": false,
    "language": "pt-BR | en-US"
  },
  "hand_off_with": ["role-a", "role-b"]
}
```

## Estados permitidos

| Status | Significado | Coordenador faz |
| --- | --- | --- |
| `done` | Outputs prontos, sem pendências | Agrega com os outros |
| `partial` | Parte dos outputs ok, parte faltou | Decide se aceita parcial ou redespacha |
| `blocked` | Não conseguiu prosseguir (auth, dado faltando) | Resolve bloqueio ou exclui do agregado |
| `error` | Falha inesperada | Loga, reporta ao user, segue sem |

## Regras de safety embutidas

1. **`destructive_actions_allowed: false` é o default.** Subagent deve **propor**, não executar (sem deletar, sem merge, sem send).
2. **Coordenador é único ponto de execução destrutiva.** E só após confirmação humana.
3. **Timeout duro: 5min.** Após isso, subagent vira `error`.
4. **Token budget compartilhado.** Coordenador pode rejeitar dispatch se budget total já estourou.

## Exemplo end-to-end

### Coordenador despacha

```json
{
  "protocol_version": "1.0",
  "swarm_id": "swarm-2026-05-21-a1b2",
  "role": "copywriter",
  "goal": "Write 3 hook variations + main copy for feature launch X",
  "inputs": {
    "feature_name": "Skill Orchestrator v0.5",
    "audience": "developers + creators using Claude Code-compatible agents",
    "tone": "BR coloquial profissional",
    "brand_kit_ref": "~/.skill-orchestrator/brand-kit.json"
  },
  "expected_outputs": ["hooks", "main_copy", "thread_twitter"],
  "constraints": {
    "token_budget": 4000,
    "time_budget_ms": 180000,
    "destructive_actions_allowed": false,
    "language": "pt-BR"
  },
  "hand_off_with": ["designer", "scheduler"]
}
```

### Subagent retorna

```json
{
  "protocol_version": "1.0",
  "role": "copywriter",
  "status": "done",
  "outputs": {
    "hooks": [
      "A skill que SE MELHORA SOZINHA.",
      "Memória cross-agent. Uma vez. Pra sempre.",
      "Swarm de subagents em produção. Não acadêmico."
    ],
    "main_copy": "...",
    "thread_twitter": ["...", "...", "..."]
  },
  "needs_from_others": [],
  "blockers": [],
  "next_step_suggestion": "Designer pode começar com o hook #2 que tem visual forte (memória)",
  "tokens_used": 2840,
  "elapsed_ms": 47200
}
```

### Coordenador agrega

Quando designer e scheduler também retornam `done`, coordenador:
1. Compila Notion page com tudo
2. Linka assets
3. Cronograma sugerido
4. Resumo 1-pager pro user revisar

---

## Não é (ainda)

- **Não é OpenAI Swarm SDK.** Inspirado mas não compatível. Spec própria, mais simples.
- **Não tem retries automáticos.** Se subagent falha, coordenador decide manualmente.
- **Não tem priority queue.** Todos disparam paralelos ou sequencial conforme dependência declarada.

## Roadmap

- [ ] Retry policy declarativa (`max_retries`, `backoff`)
- [ ] Streaming de progress entre subagents
- [ ] Cache de outputs por hash de inputs (idempotência)
