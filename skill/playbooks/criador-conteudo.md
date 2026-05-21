# Playbook — Criador de Conteúdo

Workflows pra criador solo ou time editorial pequeno. Repurpose multi-plataforma, calendário editorial, brand consistency. Usa Higgsfield (mídia), `video-use` (edição) e Notion/Drive (organização).

## 1. Calendário editorial da semana
**Gatilho:** "planejar conteúdo da semana", "calendário editorial", "o que vou postar".

1. Confirmar plataformas ativas (YouTube, Instagram, Twitter/X, TikTok, LinkedIn, blog).
2. Buscar últimos 5 posts em cada plataforma — identificar tópicos que **funcionaram** (eng > média).
3. Propor 7 dias de conteúdo com:
   - **1 conteúdo pilar** (long-form: YouTube longo, blog, podcast)
   - **3-5 atomizações** (Shorts/Reels/TikTok derivados)
   - **2 posts texto** (Twitter thread, LinkedIn)
4. Cada item: título, plataforma, dia, formato, status (rascunho/gravado/editado/agendado).
5. Saída: tabela markdown OU página Notion (perguntar destino).

## 2. Repurpose multi-plataforma (`/claw repurpose <url>`)
**Gatilho:** "/claw repurpose", "transforma esse vídeo em Shorts", "repropõe esse conteúdo".

A partir de UM conteúdo (vídeo longo, post, podcast):

1. **Transcrever** se for vídeo/áudio (usar `video-use` ou serviço de transcrição).
2. Extrair **3 hooks fortes** (frases de 1-2 linhas que param o scroll).
3. Gerar:
   - **3 Shorts/Reels** (60s cada) — cada um focado em UM hook. Roteiro de corte com timestamps.
   - **1 Twitter thread** (5-7 tweets) — TL;DR + insight + CTA.
   - **1 LinkedIn post** (200-400 palavras) — tom profissional, mesma essência.
   - **1 Instagram caption** (200-500 chars) — visual-first, hashtags relevantes.
   - **1 thumbnail/cover** via `Higgsfield.generate_image` com brief do hook principal.
4. Entregar como pasta com cada arquivo separado.

## 3. Tutorial YouTube — estrutura de 10min
**Gatilho:** "tutorial YouTube de X", "vídeo de 10 minutos", "explica X em vídeo".

Estrutura validada:

- **0:00–0:15** Hook (resultado final ou problema chocante)
- **0:15–0:45** O que você vai aprender + por que importa
- **0:45–7:00** Passo a passo (3-5 capítulos, cada um com mini-resultado)
- **7:00–8:30** Caso de uso real / resultado
- **8:30–9:30** Erros comuns e como evitar
- **9:30–10:00** CTA (inscrever, próximo vídeo, comentar)

Gerar roteiro completo + chapter markers pro YouTube.

## 4. Brand consistency check
**Gatilho:** "tá na nossa identidade?", "cor certa?", "fonte oficial".

Se user tem brand kit definido (cores HEX, fonte, logo, tom de voz):

1. Carregar do `~/.skill-orchestrator/brand-kit.json` (criar na primeira conversa).
2. Aplicar em todos os assets gerados (thumbnails, slides, posts).
3. Se alguém pediu algo que viola brand → apontar e propor versão "on-brand".

Se NÃO tem brand kit → perguntar **uma** vez:
- 3 cores HEX (primária, secundária, accent)
- Fonte principal
- Tom (formal/coloquial/técnico/criativo)
- Logo (path ou URL)

Salvar em `~/.skill-orchestrator/brand-kit.json` pra reutilizar.

## 5. Virality predictor antes de publicar
**Gatilho:** "vale postar?", "esse vídeo bomba?", "predizer engajamento".

1. `Higgsfield.virality_predictor` com o vídeo final.
2. Score < 50 → **não publicar**. Sugerir 2 ajustes concretos (hook nos 3s, retention, audio levels).
3. Score 50-70 → publicar com expectativa moderada. Apontar 1 melhoria pro próximo.
4. Score ≥ 70 → liberar + sugerir potencializar (boost pago, cross-post, thread).

## 6. Análise de performance pós-publicação
**Gatilho:** "como foi esse post", "engagement do vídeo de ontem", "performance da semana".

1. Puxar métricas da(s) plataforma(s) via MCP/API quando disponível.
2. Comparar vs. **média móvel últimos 10 posts** (não vs. melhor histórico — distorce).
3. Métricas em ordem: **CTR/Hook rate > retenção > engajamento > alcance**.
4. 1 hipótese do que funcionou + 1 do que pode melhorar. **Não inventar correlações** sem dados.

---

**Princípios:**

- **Atomização > publicação única.** 1 conteúdo bem feito vira 5-7 pieces.
- **Hook é tudo.** Os primeiros 3s decidem o vídeo. Os primeiros 60 chars decidem o post.
- **Brand kit > improviso.** Consistência visual sobe percepção de qualidade.
- **Repurpose sem repetir.** Mesma essência, embalagem diferente — não copy-paste.
