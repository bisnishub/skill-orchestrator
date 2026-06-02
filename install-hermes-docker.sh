#!/usr/bin/env bash
# 🦞 Skill Orchestrator — installer para Hermes Agent (modo DOCKER/VPS)
# Use este script se você roda o Hermes em CONTAINER DOCKER (típico em VPS).
# Para Hermes em macOS LOCAL (sem container), use install-hermes-local.sh.
# CCB — Comunidade Claude/Claw Brasil · github.com/bisnishub/skill-orchestrator
set -euo pipefail

SKILL_NAME="orchestrator"
HERMES_DATA="${HERMES_DATA:-/home/hermes/.hermes}"   # override com HERMES_DATA=... se sua VPS não usa esse path
TARGET="${HERMES_DATA}/skills/${SKILL_NAME}"
HERMES_COMPOSE_DIR="${HERMES_COMPOSE_DIR:-/home/hermes/hermes}"
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

# Preflight ------------------------------------------------------------------
banner
say "Instalando no Hermes Agent (Docker)…"

command -v git    >/dev/null 2>&1 || die "git não encontrado."
command -v docker >/dev/null 2>&1 || warn "docker não encontrado — vou copiar a skill mesmo assim, mas restart manual será necessário."

# Permissão: precisa escrever em HERMES_DATA (root ou user hermes via sudo)
if [[ ! -d "$HERMES_DATA" ]]; then
  die "Pasta Hermes não encontrada em $HERMES_DATA — defina HERMES_DATA=<caminho> e rode de novo."
fi
if [[ ! -w "$HERMES_DATA" && $EUID -ne 0 ]]; then
  die "Sem permissão de escrita em $HERMES_DATA. Rode como root/sudo, ou como user hermes."
fi

# Backup se já existir -------------------------------------------------------
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

# Permissões pro user hermes (uid/gid 1000) ----------------------------------
if id hermes >/dev/null 2>&1; then
  chown -R hermes:hermes "$TARGET" 2>/dev/null && ok "Permissões ajustadas (hermes:hermes)" \
    || warn "chown falhou — rode com sudo se necessário"
else
  # Fallback: usa UID/GID 1000 numérico
  chown -R 1000:1000 "$TARGET" 2>/dev/null && ok "Permissões ajustadas (uid 1000)" \
    || warn "chown falhou — verifique manualmente"
fi
chmod -R u+rwX,go+rX "$TARGET"

rm -rf "$TMP_DIR"

# Restart container ----------------------------------------------------------
if [[ -f "$HERMES_COMPOSE_DIR/docker-compose.yml" ]] && command -v docker >/dev/null 2>&1; then
  say "Reiniciando containers Hermes…"
  (cd "$HERMES_COMPOSE_DIR" && docker compose restart) && ok "Containers reiniciados" \
    || warn "Restart falhou — rode manualmente: cd $HERMES_COMPOSE_DIR && docker compose restart"
else
  warn "docker-compose.yml não encontrado em $HERMES_COMPOSE_DIR — restart manual necessário"
fi

cat <<EOF

  Próximos passos:

    1. Confirma carregamento:
         docker exec -it hermes bash -lc "ls /opt/data/skills/ | grep orchestrator"

    2. Testa no chat (Telegram, dashboard ou CLI):
         "Lista as skills carregadas e me confirma que orchestrator tá ativa"

    3. Lê os playbooks:
         ${TARGET}/playbooks/

  Variáveis disponíveis (override caso paths diferentes):
    HERMES_DATA          (default: /home/hermes/.hermes)
    HERMES_COMPOSE_DIR   (default: /home/hermes/hermes)

  Comunidade: github.com/bisnishub/skill-orchestrator
  CCB — Open Claw Brasil 🇧🇷

EOF
