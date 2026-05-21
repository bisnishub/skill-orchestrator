# 🦞 eval-suite — benchmark público da Skill Orchestrator

Mede acurácia do roteamento. Cada linha do `corpus.jsonl` é uma intenção do user com a rota esperada.

## Uso

```bash
python3 tools/eval-suite/runner.py
```

Output:
- Accuracy global + breakdown por domínio
- Lista de falhas (intent → expected vs predicted)
- Exit code 0 se ≥ threshold (default 85%), 1 se abaixo

Flags úteis:

```bash
python3 tools/eval-suite/runner.py --threshold 0.90       # exige 90%
python3 tools/eval-suite/runner.py --quiet                # JSON para CI
python3 tools/eval-suite/runner.py --corpus path/custom.jsonl
python3 tools/eval-suite/runner.py --skill path/SKILL.md
```

## Como funciona

1. Parser lê a matriz de roteamento do `SKILL.md` (extrai gatilhos entre aspas)
2. Pra cada intent do corpus: normaliza acentos, faz substring match com cada gatilho
3. Vence o domínio com maior **score ponderado** (gatilhos longos pesam mais)
4. Compara contra `expected_domain` → conta acerto/erro
5. Reporta accuracy + falhas pra análise

## Estado atual

- Corpus: **64 frases** cobrindo 13 domínios
- Accuracy v0.5: **95.3%**
- Threshold CI: **85%**

## Contribuir

Adicionar exemplos é a melhor maneira de melhorar:

1. Pega frases reais que você usa (sem dados sensíveis).
2. Anota o domínio esperado (`grep "Domínio" skill/SKILL.md` mostra a lista).
3. Adiciona ao `corpus.jsonl` (uma JSON por linha).
4. Roda `python3 tools/eval-suite/runner.py` — se passou, PR pode subir.
5. Se falhou, edita gatilhos no `SKILL.md` até acertar.

## Boas práticas de corpus

- **Diversidade > volume.** 5 frases bem variadas por domínio > 20 quase iguais.
- **PT-BR coloquial.** Inclua "limpa", "vê", "manda", "joga isso" — como pessoa fala mesmo.
- **Sem dados privados.** Substitua nomes/empresas/emails por placeholders.
- **Edge cases bem-vindos.** "histórico desse lead" é ambíguo entre `comercial` e `dados-outros-mcps` — anote o que faz mais sentido e force a matriz a aprender.

## Privacidade

Tudo local. O runner não envia nada pra fora. O corpus está no repo público — só inclua dados anonimizados/sintéticos.
