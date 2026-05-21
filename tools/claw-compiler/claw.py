#!/usr/bin/env python3
"""
.claw → SKILL.md compiler

Compila a DSL .claw em SKILL.md válido (com frontmatter YAML + body markdown).

Uso:
    python3 tools/claw-compiler/claw.py path/to/skill.claw [--output path/to/SKILL.md]
    python3 tools/claw-compiler/claw.py path/to/skill.claw          # stdout

Spec: docs/claw-dsl.md. Versão 1.0.

Sem deps externas. Python 3.8+.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class WhenBlock:
    triggers: list[str] = field(default_factory=list)
    ambiguous: bool = False
    actions: list[tuple[str, str]] = field(default_factory=list)  # (verb, content)


@dataclass
class CompiledSkill:
    name: str
    description: str
    mode: str = "default"
    when_blocks: list[WhenBlock] = field(default_factory=list)
    source_file: str = ""


def parse(text: str, source_file: str = "") -> CompiledSkill:
    skill = CompiledSkill(name="", description="", source_file=source_file)
    current_when: WhenBlock | None = None

    lines = text.splitlines()
    for line_num, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue

        # 1) Header declarations
        if m := re.match(r"^skill\s+(.+)$", line):
            skill.name = slugify(m.group(1).strip())
            continue
        if m := re.match(r"^description:\s*(.+)$", line):
            skill.description = m.group(1).strip()
            continue
        if m := re.match(r"^mode:\s*(.+)$", line):
            skill.mode = m.group(1).strip()
            continue

        # 2) when block start
        if m := re.match(r"^when\s+(.+)$", line):
            current_when = WhenBlock()
            content = m.group(1).strip()
            if content == "ambiguous":
                current_when.ambiguous = True
            else:
                current_when.triggers = [t.strip().strip('"') for t in re.findall(r'"([^"]+)"', content)]
                if not current_when.triggers:
                    raise SyntaxError(f"line {line_num}: 'when' precisa de gatilhos entre aspas ou 'ambiguous'")
            skill.when_blocks.append(current_when)
            continue

        # 3) action lines (indented, dentro de when)
        if line.startswith((" ", "\t")):
            if current_when is None:
                raise SyntaxError(f"line {line_num}: ação indentada fora de bloco 'when'")
            stripped = line.strip()
            verb_match = re.match(r"^(use|with|if|run|then|ask|abort)\s+(.+)$", stripped)
            if not verb_match:
                raise SyntaxError(f"line {line_num}: ação inválida: {stripped!r}")
            verb, rest = verb_match.group(1), verb_match.group(2)
            current_when.actions.append((verb, rest))
            continue

        raise SyntaxError(f"line {line_num}: linha não reconhecida: {line!r}")

    # Validações finais
    if not skill.name:
        raise SyntaxError("skill <Name> não declarado (primeira linha obrigatória)")
    if not skill.description:
        raise SyntaxError("description: não declarada")
    if not skill.when_blocks:
        raise SyntaxError("nenhum bloco 'when' encontrado — skill sem comportamento?")

    return skill


def slugify(s: str) -> str:
    s = s.strip()
    # CamelCase → kebab-case
    s = re.sub(r"([a-z])([A-Z])", r"\1-\2", s).lower()
    s = re.sub(r"[^a-z0-9-]+", "-", s).strip("-")
    return s


def emit(skill: CompiledSkill) -> str:
    """Renderiza CompiledSkill como SKILL.md."""
    out = []

    # Frontmatter
    out.append("---")
    out.append(f"name: {skill.name}")
    out.append(f"description: {skill.description}")
    out.append("metadata:")
    out.append("  source: claw-dsl")
    out.append("  compiled_from: " + (skill.source_file or "stdin"))
    out.append("  mode_default: " + skill.mode)
    out.append("  openclaw:")
    out.append("    requires:")
    out.append("      bins: []")
    out.append("      config: []")
    out.append("  hermes:")
    out.append("    compatible: true")
    out.append("  claude-code:")
    out.append("    compatible: true")
    out.append("---")
    out.append("")

    # Body
    out.append(f"# 🦞 {skill.name}")
    out.append("")
    out.append(skill.description)
    out.append("")
    out.append("> _Compilada de `.claw` DSL via skill-orchestrator. Veja [docs/claw-dsl.md](https://github.com/bisnishub/skill-orchestrator/blob/main/docs/claw-dsl.md)._")
    out.append("")
    if skill.mode and skill.mode != "default":
        out.append(f"**Modo default:** `{skill.mode}`")
        out.append("")
    out.append("---")
    out.append("")
    out.append("## Comportamento")
    out.append("")

    for i, block in enumerate(skill.when_blocks, start=1):
        if block.ambiguous:
            out.append(f"### {i}. Pedido ambíguo (fallback)")
        else:
            triggers_fmt = ", ".join(f'`"{t}"`' for t in block.triggers)
            out.append(f"### {i}. Quando ouvir {triggers_fmt}")
        out.append("")

        # Detalhar ações em prosa estruturada
        for verb, content in block.actions:
            if verb == "use":
                out.append(f"- **Use:** `{content}`")
            elif verb == "with":
                out.append(f"- **Parâmetros:** `{content}`")
            elif verb == "if":
                cond, _, action = content.partition(":")
                out.append(f"- **Guard:** se `{cond.strip()}` → {action.strip()}")
            elif verb == "run":
                out.append(f"- **Execute:** `{content}`")
            elif verb == "then":
                out.append(f"- **Depois:** {content}")
            elif verb == "ask":
                out.append(f"- **Pergunte:** {content}")
            elif verb == "abort":
                out.append(f"- **Abort:** {content}")
        out.append("")

    out.append("---")
    out.append("")
    out.append("**Padrões de execução:**")
    out.append("")
    out.append("- Ao receber a frase gatilho, **siga as ações na ordem listada**.")
    out.append("- Guards (`if X: abort Y`) são **bloqueantes** — se a condição falhar, não execute o resto.")
    out.append("- Substitua `${var}` por valores de contexto (ver `docs/claw-dsl.md` pra lista).")
    out.append("- Ações com side-effect (`run`, `then notify`) **precisam de confirmação** se forem destrutivas.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("🦞 Gerado pela CCB — Comunidade Claude/Claw Brasil")

    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile .claw → SKILL.md")
    parser.add_argument("input", help="Path to .claw file")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"::error::arquivo não encontrado: {src}", file=sys.stderr)
        return 2

    try:
        skill = parse(src.read_text(encoding="utf-8"), source_file=src.name)
    except SyntaxError as e:
        print(f"::error file={src}::{e}", file=sys.stderr)
        return 1

    output = emit(skill)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"✓ Compilado: {args.output} ({len(output)} bytes)")
    else:
        sys.stdout.write(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
