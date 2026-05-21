# 🦞 OpenClaw Orchestrator

> **Skill orquestradora de skills, tools e MCPs pro OpenClaw.**
> Você fala em português, ela despacha pro caminho certo — Gmail, Calendar, Drive, Notion, Supabase, MCPs custom, mídia (Higgsfield), conteúdo da comunidade.

Mantida pela **CCB — Comunidade Claude/Claw Brasil**. De graça. Aberta. Pra todo mundo.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-orange)](https://openclaw.ai)
[![pt-BR](https://img.shields.io/badge/lang-pt--BR-green)](https://github.com/bisnishub/openclaw-orchestrator)

---

## O que faz

Quando você fala com o OpenClaw, ele tem **N** caminhos possíveis pra te ajudar: tool nativa, plugin, MCP autenticado, outra skill. A `orchestrator` é a **porta de entrada única**: lê sua intenção, classifica num domínio, escolhe o melhor despacho e delega — sempre explicando o porquê em uma frase (pra você aprender o caminho na próxima).

**Domínios cobertos:**

- 📬 **Produtividade** — Gmail, Google Calendar, Google Drive, Notion
- 🗄️ **Dados** — Supabase, MCPs custom (ex: Eletroposto/Spark)
- 🎬 **Mídia** — Higgsfield (imagem/vídeo/virality), skill `video-use`
- 📚 **Conteúdo OpenClaw Brasil** — slides, roteiros, guias, lives, posts
- ⚙️ **Setup/Onboarding** — instalação local, VPS, canais, skills CCB

**Pipelines prontas (playbooks):**

- Inbox triage diária
- Agenda da semana com blocos de foco
- Live CCB do zero (roteiro → slides → thumb → checklist)
- Tutorial em vídeo (roteiro → corte → legenda → thumb → virality check)
- Cross-source report (Supabase + MCPs)
- Onboarding novo membro CCB (VPS + skills + canais)

---

## Instalação

### One-liner (recomendado)

```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/openclaw-orchestrator/main/install.sh | bash
```

Isso copia a skill pra `~/.openclaw/skills/orchestrator/` e mostra o próximo passo.

### Manual

```bash
git clone https://github.com/bisnishub/openclaw-orchestrator.git
cp -r openclaw-orchestrator/skill ~/.openclaw/skills/orchestrator
```

Depois, no OpenClaw:

```
/new
```

Pra forçar reload da skill numa sessão existente.

### Atualizar

```bash
cd ~/.openclaw/skills/orchestrator/.repo 2>/dev/null && git pull && cp -r skill/* ../  || \
curl -fsSL https://raw.githubusercontent.com/bisnishub/openclaw-orchestrator/main/install.sh | bash
```

---

## Como usar

A skill ativa **sozinha** quando você fala algo que cai nos domínios. Não precisa invocar — o OpenClaw decide.

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
| "Como instalo OpenClaw na minha VPS?" | Playbook `setup-openclaw.md` + guia oficial CCB |

---

## Estrutura

```
skill/
├── SKILL.md                    ← entrypoint (frontmatter + matriz de roteamento)
└── playbooks/
    ├── produtividade.md        ← Gmail/Calendar/Drive/Notion encadeados
    ├── dados.md                ← Supabase/Eletroposto/cross-source
    ├── conteudo-openclaw.md    ← slides/roteiros/lives/posts
    └── setup-openclaw.md       ← onboarding/instalação/diagnóstico
```

A skill é **pequena por design**: a matriz vive no `SKILL.md`, e os playbooks só são carregados quando o pedido pede pipeline composta. Isso evita inflar contexto.

---

## Contribuir

PRs bem-vindas. Se você é da CCB e quer adicionar um playbook (ex: "campanha de e-commerce", "atendimento WhatsApp"), abre uma issue com o gatilho e o fluxo de despacho.

Padrões:

- Português brasileiro
- Concisão > completude (instrua o agente no **que** fazer, não em **como ser um AI**)
- Cite a tool/MCP exata pelo nome
- Sem dados sensíveis em exemplos

---

## Roadmap

- [ ] Publicar no ClawHub (clawhub.ai) quando registry público liberar uploads externos
- [ ] Playbook "campanha de e-commerce" (Shopify + Instagram + Higgsfield)
- [ ] Playbook "atendimento WhatsApp" (Eletroposto MCP + WhatsApp channel)
- [ ] Skill companheira `orchestrator-stats`: telemetria de qual despacho mais usado

---

## Créditos

- **OpenClaw** — Peter Steinberger ([@steipete](https://x.com/steipete)) e contribuidores · [openclaw.ai](https://openclaw.ai)
- **CCB / Open Claw Brasil** — Eduardo Cavalcanti e a comunidade brasileira

---

## Licença

[MIT](LICENSE) — usa, forka, remixa. Só não fica rico cobrando dos outros pelo que é da comunidade.

🦞 *Made with claws in 🇧🇷*
