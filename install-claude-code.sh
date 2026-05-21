#!/usr/bin/env bash
# 🦞 Skill Orchestrator — installer para Claude Code (CLI / IDE / Desktop)
# Skills do Claude Code vivem em ~/.claude/skills/<nome>/ (machine-wide)
# ou em .claude/skills/<nome>/ na raiz do projeto (--project).
# CCB — Comunidade Claude/Claw Brasil · github.com/bisnishub/skill-orchestrator
set -euo pipefail

SKILL_NAME="orchestrator"
REPO_URL="https://github.com/bisnishub/skill-orchestrator.git"

# Default: machine-wide. Flag --project = na pasta atual.
SCOPE="user"
if [[ "${1:-}" == "--project" ]]; then
  SCOPE="project"
fi

if [[ "$SCOPE" == "project" ]]; then
  TARGET="$(pwd)/.claude/skills/${SKILL_NAME}"
else
  TARGET="${HOME}/.claude/skills/${SKILL_NAME}"
fi

TMP_DIR="$(mktemp -d)"

c_blue=$'\033[1;34m'; c_green=$'\033[1;32m'; c_yellow=$'\033[1;33m'; c_red=$'\033[1;31m'; c_reset=$'\033[0m'
say()  { printf "%s🦞 %s%s\n" "$c_blue" "$*" "$c_reset"; }
ok()   { printf "%s ✓ %s%s\n" "$c_green" "$*" "$c_reset"; }
warn() { printf "%s ⚠ %s%s\n" "$c_yellow" "$*" "$c_reset"; }
die()  { printf "%s ✗ %s%s\n" "$c_red" "$*" "$c_reset" >&2; exit 1; }

say "Instalando Skill Orchestrator no Claude Code ($SCOPE)"

command -v git >/dev/null 2>&1 || die "git não encontrado. Instale antes."

if [[ -d "$TARGET" ]]; then
  ts="$(date +%Y%m%d-%H%M%S)"
  backup="${TARGET}.backup-${ts}"
  warn "Skill já existe em $TARGET — backup em $backup"
  mv "$TARGET" "$backup"
fi

say "Clonando repositório…"
git clone --depth=1 "$REPO_URL" "$TMP_DIR/repo" >/dev/null 2>&1 || die "Falha ao clonar $REPO_URL"

mkdir -p "$(dirname "$TARGET")"
cp -r "$TMP_DIR/repo/skill" "$TARGET"
ok "Skill instalada em $TARGET"

rm -rf "$TMP_DIR"

cat <<EOF

  Próximos passos:

    1. Reinicie o Claude Code (CLI ou IDE) — ou abra uma nova sessão
    2. Teste: digite "/claw como triagem do meu inbox"
    3. Playbooks em ${TARGET}/playbooks/

  Variações:
    bash install-claude-code.sh             # ~/.claude/skills/ (machine-wide, default)
    bash install-claude-code.sh --project   # ./.claude/skills/ (só no projeto atual)

  Comunidade: github.com/bisnishub/skill-orchestrator
  CCB — Open Claw Brasil 🇧🇷

EOF
