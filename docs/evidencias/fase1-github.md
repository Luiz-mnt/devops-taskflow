# GitHub e CI — fase 1 aprovada

- Repositório público: https://github.com/Luiz-mnt/devops-taskflow
- Workflow: https://github.com/Luiz-mnt/devops-taskflow/blob/main/.github/workflows/ci.yml
- Scripts IaC: https://github.com/Luiz-mnt/devops-taskflow/tree/main/infra
- **Execução aprovada:** https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42485447573
- **Commit aprovado:** `30b49c595e931f1ea6c2e122ba4ca25ead004b48`
- **Tag:** [fase-1](https://github.com/Luiz-mnt/devops-taskflow/tree/fase-1), criada após a aprovação sem mover tag anterior.
- Conclusão em **08/11/2026 às 10:33:11, America/Sao_Paulo** (13:33:11 UTC).

| Job | Resultado observado |
|---|---|
| Qualidade e testes | Ruff/lint e formatação aprovados; 32 testes aprovados; cobertura de linhas/branches 100% |
| Terraform | fmt, init com lockfile readonly e validate aprovados |
| Provisionamento efêmero | Apply: 2 criados; inspeções; segundo plan sem alterações; cleanup: 2 removidos somente do runner |

Python do runner: **3.12.16**, Linux/Ubuntu 24.04. O pytest registrou **0.85 s**;
o relatório JUnit soma **0.857 s** de suíte. O tempo local
de 2,86 s é uma medição separada, feita no Windows em 06/11. Não se infere ganho
de desempenho comparando esses ambientes.

## Evidências permanentes

- [Metadados completos da execução aprovada](github-ci-aprovado.json)
- [Log de testes e lint do runner](logs/ci-42485447573-testes.log)
- [JUnit](ci/42485447573/testes/junit.xml) e [coverage XML](ci/42485447573/testes/coverage.xml)
- [Apply](ci/42485447573/infra/apply.log), [rede](ci/42485447573/infra/network.json), [volume](ci/42485447573/infra/volume.json)
- [Segundo plano](ci/42485447573/infra/replan.log) e [limpeza do runner](ci/42485447573/infra/destroy.log)
- [Capturas reais e procedência](imagens/fontes-capturas.json)

Os artefatos originais do Actions têm retenção de 14 dias. As cópias acima e no
pacote de entrega preservam a prova após essa retenção.

## Rastreabilidade do código e dos documentos

A tag `fase-1` congela o commit aprovado acima, incluindo o histórico disponível
no momento. Como a consolidação só pode relatar uma aprovação depois que ela
ocorre, os documentos finais foram acrescentados posteriormente em `main`.
O código da aplicação, testes, dependências, workflow e Terraform permanece o
mesmo da versão aprovada. A tag não foi movida para um commit documental posterior.

## Acesso e proteção

O repositório é público, com acesso do professor sem convite. Main exige os checks
**Qualidade e testes** e **Terraform**, mantém histórico linear e impede force-push
e exclusão. A exceção de administrador (`enforce_admins: false`) permite gerir o
projeto individual; não equivale a aprovação dos checks. [Estado consultado](github-protecao-main.json).
O workflow mantém `contents: read`, actions por SHA, timeout e ausência de segredos
de deploy. PR não publica imagens nem aplica infraestrutura.

## Histórico do impedimento resolvido

As primeiras tentativas não iniciaram os jobs devido ao bloqueio de cobrança da
conta. Em 08/11 o desbloqueio foi confirmado e a execução acima comprovou o
funcionamento. `github-bloqueio.json`, `github-anotacoes.json`, `github-execucao.json`
e as capturas com nome `bloqueado` são registros **históricos**, não pendências atuais.
Nenhum gate foi removido para obter a aprovação.
