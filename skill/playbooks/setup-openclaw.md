# Playbook — Setup OpenClaw (onboarding CCB)

Pra novos membros da comunidade. Baseado nos guias oficiais da CCB.

## 1. Instalação local (Mac/Linux)
**Gatilho:** "como instalo o OpenClaw", "primeiro setup", "começar do zero".

1. Confirmar OS (`uname -s`).
2. One-liner oficial:
   ```bash
   curl -fsSL https://openclaw.ai/install.sh | bash
   ```
3. `openclaw onboard` — interativo, deixar o user passar.
4. Após onboard: linkar `Guia Pos-Instalacao OpenClaw VPS - Para facilitar integraçoes.docx` da CCB se aplicável.

## 2. Setup VPS (deployment serviço 24/7)
**Gatilho:** "openclaw na VPS", "rodar 24h", "deploy server".

1. Linkar `Guia_Instalacao_OpenClaw_VPS_v2.docx` (`~/Downloads/01-CCB-Claw-Brasil/03-Materiais-e-Guias/`).
2. Confirmar provedor (DigitalOcean / Hetzner / outro).
3. Checklist mínimo: domínio, SSL, systemd unit, firewall (apenas portas necessárias), backup config.
4. Pós-deploy: heartbeat funcionando? Cron configurado? Memória persistindo?

## 3. Integrar canais (WhatsApp, Telegram, Discord)
**Gatilho:** "conectar WhatsApp", "Discord do meu Claw", "canal X".

1. Cada canal é um **plugin OpenClaw**. Listar disponíveis: `openclaw plugins list`.
2. Instalar: `openclaw plugins install <canal>`.
3. Auth flow (variável por canal — consultar `docs.openclaw.ai/channels`).
4. Smoke test: enviar mensagem do canal, confirmar resposta.

## 4. Instalar skills da CCB
**Gatilho:** "skills da CCB", "skills brasileiras", "marketplace BR".

1. Por enquanto, distribuição é via GitHub: `github.com/bisnishub/*`.
2. Padrão de instalação:
   ```bash
   git clone https://github.com/bisnishub/<skill>.git
   cp -r <skill>/skill ~/.openclaw/skills/<skill>
   ```
3. `openclaw skills list` → confirmar carregamento.
4. Em breve: publicar no ClawHub (clawhub.ai).

## 5. Diagnóstico ("não tá funcionando")
**Gatilho:** "tá quebrado", "não responde", "erro X".

1. `openclaw doctor` — primeira parada.
2. Logs: `~/.openclaw/logs/` (últimas 100 linhas).
3. Heartbeat ativo? `openclaw status`.
4. Conflito de skill? `openclaw skills list` + checar precedência (workspace > shared > bundled).
5. Se persistir → abrir issue no repo OpenClaw com `openclaw doctor` output anonimizado.
