# Playbook — Auto-improvement (a skill que melhora sozinha)

A Orchestrator não é estática. Ela observa cada despacho, identifica padrões, e **propõe mudanças na própria matriz de roteamento**. Você revisa e aprova — ela aplica.

## Como funciona

### 1. Logging de cada despacho

Após cada despacho bem-sucedido, **anexar** uma linha JSON em `~/.skill-orchestrator/log.jsonl`:

```json
{"ts":"2026-05-21T14:32:11Z","intent":"manda email pro joão sobre a proposta","domain":"produtividade-email","tool":"Gmail.create_draft","mode":"default","success":true}
```

Campos obrigatórios:
- `ts` — ISO 8601 UTC
- `intent` — o texto do user (truncar a 200 chars; **não** registrar dados sensíveis)
- `domain` — nome do domínio da matriz
- `tool` — tool/MCP principal usado
- `mode` — modo ativo (`default`, `dev`, `editor`, etc)
- `success` — true se o despacho foi concluído sem erro

**Privacidade:** se o intent contém dados sensíveis (CPF, email pessoal de terceiros, token), substituir por `<REDACTED>` antes de logar. Nunca registrar valores de campos como senha, token, segredo.

### 2. Comando `/claw audit`

Quando o user pedir auditoria (`/claw audit` ou "o que você aprendeu sobre mim"):

1. Ler `~/.skill-orchestrator/log.jsonl` (últimos 200 entries).
2. Rodar análise via `tools/audit/audit.py` (Python puro, sem deps):
   ```
   python3 tools/audit/audit.py ~/.skill-orchestrator/log.jsonl
   ```
3. O script retorna JSON com **propostas de mudança**:
   - `new_routes` — gatilhos novos pra rotas existentes (frases recorrentes não-mapeadas)
   - `promote_to_slash` — sequências com 5+ usos viram candidatas a slash batizado
   - `noise_terms` — termos que aparecem muito mas confundem classificação
4. Mostrar ao user em formato legível + perguntar: "Aplicar essas N mudanças no SKILL.md?"

### 3. Aplicação automática (com confirmação)

Se user aprovar:

1. **Backup** primeiro: `cp skill/SKILL.md skill/SKILL.md.bak-$(date +%Y%m%d-%H%M%S)`
2. Editar `skill/SKILL.md`:
   - **Adicionar** gatilhos novos na coluna "Sinais" das linhas correspondentes
   - **Adicionar** slash command batizado na seção própria
   - **NÃO remover** nada existente sem confirmação explícita
3. Mostrar diff resumido (linhas alteradas).
4. Logar a mudança em `~/.skill-orchestrator/audit-log.jsonl` (auditoria da auditoria — quem mudou o quê e quando).

### 4. Princípios de safety

- **Sempre backup antes de editar SKILL.md.**
- **Nunca aprovar mudanças sem o user.** Auto-edit silencioso é red flag.
- **Diff sempre visível.** User vê exatamente o que muda.
- **Reversível.** `/claw audit revert` restaura o backup mais recente.
- **Rate limit.** Não rodar audit automático mais de 1×/dia.

## Exemplo de saída

```
$ /claw audit

📚 Aprendi observando seus últimos 7 dias

📈 Padrões fortes (sugiro adicionar):

  1. "review esse PR" — você usou 8x, mas não tem gatilho específico.
     Proposta: adicionar "review PR" como sinal de Engenharia.

  2. "pagar conta" → routing manual 4x. Não tem domínio próprio.
     Proposta: criar novo playbook "financeiro.md"?

  3. /claw triage → 12 usos. Top 3 da semana.
     Proposta: deixar /claw default = triage de manhã?

Aplicar essas 3 mudanças no SKILL.md? (s/n/detalhes)
```

## Quando NÃO fazer audit

- Primeiros 30 despachos: não tem amostra significativa.
- User explicitamente disse pra parar (`/claw audit off`).
- Detecção de viés: se 90%+ dos despachos vão pra um domínio só, alertar antes de propor mais routes ali (provavelmente é seu workload, não bug — mas vale checar).

---

**Limites:**

- A skill **não** edita a si mesma sem confirmação. Self-improve ≠ auto-rewrite.
- Mudanças propostas vivem em diff humano-legível.
- Auditoria da auditoria existe (`audit-log.jsonl`) — você sempre pode reconstruir o histórico.
