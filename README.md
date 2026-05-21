# 🦞 OpenClaw Orchestrator

> **Skill orquestradora de skills, tools e MCPs.**
> Você fala em português, ela despacha pro caminho certo — Gmail, Calendar, Drive, Notion, Supabase, MCPs custom, mídia (Higgsfield), conteúdo da comunidade.
>
> **Roda em [OpenClaw](https://openclaw.ai) e em [Hermes Agent](https://nousresearch.com/hermes) (Nous Research).** Mesma skill, dois installers.

Mantida pela **CCB — Comunidade Claude/Claw Brasil**. De graça. Aberta. Pra todo mundo.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-orange)](https://openclaw.ai)
[![Hermes](https://img.shields.io/badge/Hermes-compatible-purple)](https://nousresearch.com)
[![pt-BR](https://img.shields.io/badge/lang-pt--BR-green)](https://github.com/bisnishub/openclaw-orchestrator)

---

## O que faz

Quando você fala com seu agente, ele tem **N** caminhos possíveis pra te ajudar: tool nativa, plugin, MCP autenticado, outra skill. A `orchestrator` é a **porta de entrada única**: lê sua intenção, classifica num domínio, escolhe o melhor despacho e delega — sempre explicando o porquê em uma frase (pra você aprender o caminho na próxima).

**Domínios cobertos:**

- 📬 **Produtividade** — Gmail, Google Calendar, Google Drive, Notion
- 🗄️ **Dados** — Supabase, MCPs custom (ex: Eletroposto/Spark)
- 🎬 **Mídia** — Higgsfield (imagem/vídeo/virality), skill `video-use`
- 📚 **Conteúdo CCB** — slides, roteiros, guias, lives, posts
- ⚙️ **Setup/Onboarding** — instalação OpenClaw OU Hermes, canais, skills

**Pipelines prontas (playbooks):**

- Inbox triage diária
- Agenda da semana com blocos de foco
- Live CCB do zero (roteiro → slides → thumb → checklist)
- Tutorial em vídeo (roteiro → corte → legenda → thumb → virality check)
- Cross-source report (Supabase + MCPs)
- Onboarding novo membro CCB (OpenClaw ou Hermes)

---

## Instalação

A skill é a mesma — muda só **onde** ela vive e **como** o agente recarrega.

### 🦞 OpenClaw

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/openclaw-orchestrator/main/install.sh | bash
```

Isso copia a skill pra `~/.openclaw/skills/orchestrator/`. Depois, no OpenClaw, rode `/new` ou reinicie a sessão.

**Manual:**

```bash
git clone https://github.com/bisnishub/openclaw-orchestrator.git
cp -r openclaw-orchestrator/skill ~/.openclaw/skills/orchestrator
```

---

### 🌀 Hermes Agent (Nous Research, em Docker)

Roda no **host da VPS** onde o Hermes está instalado (precisa de `sudo` pra mexer em `/home/hermes/.hermes/`):

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/openclaw-orchestrator/main/install-hermes.sh | sudo bash
```

Isso copia a skill pra `~/.hermes/skills/orchestrator/`, ajusta `chown hermes:hermes`, e reinicia os containers.

**Manual** (dentro do host, como root):

```bash
git clone https://github.com/bisnishub/openclaw-orchestrator.git
cp -r openclaw-orchestrator/skill /home/hermes/.hermes/skills/orchestrator
chown -R hermes:hermes /home/hermes/.hermes/skills/orchestrator
cd /home/hermes/hermes && docker compose restart
```

**Caso seus paths sejam diferentes** (instalação custom), override antes de rodar:

```bash
HERMES_DATA=/seu/caminho/.hermes \
HERMES_COMPOSE_DIR=/seu/caminho/hermes \
sudo -E bash install-hermes.sh
```

**Validar que carregou:**

```bash
docker exec -it hermes bash -lc "ls /opt/data/skills/ | grep orchestrator"
```

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
| "Quantas transações o Eletroposto rodou hoje?" | `spark_list_transactions` MCP |
| "Faz a thumbnail da live de hoje" | `Higgsfield.generate_image` |
| "Preciso de roteiro pra tutorial de Supabase em pt-BR" | Playbook `conteudo-openclaw.md` |
| "Como instalo OpenClaw na minha VPS?" | Playbook `setup-agents.md` (seção OpenClaw) |
| "Hermes não reconhece a skill nova" | Playbook `setup-agents.md` (seção Hermes) |

---

## Estrutura

```
skill/                          ← source-of-truth única (idêntica nos 2 agents)
├── SKILL.md                    ← entrypoint (frontmatter + matriz de roteamento)
└── playbooks/
    ├── produtividade.md        ← Gmail/Calendar/Drive/Notion encadeados
    ├── dados.md                ← Supabase/Eletroposto/cross-source
    ├── conteudo-openclaw.md    ← slides/roteiros/lives/posts
    └── setup-agents.md         ← onboarding/instalação/diagnóstico (OpenClaw + Hermes)

install.sh                      ← installer OpenClaw (nativo)
install-hermes.sh               ← installer Hermes (Docker + permissões + restart)
```

A skill é **pequena por design**: a matriz vive no `SKILL.md`, e os playbooks só são carregados quando o pedido pede pipeline composta. Isso evita inflar contexto.

**Por que mono-repo e não dois repos?** Porque OpenClaw e Hermes usam o **mesmo formato Claude Code Skills** (YAML frontmatter + markdown). Duplicar o conteúdo é receita pra divergência. Aqui o `skill/` é único — só `install.sh` vs `install-hermes.sh` diverge, e essas diferenças são puramente operacionais (path, permissões, reload).

---

## Compatibilidade

| Agent | Path destino | Reload | Status |
| --- | --- | --- | --- |
| OpenClaw (macOS/Linux/Win) | `~/.openclaw/skills/orchestrator/` | `/new` na sessão | ✅ Suportado |
| Hermes Agent (Docker) | `~/.hermes/skills/orchestrator/` → `/opt/data/skills/` | `docker compose restart` | ✅ Suportado |
| Claude Code (CLI/IDE) | `~/.claude/skills/orchestrator/` | reinicia o CLI | 🔜 Roadmap |
| Outros agents Claude Code-compatíveis | — | — | provavelmente funciona se respeita o formato Skill |

---

## Contribuir

PRs bem-vindas. Se você é da CCB e quer adicionar um playbook (ex: "campanha de e-commerce", "atendimento WhatsApp"), abre uma issue com o gatilho e o fluxo de despacho.

Padrões:

- Português brasileiro
- Concisão > completude (instrua o agente no **que** fazer, não em **como ser um AI**)
- Cite a tool/MCP exata pelo nome
- Sem dados sensíveis em exemplos
- Se mudar comportamento que afeta install, **atualizar os dois installers**

---

## Roadmap

- [ ] Suporte oficial Claude Code (`~/.claude/skills/`)
- [ ] Publicar no ClawHub (clawhub.ai) quando registry liberar uploads
- [ ] Playbook "campanha de e-commerce" (Shopify + Instagram + Higgsfield)
- [ ] Playbook "atendimento WhatsApp" (Eletroposto MCP + WhatsApp channel)
- [ ] Skill companheira `orchestrator-stats`: telemetria de qual despacho mais usado

---

## Créditos

- **OpenClaw** — Peter Steinberger ([@steipete](https://x.com/steipete)) e contribuidores · [openclaw.ai](https://openclaw.ai)
- **Hermes Agent** — Nous Research · [nousresearch.com](https://nousresearch.com)
- **CCB / Open Claw Brasil** — Eduardo Cavalcanti e a comunidade brasileira

---

## Licença

[MIT](LICENSE) — usa, forka, remixa. Só não fica rico cobrando dos outros pelo que é da comunidade.

🦞 *Made with claws in 🇧🇷*
