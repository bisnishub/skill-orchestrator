# 🦞 Skill Orchestrator

**🇺🇸 English** · [🇧🇷 Português](README.md)

> **A skill that orchestrates skills, tools, and MCPs.**
> You speak in plain language, it dispatches to the right path — Gmail, Calendar, Drive, Notion, Supabase, authenticated MCPs, media (Higgsfield), content creation, engineering, sales, research.
>
> Runs on **three Claude Code–compatible agents**:
>
> - 🦞 [OpenClaw](https://openclaw.ai)
> - 🌀 [Hermes Agent](https://nousresearch.com) (Nous Research)
> - 💎 [Claude Code](https://claude.com/claude-code) (Anthropic)
>
> One skill, three installers.

Maintained by the **CCB — Comunidade Claude/Claw Brasil** community. Free. Open. For everyone.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![lint](https://github.com/bisnishub/skill-orchestrator/actions/workflows/lint.yml/badge.svg)](https://github.com/bisnishub/skill-orchestrator/actions/workflows/lint.yml)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-orange)](https://openclaw.ai)
[![Hermes](https://img.shields.io/badge/Hermes-compatible-purple)](https://nousresearch.com)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)](https://claude.com/claude-code)

---

## What it does

When you talk to your agent, it has **N** possible paths to help you: native tool, plugin, authenticated MCP, another skill. The `orchestrator` is the **single entry point**: reads your intent, classifies it, picks the best dispatch, and delegates — always explaining the *why* in one line (so you learn the path for next time).

**Covered domains:**

- 📬 **Productivity** — Gmail, Google Calendar, Google Drive, Notion
- 🗄️ **Data** — Supabase + authenticated MCPs (CRMs, databases, services)
- 🎬 **Media** — Higgsfield (image/video/virality), `video-use` skill
- ✍️ **Content creation** — lives/streams, tutorials, social posts, guides, virality check
- 🛠️ **Engineering (solo dev)** — PR triage, code review, ship, debug CI
- 💼 **Sales / commercial** — lead pipeline, qualification, follow-up, proposals
- 🔍 **Research / analyst** — web research, comparisons, fact-check, monitoring
- ⚙️ **Setup/Onboarding** — install OpenClaw/Hermes/Claude Code; channels; skills

**Named slash commands:**

| Command | Does |
| --- | --- |
| `/claw triage` | Inbox triage with ACTION/FYI/TRASH classification |
| `/claw weekly` | Week ahead + focus block suggestions |
| `/claw briefing` | Today's briefing (urgent emails, next meeting, top 3 tasks) |
| `/claw ship` | Pre-flight deploy check (PR, CI, changelog, migrations) |
| `/claw live` | Live/stream from scratch (script + slides + thumb + checklist) |
| `/claw repurpose <url>` | Turn 1 content into Shorts + thread + IG caption |
| `/claw followup` | Auto-draft follow-ups for stale CRM leads |
| `/claw research <topic>` | Structured research + Notion report |
| `/claw stats` | Local telemetry (privacy first) |
| `/claw skills` | List loaded skills |
| `/claw help` | Slash command reference |

**Modes (personas):**

- `--mode dev` — technical, direct (engineering > data > productivity)
- `--mode editor` — creative, brand-aware (content > media > productivity)
- `--mode comercial` — CRM-first (sales > productivity > data)
- `--mode analista` — data-driven, citation-heavy (research > data > productivity)

**Meta features:**

- 🧠 **Auto-skill suggestion** — if you use the same route 3× in a week, it offers to turn it into a dedicated skill
- 📊 **Local telemetry** — `~/.skill-orchestrator/stats.json`, nothing leaves the agent

---

## Installation

Same skill, different install paths and reload commands per agent.

### 🦞 OpenClaw

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install.sh | bash
```

Target: `~/.openclaw/skills/orchestrator/`. Then run `/new` or restart your session.

### 🌀 Hermes Agent (Nous Research)

Hermes runs in two configurations. **Pick yours:**

#### Hermes local (macOS, no container)

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install-hermes-local.sh | bash
```

Target: `~/.hermes/skills/orchestrator/`. No `sudo`, no Docker. Reload the agent (`uv run hermes setup` or restart).

#### Hermes Docker (VPS, `nousresearch/hermes-agent` container)

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install-hermes-docker.sh | sudo bash
```

Target: `/home/hermes/.hermes/skills/orchestrator/`. Installer handles `chown hermes:hermes` (uid 1000) and `docker compose restart`.

Custom paths:

```bash
HERMES_DATA=/your/.hermes \
HERMES_COMPOSE_DIR=/your/hermes \
sudo -E bash install-hermes-docker.sh
```

Verify:

```bash
docker exec -it hermes bash -lc "ls /opt/data/skills/ | grep orchestrator"
```

### 💎 Claude Code (Anthropic)

Machine-wide (default):

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install-claude-code.sh | bash
```

Per-project only:

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install-claude-code.sh | bash -s -- --project
```

Restart the CLI or start a new session.

---

## How to use

The skill **activates automatically** when you speak something matching a domain. No invocation needed — the agent decides.

To force it, use the slash:

```
/claw clean my inbox and block 2h of focus time this week
```

Examples that route well:

| You say | It dispatches to |
| --- | --- |
| "Check my inbox and give me the top 3" | `Gmail.search_threads` + classification |
| "Block 2h of focus tomorrow morning" | `Calendar.suggest_time` + `create_event` |
| "How many rows in the users table?" | `Supabase.execute_sql` (read-only) |
| "Generate today's stream thumbnail" | `Higgsfield.generate_image` |
| "Review PR #142" | `gh pr view` + structured review |
| "Follow up with quiet leads" | `playbooks/comercial.md` §3 |
| "Compare Supabase vs Firebase for our case" | `playbooks/pesquisa.md` §2 |

---

## Structure

```
skill/                          ← single source of truth (identical across all 3 agents)
├── SKILL.md                    ← entrypoint (frontmatter + routing matrix + slash commands)
└── playbooks/
    ├── produtividade.md        ← Gmail/Calendar/Drive/Notion chained
    ├── dados.md                ← Supabase + MCPs / cross-source
    ├── conteudo.md             ← lives/tutorials/social posts/guides
    ├── engenheiro-solo.md      ← PR triage/review/ship/CI debug
    ├── criador-conteudo.md     ← editorial calendar/repurpose/brand
    ├── comercial.md            ← lead pipeline/qualification/follow-up
    ├── pesquisa.md             ← web research/comparison/fact-check
    └── setup-agents.md         ← onboarding/install/diagnose (3 agents)

install.sh                      ← OpenClaw installer (native)
install-hermes.sh               ← Hermes installer (Docker + perms + restart)
install-claude-code.sh          ← Claude Code installer (machine-wide or per-project)
```

The skill is **small by design**: the routing matrix lives in `SKILL.md`, playbooks are loaded only when the request asks for a composed pipeline. This prevents context bloat.

**Why mono-repo?** All three agents use the same Claude Code Skills format (YAML frontmatter + markdown body). Duplicating content is a recipe for divergence. Here, `skill/` is unique — only the installers differ, and those differences are purely operational (path, permissions, reload).

---

## Compatibility

| Agent | Target path | Reload | Status |
| --- | --- | --- | --- |
| OpenClaw (macOS/Linux/Win) | `~/.openclaw/skills/orchestrator/` | `/new` in session | ✅ |
| Hermes Agent (Docker) | `~/.hermes/skills/orchestrator/` → `/opt/data/skills/` | `docker compose restart` | ✅ |
| Claude Code (CLI/IDE) | `~/.claude/skills/orchestrator/` or `.claude/skills/orchestrator/` | restart CLI / new session | ✅ |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) (PT-BR). Issue templates: bug report, playbook proposal. PR template enforces the install-trio update rule.

---

## Roadmap

- [ ] Publish on ClawHub (clawhub.ai) when external uploads open
- [ ] More installers: Codex (OpenAI), Goose (Block), Aider, Cursor agents
- [ ] More playbooks: e-commerce campaign, customer support, financial ops
- [ ] Visual brand kit (logo SVG, social cards)

---

## Credits

- **OpenClaw** — Peter Steinberger ([@steipete](https://x.com/steipete)) and contributors · [openclaw.ai](https://openclaw.ai)
- **Hermes Agent** — Nous Research · [nousresearch.com](https://nousresearch.com)
- **Claude Code** — Anthropic · [claude.com/claude-code](https://claude.com/claude-code)
- **CCB / Open Claw Brasil** — Brazilian community maintaining this repo

---

## License

[MIT](LICENSE) — use it, fork it, remix it. Just don't get rich charging others for what belongs to the community.

🦞 *Made with claws in 🇧🇷*
