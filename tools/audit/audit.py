#!/usr/bin/env python3
"""
Skill Orchestrator — audit tool

Lê o log de despachos (~/.skill-orchestrator/log.jsonl), identifica padrões,
e propõe mudanças na matriz de roteamento.

Uso:
    python3 audit.py [path/to/log.jsonl]

Default path: ~/.skill-orchestrator/log.jsonl

Saída: JSON com chaves:
    - new_routes: gatilhos não-mapeados que aparecem ≥3 vezes
    - promote_to_slash: rotas com ≥5 usos candidatas a slash batizado
    - noise_terms: termos comuns que aparecem em múltiplos domínios (confundem)
    - top_domains: ranking de domínios por uso (últimos 7d)
    - meta: contagem total, janela, sample size

Sem dependências externas. Python 3.8+.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


STOPWORDS_PT = {
    "a", "o", "e", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas",
    "para", "pra", "por", "com", "sem", "que", "quem", "se", "um", "uma", "uns", "umas",
    "eu", "você", "voce", "vc", "ele", "ela", "nós", "nos", "isso", "isto", "aquilo",
    "esse", "essa", "este", "esta", "aquele", "aquela",
    "meu", "minha", "seu", "sua", "nosso", "nossa",
    "ja", "já", "ainda", "muito", "pouco", "mais", "menos", "também", "tambem",
    "mas", "ou", "como", "quando", "onde", "porque", "pq",
    "tem", "ter", "ser", "estar", "ir", "vir", "fazer", "faz",
    "é", "eh", "foi", "vai", "vou", "tá", "ta", "to", "tô",
}


def load_log(path: Path, days: int = 7) -> list[dict]:
    if not path.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    entries = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
                ts = datetime.fromisoformat(e["ts"].replace("Z", "+00:00"))
                if ts >= cutoff:
                    entries.append(e)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    return entries


def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r"[a-zà-ÿ0-9]{3,}", text)
    return [t for t in tokens if t not in STOPWORDS_PT]


def detect_new_routes(entries: list[dict]) -> list[dict]:
    """Frases recorrentes não mapeadas em nenhum domínio óbvio."""
    domain_tokens: dict[str, Counter] = defaultdict(Counter)
    for e in entries:
        for t in tokenize(e.get("intent", "")):
            domain_tokens[e["domain"]][t] += 1

    # Tokens que aparecem em ≥3 intents do mesmo domínio mas em NENHUM outro
    # podem ser candidatos a gatilho novo (mais específicos que os atuais)
    proposals = []
    for domain, counter in domain_tokens.items():
        for token, count in counter.most_common(10):
            if count < 3:
                continue
            # Aparece em outros domínios?
            appears_elsewhere = any(
                token in other for d, other in domain_tokens.items() if d != domain
            )
            if not appears_elsewhere:
                proposals.append({"domain": domain, "trigger": token, "count": count})
    # ordenar por count desc, limitar
    proposals.sort(key=lambda p: -p["count"])
    return proposals[:10]


def detect_promote_to_slash(entries: list[dict]) -> list[dict]:
    """Sequências (domain, tool) com ≥5 usos viram candidatas a slash."""
    seq_counter = Counter((e["domain"], e.get("tool", "")) for e in entries)
    proposals = []
    for (domain, tool), count in seq_counter.most_common():
        if count >= 5:
            proposals.append({
                "domain": domain,
                "tool": tool,
                "count": count,
                "suggested_slash": suggest_slash_name(domain, tool),
            })
    return proposals[:5]


def suggest_slash_name(domain: str, tool: str) -> str:
    """Heurística simples pra nome curto."""
    base = (tool or domain).lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    parts = base.split("-")
    # Tomar 2 primeiros tokens significativos
    return "/claw " + "-".join(parts[:2]) if parts else "/claw cmd"


def detect_noise_terms(entries: list[dict]) -> list[dict]:
    """Tokens que aparecem em ≥3 domínios — confundem classificação."""
    token_domains: dict[str, set[str]] = defaultdict(set)
    for e in entries:
        for t in tokenize(e.get("intent", "")):
            token_domains[t].add(e["domain"])

    noise = []
    for token, domains in token_domains.items():
        if len(domains) >= 3:
            noise.append({"token": token, "appears_in": sorted(domains)})
    noise.sort(key=lambda n: -len(n["appears_in"]))
    return noise[:10]


def top_domains(entries: list[dict]) -> list[dict]:
    c = Counter(e["domain"] for e in entries)
    return [{"domain": d, "count": n} for d, n in c.most_common(10)]


def main(argv: list[str]) -> int:
    log_path = Path(argv[1]) if len(argv) > 1 else Path.home() / ".skill-orchestrator" / "log.jsonl"
    days = 7

    entries = load_log(log_path, days=days)

    result = {
        "meta": {
            "log_path": str(log_path),
            "log_exists": log_path.exists(),
            "window_days": days,
            "sample_size": len(entries),
        },
        "top_domains": top_domains(entries),
        "new_routes": detect_new_routes(entries),
        "promote_to_slash": detect_promote_to_slash(entries),
        "noise_terms": detect_noise_terms(entries),
    }

    if len(entries) < 30:
        result["meta"]["warning"] = (
            f"Apenas {len(entries)} entries nos últimos {days}d. "
            "Análise pode ser instável. Use a skill por mais alguns dias antes de aplicar mudanças."
        )

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
