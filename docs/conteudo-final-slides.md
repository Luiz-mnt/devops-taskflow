# Conteúdo consolidado da fase 1

## Slide 1

Luiz Eduardo Santos Monteiro

TaskFlow API: Configuração e Automação Inicial

Entrega da Fase 1

## Slide 3

Projeto

TaskFlow API: serviço HTTP para criar, listar e concluir tarefas. Projeto acadêmico independente de sistemas empresariais.

Objetivo

Aplicar integração contínua, testes automatizados e infraestrutura como código em um laboratório reproduzível e versionado.

Requisitos funcionais

POST /tasks, GET /tasks, PATCH /tasks/{id} e GET /health. SQLite persistente, título obrigatório com até 200 caracteres e validação de entradas.

Requisitos de qualidade

Testes isolados com banco temporário, cobertura mínima de 80%, lint e formatação Ruff, dependências fixadas e configuração por ambiente.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 4

Eventos e validações

Push e pull request para main, além de execução manual, acionam jobs de aplicação e infraestrutura em runners Linux hospedados pelo GitHub.

Aplicação e infraestrutura

Python 3.12, dependências fixadas, Ruff e pytest. Job Terraform: fmt -check, init -backend=false e validate. Outro job executa apply, inspeções, plan e limpeza efêmeros.

Critérios de aprovação

Falhas de lint, testes, cobertura abaixo de 80% ou validação Terraform reprovam o CI. Relatórios JUnit e cobertura são publicados mesmo em falha.

Rastreabilidade e acesso

Execuções vinculadas ao commit. Actions fixadas por SHA, contents: read, timeout por job e sem segredos de deploy ou publicação de pacotes nesta fase.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 5

Ambiente de desenvolvimento

Windows/PowerShell e Python 3.12; Ubuntu 24.04.4 WSL2 com Docker 29.9.3 e Terraform 1.17.1. CI aprovado em Ubuntu 24.04 hospedado no GitHub, com Docker 28.0.4.

Recursos definidos como código

Provider kreuzwerker/docker: rede bridge e volume. Padrão local taskflow-net/taskflow-data; CI usa prefixo exclusivo. Lockfile versionado; estado local fora do Git.

Execução e dados

Nesta fase, API em 127.0.0.1:8000 e SQLite em caminho configurável. Rede e volume são geridos exclusivamente pelo Terraform e reservados à evolução com containers.

Escopo e capacidade

Laboratório em host único, sem nuvem contratada. Referência: 4 CPUs, 8 GB RAM e 10 GB livres. Sem alta disponibilidade ou SLA de produção.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 7

Repositório

https://github.com/Luiz-mnt/devops-taskflow

Organização implementada

app/ e tests/: aplicação e testes. infra/: Terraform. .github/workflows/ci.yml: CI. docs/: planejamento, ambiente e evidências verificáveis.

Versionamento

Branch main para integração e branches curtas para mudanças. Referência da entrega: fase-1. Commit da entrega: 30b49c595e93.

Controle de acesso

Repositório público, acessível sem login. Segredos, .env, banco, venv, .terraform/ e terraform.tfstate excluídos do versionamento. Acesso do avaliador conforme visibilidade.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

GitHub

## Slide 8

GitHub

Repositório e tag fase-1 — captura real

Recorte da captura real da tag fase-1 no commit 30b49c5. O código foi aprovado; os documentos finais são consolidados em main.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 9

Workflow configurado

https://github.com/Luiz-mnt/devops-taskflow/blob/main/.github/workflows/ci.yml

Execução no GitHub Actions

Resultado: Aprovado: qualidade/testes, Terraform e provisionamento efêmero. https://github.com/Luiz-mnt/devops-taskflow/actions/runs/42485447573

Testes funcionais integrados

Criação, entradas inválidas, listagem, conclusão, IDs inexistentes, saúde com acesso ao banco e persistência entre instâncias. Bancos temporários por teste.

Resultados do CI e validação local

CI 08/11/2026: 32/32 testes aprovados, cobertura 100.0%, 0.85 s. LOCAL 06/11/2026: 32/32 testes aprovados, cobertura 100.0%, 2.86 s.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 10

GitHub Actions — três jobs aprovados

Recorte da captura real da execução 42485447573: qualidade/testes, Terraform e provisionamento efêmero aprovados.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 11

Relatórios produzidos pelo CI

Recorte real dos artefatos de testes/cobertura e infraestrutura. Cópias permanentes estão no repositório e no pacote de entrega.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 12

Testes no GitHub — Python 3.12.16

Log real do runner Linux em 08/11: 32 testes aprovados, 100% de linhas e branches; pytest 0.85 s. Local Windows: 2,86 s em 06/11.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 14

Código de infraestrutura

https://github.com/Luiz-mnt/devops-taskflow/tree/fase-1/infra

Arquivos e responsabilidades

versions.tf fixa versões. main.tf cria rede e volume. variables.tf define prefixo e conexão Docker. outputs.tf expõe nomes/IDs. Lockfile gerado por init.

Procedimento de provisionamento

terraform init, fmt -check, validate, plan e apply. Inspeções Docker confirmam rede e volume; segundo plan verifica idempotência. Validação de sintaxe não cria recursos.

Resultados local e remoto

CI: Aprovado: 2 criados, inspeções OK, plan sem alterações; 2 removidos somente no runner efêmero. Local: Apply: 2 criados; inspeções OK; plan posterior sem alterações (exit 0). Local WSL2: No changes; exit 0.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

Terraform

## Slide 15

Terraform

Terraform apply — laboratório WSL2 local

Registro real local: 2 recursos criados, 0 alterados e 0 destruídos. Rede e volume locais continuam preservados.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 16

Terraform

Plano local posterior sem alterações

Registro real do WSL2: No changes e exit 0. A preservação foi confirmada novamente em 07/11.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 17

Terraform

Terraform apply — runner GitHub

Registro real do runner: 2 recursos efêmeros criados com prefixo exclusivo. Docker do runner 28.0.4; local 29.9.3.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 18

Terraform

Plano do runner sem alterações

Registro real após o apply no runner: No changes. Etapa aprovada com exit 0, sem reduzir a exigência de validação.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 19

Terraform

Limpeza dos recursos efêmeros

Registro real: 2 recursos removidos somente no runner após coleta das provas. O laboratório local não foi destruído.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

## Slide 20

Verificação dos requisitos

Planejamento, código versionado, GitHub Actions, testes automatizados e scripts Terraform. Registros e links permitem reproduzir e auditar os resultados.

Atualização do documento

Documento: 08/11/2026; código 30b49c595e93; Python 3.12.16; Terraform 1.17.1. CI: 08/11/2026. Medições locais: testes 06/11/2026; IaC 06/11/2026.

Resultados observados

CI 08/11/2026: 32/32 testes aprovados, cobertura 100.0%, 0.85 s. IaC CI: Aprovado: 2 criados, inspeções OK, plan sem alterações; 2 removidos somente no runner efêmero. IaC local: Apply: 2 criados; inspeções OK; plan posterior sem alterações (exit 0).

Estado da entrega

Validações obrigatórias concluídas; links e registros incluídos.

TaskFlow API • Fase 1 • atualizado em 08/11/2026 • código 30b49c595e93

Terraform
