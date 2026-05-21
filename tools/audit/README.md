# 🦞 audit — self-improvement tool

Analisa o log de despachos da Skill Orchestrator e propõe mudanças na matriz.

## Uso

```bash
python3 tools/audit/audit.py                       # lê ~/.skill-orchestrator/log.jsonl
python3 tools/audit/audit.py /caminho/custom.jsonl
```

Saída: JSON estruturado com:

- `meta` — contadores, janela, warning se sample < 30
- `top_domains` — ranking de uso por domínio
- `new_routes` — tokens específicos a um domínio que ainda não são gatilhos
- `promote_to_slash` — sequências (domain, tool) com 5+ usos viram candidatas a `/claw <nome>`
- `noise_terms` — tokens que aparecem em ≥3 domínios (confundem classificação)

## Quick test

```bash
# Gerar um log de exemplo
mkdir -p ~/.skill-orchestrator
cat > ~/.skill-orchestrator/log.jsonl <<'EOF'
{"ts":"2026-05-15T09:00:00Z","intent":"limpa meu inbox","domain":"produtividade-email","tool":"Gmail.search_threads","mode":"default","success":true}
{"ts":"2026-05-16T09:01:00Z","intent":"triagem do inbox","domain":"produtividade-email","tool":"Gmail.search_threads","mode":"default","success":true}
{"ts":"2026-05-17T09:00:00Z","intent":"inbox triage","domain":"produtividade-email","tool":"Gmail.search_threads","mode":"default","success":true}
{"ts":"2026-05-18T14:00:00Z","intent":"review PR 142","domain":"engenharia","tool":"gh pr view","mode":"dev","success":true}
{"ts":"2026-05-19T14:30:00Z","intent":"review PR 145","domain":"engenharia","tool":"gh pr view","mode":"dev","success":true}
{"ts":"2026-05-20T15:00:00Z","intent":"review PR 148","domain":"engenharia","tool":"gh pr view","mode":"dev","success":true}
EOF

python3 tools/audit/audit.py
```

## Privacidade

O script **não envia nada pra fora**. Lê arquivo local, escreve em stdout. O agente que invoca é responsável por:

1. Redact dados sensíveis no log antes de escrever
2. Mostrar resultado ao user
3. Pedir confirmação antes de aplicar mudanças

## Integração com SKILL.md

Quando user digita `/claw audit`, o agente executa:

```bash
python3 ~/.openclaw/skills/orchestrator/tools/audit/audit.py
# ou ~/.hermes/.../tools/audit/audit.py
# ou ~/.claude/skills/orchestrator/tools/audit/audit.py
```

Parse do JSON e mostra ao user. Se user aprova mudanças, agente edita `SKILL.md` com diff visível.

Veja `skill/playbooks/auto-improve.md` para o fluxo completo.
