# Contribuindo com a Skill Orchestrator 🦞

Obrigado por querer contribuir! Esse repo é mantido pela **CCB — Comunidade Claude/Claw Brasil** e tá aberto pra qualquer pessoa que queira melhorar o roteador.

## Tipos de contribuição

### 🐛 Reportar bug
Abre uma issue usando o template **Bug Report**. Inclua:
- Qual agent (OpenClaw, Hermes, Claude Code)
- Versão do agent (`openclaw --version`, etc)
- O que você esperava vs o que aconteceu
- Logs ou print se possível

### 💡 Propor playbook novo
Os playbooks são o coração do projeto. Pra propor um:

1. Abre uma issue com o template **Playbook Proposal**.
2. Descreve o **gatilho** (frases típicas que disparam o playbook) — pelo menos 3 exemplos.
3. Descreve o **fluxo de despacho**: pra cada passo, qual tool/MCP é chamado.
4. Se aprovado, abre o PR com o `.md` em `skill/playbooks/`.

### 🔧 Pull Request

1. Fork → branch nova (`git checkout -b feat/meu-playbook`).
2. Implementa.
3. Roda o lint local (`bash .github/scripts/lint.sh` se existir, ou só confere frontmatter manualmente).
4. Atualiza `CHANGELOG.md` com sua mudança.
5. Abre o PR usando o template.

## Padrões de qualidade

- **Idioma**: Português brasileiro (PT-BR). Comentários técnicos em código podem ser EN.
- **Concisão**: instrua o agente no **que** fazer, não em **como ser um AI**. Sem floreio motivacional.
- **Cite a tool exata**: `Gmail.search_threads`, `Supabase.execute_sql`, `gh pr list`. Sem placeholders genéricos.
- **Sem dados sensíveis**: nenhum exemplo deve conter CPF, email pessoal, token, business privado.
- **Multi-agent first**: se sua mudança afeta install, atualize **os três installers** (`install.sh`, `install-hermes.sh`, `install-claude-code.sh`).
- **Frontmatter válido**: `SKILL.md` precisa ter `name` (kebab-case) e `description` (uma linha clara).

## Estrutura esperada de um playbook

```markdown
# Playbook — Nome curto

Frase de uma linha explicando escopo + ferramentas usadas.

## 1. Workflow X
**Gatilho:** "frase 1", "frase 2", "frase 3".

1. Primeiro passo (com tool/MCP exato).
2. Segundo passo.
3. ...

## 2. Workflow Y
...

---

**Princípios:** (opcional, mas recomendado)
- Regra de safety/qualidade 1
- Regra 2
```

## Tom da comunidade

Esse repo é da CCB. A vibe é descontraída, brasileira, sem corporativês. Você pode dizer "FODA" no commit message — é tradição. Mas mantenha respeito: ver `CODE_OF_CONDUCT.md`.

## Dúvidas?

- Issue com label `question`
- Discord da CCB (se você é membro)
- GitHub Discussions desse repo

🦞 *Made with claws in 🇧🇷*
