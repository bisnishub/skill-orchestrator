#!/usr/bin/env bash
# 🦞 Skill Orchestrator — installer para Hermes Agent (modo LOCAL macOS)
# Use este script se você roda o Hermes NATIVAMENTE no macOS (sem Docker).
# Para Hermes em container Docker/VPS, use install-hermes-docker.sh.
# CCB — Comunidade Claude/Claw Brasil · github.com/bisnishub/skill-orchestrator
set -euo pipefail

SKILL_NAME="orchestrator"
# Default macOS: ~/.hermes/skills/. Override com HERMES_DATA=... se path custom.
HERMES_DATA="${HERMES_DATA:-${HOME}/.hermes}"
TARGET="${HERMES_DATA}/skills/${SKILL_NAME}"
REPO_URL="https://github.com/bisnishub/skill-orchestrator.git"
TMP_DIR="$(mktemp -d)"

c_blue=$'\033[1;34m'; c_green=$'\033[1;32m'; c_yellow=$'\033[1;33m'; c_red=$'\033[1;31m'; c_magenta=$'\033[1;35m'; c_reset=$'\033[0m'
say()  { printf "%s🦞 %s%s\n" "$c_blue" "$*" "$c_reset"; }
ok()   { printf "%s ✓ %s%s\n" "$c_green" "$*" "$c_reset"; }
warn() { printf "%s ⚠ %s%s\n" "$c_yellow" "$*" "$c_reset"; }
die()  { printf "%s ✗ %s%s\n" "$c_red" "$*" "$c_reset" >&2; exit 1; }

banner() {
  printf "%s" "$c_magenta"
  cat <<'BANNER'

    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║     🦞   S K I L L   O R C H E S T R A T O R ║
    ║                                              ║
    ║         ,_,    o roteador FODA da CCB        ║
    ║        (o,o)        — pt-BR · MIT —          ║
    ║       <)   (>                                ║
    ║         " "    github.com/bisnishub           ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝

BANNER
  printf "%s" "$c_reset"
}

banner
say "Instalando no Hermes Agent (modo LOCAL macOS)…"

# Preflight ------------------------------------------------------------------
command -v git >/dev/null 2>&1 || die "git não encontrado."

if [[ "$(uname)" != "Darwin" ]]; then
  warn "Esse script foi feito pra macOS. Você está em $(uname). Considere install-hermes-docker.sh."
fi

if [[ ! -d "$HERMES_DATA" ]]; then
  warn "Pasta $HERMES_DATA não existe — vou criar."
  mkdir -p "$HERMES_DATA/skills"
fi

if [[ ! -w "$HERMES_DATA" ]]; then
  die "Sem permissão de escrita em $HERMES_DATA. Verifique o owner da pasta."
fi

# Backup ---------------------------------------------------------------------
if [[ -d "$TARGET" ]]; then
  ts="$(date +%Y%m%d-%H%M%S)"
  backup="${TARGET}.backup-${ts}"
  warn "Skill já existe em $TARGET — backup em $backup"
  mv "$TARGET" "$backup"
fi

# Clone + copy ---------------------------------------------------------------
say "Clonando repositório…"
git clone --depth=1 "$REPO_URL" "$TMP_DIR/repo" >/dev/null 2>&1 || die "Falha ao clonar $REPO_URL"

mkdir -p "$(dirname "$TARGET")"
cp -r "$TMP_DIR/repo/skill" "$TARGET"
ok "Skill copiada pra $TARGET"

rm -rf "$TMP_DIR"

# Validate -------------------------------------------------------------------
if [[ -f "$TARGET/SKILL.md" ]]; then
  ok "SKILL.md encontrado"
else
  die "Algo deu errado — SKILL.md não está em $TARGET"
fi

cat <<EOF

  Próximos passos:

    1. Recarregue o Hermes pra detectar a skill (\`uv run hermes setup\` ou reinicie o agent local)
    2. Confirma:  \`uv run hermes skills list | grep orchestrator\`
    3. Teste:     digite "/claw briefing" ou "limpa meu inbox" no chat
    4. Playbooks: $TARGET/playbooks/

  Variável disponível pra override:
    HERMES_DATA   (default: \$HOME/.hermes)

  Comunidade: github.com/bisnishub/skill-orchestrator
  CCB — Open Claw Brasil 🇧🇷

EOF
