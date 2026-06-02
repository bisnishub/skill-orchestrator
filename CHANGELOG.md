# Changelog

Todas as mudanças relevantes da Skill Orchestrator. Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e [SemVer](https://semver.org/lang/pt-BR/).

## [0.7.0] — 2026-06-02

### Adicionado
- 🧠 **Memory MCP server (`tools/skill-memory/`)** — Node.js MCP server pra memória cross-agent compartilhada. SQLite local em `~/.skill-orchestrator/memory.db`. 4 tools: `remember`, `recall`, `forget`, `list`. Tags + busca em texto. Zero rede.
- 📘 `docs/memory-mcp.md` — guia de integração nos 3 agents (Claude Code config, Hermes config, OpenClaw plugin)
- SKILL.md ganhou seção "Memory cross-agent (opcional via MCP)" com procedure de detecção + fallback graceful pro arquivo local

### Comportamento novo
- Quando MCP `skill-memory` disponível: preferências, decisões, brand kit e modo default vivem nele → cross-agent
- Quando indisponível: fallback automático pro `~/.skill-orchestrator/stats.json` (comportamento anterior preservado)

### Privacy
- MCP nunca envia dados pra rede
- Dados sensíveis (tokens, senhas) explicitamente fora do escopo — usar secrets manager dedicado

## [0.6.0] — 2026-05-21

### Mudado (filosofia)
- 🎯 **Ação > explicação.** SKILL.md agora distingue rotas simples (executar direto) de compostas (delegar/playbook) de complexas (swarm). Princípio antigo "NÃO é executar" foi correção literal demais — virou regra prática
- 🔍 **Tool Discovery & Fallback** explícitos. Seção nova com tabela mapeando tools canônicas pros equivalentes em cada agente host (OpenClaw plugins, Hermes skills, Claude Code MCPs). Falha de tool nunca vira "não consigo" — sempre fallback

### Adicionado
- `install-hermes-local.sh` — installer dedicado pra Hermes em macOS LOCAL (sem container, sem sudo, sem Docker)

### Mudado (estrutura)
- `install-hermes.sh` → renomeado pra `install-hermes-docker.sh` (deixa explícito que é o caminho VPS/container)
- README e setup-agents.md com seções separadas: Hermes local macOS vs Hermes Docker

## [0.5.0] — 2026-05-21

### Adicionado
- 🧠 **Self-improving orchestrator** — playbook `auto-improve.md` instrui logging em `~/.skill-orchestrator/log.jsonl`. Comando `/claw audit` lê padrões via `tools/audit/audit.py` (Python puro), propõe diffs no SKILL.md com backup + confirmação humana. Auto-edit silencioso é red flag — sempre diff visível, sempre reversível.
- 🎯 **Eval suite pública** — `tools/eval-suite/corpus.jsonl` (64 frases anotadas, 13 domínios) + `runner.py` (parser + scoring + breakdown). Accuracy atual **95.3%**. Matriz expandida com gatilhos descobertos pelo eval: inbox, CRM, follow-up, fact-check, etc.
- 🤖 **Multi-agent swarm** — `/claw swarm <objetivo>` dispara N subagents em paralelo. `playbooks/swarm.md` + `docs/swarm-protocol.md` formaliza JSON de hand-off (status, outputs, needs_from_others, blockers). Cap 7 subagents, timeout 5min, sem ações destrutivas sem confirmação humana.
- 🦞 **`.claw` DSL + compiler** — linguagem declarativa pra escrever skills sem YAML/markdown. `docs/claw-dsl.md` (spec), `tools/claw-compiler/claw.py` (compiler Python puro), 3 exemplos: deploy/briefing/triage. Democratiza criação de skills pra não-devs.

### Mudado
- Matriz de roteamento expandida com gatilhos descobertos pelo eval suite (inbox, CRM, follow-up, compara/vs, fact-check, Hermes/Telegram/conectar)

### Nova estrutura
- `docs/` — specs formais (DSL, protocolos)
- `tools/` — utilitários executáveis (audit, eval-suite, claw-compiler)

## [0.4.0] — 2026-05-21

### Adicionado
- 🎨 ASCII art banner nos 3 installers (welcome message com lagostinha)
- 🎯 **Slash commands batizados**: `/claw triage`, `/claw weekly`, `/claw ship`, `/claw briefing`, `/claw live`, `/claw repurpose`, `/claw followup`, `/claw research`, `/claw stats`, `/claw skills`, `/claw help`
- 🎭 **Sistema de modos/personas**: `--mode dev`, `--mode editor`, `--mode comercial`, `--mode analista`. Persistência via `~/.skill-orchestrator/mode`
- 🧠 **Auto-sugestão de skills**: após 3 usos da mesma rota em 7 dias, propõe criar skill especializada
- 📊 **Telemetria local** (privacy first): `~/.skill-orchestrator/stats.json`, comando `/claw stats` com ranking visual
- 📘 4 playbooks novos:
  - `engenheiro-solo.md` — PR triage, code review, ship, debug CI, issue→PR, health check
  - `criador-conteudo.md` — calendário editorial, repurpose multi-plataforma, brand kit, virality
  - `comercial.md` — triagem de leads, qualificação, follow-up, proposta, discovery call, pipeline review
  - `pesquisa.md` — pesquisa estruturada, comparativos, scraping ético, monitoramento, fact-check
- 📜 Documentação institucional: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue/PR templates
- 🔧 GitHub Action de lint (frontmatter YAML, shell scripts, links)
- 🌍 README bilíngue (`README_EN.md`)
- 🎬 `MEDIA.md` — roteiro de gravação do GIF demo

### Mudado
- Matriz de roteamento expandida: +3 domínios (Engenharia, Comercial, Pesquisa)
- SKILL.md description atualizada com features novas (relevante pra descoberta no ClawHub)

## [0.3.0] — 2026-05-21

### Adicionado
- 💎 Suporte Claude Code (3º target)
- `install-claude-code.sh` com flag `--project` (machine-wide vs per-project)
- Frontmatter declara `metadata.claude-code.compatible: true`

### Removido
- Referências a MCPs e tools de negócios privados da mantenedora
- Paths absolutos pessoais sob `~/Downloads/...`
- Arquivos amarrados a templates internos

### Mudado
- `playbooks/conteudo-openclaw.md` → `conteudo.md` (escopo generalizado)
- `playbooks/dados.md` cobre Supabase + MCPs genéricos
- README com tabela de compatibilidade pros 3 agents
- Bug pré-existente em `setup-agents.md` (duas seções "5") corrigido

## [0.2.0] — 2026-05-21

### Adicionado
- 🌀 Suporte Hermes Agent (2º target)
- `install-hermes.sh` com ajuste de permissões (`chown hermes:hermes`) e restart automático do container
- Frontmatter declara `metadata.hermes.compatible: true`
- Setup playbook expandido com seções dedicadas a Hermes (instalação, canais, diagnóstico)

### Mudado
- Mono-repo passou a servir múltiplos agents com source-of-truth única em `skill/`
- README justifica a estratégia de mono-repo vs múltiplos repos

## [0.1.0] — 2026-05-21

### Adicionado
- 🦞 Release inicial: skill orquestradora pra **OpenClaw**
- Matriz de roteamento com 11 domínios (Produtividade, Dados, Mídia, Conteúdo, Pipeline cross-domain, Setup)
- 4 playbooks: `produtividade.md`, `dados.md`, `conteudo-openclaw.md`, `setup-openclaw.md`
- `install.sh` (one-liner) + README pt-BR + LICENSE MIT
- `EXAMPLES.md` com 5 conversas reais demonstrando o roteamento

---

**Mantenedora:** [CCB — Comunidade Claude/Claw Brasil](https://github.com/bisnishub) · 🦞 *Made with claws in 🇧🇷*
