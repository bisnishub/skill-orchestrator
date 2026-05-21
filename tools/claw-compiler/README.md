# 🦞 claw-compiler

Compila `.claw` (DSL declarativa) em `SKILL.md` válido pro OpenClaw, Hermes ou Claude Code.

## TL;DR

```bash
# Compila pra stdout
python3 tools/claw-compiler/claw.py examples/deploy.claw

# Compila pra arquivo
python3 tools/claw-compiler/claw.py examples/deploy.claw -o ../my-skill/SKILL.md

# Pipe pra um skill folder novo
mkdir -p ~/.claude/skills/deploy-helper
python3 tools/claw-compiler/claw.py examples/deploy.claw -o ~/.claude/skills/deploy-helper/SKILL.md
```

## Por que .claw

Skills da Anthropic são markdown + YAML. Pra um dev é OK. Pra criadores, vendedores, pesquisadores → é fricção. `.claw` é a camada de simplificação.

Filosofia: **se você sabe escrever uma receita ou um cronograma, sabe escrever uma .claw.**

Spec completa em [`docs/claw-dsl.md`](../../docs/claw-dsl.md).

## Exemplo mínimo

```claw
skill HelloWorld
description: Skill mais simples possível

when "oi", "hello", "/claw hello"
  use echo
  with msg="Oi! 🦞"
```

Compile, instala, pronto.

## Sintaxe em uma tela

```claw
skill <Name>                     # CamelCase ou kebab-case
description: <one-liner>
mode: dev | editor | comercial | analista | default

when "frase 1", "frase 2"        # ou: when ambiguous
  use <Tool|MCP>
  with key1=val1, key2=val2
  if <cond>: abort "razão"
  run "<shell command>"
  then notify <canal> "<msg>"
  ask "<pergunta>"
```

## Exemplos prontos

- [`examples/deploy.claw`](examples/deploy.claw) — pre-flight de deploy + rollback
- [`examples/briefing.claw`](examples/briefing.claw) — briefing matinal (inbox + agenda + memória)
- [`examples/triage.claw`](examples/triage.claw) — triagem de inbox

Compile cada um:

```bash
for f in examples/*.claw; do
  echo "=== $f ==="
  python3 claw.py "$f" | head -10
done
```

## Próximos passos

- [ ] LSP server (autocomplete em VS Code)
- [ ] `claw lint` standalone
- [ ] Reverse compile (`SKILL.md` → `.claw`) pra migrar skills existentes
- [ ] Includes (`import "common.claw"`)
