# 🎬 Roteiro de gravação — GIF demo do README

Esse documento te guia pra gravar o GIF de ~30 segundos que vai pro topo do README. **Tu grava, eu não consigo.** Mas deixei tudo mastigado.

## Setup pré-gravação

### 1. Terminal limpo

- Tema escuro (Dracula, Tokyo Night, Solarized Dark — escolhe)
- Fonte: JetBrains Mono ou Fira Code, **16-18pt** (legível em GIF)
- Janela: **1280×720** (ratio HD, perfeito pro README)
- Prompt enxuto: idealmente só `$ ` ou um `❯`. Tira branch git, hostname etc. Distrai.

Pra mudar prompt temporário no zsh:
```bash
export PROMPT='%F{magenta}❯%f '
clear
```

### 2. Tools de gravação

- **QuickTime** (Mac, nativo) → grava `.mov`. Bom o suficiente.
- **Kap** (kap.app, gratuito) → exporta direto pra GIF otimizado. **Recomendado.**
- **asciinema + agg** (terminal puro, super leve) → quem quer minimalismo.

### 3. Conversão pra GIF (se gravou em vídeo)

Com `ffmpeg`:
```bash
ffmpeg -i input.mov -vf "fps=15,scale=1280:-1:flags=lanczos" -loop 0 demo.gif
```

Otimizar tamanho:
```bash
gifsicle -O3 --lossy=80 demo.gif -o demo-optimized.gif
```

Alvo: **<3 MB** (GitHub renderiza sem placeholder). Se passar, baixa fps pra 10 ou escala pra 1024.

---

## Roteiro (30s) — 3 cenas

> **Dica:** use `pv -L 30` ou `typeit` pra simular digitação no ritmo certo. OU digite manualmente devagar — autenticidade conta.

### Cena 1 — Briefing (0:00–0:10)

```
$ /claw briefing
```

*[Pausa de 1s — agente "pensa"]*

Output simulado (cola via macro/snippet pra ficar instantâneo, ou roda de verdade se já tem skill instalada):

```
🦞 Briefing — 21/05/2026

📬 3 emails urgentes (1 resposta esperada hoje)
📅 Próxima reunião: 14:00 — Discovery call com Acme Corp
🎯 Top 3 do dia:
   1. Fechar proposta v2 (Acme)
   2. Review PR #142 (api-gateway)
   3. Gravar tutorial — Supabase RLS

Quer que eu prepare o briefing da call das 14h?
```

### Cena 2 — Slash command + dispatch (0:10–0:20)

```
$ /claw ship
```

```
🦞 Pre-flight de deploy

✓ Branch:        feat/checkout-v2 (≠ main)
✓ Working tree:  limpo
✓ CI:            verde (último run 3min atrás)
✓ PR:            mergeable
⚠ CHANGELOG:     não foi tocado nesse branch

Sugiro adicionar entry no CHANGELOG antes do merge.
Continuar mesmo assim? (s/n)
```

### Cena 3 — Stats local (0:20–0:30)

```
$ /claw stats
```

```
📊 Skill Orchestrator — sua semana

Top despachos (últimos 7d):
  1. produtividade-email     ████████████ 12
  2. dados-supabase          ████████      8
  3. engenharia-github       ██████        6
  4. conteudo                ████          4

Modo default: dev
Sugestões pendentes: 1

💡 Você manda email 12x/semana — bora batizar
   /claw email <pessoa> e poupar tempo?
```

*[Fade out lento, último frame com o logo 🦞]*

---

## Pós-gravação

1. Salva o GIF como `docs/demo.gif` no repo.
2. Adiciona no topo do README, **logo abaixo do título**:

```markdown
# 🦞 Skill Orchestrator

![Demo](docs/demo.gif)

**🇧🇷 Português** · [🇺🇸 English](README_EN.md)
```

3. Commit:
```bash
git add docs/demo.gif README.md
git commit -m "feat: add demo GIF to README"
git push
```

---

## Variações se quiser gravar mais coisa

- **Modo dev**: `/claw --mode dev "deploya isso"` → mostra como o tom muda
- **Repurpose**: `/claw repurpose https://youtube.com/...` → produz Shorts + thread + caption
- **Research**: `/claw research mcp ecosystem 2026` → relatório estruturado

Cada uma vira um GIF curto. Pode rotacionar no README com tag `<picture>` se quiser ser fancy.

---

## Compressão de áudio (se incluir voz)

Se quiser narrar e gerar MP4 em vez de GIF (melhor pra Twitter/LinkedIn):

```bash
ffmpeg -i input.mov -c:v libx264 -preset slow -crf 23 -c:a aac -b:a 128k -movflags +faststart demo.mp4
```

Alvo: <8 MB pra atachar no Twitter sem perder qualidade.

🦞 Bora gravar.
