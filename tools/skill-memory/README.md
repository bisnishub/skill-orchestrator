# 🦞 skill-memory — MCP server pra memória cross-agent

> **Uma memória pra todos os seus agents.** OpenClaw, Hermes e Claude Code rodando no mesmo Mac compartilham UMA base de dados local. Você grava no Claude Code de manhã, o Hermes lembra à tarde.

## Por que existe

Cada agente Claude Code-compatível tem sua própria memória. Você usa 2-3 agents em paralelo? Cada um tem amnésia em relação aos outros. Esse MCP resolve: SQLite local único, 4 tools simples (`remember`, `recall`, `forget`, `list`), todos os agents conectam, todos vêem a mesma memória.

**Zero rede.** Tudo em `~/.skill-orchestrator/memory.db` (override via `SKILL_MEMORY_DB`).

## Instalar

```bash
cd ~/Developer/skill-orchestrator/tools/skill-memory
npm install
npm link               # vira disponível como `skill-memory` no PATH
```

Ou rodar local sem global:

```bash
node ~/Developer/skill-orchestrator/tools/skill-memory/server.js
```

## Conectar nos agents

### Claude Code

Adicione ao `~/.claude/config.json` (ou `.claude/config.json` por projeto):

```json
{
  "mcpServers": {
    "skill-memory": {
      "command": "node",
      "args": ["/Users/SEU_USER/Developer/skill-orchestrator/tools/skill-memory/server.js"]
    }
  }
}
```

Reinicie o CLI/IDE. As tools `remember`, `recall`, `forget`, `list` ficam disponíveis.

### Hermes Agent

Edite o config do Hermes (path varia — `~/.hermes/config.yaml` ou similar):

```yaml
mcp_servers:
  skill-memory:
    command: node
    args:
      - /Users/SEU_USER/Developer/skill-orchestrator/tools/skill-memory/server.js
```

Restart Hermes (`uv run hermes setup` ou restart container se Docker).

### OpenClaw

Plugin MCP do OpenClaw (consulte docs.openclaw.ai/plugins/mcp se houver). Em geral é registro similar via config.

## API

### `remember`

```json
{
  "key": "preferencia-email-style",
  "value": "informal, sem 'prezado', assina 'abs Edu'",
  "tags": ["email", "preferencia", "estilo"],
  "source_agent": "claude-code"
}
```

Returns: `{ "action": "created" | "updated", "key": "...", "..._at": "iso" }`

### `recall`

Três formas:

```json
{ "key": "preferencia-email-style" }     // match exato
{ "tag": "email" }                       // tudo com essa tag
{ "query": "informal" }                  // busca texto livre
```

### `forget`

```json
{ "key": "preferencia-email-style" }
```

### `list`

```json
{ "tag": "email", "limit": 20 }     // ou apenas {} pra listar tudo (ordem: updated_at desc)
```

## Schema

```sql
CREATE TABLE memories (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  tags TEXT,                        -- CSV: "email,preferencia,estilo"
  created_at TEXT NOT NULL,         -- ISO 8601
  updated_at TEXT NOT NULL,
  accessed_at TEXT,                 -- atualizado em recall(key)
  access_count INTEGER DEFAULT 0,
  source_agent TEXT                 -- 'openclaw' | 'hermes' | 'claude-code'
);
```

Hot keys (acessadas frequentemente) podem ser priorizadas no futuro via `access_count`.

## Padrões de uso

### Cross-agent personality

```
remember(key: "user-tone", value: "pt-BR coloquial, gírias ok, 'FODA' tradição")
```

Qualquer agent que recall isso entrega tom consistente.

### Decisões importantes

```
remember(key: "decision-db-choice-2026-q2",
         value: "escolhemos Supabase ao invés de Firebase — razão: RLS + Postgres",
         tags: ["decisao", "tech-stack"])
```

3 meses depois, qualquer agent: `recall(key: "decision-db-choice-2026-q2")` → contexto recuperado.

### Brand kit

```
remember(key: "brand-clawdete",
         value: {"primary":"#A53860","font":"Inter","tone":"BR coloquial"},
         tags: ["brand", "clawdete"])
```

Skill de criação de conteúdo carrega antes de gerar visual.

## Segurança

- **Nunca conecte agents que você não confia ao mesmo memory store.** A memória é compartilhada — se um agent maluco grava lixo, todos veem.
- **Dados sensíveis (tokens, senhas) NÃO devem entrar.** Use um secrets manager dedicado (1Password CLI, `pass`, etc).
- **Backup:** `~/.skill-orchestrator/memory.db` é um SQLite normal. Inclua em backup periódico.

## Roadmap

- [ ] Migrations versionadas (quando schema mudar)
- [ ] TTL opcional por chave (`remember(..., expires_in_days: 30)`)
- [ ] Encryption-at-rest opcional (chave do Keychain do macOS)
- [ ] CLI standalone (`skill-memory recall <key>` sem precisar de agent)
- [ ] Embeddings opcionais pra semantic recall (sqlite-vec) — só se aderência justificar deps
