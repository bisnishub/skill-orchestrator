# Playbook — Conteúdo OpenClaw Brasil

Pipelines de criação de conteúdo pra CCB. Os templates da comunidade vivem em:

- `~/Downloads/01-CCB-Claw-Brasil/`
- `~/Downloads/AI Library/`

## 1. Live CCB do zero
**Gatilho:** "live de hoje", "preparar live", "vai rolar live".

1. Tópico definido? Se não → perguntar.
2. Buscar roteiros anteriores em `~/Downloads/01-CCB-Claw-Brasil/03-Materiais-e-Guias/` e `~/Downloads/AI Library/Documents/roteiros_teleprompter_openclaw.docx` pra tom/estilo.
3. Gerar roteiro teleprompter (markdown, 8–12min de fala, blocos de 60s).
4. Slides → adaptar `slides_openclaw.html` ou `openclaw-dashboard.html` em `~/Downloads/AI Library/Presentations/`.
5. Countdown overlay → reaproveitar `openclaw-countdown-30s.mp4` em `~/Downloads/01-CCB-Claw-Brasil/09-Midia-para-Lives/`.
6. Thumbnail → `Higgsfield.generate_image` com brief baseado no tópico + logo `openclaw_brasil_logo.png`.
7. Entregar: pasta com `roteiro.md`, `slides.html`, `thumbnail.png`, checklist de live.

## 2. Tutorial em vídeo
**Gatilho:** "tutorial", "passo a passo gravado", "vídeo de X".

1. Roteiro com 3 atos (problema → caminho → resultado).
2. `Higgsfield.generate_video` pra cenas de B-roll **OU** gravar tela (instruir user).
3. `video-use` skill pra cortes, legendas burnadas, color grade.
4. Thumbnail (mesmo fluxo da live, item 1.6).
5. Sugerir descrição/título YouTube otimizado pro algoritmo.

## 3. Post na comunidade
**Gatilho:** "anúncio na comunidade", "post no Discord", "comunicado".

1. Tom: direto, brasileiro, sem corporativês. Olhar `feedback-communication` da memória.
2. Estrutura: hook (1 linha) → contexto (3 linhas) → CTA (1 linha).
3. Se for sobre release/nova skill → linkar repo github.com/bisnishub/...
4. Output em markdown, ≤ 800 chars (Discord-friendly).

## 4. Guia novo (formato CCB)
**Gatilho:** "novo guia", "fazer guia de X", "documentar X".

1. Olhar `guia-instalacao-openclaw.docx`, `guia-modelos-ia-openclaw.docx` pra formato/tom.
2. Estrutura padrão CCB:
   - **O que é** (1 parágrafo)
   - **Por que importa** (1 parágrafo)
   - **Pré-requisitos** (lista)
   - **Passo a passo** (numerado, screenshots quando crítico)
   - **Problemas comuns** (FAQ curto)
   - **Próximos passos** (links)
3. Entregar como `.md` + sugerir conversão pra `.docx` se for pra distribuição.

## 5. Virality check antes de publicar
**Gatilho:** "vale postar?", "esse vídeo bomba?", "predizer engajamento".

1. `Higgsfield.virality_predictor` com o vídeo final.
2. Score < 60 → sugerir 2 ajustes específicos (hook nos 3s iniciais, retention curve).
3. Score ≥ 60 → liberar pra publicação.
