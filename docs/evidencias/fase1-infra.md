# Infraestrutura como Código — evidência concluída localmente

Em **06/11/2026, às 21:55 (America/Sao_Paulo)**, o Terraform provisionou os
recursos no Docker Engine do Ubuntu/WSL2 **TaskFlowDevOps**, no computador local.
Não foi utilizada nuvem nem Docker remoto para esta comprovação.

| Verificação | Resultado real |
|---|---|
| Terraform / provider | 1.17.1 / kreuzwerker/docker 4.6.0 |
| Docker Engine | 29.9.3, cliente e servidor Linux confirmados |
| fmt, init e validate | Aprovados |
| Lockfile | Gerado pelo Terraform; hashes Linux e Windows versionados |
| Plano inicial | 2 adições, 0 alterações, 0 exclusões |
| Apply | **2 adicionados, 0 alterados, 0 destruídos** |
| Rede criada | **taskflow-net**, driver bridge |
| Volume criado | **taskflow-data**, driver local |
| Inspeções | Rede/volume confirmados com labels de propriedade Terraform |
| Plano posterior | **No changes. Your infrastructure matches the configuration.** |
| Exit code do plano posterior | **0** |
| Preservação | Recursos permanecem criados; nenhum destroy local |

As inspeções completas e outputs registram IDs, subnet e caminho do volume.
O volume prepara a infraestrutura da fase 2; o banco da API no ambiente virtual
ainda utiliza `TASKFLOW_DB_PATH`, sem montar esse volume nesta fase.

## Arquivos e comandos

[`infra/`](../../infra/) contém `versions.tf`, `main.tf`, `variables.tf`, `outputs.tf`
e `.terraform.lock.hcl`. Consulte [o procedimento WSL](../ambiente-wsl.md) para
iniciar o daemon e repetir os comandos exatos. Terraform gerencia exclusivamente
rede/volume; Compose deverá consumi-los como externos na fase 2.

## Registros originais

- [Ambiente e versões](logs/terraform-local-ambiente.log)
- [Init](logs/terraform-local-init.log) e [validate](logs/terraform-local-validate.log)
- [Plano inicial](logs/terraform-local-plan.log)
- [Apply real](logs/terraform-local-apply.log)
- [Inspeções completas](logs/terraform-local-inspect.log) e [resumo legível](logs/terraform-local-inspecao-resumo.log)
- [Outputs JSON](logs/terraform-local-outputs.json)
- [Plano posterior e exit code](logs/terraform-local-plan-after.log)
- [Reverificação em 07/11: recursos preservados, plano sem alterações](logs/terraform-local-reverificacao-2026-11-07.log)
- [Fmt, validate e actionlint](logs/terraform-validacao.log)

## CI: configuração distinta da execução

O workflow possui um job de provisionamento efêmero, prefixo exclusivo, inspeções,
plano posterior e limpeza em `always`, restrita ao runner. **Esse job não executou**:
a conta GitHub bloqueou os jobs antes das etapas por questão de cobrança. Não há
apply remoto aprovado. Isso não altera a evidência local acima.
