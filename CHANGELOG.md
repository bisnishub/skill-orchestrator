# Changelog

Todas as mudanças relevantes da Skill Orchestrator. Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e [SemVer](https://semver.org/lang/pt-BR/).

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
