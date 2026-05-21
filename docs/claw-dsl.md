# .claw DSL — spec mínima

Linguagem declarativa pra escrever **skills sem entender YAML, frontmatter ou markdown**. Você descreve a intenção em alto nível, o compiler gera `SKILL.md` válido.

## Por que existe

Skills da Anthropic são markdown + YAML frontmatter. Pra um dev é OK. Pra um criador de conteúdo, vendedor, ou pesquisador → é fricção. `.claw` é a camada de simplificação.

Filosofia: **se você sabe escrever uma receita ou um cronograma, sabe escrever uma .claw.**

## Sintaxe

```claw
skill MyAwesomeSkill
description: O que essa skill faz, em uma linha
mode: dev | editor | comercial | analista | default

when "frase gatilho 1", "frase gatilho 2"
  use Gmail.create_draft
  with subject="Re: ${topic}", to="${recipient}"
  then notify telegram "draft criado pro ${recipient}"

when "/claw deploy"
  if branch != "main": abort "não deployar de outra branch"
  if not ci_green: abort "CI vermelho"
  use gh
  run "gh pr merge --squash --auto"
  then notify discord "#deploys" "shippei ${branch}"

when ambiguous
  ask "Você quer X ou Y?"
```

## Elementos

### `skill <Name>` (obrigatório, primeira linha)
Nome em CamelCase ou kebab-case. Vira o `name` no frontmatter.

### `description: <text>` (obrigatório)
Uma linha. Vira `description` no frontmatter.

### `mode: <modo>` (opcional)
Default da skill. Override-able pelo user.

### `when <gatilhos>`
Bloco condicional. Aceita:
- Strings entre aspas: `when "limpa inbox", "triage", "/claw triage"`
- Slash explícito: `when "/claw <comando>"`
- Keyword `ambiguous`: fallback pra pedidos não-claros

### Ações dentro do bloco `when`

- `use <Tool|MCP>` — declara qual tool/MCP usar
- `with <key>=<value>, ...` — parâmetros (suporta `${var}` placeholders)
- `if <condition>: <action>` — guards de safety
- `run <shell_command>` — comando exato a executar (use com cuidado)
- `then <action>` — encadeamento sequencial
- `ask <question>` — pergunta ao user
- `abort <reason>` — sai sem executar

### Variáveis disponíveis dentro de blocos

- `${user_intent}` — texto original do user
- `${branch}` — branch git atual (se aplicável)
- `${date}`, `${time}` — agora
- `${mode}` — modo ativo
- Variáveis nomeadas: qualquer `with foo=...` injeta `${foo}`

## Exemplo completo

```claw
skill DeployHelper
description: Atalho seguro de deploy com pre-flight checks
mode: dev

when "/claw deploy", "deployar", "ship"
  if branch == "main": abort "deploy só a partir de branch != main"
  if not working_tree_clean: abort "commitar mudanças primeiro"
  if not ci_green: abort "CI vermelho — veja gh run list"
  use gh
  run "gh pr merge --squash --auto"
  then notify telegram "deployei ${branch} → main"

when "/claw rollback"
  ask "Qual SHA voltar?"
  with sha=${answer}
  run "git revert ${sha} && git push"
  then notify discord "#alerts" "ROLLBACK: ${sha}"
```

## Compilação

```bash
python3 tools/claw-compiler/claw.py path/to/MySkill.claw > skill/MySkill/SKILL.md
```

O compiler:
1. Parse o `.claw`
2. Valida sintaxe
3. Gera `SKILL.md` com frontmatter + body
4. Frontmatter inclui `metadata.source: .claw` + `metadata.compiled_from: <arquivo>`

## Limitações conhecidas (v1.0)

- Sem loops (`for`/`while`). Use playbooks pra iteração.
- Sem chamadas condicionais aninhadas profundas. Use `if/abort` pra short-circuit.
- Sem includes/imports. Cada `.claw` é auto-contido.

## Roadmap

- [ ] `import "common.claw"` — modularização
- [ ] `for each <var> in <list>: <action>` — loops simples
- [ ] LSP server (autocomplete em editores)
- [ ] Linter (`claw lint`) sem precisar compilar
- [ ] Bidirecional: ler `SKILL.md` e gerar `.claw` (reverse)
