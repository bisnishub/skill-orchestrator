# 🦞 Skill Orchestrator

**🇧🇷 Português** · [🇺🇸 English](README_EN.md)

> **Skill orquestradora de skills, tools e MCPs.**
> Você fala em português, ela despacha pro caminho certo — Gmail, Calendar, Drive, Notion, Supabase, MCPs autenticados, mídia (Higgsfield), criação de conteúdo.
>
> Roda em **três agentes Claude Code-compatíveis**:
>
> - 🦞 [OpenClaw](https://openclaw.ai)
> - 🌀 [Hermes Agent](https://nousresearch.com) (Nous Research)
> - 💎 [Claude Code](https://claude.com/claude-code) (Anthropic)
>
> Mesma skill, três installers.

Mantida pela **CCB — Comunidade Claude/Claw Brasil**. De graça. Aberta. Pra todo mundo.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![lint](https://github.com/bisnishub/skill-orchestrator/actions/workflows/lint.yml/badge.svg)](https://github.com/bisnishub/skill-orchestrator/actions/workflows/lint.yml)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-orange)](https://openclaw.ai)
[![Hermes](https://img.shields.io/badge/Hermes-compatible-purple)](https://nousresearch.com)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)](https://claude.com/claude-code)
[![pt-BR](https://img.shields.io/badge/lang-pt--BR-green)](https://github.com/bisnishub/skill-orchestrator)

---

## O que faz

Quando você fala com seu agente, ele tem **N** caminhos possíveis pra te ajudar: tool nativa, plugin, MCP autenticado, outra skill. A `orchestrator` é a **porta de entrada única**: lê sua intenção, classifica num domínio, escolhe o melhor despacho e delega — sempre explicando o porquê em uma frase (pra você aprender o caminho na próxima).

**Domínios cobertos:**

- 📬 **Produtividade** — Gmail, Google Calendar, Google Drive, Notion
- 🗄️ **Dados** — Supabase + MCPs autenticados (CRMs, bancos, serviços)
- 🎬 **Mídia** — Higgsfield (imagem/vídeo/virality), skill `video-use`
- ✍️ **Criação de conteúdo** — lives, tutoriais, posts, guias, virality check
- 🛠️ **Engenharia (dev solo)** — PR triage, code review, ship, debug CI
- 💼 **Comercial / vendas** — pipeline lead → qualificação → follow-up → proposta
- 🔍 **Pesquisa / análise** — web research, comparativos, fact-check, monitoramento
- ⚙️ **Setup/Onboarding** — instalar OpenClaw, Hermes ou Claude Code; canais; skills

**Slash commands batizados:**

| Comando | Faz |
| --- | --- |
| `/claw triage` | Triagem de inbox com classificação AÇÃO/FYI/LIXO |
| `/claw weekly` | Agenda da semana + blocos de foco |
| `/claw briefing` | Briefing do dia (emails urgentes, próxima reunião, top 3 tarefas) |
| `/claw ship` | Pre-flight de deploy (PR, CI, changelog, migrations) |
| `/claw live` | Live/stream do zero (roteiro + slides + thumb + checklist) |
| `/claw repurpose <url>` | Repurpose 1 conteúdo em Shorts + thread + IG |
| `/claw followup` | Drafts automáticos de follow-up pra leads silenciosos no CRM |
| `/claw research <tópico>` | Pesquisa estruturada + relatório em Notion |
| `/claw stats` | Telemetria local (privacy first) |
| `/claw skills` | Lista skills carregadas |
| `/claw help` | Referência de slash commands |

**Modos / personas:**

- `--mode dev` — técnico, direto (engenharia > dados > produtividade)
- `--mode editor` — criativo, brand-aware (conteúdo > mídia > produtividade)
- `--mode comercial` — CRM-first (comercial > produtividade > dados)
- `--mode analista` — data-driven, sempre cita fonte (pesquisa > dados > produtividade)

**Meta features que ninguém esperava:**

- 🧠 **Auto-sugestão de skills** — se você usar a mesma rota 3× numa semana, ela se oferece pra virar skill própria
- 📊 **Telemetria local** — `~/.skill-orchestrator/stats.json`, nada sai do agente
- 🎭 **Persistência de modo** — fixa `--mode` como default até você desfixar

---

## Instalação

A skill é a mesma — muda só **onde** ela vive e **como** o agente recarrega.

### 🦞 OpenClaw

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install.sh | bash
```

Destino: `~/.openclaw/skills/orchestrator/`. Depois rode `/new` ou reinicie a sessão.

---

### 🌀 Hermes Agent (Nous Research)

O Hermes pode rodar em duas configurações. **Escolha a sua:**

#### Hermes local (macOS, sem container)

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install-hermes-local.sh | bash
```

Destino: `~/.hermes/skills/orchestrator/`. Sem `sudo`, sem Docker. Recarregue o agent (`uv run hermes setup` ou reinicie).

Override de path:

```bash
HERMES_DATA=/seu/caminho/.hermes bash install-hermes-local.sh
```

#### Hermes Docker (VPS, container `nousresearch/hermes-agent`)

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install-hermes-docker.sh | sudo bash
```

Destino: `/home/hermes/.hermes/skills/orchestrator/`. O installer ajusta `chown hermes:hermes` (uid 1000) e roda `docker compose restart`.

Override de paths:

```bash
HERMES_DATA=/seu/.hermes \
HERMES_COMPOSE_DIR=/seu/hermes \
sudo -E bash install-hermes-docker.sh
```

Validar:

```bash
docker exec -it hermes bash -lc "ls /opt/data/skills/ | grep orchestrator"
```

---

### 💎 Claude Code (Anthropic)

Machine-wide (default):

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install-claude-code.sh | bash
```

Destino: `~/.claude/skills/orchestrator/`.

Só no projeto atual:

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/skill-orchestrator/main/install-claude-code.sh | bash -s -- --project
```

Destino: `./.claude/skills/orchestrator/` (na pasta atual). Reinicie o CLI ou abra nova sessão.

---

## Como usar

A skill ativa **sozinha** quando você fala algo que cai nos domínios. Não precisa invocar — o agente decide.

Se quiser **forçar**, use o slash:

```
/claw quero limpar meu inbox e marcar foco profundo nessa semana
```

Exemplos que ela roteia bem:

| Você diz | Ela despacha pra |
| --- | --- |
| "Vê o que tem no inbox e me dá os 3 mais importantes" | `Gmail.search_threads` + classificação |
| "Marca 2h de foco amanhã de manhã" | `Calendar.suggest_time` + `create_event` |
| "Quantos registros tem a tabela users?" | `Supabase.execute_sql` (read-only) |
| "Faz a thumbnail da live de hoje" | `Higgsfield.generate_image` |
| "Preciso de roteiro pra tutorial em pt-BR" | Playbook `conteudo.md` |
| "Como instalo OpenClaw / Hermes / Claude Code?" | Playbook `setup-agents.md` |

---

## Estrutura

```
skill/                          ← source-of-truth única (idêntica nos 3 agents)
├── SKILL.md                    ← entrypoint (frontmatter + matriz + slashes + modos + telemetria)
└── playbooks/
    ├── produtividade.md        ← Gmail/Calendar/Drive/Notion encadeados
    ├── dados.md                ← Supabase + MCPs / cross-source
    ├── conteudo.md             ← lives/tutoriais/posts/guias
    ├── engenheiro-solo.md      ← PR triage/review/ship/debug CI
    ├── criador-conteudo.md     ← calendário editorial/repurpose/brand kit
    ├── comercial.md            ← pipeline lead/qualificação/follow-up/proposta
    ├── pesquisa.md             ← web research/comparativos/fact-check
    └── setup-agents.md         ← onboarding/instalação/diagnóstico (3 agents)

install.sh                      ← installer OpenClaw (nativo)
install-hermes-local.sh         ← installer Hermes local macOS (sem container)
install-hermes-docker.sh        ← installer Hermes Docker/VPS (chown + restart container)
install-claude-code.sh          ← installer Claude Code (machine-wide ou per-project)
```

A skill é **pequena por design**: a matriz vive no `SKILL.md`, e os playbooks só são carregados quando o pedido pede pipeline composta. Isso evita inflar contexto.

**Por que mono-repo?** Os três agents usam o **mesmo formato Claude Code Skills da Anthropic** (YAML frontmatter `name`/`description` + markdown body). Duplicar conteúdo é receita pra divergência. Aqui o `skill/` é único — só os installers divergem, e as diferenças são puramente operacionais (path, permissões, reload).

---

## Compatibilidade

| Agent | Path destino | Reload | Status |
| --- | --- | --- | --- |
| OpenClaw (macOS/Linux/Win) | `~/.openclaw/skills/orchestrator/` | `/new` na sessão | ✅ |
| Hermes Agent (local macOS) | `~/.hermes/skills/orchestrator/` | `uv run hermes setup` / restart | ✅ |
| Hermes Agent (Docker/VPS) | `~/.hermes/skills/orchestrator/` → `/opt/data/skills/` | `docker compose restart` | ✅ |
| Claude Code (CLI/IDE) | `~/.claude/skills/orchestrator/` ou `.claude/skills/orchestrator/` | reinicia o CLI / nova sessão | ✅ |
| Outros agents Claude Code-compatíveis | — | — | provavelmente funciona se respeita o formato Skill |

---

## Contribuir

PRs bem-vindas. Se quiser adicionar um playbook (ex: "campanha de e-commerce", "atendimento WhatsApp"), abre uma issue com o **gatilho** (frases que disparam) e o **fluxo de despacho** (qual tool/MCP em cada passo).

Padrões:

- Português brasileiro
- Concisão > completude (instrua o agente no **que** fazer, não em **como ser um AI**)
- Cite a tool/MCP exata pelo nome
- Sem dados sensíveis em exemplos
- Se mudar comportamento que afeta install, **atualizar os três installers**

---

## Roadmap

- [ ] Publicar no ClawHub (clawhub.ai) quando registry liberar uploads externos
- [ ] Skill companheira `orchestrator-stats`: telemetria de qual despacho mais usado
- [ ] Playbook "campanha de e-commerce"
- [ ] Playbook "atendimento WhatsApp" (canal + CRM via MCP)

---

## Créditos

- **OpenClaw** — Peter Steinberger ([@steipete](https://x.com/steipete)) e contribuidores · [openclaw.ai](https://openclaw.ai)
- **Hermes Agent** — Nous Research · [nousresearch.com](https://nousresearch.com)
- **Claude Code** — Anthropic · [claude.com/claude-code](https://claude.com/claude-code)
- **CCB / Open Claw Brasil** — comunidade brasileira mantenedora deste repo

---

## Licença

[MIT](LICENSE) — usa, forka, remixa. Só não fica rico cobrando dos outros pelo que é da comunidade.

🦞 *Made with claws in 🇧🇷*
