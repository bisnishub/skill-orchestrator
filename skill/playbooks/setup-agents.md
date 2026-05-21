# Playbook — Setup de Agentes

Onboarding pra **OpenClaw**, **Hermes Agent** e **Claude Code**. Inclui instalação, integração de canais, instalação de skills e diagnóstico.

---

## 1. OpenClaw — instalação local (macOS/Linux/Windows)
**Gatilho:** "como instalo o OpenClaw", "primeiro setup OpenClaw", "começar do zero".

1. Confirmar OS (`uname -s`).
2. One-liner oficial:
   ```bash
   curl -fsSL https://openclaw.ai/install.sh | bash
   ```
3. `openclaw onboard` — interativo, deixar o user conduzir.
4. Documentação: `docs.openclaw.ai`.

## 2. OpenClaw — Setup VPS (24/7)
**Gatilho:** "openclaw na VPS", "rodar 24h", "deploy server".

1. Confirmar provedor (DigitalOcean / Hetzner / outro).
2. Mesmo one-liner do item 1 na VPS, garantir modo serviço.
3. Checklist: domínio (se expor), SSL, systemd unit, firewall (só portas necessárias), backup do `~/.openclaw/`.
4. Pós-deploy: heartbeat ok? Cron configurado? Memória persistindo?

## 3. OpenClaw — Integrar canais (WhatsApp, Telegram, Discord, Slack…)
**Gatilho:** "conectar canal X", "Discord do meu Claw", "OpenClaw no Telegram".

1. Cada canal é um **plugin OpenClaw**. Listar: `openclaw plugins list`.
2. Instalar: `openclaw plugins install <canal>`.
3. Auth flow varia por canal — consultar `docs.openclaw.ai/channels`.
4. Smoke test: enviar mensagem do canal, confirmar resposta.

---

## 4. Hermes Agent — instalação (Docker)
**Gatilho:** "instalar Hermes", "Hermes na VPS", "Nous Research agent".

1. Pré-requisitos: VPS ou máquina Linux com Docker + docker-compose v2.
2. Estrutura recomendada: `~/hermes/docker-compose.yml` + dados em `~/.hermes/`.
3. Imagem oficial: `nousresearch/hermes-agent:latest`.
4. Subir: `docker compose up -d` dentro de `~/hermes/`.
5. Wizard interativo: `docker exec -it hermes bash` → `uv run hermes setup`.

## 5. Hermes — Integrar canais
**Gatilho:** "Telegram no Hermes", "conectar canal Hermes".

1. Telegram built-in: `uv run hermes setup gateway` → seguir wizard.
2. Demais canais (Discord, Slack, WhatsApp via Twilio) — verificar status em `docs` da Nous Research.
3. Multi-canal compartilha memória — mesma conversa do CLI e do Telegram.

---

## 6. Claude Code — instalação
**Gatilho:** "instalar Claude Code", "como começo com Claude Code", "CLI Anthropic".

1. CLI: `npm install -g @anthropic-ai/claude-code` (ou via brew/binary release).
2. IDE: extensões oficiais pra VS Code e JetBrains.
3. Web: claude.ai/code.
4. Desktop: Mac/Windows app.
5. Skills vivem em `~/.claude/skills/<nome>/` (machine-wide) **ou** `.claude/skills/<nome>/` na raiz do projeto.

---

## 7. Instalar skills da CCB
**Gatilho:** "skills da CCB", "skills BR", "instalar skill comunitária".

Distribuição via GitHub: `github.com/bisnishub/*`.

**OpenClaw:**
```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/<skill>/main/install.sh | bash
```
→ `openclaw skills list` confirma.

**Hermes** (na VPS, com sudo):
```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/<skill>/main/install-hermes.sh | sudo bash
```
→ valida: `docker exec -it hermes bash -lc "ls /opt/data/skills/"`.

**Claude Code:**
```bash
curl -fsSL https://raw.githubusercontent.com/bisnishub/<skill>/main/install-claude-code.sh | bash
```
→ reinicia o CLI ou abre nova sessão.

---

## 8. Diagnóstico ("não tá funcionando")
**Gatilho:** "tá quebrado", "não responde", "erro X".

**OpenClaw:**
1. `openclaw doctor` — primeira parada.
2. Logs: `~/.openclaw/logs/` (últimas 100 linhas).
3. Heartbeat: `openclaw status`.
4. Conflito de skill: `openclaw skills list` + checar precedência (workspace > shared > bundled).

**Hermes:**
1. `docker exec -it hermes bash -lc "uv run hermes doctor"`.
2. Logs: `uv run hermes logs -f` dentro do container.
3. Container saudável? `docker compose ps` em `~/hermes/`.
4. Dashboard: `curl -I http://127.0.0.1:9119` deve retornar HTTP 405 (sinal de vida — endpoint root só aceita GET).

**Claude Code:**
1. `claude --version` confere versão.
2. Skills carregando? Olhar `~/.claude/skills/` e `.claude/skills/` da pasta atual.
3. Logs em `~/.claude/logs/` (se existirem).
4. Issue tracker oficial: github.com/anthropics/claude-code.

Em todos os casos: se persistir, abrir issue no repo correspondente com output do `doctor` **anonimizado** (sem tokens, sem paths sensíveis).
