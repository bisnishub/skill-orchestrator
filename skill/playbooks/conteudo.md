# Playbook — Criação de Conteúdo

Pipelines de produção de conteúdo (roteiros, vídeos, slides, posts, thumbnails). Usa Higgsfield pra mídia e a skill `video-use` pra edição quando disponível.

> **Dica:** se o user tem uma biblioteca local de templates/roteiros (pasta com modelos, brand kit, etc.), pergunte o caminho **uma vez** e reaproveite tom/estilo. Não invente paths.

## 1. Live / stream do zero
**Gatilho:** "live de hoje", "preparar live", "vai rolar transmissão".

1. Tópico definido? Se não → perguntar (UMA pergunta).
2. Se user tem biblioteca de roteiros anteriores → ler 2-3 pra capturar tom/estilo.
3. Gerar roteiro tipo teleprompter (markdown, 8–12min de fala, blocos de 60s, com headers `[BLOCO N - tópico]`).
4. Slides → estrutura de 8-12 slides (capa, agenda, 3-5 conteúdo, CTA, encerramento). HTML/Reveal.js ou markdown.
5. Thumbnail → `Higgsfield.generate_image` com brief curto (tópico + estilo + brand colors se conhecidos).
6. Checklist de live: pré-live (10min), durante (câmera/áudio/tela), pós (publicar VOD, post de divulgação).
7. Entregar: pasta com `roteiro.md`, `slides.html`, `thumbnail.png`, `checklist.md`.

## 2. Tutorial em vídeo
**Gatilho:** "tutorial", "passo a passo gravado", "vídeo explicando X".

1. Roteiro com 3 atos: **problema** (por que importa) → **caminho** (passo a passo) → **resultado** (o que muda).
2. Mídia: gravar tela (instruir user) **ou** `Higgsfield.generate_video` pra B-roll/cenas.
3. Edição: skill `video-use` pra cortes, legendas burnadas, color grade.
4. Thumbnail: mesmo fluxo da live (item 1.5).
5. Sugerir título/descrição YouTube otimizados (hook nos primeiros 60 chars).

## 3. Post pra comunidade / social
**Gatilho:** "anúncio", "post no Discord", "comunicado", "thread Twitter".

1. Definir tom (formal vs informal) — se user falou em pt-BR coloquial, manter.
2. Estrutura: **hook** (1 linha que para o scroll) → **contexto** (3 linhas) → **CTA** (1 linha).
3. Para release/produto → linkar repo ou landing page.
4. Discord: ≤ 800 chars. Twitter: ≤ 280 chars (thread se preciso). Instagram: caption ≤ 2200 chars.
5. Saída em markdown, pronta pra copiar.

## 4. Guia / documentação
**Gatilho:** "novo guia", "documentar X", "tutorial em texto".

Estrutura padrão recomendada:
- **O que é** (1 parágrafo)
- **Por que importa** (1 parágrafo)
- **Pré-requisitos** (lista)
- **Passo a passo** (numerado; screenshots só quando crítico)
- **Problemas comuns** (FAQ curto)
- **Próximos passos** (links)

Entregar como `.md`. Sugerir conversão pra `.docx`/`.pdf` se for pra distribuição interna.

## 5. Virality check antes de publicar
**Gatilho:** "vale postar?", "esse vídeo bomba?", "predizer engajamento".

1. `Higgsfield.virality_predictor` com o vídeo final.
2. Score < 60 → sugerir 2 ajustes específicos (hook nos 3s iniciais, retention curve).
3. Score ≥ 60 → liberar.

## 6. Brand consistency
**Gatilho:** "essa cor não é nossa", "fonte errada", "logo certo".

Se user tem brand kit (cores hex, fonte, logo) já definido em conversa anterior ou memória persistente → aplicar. Se não tem → perguntar **uma** vez e oferecer salvar pra próximas.
