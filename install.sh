#!/usr/bin/env bash
# OpenClaw Orchestrator installer
# CCB — Comunidade Claude/Claw Brasil · github.com/bisnishub/openclaw-orchestrator
set -euo pipefail

SKILL_NAME="orchestrator"
TARGET="${HOME}/.openclaw/skills/${SKILL_NAME}"
REPO_URL="https://github.com/bisnishub/openclaw-orchestrator.git"
TMP_DIR="$(mktemp -d)"

c_blue=$'\033[1;34m'; c_green=$'\033[1;32m'; c_yellow=$'\033[1;33m'; c_red=$'\033[1;31m'; c_reset=$'\033[0m'
say()  { printf "%s🦞 %s%s\n" "$c_blue" "$*" "$c_reset"; }
ok()   { printf "%s ✓ %s%s\n" "$c_green" "$*" "$c_reset"; }
warn() { printf "%s ⚠ %s%s\n" "$c_yellow" "$*" "$c_reset"; }
die()  { printf "%s ✗ %s%s\n" "$c_red" "$*" "$c_reset" >&2; exit 1; }

say "Instalando OpenClaw Orchestrator (CCB)"

command -v git >/dev/null 2>&1 || die "git não encontrado. Instale antes de continuar."

if [[ -d "$TARGET" ]]; then
  ts="$(date +%Y%m%d-%H%M%S)"
  backup="${TARGET}.backup-${ts}"
  warn "Skill já existe em $TARGET — fazendo backup em $backup"
  mv "$TARGET" "$backup"
fi

say "Clonando repositório…"
git clone --depth=1 "$REPO_URL" "$TMP_DIR/repo" >/dev/null 2>&1 || die "Falha ao clonar $REPO_URL"

mkdir -p "$(dirname "$TARGET")"
cp -r "$TMP_DIR/repo/skill" "$TARGET"
ok "Skill instalada em $TARGET"

rm -rf "$TMP_DIR"

cat <<'EOF'

  Próximos passos:

    1. Reinicie o OpenClaw OU rode `/new` numa sessão ativa
    2. Teste: diga "limpa meu inbox" ou "/claw como instalo na VPS"
    3. Leia os playbooks em ~/.openclaw/skills/orchestrator/playbooks/

  Comunidade: github.com/bisnishub/openclaw-orchestrator
  CCB — Open Claw Brasil 🇧🇷

EOF
