#!/usr/bin/env python3
"""
Skill Orchestrator — eval suite runner

Roda o corpus.jsonl contra a matriz de roteamento do SKILL.md e mede acurácia.

Cada linha do corpus tem:
    {"intent": "...", "expected_domain": "...", "expected_tool": "..."}

Como funciona:
1. Parseia a matriz do SKILL.md (lê os "Sinais" de cada domínio)
2. Pra cada intent, encontra o domínio cujos gatilhos têm maior overlap
3. Compara contra expected_domain
4. Reporta accuracy + breakdown por domínio + casos que falharam

Uso:
    python3 runner.py [--corpus path/to/corpus.jsonl] [--skill path/to/SKILL.md] [--threshold 0.85]

Exit code:
    0 — accuracy >= threshold
    1 — accuracy < threshold (CI falha)

Sem deps externas. Python 3.8+.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def parse_matrix(skill_path: Path) -> list[dict]:
    """Extrai as linhas da matriz de roteamento."""
    text = skill_path.read_text(encoding="utf-8")
    in_matrix = False
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("## Matriz de roteamento"):
            in_matrix = True
            continue
        if in_matrix and line.startswith("##"):
            break
        if in_matrix and line.startswith("|") and " | " in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            # skip header e separadores
            if len(cells) < 4 or cells[0].startswith("---") or cells[0] == "Domínio":
                continue
            domain_raw = cells[0]
            triggers_raw = cells[1]
            tool_raw = cells[2]
            # Extrair gatilhos entre aspas
            triggers = re.findall(r'"([^"]+)"', triggers_raw)
            # Slugificar domain — normaliza acentos PRIMEIRO, depois regex
            domain = re.sub(r"\*+", "", domain_raw).lower().strip()
            domain = normalize(domain)  # remove acentos
            domain = re.sub(r"[—–—–]", "-", domain)  # em/en dash
            domain = re.sub(r"[^a-z0-9-]+", "-", domain).strip("-")
            rows.append({
                "domain": domain,
                "triggers": [t.lower() for t in triggers],
                "tool_hint": tool_raw.lower(),
            })
    return rows


def normalize(text: str) -> str:
    text = text.lower()
    # remover acentos básicos
    repl = str.maketrans("áàâãäéèêëíìîïóòôõöúùûüçñ", "aaaaaeeeeiiiiooooouuuucn")
    return text.translate(repl)


def classify(intent: str, matrix: list[dict]) -> tuple[str, float]:
    """Retorna (domain_slug, confidence)."""
    intent_norm = normalize(intent)
    best_domain = "unknown"
    best_score = 0.0
    for row in matrix:
        score = 0.0
        for trigger in row["triggers"]:
            trigger_norm = normalize(trigger)
            if trigger_norm in intent_norm:
                # peso baseado no comprimento do gatilho (mais longo = mais específico)
                score += 1.0 + len(trigger_norm.split()) * 0.5
        if score > best_score:
            best_score = score
            best_domain = row["domain"]
    return best_domain, best_score


def normalize_domain_for_compare(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    # Mapping de aliases comuns (matriz usa em-dash, corpus usa hyphen)
    aliases = {
        "produtividade-email": ["produtividade-email"],
        "produtividade-agenda": ["produtividade-agenda"],
        "produtividade-arquivos": ["produtividade-arquivos"],
        "produtividade-notas": ["produtividade-notas"],
        "dados-supabase": ["dados-supabase"],
        "dados-outros-mcps": ["dados-outros-mcps", "dados-outros"],
        "conteudo": ["conteudo", "conteúdo"],
        "midia": ["midia", "mídia"],
        "engenharia": ["engenharia"],
        "comercial": ["comercial"],
        "pesquisa": ["pesquisa"],
        "pipeline-cross-domain": ["pipeline-cross-domain"],
        "setup": ["setup", "setup-instalacao", "setup-instalação"],
    }
    for canonical, variants in aliases.items():
        if s in variants:
            return canonical
    return s


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--skill", default=None)
    parser.add_argument("--threshold", type=float, default=0.85)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    corpus_path = Path(args.corpus) if args.corpus else repo_root / "tools" / "eval-suite" / "corpus.jsonl"
    skill_path = Path(args.skill) if args.skill else repo_root / "skill" / "SKILL.md"

    if not corpus_path.exists():
        print(f"::error::corpus não encontrado: {corpus_path}", file=sys.stderr)
        return 2
    if not skill_path.exists():
        print(f"::error::SKILL.md não encontrado: {skill_path}", file=sys.stderr)
        return 2

    matrix = parse_matrix(skill_path)
    if not matrix:
        print("::error::matriz vazia — parser falhou?", file=sys.stderr)
        return 2

    total = 0
    correct = 0
    per_domain = defaultdict(lambda: {"total": 0, "correct": 0})
    failures = []

    with corpus_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            intent = row["intent"]
            expected = normalize_domain_for_compare(row["expected_domain"])
            predicted_raw, conf = classify(intent, matrix)
            predicted = normalize_domain_for_compare(predicted_raw)

            total += 1
            per_domain[expected]["total"] += 1
            if predicted == expected or expected in predicted or predicted in expected:
                correct += 1
                per_domain[expected]["correct"] += 1
            else:
                failures.append({
                    "intent": intent,
                    "expected": expected,
                    "predicted": predicted,
                    "confidence": conf,
                })

    accuracy = (correct / total) if total else 0.0

    if not args.quiet:
        print(f"\n🦞 Skill Orchestrator — Eval Suite")
        print(f"   Corpus: {corpus_path.name}")
        print(f"   Total: {total}    Correct: {correct}    Accuracy: {accuracy:.1%}")
        print(f"   Threshold: {args.threshold:.1%}\n")

        print("Por domínio:")
        for domain in sorted(per_domain.keys()):
            d = per_domain[domain]
            acc = (d["correct"] / d["total"]) if d["total"] else 0
            bar = "█" * int(acc * 20)
            print(f"   {domain:30} {d['correct']:>3}/{d['total']:<3}  {bar} {acc:.0%}")

        if failures:
            print(f"\nFalhas ({len(failures)}):")
            for f in failures[:15]:
                print(f"   ❌ \"{f['intent']}\"")
                print(f"      expected={f['expected']}  predicted={f['predicted']}  conf={f['confidence']:.1f}")
            if len(failures) > 15:
                print(f"   ... +{len(failures) - 15} mais")

    # JSON output pra CI parse
    if args.quiet:
        json.dump({
            "total": total,
            "correct": correct,
            "accuracy": accuracy,
            "threshold": args.threshold,
            "passed": accuracy >= args.threshold,
            "per_domain": dict(per_domain),
            "failures_count": len(failures),
        }, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")

    return 0 if accuracy >= args.threshold else 1


if __name__ == "__main__":
    sys.exit(main())
