# Playbook — Engenheiro Solo

Workflows pra dev que toca produto sozinho ou em time pequeno. Usa GitHub MCP/`gh` CLI, Linear (se houver), e Bash do agente.

## 1. PR triage matinal
**Gatilho:** "PRs abertos", "o que tá no review", "triage de PR".

1. `gh pr list --state open --json number,title,author,createdAt,reviewDecision,mergeable` → lista enriquecida.
2. Classificar: **READY** (aprovado + mergeable), **BLOCKED** (changes requested ou conflito), **STALE** (>7 dias sem update).
3. Sugerir: merge dos READY (com `gh pr merge --auto --squash` se CI verde), comentário nos BLOCKED, follow-up nos STALE.
4. Resumir: `{ready: N, blocked: N, stale: N}` + comando exato pra cada ação.

## 2. Code review automático
**Gatilho:** "revisa esse PR", "code review PR #N", "olha o que mudou".

1. `gh pr view <N> --json files,additions,deletions` → escopo.
2. `gh pr diff <N>` → diff completo.
3. Análise estruturada (não inventar requisitos): **bugs**, **segurança**, **estilo/legibilidade**, **testes faltando**.
4. **Comentário inline** via `gh pr review --comment` apenas se user pediu — caso contrário, devolver markdown e perguntar se quer publicar.
5. Nunca aprovar/rejeitar sem confirmação explícita.

## 3. Ship — pre-flight de deploy
**Gatilho:** "ship", "deployar", "release", "/claw ship".

Checklist em ordem:

1. **Branch certo?** `git branch --show-current` ≠ `main`/`master` → pergunta antes.
2. **Working tree limpo?** `git status --porcelain` → se sujo, propor commit ou stash.
3. **CI verde?** `gh run list --branch <branch> --limit 1 --json status,conclusion`. Se vermelho → bloqueia, lista falha.
4. **PR mergeable?** Se for via PR.
5. **Changelog atualizado?** Se `CHANGELOG.md` existe e não foi tocado nesse branch, sugerir entry.
6. **Migrations pendentes?** Se houver Supabase, `Supabase.list_migrations` + diff contra remoto.
7. Tudo OK → propor `gh pr merge --squash` OU `git push` (depende do fluxo do repo).

## 4. Debug CI quebrado
**Gatilho:** "CI quebrou", "build vermelho", "porque tá falhando", "GitHub Actions errado".

1. `gh run list --branch $(git branch --show-current) --limit 1 --json databaseId` → pegar último run.
2. `gh run view <id> --log-failed` → logs das jobs que falharam.
3. Identificar **a primeira** linha de erro (não a última — geralmente é cascata).
4. Se for erro óbvio (typo, dep faltando, env var) → propor fix exato no código.
5. Se for flaky test → sugerir rerun (`gh run rerun <id>`) **uma vez**. Se falhar de novo, tratar como bug real.

## 5. Issue → PR
**Gatilho:** "implementa essa issue", "abre PR pra isso", "issue #N".

1. `gh issue view <N> --json title,body,labels` → contexto.
2. Criar branch: `git checkout -b <slug-da-issue>`.
3. Implementar (delegando pro agente principal, não tentar fazer aqui).
4. Commit com `Closes #<N>` no body.
5. `gh pr create --title "..." --body "..." --base main` com link pra issue.
6. **Não fazer auto-merge.** Esperar review humano.

## 6. Branch / repo health check
**Gatilho:** "como tá esse repo", "branches stale", "limpar repo".

1. `git for-each-ref --sort=-committerdate refs/remotes/origin --format='%(refname:short) %(committerdate:short)' | head -20` → top 20 branches por atividade.
2. Branches sem commit há >30 dias → candidatas a delete (perguntar antes).
3. PRs abertos vs branches ativas — gap indica branches "fantasma".
4. `gh repo view --json defaultBranchRef,diskUsage,issues,pullRequests` → métricas gerais.
5. Reportar com 1-3 ações concretas.

---

**Princípios de safety:**

- NUNCA `git push --force` em `main`/`master` sem 2 confirmações.
- NUNCA `git reset --hard` sem stash/branch de backup.
- Hooks que falharem → corrigir o problema, não usar `--no-verify`.
- Operações destrutivas em produção (drop table, force-push, delete branch remoto) → **sempre** mostrar o comando e pedir `confirma` antes de executar.
