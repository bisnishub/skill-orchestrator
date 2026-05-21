# 🦞 OpenClaw Orchestrator

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
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-orange)](https://openclaw.ai)
[![Hermes](https://img.shields.io/badge/Hermes-compatible-purple)](https://nousresearch.com)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)](https://claude.com/claude-code)
[![pt-BR](https://img.shields.io/badge/lang-pt--BR-green)](https://github.com/bisnishub/openclaw-orchestrator)

---

## O que faz

Quando você fala com seu agente, ele tem **N** caminhos possíveis pra te ajudar: tool nativa, plugin, MCP autenticado, outra skill. A `orchestrator` é a **porta de entrada única**: lê sua intenção, classifica num domínio, escolhe o melhor despacho e delega — sempre explicando o porquê em uma frase (pra você aprender o caminho na próxima).

**Domínios cobertos:**

- 📬 **Produtividade** — Gmail, Google Calendar, Google Drive, Notion
- 🗄️ **Dados** — Supabase + MCPs autenticados (CRMs, bancos, serviços)
- 🎬 **Mídia** — Higgsfield (imagem/vídeo/virality), skill `video-use`
- ✍️ **Criação de conteúdo** — lives, tutoriais, posts, guias, virality check
- ⚙️ **Setup/Onboarding** — instalar OpenClaw, Hermes ou Claude Code; canais; skills

**Pipelines prontas (playbooks):**

- Inbox triage diária
- Agenda da semana com blocos de foco
- Live/stream do zero (roteiro → slides → thumb → checklist)
- Tutorial em vídeo (roteiro → corte → legenda → thumb → virality check)
- Cross-source report (Supabase + MCPs)
- Onboarding de agente (OpenClaw, Hermes ou Claude Code)

---

## Instalação

A skill é a mesma — muda só **onde** ela vive e **como** o agente recarrega.

### 🦞 OpenClaw

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/openclaw-orchestrator/main/install.sh | bash
```

Destino: `~/.openclaw/skills/orchestrator/`. Depois rode `/new` ou reinicie a sessão.

---

### 🌀 Hermes Agent (Nous Research, em Docker)

Roda no **host da VPS** onde o Hermes está instalado (precisa de `sudo` pra mexer em `/home/hermes/.hermes/`):

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/openclaw-orchestrator/main/install-hermes.sh | sudo bash
```

Destino: `~/.hermes/skills/orchestrator/`. O installer ajusta `chown hermes:hermes` e roda `docker compose restart`.

Override de paths (instalação custom):

```bash
HERMES_DATA=/seu/caminho/.hermes \
HERMES_COMPOSE_DIR=/seu/caminho/hermes \
sudo -E bash install-hermes.sh
```

Validar:

```bash
docker exec -it hermes bash -lc "ls /opt/data/skills/ | grep orchestrator"
```

---

### 💎 Claude Code (Anthropic)

Machine-wide (default):

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/openclaw-orchestrator/main/install-claude-code.sh | bash
```

Destino: `~/.claude/skills/orchestrator/`.

Só no projeto atual:

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/openclaw-orchestrator/main/install-claude-code.sh | bash -s -- --project
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
├── SKILL.md                    ← entrypoint (frontmatter + matriz de roteamento)
└── playbooks/
    ├── produtividade.md        ← Gmail/Calendar/Drive/Notion encadeados
    ├── dados.md                ← Supabase + MCPs / cross-source
    ├── conteudo.md             ← lives/tutoriais/posts/guias
    └── setup-agents.md         ← onboarding/instalação/diagnóstico (OpenClaw + Hermes + Claude Code)

install.sh                      ← installer OpenClaw (nativo)
install-hermes.sh               ← installer Hermes (Docker + permissões + restart)
install-claude-code.sh          ← installer Claude Code (machine-wide ou per-project)
```

A skill é **pequena por design**: a matriz vive no `SKILL.md`, e os playbooks só são carregados quando o pedido pede pipeline composta. Isso evita inflar contexto.

**Por que mono-repo?** Os três agents usam o **mesmo formato Claude Code Skills da Anthropic** (YAML frontmatter `name`/`description` + markdown body). Duplicar conteúdo é receita pra divergência. Aqui o `skill/` é único — só os installers divergem, e as diferenças são puramente operacionais (path, permissões, reload).

---

## Compatibilidade

| Agent | Path destino | Reload | Status |
| --- | --- | --- | --- |
| OpenClaw (macOS/Linux/Win) | `~/.openclaw/skills/orchestrator/` | `/new` na sessão | ✅ |
| Hermes Agent (Docker) | `~/.hermes/skills/orchestrator/` → `/opt/data/skills/` | `docker compose restart` | ✅ |
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
